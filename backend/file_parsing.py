from bs4 import BeautifulSoup
import re
import datetime
import json


def get_first_message_time(posts):
    # get the time of the first message and convert it
    index = 0
    for val in posts:
        if val.USERNAME.string != None:
            break
        index += 1
    temp_time = posts[index].DATETIME.string
    if temp_time == None:
        return "0:0"
    temp_time = temp_time.split(':')
    if '/' in temp_time[0]:
        temp_time[0] = temp_time[0].split()[1]
    temp_time[0] = re.sub(r'[^0-9]', '', temp_time[0])
    if len(temp_time) == 3:
        temp_time[0] = int(temp_time[0])
        temp_time[1] = int(temp_time[1])
        if 'pm' in temp_time[2].lower() or 'p.m.' in temp_time[2].lower():
            temp_time[0] += 12
    elif len(temp_time) == 2:
        temp_time[0] = int(temp_time[0])
        if 'pm' in temp_time[1].lower() or 'p.m.' in temp_time[1].lower():
            temp_time[0] += 12
        temp_time[1] = int(temp_time[1].split()[0])
    if temp_time[0] > 23:
        # because if its more than 23 it means that 12 pm was converted to 24
        temp_time[0] = 12
    return str(temp_time[0]) + ":" + str(temp_time[1])

# warning some values are hardcoded to work with this specific dataset, should inspect and change what is
# needed if trying to convert from a different dataset


def get_conversation_information(soup):
    conversation = ""  # we will save the entire conversation text to this string
    time_first = ""  # store the time of the first message
    number_participants = -1
    # each entry of the dictionary will have a counter for how many words that use sent
    interaction_word_count = {}
    total_words = 0
    label = 1  # this is because all the data we are doing is for groomers, but this could be changed in the future
    posts = soup.find_all('POST')
    # get the id of the perpetrator
    predator_id = soup.PREDATOR.SCREENNAME.USERNAME.string
    # and id of victim
    victim_id = soup.VICTIM.SCREENNAME.USERNAME.string
    # initialize the word counts
    interaction_word_count[predator_id] = 0
    interaction_word_count[victim_id] = 0
    # get the start time of conversation
    time_first = get_first_message_time(posts)
    # because all of these conversations are between two different people
    number_participants = 2

    for post in posts:
        poster = post.USERNAME.string
        message = post.BODY.string
        if message == None:
            continue
        word_count = len(message.split(" "))

        if poster == predator_id or poster == victim_id:
            conversation += " " + message
            total_words += word_count
            interaction_word_count[poster] += word_count
        else:
            continue  # there is no point in getting a message that is not from either the predator or victim
    interaction_words_per_user = [interaction_word_count[predator_id] /
                                  total_words, interaction_word_count[victim_id]/total_words]

    # remove newlines from the conversation
    conversation = conversation.replace('\\n', "")
    interaction_words_per_user += ([0, 0, 0])

    return conversation, time_first, [number_participants], interaction_words_per_user, label


def get_online_conversation_information(soup):
    online_info = []

    conversation = ""  # we will save the entire conversation text to this string
    time_first = ""  # store the time of the first message
    number_participants = -1
    # each entry of the dictionary will have a counter for how many words that use sent
    interaction_word_count = {}
    total_words = 0
    label = 1  # this is because all the data we are doing is for groomers, but this could be changed in the future
    posts = soup.find_all('POST')
    # get the id of the perpetrator
    predator_id = soup.PREDATOR.SCREENNAME.USERNAME.string
    # and id of victim
    victim_id = soup.VICTIM.SCREENNAME.USERNAME.string
    # initialize the word counts
    interaction_word_count[predator_id] = 0
    interaction_word_count[victim_id] = 0
    # get the start time of conversation
    time_first = get_first_message_time(posts)
    # because all of these conversations are between two different people
    number_participants = 2

    for post in posts:
        poster = post.USERNAME.string
        message = post.BODY.string
        if message == None:
            continue
        word_count = len(message.split(" "))

        if poster == predator_id or poster == victim_id:
            conversation += " " + message
            total_words += word_count
            interaction_word_count[poster] += word_count

            interaction_words_per_user = [interaction_word_count[predator_id] /
                                          total_words, interaction_word_count[victim_id]/total_words]

            # remove newlines from the conversation
            conversation = conversation.replace('\\n', "")
            interaction_words_per_user += ([0, 0, 0])

            info = [conversation, time_first, [number_participants],
                    interaction_words_per_user, label]
            online_info.append([poster, message, info])

        else:
            continue  # there is no point in getting a message that is not from either the predator or victim

    return online_info


def fb_get_online_conversation_information(file):
    online_info = []

    number_participants = len(file["participants"])  # very easy lol
    conversation = ""
    interaction_words_per_user = {}
    # initialize the value for each participant to 0 at the start
    for i in range(number_participants):
        interaction_words_per_user[file["participants"][i]["name"]] = 0
    total_words = 0
    time_first_ms = file["messages"][-1]["timestamp_ms"]
    time_first = datetime.datetime.fromtimestamp(time_first_ms/1000.0)
    time_first = str(time_first.hour) + ":" + str(time_first.minute)

    for message in file["messages"]:
        if "content" in message:
            text = message["content"]
            word_count = len(text.split(" "))
            total_words += word_count
            conversation += " " + text
            interaction_words_per_user[message["sender_name"]] += word_count

            interaction_words = []
            for name, words in interaction_words_per_user.items():
                interaction_words.append(words/word_count)
            while len(interaction_words) < 5:
                interaction_words.append(0)
            info = [conversation, time_first, [number_participants],
                    interaction_words, 0]

            online_info.append([message["sender_name"], text, info])

    return online_info[::-1]


def fb_get_conversation_information(file):
    number_participants = len(file["participants"])  # very easy lol
    conversation = ""
    interaction_words_per_user = {}
    # initialize the value for each participant to 0 at the start
    for i in range(number_participants):
        interaction_words_per_user[file["participants"][i]["name"]] = 0
    total_words = 0
    time_first_ms = file["messages"][-1]["timestamp_ms"]
    time_first = datetime.datetime.fromtimestamp(time_first_ms/1000.0)
    time_first = str(time_first.hour) + ":" + str(time_first.minute)

    for message in file["messages"]:
        if "content" in message:
            text = message["content"]
            word_count = len(text.split(" "))
            total_words += word_count
            conversation += " " + text
            interaction_words_per_user[message["sender_name"]] += word_count

    # now we just have to clean up the interaction words and we are set
    interaction_words = []
    for name, words in interaction_words_per_user.items():
        interaction_words.append(words/word_count)
    while len(interaction_words) < 5:
        interaction_words.append(0)

    # label doesn't really matter
    return conversation, time_first, [number_participants], interaction_words, 0


def get_online_info_from_xml(file):
    soup = BeautifulSoup(file, 'xml')
    online_info = get_online_conversation_information(soup)
    return online_info


def get_info_from_xml(file):
    soup = BeautifulSoup(file, 'xml')
    info = get_conversation_information(soup)
    return info


def get_info_from_facebook_json(file):
    file = json.loads(file)
    info = fb_get_conversation_information(file)
    return info


def get_online_info_from_fb_json(file):
    file = json.loads(file)
    online_info = fb_get_online_conversation_information(file)
    return online_info
