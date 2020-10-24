import search

import pytest
import re
from subprocess import Popen, PIPE
import signal
from time import sleep
import requests
import json
import auth, channels, channel
from helper_functions import clear_data

# Use this fixture to get the URL of the server. It starts the server for you,
# so you don't need to.
import message

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

def starter(url):
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

    return [u0,u1,u2]

def test_search_1(url):
    info = starter(url)
    u0 = info[0]

    r = requests.post( url + '/channels/create', json = {'token':u0['token'], 'name':'public', 'is_public' : True})
    ch1 = r.json()

    r = requests.post( url + '/message/send', json = {'token':u0['token'], 'channel_id':ch1['channel_id'], 'message':'hey'})
    m1 = r.json()

    r = requests.get( url + '/search', params = {'token':u0['token'], 'message':'hey'})
    m_list = r.json()

    assert m_list[0] == 'hey'

def test_search_2(url):
    info = starter(url)
    u0 = info[0]

    r = requests.post( url + '/channels/create', json = {'token':u0['token'], 'name':'public', 'is_public' : True})
    ch1 = r.json()

    r = requests.post( url + '/message/send', json = {'token':u0['token'], 'channel_id':ch1['channel_id'], 'message':'hey'})
    r = requests.post( url + '/message/send', json = {'token':u0['token'], 'channel_id':ch1['channel_id'], 'message':'hello'})

    r = requests.get( url + '/search', params = {'token':u0['token'], 'message':'hey'})
    m_list = r.json()

    print(m_list)

    assert m_list[0] == 'hey'

def test_search_3(url):
    info = starter(url)
    u0, u1 = info[0], info[1]

    r = requests.post( url + '/channels/create', json = {'token':u0['token'], 'name':'public', 'is_public' : True})
    ch1 = r.json()

    #user 2 creates private channel
    r = requests.post( url + '/channels/create', json = {'token':u1['token'], 'name':'public', 'is_public' : False})
    ch2 = r.json()

    r = requests.post( url + '/message/send', json = {'token':u0['token'], 'channel_id':ch1['channel_id'], 'message':'hey'})
    r = requests.post( url + '/message/send', json = {'token':u0['token'], 'channel_id':ch1['channel_id'], 'message':'heya'})

    r = requests.post( url + '/message/send', json = {'token':u1['token'], 'channel_id':ch2['channel_id'], 'message':'heya'})

    # user 2 joins channel 1
    requests.post(url + 'channel/join', json = {'token': u1['token'], 'channel_id': ch1['channel_id']}) 

    r = requests.get( url + '/search', params = {'token':u1['token'], 'message':'hey'})
    m_list = r.json()

    assert m_list[0] == 'heya'
    assert m_list[1] == 'hey'
