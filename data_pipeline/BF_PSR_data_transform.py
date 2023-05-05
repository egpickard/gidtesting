from bs4 import BeautifulSoup
import os
import re

def get_soup(filename):
    with open(filename) as fp:
        soup = BeautifulSoup(fp, 'xml')
    return soup


def get_first_message_time(posts):
    #get the time of the first message and convert it
    index = 0
    for val in posts:
        if val.USERNAME.string != None:
            break
        index +=1
    temp_time = posts[index].DATETIME.string
    print("Initial time value")
    print(temp_time)
    if temp_time == None:
        return "0:0"
    temp_time = temp_time.split(':')
    print(temp_time)
    if '/' in temp_time[0]:
        temp_time[0] = temp_time[0].split()[1]
    temp_time[0] = re.sub(r'[^0-9]', '', temp_time[0])
    print(temp_time)
    if len(temp_time) == 3:
        temp_time[0] = int(temp_time[0])
        temp_time[1] = int(temp_time[1])
        if 'pm' in temp_time[2].lower() or 'p.m.' in temp_time[2].lower():
            temp_time[0] += 12
    elif len(temp_time) == 2:
        temp_time[0] = int(temp_time[0])
        print(temp_time[1].lower())
        if 'pm' in temp_time[1].lower() or 'p.m.' in temp_time[1].lower():
            temp_time[0] += 12
        temp_time[1] = int(temp_time[1].split()[0])
    if temp_time[0] > 23:
        temp_time[0] = 12 #because if its more than 23 it means that 12 pm was converted to 24
    return str(temp_time[0]) + ":" + str(temp_time[1])

#warning some values are hardcoded to work with this specific dataset, should inspect and change what is 
# needed if trying to convert from a different dataset
def get_conversation_information(soup,asarray=False):
    conversation = "" # we will save the entire conversation text to this string
    time_first = "" #store the time of the first message
    number_participants = -1 
    interaction_word_count = {} #each entry of the dictionary will have a counter for how many words that use sent
    total_words = 0
    label = 1 # this is because all the data we are doing is for groomers, but this could be changed in the future
    posts = soup.find_all('POST')
    #get the id of the perpetrator
    predator_id = soup.PREDATOR.SCREENNAME.USERNAME.string
    #and id of victim
    victim_id = soup.VICTIM.SCREENNAME.USERNAME.string
    #initialize the word counts
    interaction_word_count[predator_id] = 0
    interaction_word_count[victim_id] = 0 
    #get the start time of conversation
    time_first = get_first_message_time(posts)
    number_participants = 2 #because all of these conversations are between two different people

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
            continue # there is no point in getting a message that is not from either the predator or victim
    interaction_words_per_user = [interaction_word_count[predator_id]/total_words,interaction_word_count[victim_id]/total_words]

    #remove newlines from the conversation
    conversation = conversation.replace('\\n', "") 
    if asarray:
        return [conversation, time_first, number_participants, interaction_words_per_user, label]
    return conversation, time_first, number_participants, interaction_words_per_user, label
        
def write_conversation(info, filename):
    f = open("data/Cleaned_BF-PSR/"+filename+".txt", "w")
    for val in info:
        f.write(str(val) + "*+*") #use this instead of commas, because when we split it later, don't want to split on commas in the message itself
    f.close()        
    
directory = 'data/GeneralData/'
filename = 'ArmySgt1961'
#conv_text,time,number_participants,interaction_words,label = get_conversation_information(get_soup(directory+filename+".xml"),asarray=False)

#converted_info = get_conversation_information(get_soup(directory+filename+".xml"),asarray=True)

#write_conversation(converted_info,filename)

directory = 'data/GeneralData'
# iterate over files in
# that directory
for filename in os.scandir(directory):
    if filename.is_file():
        print("*********")
        print(filename.name)
        soup = get_soup(filename.path)
        info = get_conversation_information(soup)
        write_conversation(info,filename.name.split(".")[0])