import traceback
from utils_functions import *  # the util functions from the paper
from file_parsing import get_info_from_xml, get_info_from_facebook_json, get_online_info_from_xml, get_online_info_from_fb_json

# load all the pickle files

model = loading_pkl('model_pickle_files/model.pkl')
psr_weights = loading_pkl('model_pickle_files/psr.pkl')
sexual_words = loading_pkl(
    'model_pickle_files/augmented_sexual_words.pkl')
nrc_emotions = loading_pkl("model_pickle_files/emotions_nrc.pkl")
depeche_emotions_lexicon = loading_pkl(
    "model_pickle_files/emotions_depeche.pkl")
depeche_emotions = processing_depeche_lexicon(depeche_emotions_lexicon)
emoticons_set = loading_pkl("model_pickle_files/emoticons_set.pkl")

# I added verbose option to figure out what things should look like


def single_conv_groomer_predictions(model, doc_partial, X_time_partial, X_participants_partial, X_int_user_partial, labels=[], _predict=False, verbose=False):

    # print("Document: ",doc_partial)
    if verbose:
        print("Document: ", doc_partial)
    # Obtaining the partial profiles with the PSR++ method
    DRT_partial = PSR_plus_document_representation(doc_partial, psr_weights)
    if verbose:
        print("DRT shape: ", DRT_partial)
#     print("  ",DRT_partial.shape)

    # Calculating proposed BF with partial information
    '''Time when a conversation starts BF'''
    # print("Calculating: Time when a conversation starts BF ...")

    # Number of conversations x num features
    time_feature = np.zeros((len(X_time_partial), 2))
    id = 0
    for i in X_time_partial:
        hours, minutes = i.split(":")
        time_feature[id][0], time_feature[id][1] = int(hours), int(minutes)
        id += 1
    if verbose:
        print(X_time_partial)
#     print("####TIME FEATURE")
#     print(time_feature)
    # this is because if we don't normalize it then it will always be an entry like [0,1] or [1,0] this step just does a similar for of normalization as would be expected when operating on the large dataset
    time_feature = (time_feature - 0) / (59 - 0)
#     print(time_feature)
    # because we want to it be closer to what it would be when lots of data is being processed together
    time_partial = time_feature
#     time_partial = calculating_time(X_time_partial,2)
#     time_partial = np.nan_to_num(time_partial) ## might need to change this because they normalize based on there being other values but we are doing only one value
    if verbose:
        print("Time: ", time_partial)  # HH, MM

    # print("  ",time_partial.shape)

    '''Correctly spelled words BF'''
    # print("Calculating: Correctly spelled words BF ...")
    csw_partial = calculating_CSW(doc_partial)
    # print("  ",csw_partial.shape)
    if verbose:
        print("Correctly spelled words: ", csw_partial)

    '''Sexual topic words BF'''
    # print("Calculating: Sexual topic words BF ...")
    sexual_partial = calculating_sexual_words(sexual_words, doc_partial)
    # print("  ",sexual_partial.shape)
    if verbose:
        print("Sexual topic words: ", sexual_partial)

    '''NRC emotional markers BF'''
    # print("Calculating: NRC emotional markers BF ...")
    nrc_partial = calculating_emotional_markers(nrc_emotions, doc_partial, 10)
    nrc_partial = nrc_partial[:, [0, 1, 4, 6, 7, 8]]
    # print("  ",nrc_partial.shape)
    if verbose:
        print("NRC emotional markers: ", nrc_partial)

    '''Depeche emotional markers BF'''
    # print("Calculating: Depeche emotional markers BF ...")
    de_partial = calculating_emotional_markers(
        depeche_emotions, doc_partial, 8)
    de_partial = de_partial[:, [1, 2, 6, 7]]
    # print("  ",de_partial.shape)
    if verbose:
        print("Depeche emotional markers: ", de_partial)

    '''Emoticons BF'''
    # print("Calculating: Emoticons BF ...")
    emoticon_partial = calculating_emoticons_faster(emoticons_set, doc_partial)
    # print("  ",emoticon_partial.shape)
    if verbose:
        print("Emoticons: ", emoticon_partial)

    '''Number of participants BF'''
    # print("Calculating: Number of participants BF ...")
    participants_partial = np.asarray(X_participants_partial)
    # print("  ",participants_partial.shape)
    if True:
        temp = [X_participants_partial]
        if verbose:
            print(temp)
            print(X_participants_partial)
        participants_partial = np.asarray(temp)
        if verbose:
            print("number of participants: ", participants_partial)

    '''% Word interactions per user BF'''
    # print("Calculating: Word interactions per user BF ...")
    int_user_partial = column_extract(X_int_user_partial)
    # print("  ",int_user_partial.shape)
    if True:
        int_user_partial = X_int_user_partial
        if verbose:
            print("word interactions per used: ", int_user_partial)

    '''Putting toguether all proposed BFs'''
    BFS = [participants_partial, int_user_partial, de_partial,
           emoticon_partial, csw_partial, time_partial, sexual_partial, nrc_partial]
    labels_BFS = ["Number of participants", "Interaction words per user", "Depeche emotions", "Emoticons",
                  "Correctly spelled words", "Time when a conversation starts", "Sexual topic words", "NRC emotions",]
    BF_PSR_partial = DRT_partial
    if verbose:
        print("SHAPES:")
        print(BF_PSR_partial.shape)
    for i in range(8):
        bf_partial = BFS[i]
        if verbose:
            pass
            # print(bf_partial.shape)
        # print(i,") Stacking ",labels_BFS[i]," BF")
        BF_PSR_partial = np.hstack((BF_PSR_partial, bf_partial))
        # print("The final BF-PSR vector is of size: ",BF_PSR_partial.shape)

    if _predict == False:
        probabilities = model.predict_proba(BF_PSR_partial)
        return probabilities
    else:
        predictions = model.predict(BF_PSR_partial)
        f1_g = np.round(f1_score(labels, predictions,
                        average='binary', pos_label=1), 4)
        error_f1_g = error_filtering_PJdataset(labels, predictions)
        print("error_f1_g: ", error_f1_g)
        return f1_g, error_f1_g


def model_predict(info, verbose=False, return_probs=False):
    c = tokenizer_Somajo_vectorizer
    probs = list()

    ###
    # My horrible abomination code
    # enclose in brackets so that we get 1 conversation
    doc_partial = [info[0]]
    X_time_partial = [info[1]]
    X_participants_partial = info[2]
    X_int_user_partial = [info[3]]
    Y_partial = [info[4]]  # same reasoning as above

    # print("Doc partial before: ")
#     print(doc_partial)
    '''Applying preprocessing'''
    doc_partial, X_time_partial, X_participants_partial, X_int_user_partial, Y_partial = pre_processing_conversations_new_datasets(
        c, doc_partial, X_time_partial, X_participants_partial, X_int_user_partial, Y_partial, True)
    Y_partial = np.asarray(Y_partial)

    # need to change the single_conv_groomer_predictions
    # using this line for verbose
    probs = single_conv_groomer_predictions(
        model, doc_partial, X_time_partial, X_participants_partial, X_int_user_partial, Y_partial, False, verbose)
#     print(probs)
#     print("Label is: ", Y_partial)
#     print("Predicted label is:", np.argmax(probs))
    if return_probs:
        return float(np.round(probs[0][1], 4))
    else:
        pred = np.argmax(probs)
        return int(pred)


def get_conversation_information(convo):
    # so that each entry in the array is a different line of conversation
    per_line = convo.split("{-s-c-}")
    text = ""
    # unfortuantely we don't have the time for these messages so I will just set it to be 0:0
    time_first = "0:0"
    number_participants = 2  # just assuming because we have no other knowledge
    interaction_words = [0, 0]
    label = 0
    total_words = 0
    for i in range(len(per_line)):
        message = per_line[i]
        text += " " + message
        word_count = len(message.split(" "))
        total_words += word_count
        interaction_words[i % 2] += word_count
    interaction_words[0] /= total_words
    interaction_words[1] /= total_words

    # we have to pad it because the model expects interaction words to have length 5
    interaction_words += ([0, 0, 0])

    if len(text) < 5:  # if conversation is basically empty
        return False
    return text, time_first, [number_participants], interaction_words, label

# the input should be a string where messages from users are seperated by '\n' newlines


ERROR_STRING = "Error parsing file."


def predict_from_convo(conversation):
    info = get_conversation_information(conversation)
    # print(info)
    res = model_predict(info)
    return int(res)

def give_id_for_online(online_info):
    participants = []
    for i in range(len(online_info)):
        if online_info[i][0] not in participants: #name not in participants
            participants.append(online_info[i][0])
            online_info[i].append(len(participants))
        else:
            online_info[i].append(participants.index(online_info[i][0]) + 1)
    return online_info
    # now it will be (sender, messge, percent, label)

def online_predict_from_xml(xml_data):
    try:
        online_info = get_online_info_from_xml(xml_data)
        for i in range(len(online_info)):
            res = model_predict(online_info[i][2], return_probs=True)
            online_info[i][2] = res
        return online_info
    except Exception as e:
        print(e)
        return ERROR_STRING


def predict_from_xml(xml_data):
    try:
        info = get_info_from_xml(xml_data)
        res = model_predict(info)
        return int(res)
    except:
        return ERROR_STRING


def predict_from_fb_json(json_data):
    try:
        info = get_info_from_facebook_json(json_data)
        res = model_predict(info)
        return int(res)
    except:
        return ERROR_STRING


def online_predict_from_fb_json(json_data):
    try:
        online_info = get_online_info_from_fb_json(json_data)
        for i in range(len(online_info)):
            res = model_predict(online_info[i][2], return_probs=True)
            online_info[i][2] = res
        return online_info
    except Exception as e:
        print(traceback.format_exc())
        return ERROR_STRING

# this will try all the predictors until one works


def brute_predictor(data, as_percent=False):
    info = None

    try:
        info = get_info_from_xml(data)

        res = model_predict(info, return_probs=as_percent)
        return res
    except Exception as e:
        print(e)
    try:
        info = get_info_from_facebook_json(data)
        res = model_predict(info, return_probs=as_percent)
        return res
    except Exception as e:
        print(e)
    return "Error parsing file."


def online_brute_predictor(data):
    online_info = None
    online_info = online_predict_from_xml(data)
    if online_info != ERROR_STRING:
        return give_id_for_online(online_info)
    online_info = online_predict_from_fb_json(data)
    if online_info != ERROR_STRING:
        return give_id_for_online(online_info)
    return ERROR_STRING
