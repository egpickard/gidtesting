import os
import re


def write_conversation(info, filename):
    f = open("data/Cleaned_twitterData/"+filename+".txt", "w")
    for val in info:
        f.write(str(val) + "*+*") #use this instead of commas, because when we split it later, don't want to split on commas in the message itself
    f.close()        

#because this is all from one file we need to just read through sequentially and split the conversations
def seperate_conversations():
    f = open("data/TwitterData/TwitterConvCorpus.txt", "r")
    conversations = f.read()
    f.close()
    convos = conversations.split("\n\n\n\n")
    return convos



def get_conversation_information(convo):
    per_line = convo.split("\n") #so that each entry in the array is a different line of conversation
    text = ""
    time_first = "0:0" #unfortuantely we don't have the time for these messages so I will just set it to be 0:0 
    number_participants = 2 #just assuming because we have no other knowledge 
    interaction_words = [0,0]
    label = 0
    total_words = 0
    for i in range(len(per_line)):
        message = per_line[i]
        text += " " + message
        word_count = len(message.split(" "))
        total_words += word_count
        interaction_words[i%2] += word_count
    interaction_words[0] /= total_words
    interaction_words[1] /= total_words

    if len(text) < 5: # if conversation is basically empty
        return False

    return text, time_first, number_participants, interaction_words, label

convos = seperate_conversations()

id = 0
for convo in convos:
    info = get_conversation_information(convo)
    if not info:
        continue #this means that there was no conversation data
    write_conversation(info,"twitterData_" + str(id))
    id += 1
