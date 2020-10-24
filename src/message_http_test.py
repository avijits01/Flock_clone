import pytest
import re
from subprocess import Popen, PIPE
import signal
from time import sleep
import requests
import json

import time

# Use this fixture to get the URL of the server. It starts the server for you,
# so you don't need to.
@pytest.fixture
def url():
    url_re = re.compile(r' \* Running on ([^ ]*)')
    server = Popen(["python3", "src/server.py"], stderr=PIPE, stdout=PIPE)
    line = server.stderr.readline()
    local_url = url_re.match(line.decode())
    if local_url:
        yield local_url.group(1)
        # Terminate the server
        server.send_signal(signal.SIGINT)
        waited = 0
        while server.poll() is None and waited < 5:
            sleep(0.1)
            waited += 0.1
        if server.poll() is None:
            server.kill()
    else:
        server.kill()
        raise Exception("Couldn't get URL from local server")



## starter
def starter(url):
    
    # register three users
    
    u0_info = {'email': 'king@gmail.com', 'password': 'youshallpass', 'name_first': 'King', 'name_last': 'Kingson'}
    u1_info = {'email': 'elizabeth@gmail.com', 'password': 'youshallpass', 'name_first': 'Elizabeth', 'name_last': 'Alexander'}
    u2_info = {'email': 'jane@gmail.com', 'password': 'youshallpass', 'name_first': 'Jane', 'name_last': 'Anton'}

    # user 0 is a global owner
    r = requests.post(url + 'auth/register', json = u0_info)
    u0 = r.json()
    r = requests.post(url + 'auth/register', json = u1_info)
    u1 = r.json()
    r = requests.post(url + 'auth/register', json = u2_info)
    u2 = r.json()


    # user 1 creates a public channel (channel owner)
    c1_info = {'token': u1['token'], 'name': 'public channel', 'is_public': True}
    r = requests.post(url + 'channels/create', json = c1_info)
    c1 = r.json()
    
    
    return [u0, u1, u2, c1]



##############################
#     message_send tests     #
##############################

# InputError: message is longer than 1000 chars
def test_send_input_err(url):
    info = starter(url)
    u1, c1 = info[1], info[3]
    long_str = 'A' * 1001
    
    r = requests.post(url + 'message/send', json = {'token': u1['token'], 'channel_id': c1['channel_id'], 'message': long_str})
    err = r.json()
    
    assert err['code'] == 400
    assert err['message'] == '<p>Message exceeds 1000 characters</p>'


# AccessError: authorised user is not member of channel with channel_id
def test_send_access_err(url):
    info = starter(url)
    u2, c1 = info[2], info[3]

    r = requests.post(url + 'message/send', json = {'token': u2['token'], 'channel_id': c1['channel_id'], 'message': 'Hi'})
    err = r.json()
    
    assert err['code'] == 400
    assert err['message'] == '<p>User is not a member of channel</p>'


# no errors: message is sent to channel
def test_send_standard(url):
    info = starter(url)
    u1, c1 = info[1], info[3]
    
    # get current timestamp
    time_created = int(time.time())
    
    # u1 (member of c1) sends first message
    r = requests.post(url + 'message/send', json = {'token': u1['token'], 'channel_id': c1['channel_id'], 'message': "One"})
    m_id1 = r.json()
    m1_info = {'message_id': m_id1['message_id'], 'u_id': u1['u_id'], 'message': 'One', 'time_created': time_created}
   
    # message should appear in channel messages list
    r = requests.get(url + 'channel/messages', params = {'token': u1['token'], 'channel_id': c1['channel_id'], 'start': 0})
    c1_messages = r.json()
    print(c1_messages)
    assert c1_messages['messages'] == [m1_info]
  
    # u1 sends another message
    r = requests.post(url + 'message/send', json = {'token': u1['token'], 'channel_id': c1['channel_id'], 'message': "Two"})
    m_id2 = r.json()
    m2_info = {'message_id': m_id2['message_id'], 'u_id': u1['u_id'], 'message': 'Two', 'time_created': time_created}
    
    # boths message should appear in channel messages list, with m2 appearing first 
    r = requests.get(url + 'channel/messages', params = {'token': u1['token'], 'channel_id': c1['channel_id'], 'start': 0})
    c1_messages = r.json()
    assert c1_messages['messages'] == [m2_info, m1_info]


##############################
#    message_remove tests    #
##############################


# InputError: message with message_id does not exist
def test_remove_input_err(url):
    info = starter(url)
    u1 = info[1]
    
    # u1 attempts to remove a message from empty channel
    r = requests.delete(url + 'message/remove', json = {'token': u1['token'], 'message_id': 1}) 
    err = r.json()

    assert err['code'] == 400
    assert err['message'] == '<p>Message does not exist</p>'
    

# AccessError: message was not sent by authorised user (who is a regular member)
def test_remove_access(url):
    info = starter(url)
    u1, u2, c1 = info[1], info[2], info[3]
    
    # user 2 joins channel
    requests.post(url + 'channel/join', json = {'token': u2['token'], 'channel_id': c1['channel_id']}) 
    
    # u1 sends a message to c1
    r = requests.post(url + 'message/send', json = {'token': u1['token'], 'channel_id': c1['channel_id'], 'message': 'Hello'})
    m_id = r.json()
    
    r = requests.delete(url + 'message/remove', json = {'token': u2['token'], 'message_id': m_id['message_id']})
    err = r.json()
    
    assert err['code'] == 400
    assert err['message'] == '<p>User is not authorised to remove message</p>'
    

# no errors: message is removed from channel
def test_remove_standard(url):
    info = starter(url)
    u1, c1 = info[1], info[3]
    
    # user 1 sends two messages
    r = requests.post(url + 'message/send', json = {'token': u1['token'], 'channel_id': c1['channel_id'], 'message': "One"})
    m_id1 = r.json()
    r = requests.post(url + 'message/send', json = {'token': u1['token'], 'channel_id': c1['channel_id'], 'message': "Two"})
    m_id2 = r.json()
    
    # user 1 deletes m1
    requests.delete(url + 'message/remove', json = {'token': u1['token'], 'message_id': m_id1['message_id']})
    
    # only message 2 should be in c1
    r = requests.get(url + 'channel/messages', params = {'token': u1['token'], 'channel_id': c1['channel_id'], 'start': 0})
    c1_messages = r.json()
    
    assert len(c1_messages['messages']) == 1
    assert c1_messages['messages'][0]['message_id'] == m_id2['message_id']


#Access error
def test_edit_access(url):

    info = starter(url)
    u1,u2,c1 = info[1], info[2], info[3]

    # user 2 joins channel
    requests.post(url + 'channel/join', json = {'token': u2['token'], 'channel_id': c1['channel_id']}) 

    #user 1 sends a message
    r = requests.post(url + 'message/send', json = {'token':u1['token'], 'channel_id': c1['channel_id'], 'message':'lol'})
    m_id = r.json()

    #user 2 edits the message
    r = requests.post(url + 'message/edit', json = {'token':u2['token'], 'message_id':m_id['message_id'], 'message':'hey'})
    err = r.json()

    assert err['code'] == 400
    assert err['message'] == '<p>User is not authorised to edit message</p>'

def test_message_edit(url):

    info = starter(url)
    u1, c1 = info[1], info[3]

    #user 1 sends a message
    r = requests.post(url + 'message/send', json = {'token':u1['token'], 'channel_id': c1['channel_id'], 'message': 'hey'})
    m_id = r.json()

    #user 1 edits the message
    r = requests.post(url + 'message/edit', json = {'token':u1['token'], 'message_id':m_id['message_id'], 'message':'hello'})

    # only message 2 should be in c1
    r = requests.get(url + 'channel/messages', params = {'token': u1['token'], 'channel_id': c1['channel_id'], 'start': 0})
    c1_messages = r.json()

    assert c1_messages['messages'][0]['message'] == 'hello'






