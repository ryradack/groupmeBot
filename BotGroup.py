from groupy.client import Client

import interfaceActiveGroups as iAG
import interfaceDogBreeds as iDB
import time, os
import random

keywords = ["dog breed", "dum", "date", "time", "deactivate"]

tokenFileHandle = open('token.txt', 'r')
token = tokenFileHandle.readline()
tokenFileHandle.close()
print(token)

client = Client.from_token(token)

##############################################################################
#-------------------Header---------------------------------------------------#
##############################################################################

groups = client.groups.list()
chats = client.chats.list()

for group in groups:
    if group.id == '52023517':
        bot_group = group

messages = bot_group.messages.list()
last_message = messages[0]

iAG.getActiveGroups()

print(bot_group.name)
print(last_message.text)
print(groups[0])

count = 0

#setup timezone
os.environ['TZ'] = 'America/Chicago'
time.tzset()

#######  Setup ^^^

def botResponse(group, message):
    text = message.text.lower();
    if 'help' in text:
        message_string = "Bot: "
        for i in keywords:
            message_string = message_string + i
            if i != keywords[-1]:
                message_string += ", "
        new_message = group.post(text=message_string)
    elif keywords[0] in text:#dog breed
        message_string = "Bot: " + random.choice(iDB.dog1) + " " + random.choice(iDB.dog2)
        new_message = group.post(text=message_string)
    elif keywords[1] in text:#dum
        new_message = group.post(text='Bot: u dum')
    elif keywords[2] in text:#date
        message_string = 'Bot: ' + time.strftime('%d-%m-%Y')
        new_message = group.post(text=message_string)
    elif keywords[3] in text:#time
        message_string = 'Bot: ' + time.strftime('%H:%M:%S %Z')
        new_message = group.post(text=message_string)
    elif keywords[4] in text:#deactivate
        iAG.removeActiveGroup(group.id)
        message_string = 'Bot: I am no longer active in this chat :\'('
        new_message = group.post(text=message_string)
    else:
        message_string = "Bot: I'm stupid and don't know what to do :(\nTry including one of these keywords: "
        for i in keywords:
            message_string += i
            if i != keywords[-1]:
                message_string += ", "
        new_message = group.post(text=message_string)
    new_message.like()

while(1):
    for group in groups:
        last_message = group.messages.list()[0]
        if '@bot' in last_message.text.lower():
            if group.id in iAG.active_groups:
                botResponse(group, last_message)
            elif last_message.name == 'Ryley Radack' and 'activate' in last_message.text.lower():
                print(group.id)
                iAG.addActiveGroup(group.id)
                message_string = "Bot: I am now active in this chat :)"
                new_message = group.post(text=message_string)
                new_message.like()
            elif 'update' in last_message.text.lower():
                iAG.getActiveGroups()
                print(iAG.active_groups)

#    for chat in chats: #Chats id's overlap with group ids?? chats mess stuff up, playin with fire...
#        last_chat_message = chat.messages.list()[0]
        #print(last_chat_message)
        #print(last_chat_message.text)
#        if '@bot' in last_chat_message.text:
#            print(chat.other_user['name'])
#            botResponse(group, last_chat_message)

    count += 1;
    time.sleep(5)
    if count > 1000000:
        groups = client.groups.list()#_all()
        count = 0
#        chats = client.chats.list_all()
