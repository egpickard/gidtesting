from bs4 import BeautifulSoup
import os

def get_soup(filename):
    with open(filename) as fp:
        soup = BeautifulSoup(fp, 'xml')
    return soup

#This will print the entire xml document
# print(soup.prettify())

# This finds the first instance of a POST tag and prints the string the BODY tag contains
# print(soup.POST.BODY.string)
# Use Find all to obtain a list containing all instances of POST tags
# print(soup.find_all('POST'))
def get_conversation(soup):
    posts = soup.find_all('POST')

    sender_and_message = []
    #get the id of the perpetrator
    predator_id = soup.PREDATOR.SCREENNAME.USERNAME.string
    #and id of victim
    victim_id = soup.VICTIM.SCREENNAME.USERNAME.string
    #Iterate through the list and obtain a list of usernames and strings
    for post in posts:
        poster = post.USERNAME.string
        if poster == predator_id:
            poster = "1"
        elif poster == victim_id:
            poster = "2"
        else:
            continue # there is no point in getting a message that is not from either the predator or
        message = post.BODY.string
        #Added this just in case there is no mesage
        message = message if message != None else "no message"
        sender_and_message.append([poster, message])
    return sender_and_message

#Print out the messages
# for val in sender_and_message:
#     print(val[0] + " : " + val[1])

def write_conversation(sender_and_message, filename):
    f = open("data/cleaned/"+filename+".txt", "w")
    for val in sender_and_message:
        f.write(val[0] + " : " + val[1]+"\n")
    f.close()

'''
directory = 'data/GeneralData'
# iterate over files in
# that directory
for filename in os.scandir(directory):
    if filename.is_file():
        print(filename.name)
        soup = get_soup(filename.path)
        sender_and_message = get_conversation(soup)
        write_conversation(sender_and_message,filename.name.split(".")[0])
'''