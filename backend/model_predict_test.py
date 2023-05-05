from model_predict import *
import os


def read_data(filename):
    #     f = open("Data/Cleaned_BF-PSR/asian_kreationz.txt", "r")
    f = open(filename, "r")
    info = f.read()
    f.close()
    info = info.split('*+*')[:-1]
    info[2] = [int(info[2])]
    info[4] = int(info[4])
    # make the interaction words correct
    info[3] = info[3][1:-1].split(',')
    info[3][0] = float(info[3][0])
    info[3][1] = float(info[3][1])
    if len(info[3]) < 5:  # this will always be true for this dataset
        for i in range(5-len(info[3])):
            info[3].append(0.0)
    return info


def analyze_files(directory):
    correct = 0
    total = 0
    wrong_files = []
    for filename in os.scandir(directory):

        if filename.is_file():
            print("*********")
            print(filename.name)
            info = read_data(filename)
            res = model_predict(info, verbose=False, return_probs=True)
            pred = np.argmax(res)
            print(res)
            print(pred)
            if pred == info[-1]:
                correct += 1
            else:
                wrong_files.append([filename.name, info[0]])
            total += 1
    print("Correct: ", str(correct))
    print("Total: ", str(total))
    print(correct/total)
    return wrong_files


# directory = "data/Cleaned_BF-PSR/"
# wrong_files_TP = analyze_files(directory)

# test = "what's up dadyo when did you get back on Twitter? Haha \nlike 2 weeks ago and it's going as terribly as I remember, but Deg is still hilarious so it's ok\nliterally never about that account, love it."
# test = "what's up dadyo when did you get back on Twitter? Haha{-s_w-}like 2 weeks ago and it's going as terribly as I remember, but Deg is still{-s_w-}hilarious so it's ok{-s_w-}literally never about that account, love it."
# res = predict_from_convo(test)
# print(type(res))


filename = "../data/GeneralData/asian_kreationz.xml"


# f = open(filename, "r")
# xml_data = f.read()
# f.close()
# online_pred = online_predict_from_xml(xml_data)
# for val in online_pred:
#     print(str(val[2]) + " :: " + val[0] + " : " + val[1])
#     print()

f = open(filename, "r")
json_data = f.read()
f.close()
online_pred = online_predict_from_xml(json_data)
for val in online_pred:
    print(str(val[2]) + " :: " + val[0] + " : " + val[1])
    print()
