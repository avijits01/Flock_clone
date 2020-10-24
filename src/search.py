from data import data

from channel import channel_details
from channels import channels_list
import time

def check(string, sub_str): 
    if (string.find(sub_str) == -1): 
        return False
    else: 
        return True

def search(token,query_str):
    message_list = []
    tok_uid = data.get('tok_uid')
    channels = data.get('channels')
    if token is None:
        print('Not logged in')
    else:
        uid = tok_uid.get(token) 

        for i in channels:
            id = i.get('channel_id')
            #will give access error if other user tried to access
            try:
                diction = channel_details(token,id)
            except:
                continue
            members = diction.get('all_members')
            for j in members:
                check_id = j.get('u_id')

                if check_id is uid:
                    message = i.get('messages')
                    for j in message:
                        if check(j.get('message'),query_str):
                            message_list.append(j.get('message'))
    return message_list
