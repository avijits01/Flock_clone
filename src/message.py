from error import InputError, AccessError
from data import data

from channel import is_channel_member, is_channel_owner, is_global_owner
import time

# note: changed message to messages in data


##########################
#    helper functions    #
##########################

# returns {} if message_id does not exist
# returns {u_id, channel_id, message} otherwise
def get_message_details(message_id):
    # search through channels for message
    for channel in data['channels']:
        for message in channel['messages']:
            if message['message_id'] == message_id:
                return {
                    'u_id': message['u_id'],
                    'channel_id': channel['channel_id'],
                    'message' : message['message']
                }
                
    return { }


##########################
#    implementations     #
##########################

## message_send ##

def message_send(token, channel_id, message):
    
    # get u_id 
    u_id = data['tok_uid'][token]
    
    # InputError: message is more than 1000 characters
    if (len(message) > 1000):
        raise InputError(description='Message exceeds 1000 characters')
    
    # AccessError: authorised user is not a member of the channel
    if not is_channel_member(u_id, channel_id):
        raise AccessError(description='User is not a member of channel')
    
    # generate message_id
    message_id = data['last_m_id'] + 1
    data['last_m_id'] = message_id
    
    # unix timestamp
    time_created = int(time.time())
    
    # create message dictionary 
    new_message = {
        'message_id': message_id,
        'u_id': u_id,
        'message': message,
        'time_created': time_created
    }
    
    # append to messages list of given channel
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            channel['messages'].insert(0, new_message)
    
    return {
        'message_id': message_id
    }

def message_remove(token, message_id):
    
    u_id = data['tok_uid'][token]
    message_det = get_message_details(message_id)

    # InputError: message does not exist
    if message_det == {}:
        raise InputError(description='Message does not exist')
    
    
    # AccessError: authorised user was not the sender of message
    # AND authorised user is not an owner of the channel or a global owner
    if message_det['u_id'] != u_id and not is_global_owner(u_id) and not is_channel_owner(u_id, message_det['channel_id']):
        raise AccessError(description='User is not authorised to remove message')
    
    # find message in channel
    for channel in data['channels']:
        if channel['channel_id'] == message_det['channel_id']:
            for message in channel['messages']:
                if message['message_id'] == message_id:
                    channel['messages'].remove(message)
                    

    return { }


def message_edit(token, message_id, message):
    u_id = data.get('tok_uid')[token]

    message_det = get_message_details(message_id)

    # AccessError: authorised user was not the sender of message
    # AND authorised user is not an owner of the channel or a global owner
    if message_det['u_id'] != u_id and not is_global_owner(u_id) and not is_channel_owner(u_id, message_det['channel_id']):
        raise AccessError(description='User is not authorised to edit message')

    for channel in data['channels']:
        if channel['channel_id'] == message_det['channel_id']:
            for m in channel['messages']:
                if m['message_id'] == message_id:
                    # if edit is empty, delete message
                    if message == '':
                        channel['messages'].remove(m)
                    # else, update message string
                    else:
                        m['message'] = message
    
    return { }
    
    

