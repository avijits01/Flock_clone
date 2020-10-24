import pytest
from data import data
from error import InputError, AccessError
import message
import auth
import channel
import channels
import other

import time

def starter():
    # clear all data
    other.clear()
    
    # register three users
    # user 0 is a global owner
    u0 = auth.auth_register('king@gmail.com', 'youshallpass', 'King', 'Kingson')
    u1 = auth.auth_register('elizabeth@gmail.com', 'youshallpass', 'Elizabeth', 'Alexander')
    u2 = auth.auth_register('jane@gmail.com', 'youshallpass', 'Jane', 'Anton')

    # user 1 creates a public channel (channel owner)
    c1 = channels.channels_create(u1['token'], 'public channel', True)
    
    return [u0, u1, u2, c1]


##############################
#     message_send tests     #
##############################

# InputError: message is longer than 1000 chars
def test_send_input_err():
    info = starter()
    u1, c1 = info[1], info[3]
    long_str = 'A' * 1001
    with pytest.raises(InputError):
        assert message.message_send(u1['token'], c1['channel_id'], long_str)
        

# AccessError: authorised user is not member of channel with channel_id
def test_send_access_err():
    info = starter()
    u2, c1 = info[2], info[3]
    with pytest.raises(AccessError):
        # user 2 (not a member of c1) attempts to send message in c1
        assert message.message_send(u2['token'], c1['channel_id'], 'Hi')


# no errors: message is sent to channel
def test_send_standard():
    info = starter()
    u1, c1 = info[1], info[3]
    
    # get current timestamp
    time_created = int(time.time())
    
    # u1 (member of c1) sends first message
    m_id1 = message.message_send(u1['token'], c1['channel_id'], "One")
    m1_info = {'message_id': m_id1['message_id'], 'u_id': u1['u_id'], 'message': 'One', 'time_created': time_created}
   
    # message should appear in channel messages list
    c1_messages = channel.channel_messages(u1['token'], c1['channel_id'], 0)
    assert c1_messages['messages'] == [m1_info]
    
    # u1 sends another message
    m_id2 = message.message_send(u1['token'], c1['channel_id'], "Two")
    m2_info = {'message_id': m_id2['message_id'], 'u_id': u1['u_id'], 'message': 'Two', 'time_created': time_created}
    
    # boths message should appear in channel messages list, with m2 appearing first 
    c1_messages = channel.channel_messages(u1['token'], c1['channel_id'], 0)
    assert c1_messages['messages'] == [m2_info, m1_info]
    

##############################
#    message_remove tests    #
##############################

# InputError: message with message_id does not exist
def test_remove_input_err():
    info = starter()
    u1 = info[1]
    with pytest.raises(InputError):
        # u1 attempts to remove a message from empty channel
        assert message.message_remove(u1['token'], 1)
 
 
# AccessError: message was not sent by authorised user (who is a regular member)
def test_remove_access():
    info = starter()
    u1, u2, c1 = info[1], info[2], info[3]
    
    # user 2 joins channel 
    channel.channel_join(u2['token'], c1['channel_id'])
    
    # u1 sends a message to c1
    m_id = message.message_send(u1['token'], c1['channel_id'], 'Hello')
    
    with pytest.raises(AccessError):
       # u2 attempts to remove u1's message
        assert message.message_remove(u2['token'], m_id['message_id'])


# no errors: message is removed from channel
def test_remove_standard():
    info = starter()
    u1, c1 = info[1], info[3]
    
    # user 1 sends two messages
    m_id1 = message.message_send(u1['token'], c1['channel_id'], "One")
    m_id2 = message.message_send(u1['token'], c1['channel_id'], "Two")
    
    # user 1 deletes m1
    message.message_remove(u1['token'], m_id1['message_id'])
    
    # only message 2 should be in messages now
    c1_messages = channel.channel_messages(u1['token'], c1['channel_id'], 0)
    assert len(c1_messages['messages']) == 1
    assert c1_messages['messages'][0]['message_id'] == m_id2['message_id']
    

##############################
#     message_edit tests     #
##############################

# AccessError: message was not sent by authorised user (who is a regular member)
def test_edit_access_err():
    info = starter()
    u1, u2, c1 = info[1], info[2], info[3]
    
    # user 2 joins channel 
    channel.channel_join(u2['token'], c1['channel_id'])
    
    # u1 sends a message to c1
    m_id = message.message_send(u1['token'], c1['channel_id'], 'Hello')
    
    with pytest.raises(AccessError):
       # u2 attempts to edit u1's message
        assert message.message_edit(u2['token'], m_id['message_id'], 'edited')


# no errors: message is edited
def test_edit_standard():
    info = starter()
    u1, c1 = info[1], info[3]
    
    # user 1 sends a message to c1
    m_id = message.message_send(u1['token'], c1['channel_id'], "Original")
    # user 1 edits the message
    message.message_edit(u1['token'], m_id['message_id'], "Edited")
    
    # message should now be "Edited"
    c1_messages = channel.channel_messages(u1['token'], c1['channel_id'], 0)
    assert c1_messages['messages'][0]['message'] == "Edited"


# no errors: edit string is empty and message is deleted
def test_edit_standard_del():
    info = starter()
    u1, c1 = info[1], info[3]
    
    # user 1 sends two messages to c1
    m_id1 = message.message_send(u1['token'], c1['channel_id'], "One")
    m_id2 = message.message_send(u1['token'], c1['channel_id'], "Two")
    # user 1 edits message 1 with empty string
    message.message_edit(u1['token'], m_id1['message_id'], "")
    
    # message 1 should be deleted (only message 2 remains)
    c1_messages = channel.channel_messages(u1['token'], c1['channel_id'], 0)
    assert c1_messages['messages'][0]['message_id'] == m_id2['message_id']





    
