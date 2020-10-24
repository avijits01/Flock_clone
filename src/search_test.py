import pytest
from data import data
from error import InputError, AccessError
import random
import string
import message
import auth
import channel
import channels
import other
import search

import time

def starter():
    # clear all data
    other.clear()
    
    # register four users
    # user 0 is a global owner
    u0 = auth.auth_register('king@gmail.com', 'youshallpass', 'King', 'Kingson')
    u1 = auth.auth_register('elizabeth@gmail.com', 'youshallpass', 'Elizabeth', 'Alexander')
    u2 = auth.auth_register('jane@gmail.com', 'youshallpass', 'Jane', 'Anton')

    return [u0, u1, u2]

def get_random_string(length):
    # Random string with the combination of lower and upper case
    letters = string.ascii_letters
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

def get_message_list(m_id,m):
    message_list = []
    for i in m_id:
        message_details = message.get_message_details(i.get('message_id')).get('message')
        if message_details == m:
            message_list.append(message_details) 
    return message_list


def test_search_0():
    #no messages exits
    starter()
    #one user logs in one channel and one message and searches it
    user = auth.auth_login('king@gmail.com', 'youshallpass')
    token = user.get('token')

    channels.channels_create(token,'1234',True)

    #searches hey
    message_list2 = search.search(token,'hey')

    assert [] == message_list2

def test_search_1():
    starter()
    #one user logs in one channel and one message and searches it
    message_list1 = []
    user = auth.auth_login('king@gmail.com', 'youshallpass')
    token = user.get('token')

    ch = channels.channels_create(token,'1234',True)

    #user sends message hey to channel
    m_id = message.message_send(token,ch.get('channel_id'),'hey')
    message_details = message.get_message_details(m_id.get('message_id')).get('message')

    message_list1.append(message_details)
    #searches hey
    message_list2 = search.search(token,'hey')

    assert message_list1 == message_list2

def test_search_substring():
    starter()
    #one user logs in one channel and one message and searches its substring
    message_list1 = []
    user = auth.auth_login('king@gmail.com', 'youshallpass')
    token = user.get('token')

    ch = channels.channels_create(token,'1234',True)

    #user sends message hey to channel
    m_id = message.message_send(token,ch.get('channel_id'),'hey')
    message_details = message.get_message_details(m_id.get('message_id')).get('message')

    message_list1.append(message_details)
    #searches hey
    message_list2 = search.search(token,'ey')

    assert message_list1 == message_list2


def test_search_mul():
    ''' One user searches for multiple messages in one channel '''
    
    starter()
    #one user logs in one channel and one message and searches it
    user = auth.auth_login('king@gmail.com', 'youshallpass')
    token = user.get('token')

    ch = channels.channels_create(token,'1234',True)

    #user sends messages to channel
    m_id = []
    m_id.append(message.message_send(token,ch.get('channel_id'),'hey'))
    m_id.append(message.message_send(token,ch.get('channel_id'),'hey'))
    m_id.append(message.message_send(token,ch.get('channel_id'),'Im alpha'))
    
    message_list1 = get_message_list(m_id,'hey')

    message_list2 = search.search(token,'hey')

    assert message_list1 == message_list2

def test_search_mul_ch():
    ''' User creates multiple channels and send multiple messages and searches for a message '''

    starter()
    #one user logs in
    user = auth.auth_login('king@gmail.com', 'youshallpass')
    token = user.get('token')

    ch = []
    #create 10 channels
    for i in range(10):
        ch.append(channels.channels_create(token,get_random_string(5),True))
       

    #user sends hey messages to channel1-8
    m_id = []
    for i in ch:
        m_id.append(message.message_send(token,i.get('channel_id'),'hey'))

    #user sends messages to channel9
    m_id.append(message.message_send(token,ch[9].get('channel_id'),'1234'))
    m_id.append(message.message_send(token,ch[9].get('channel_id'),'lol'))

    #user sends messages to channel10
    m_id.append(message.message_send(token,ch[9].get('channel_id'),'1234'))
    m_id.append(message.message_send(token,ch[9].get('channel_id'),'1234'))

    message_list1 = get_message_list(m_id,'hey')

    #user searches for hey
    message_list2 = search.search(token,'hey')
    assert message_list1 == message_list2

    #user searches for lol
    message_list1 = get_message_list(m_id,'lol')
    message_list2 = search.search(token,'lol')
    assert message_list1 == message_list2

    #user searches for 1234
    message_list1 = get_message_list(m_id,'1234')
    message_list2 = search.search(token,'1234')
    assert message_list1 == message_list2

def test_search_mul_user_channel():
    ''' multiple users send different messages in multiple channels and one user searches for a message '''
    starter()

    #one user logs in
    user = auth.auth_login('king@gmail.com', 'youshallpass')
    token = user.get('token')

    #creates two channels
    ch1 = channels.channels_create(token,'1234',True)
    ch2 = channels.channels_create(token,'234',True)

    #user1 sends messages to channel1
    m_id = []
    m_id.append(message.message_send(token,ch1.get('channel_id'),'hey'))
    m_id.append(message.message_send(token,ch1.get('channel_id'),'1234'))

    #user1 sends messages to channel2
    m_id.append(message.message_send(token,ch2.get('channel_id'),'lol'))
    m_id.append(message.message_send(token,ch2.get('channel_id'),'1234'))

    #user1 logs out
    auth.auth_logout(token)

    #user2 logs in
    user = auth.auth_login('elizabeth@gmail.com', 'youshallpass')
    token = user.get('token')

    #user2 joins channel1 only
    channel.channel_join(token,ch1.get('channel_id'))

    #user2 sends messages to channel1
    m_id.append(message.message_send(token,ch1.get('channel_id'),'xyz'))

    #user2 searches for lol
    message_list1 = ['xyz']

    message_list2 = search.search(token,'xyz')
    
    assert message_list1 == message_list2

    #user 2 searches for hey

    message_list1 = ['hey']

    message_list2 = search.search(token,'hey')
    
    assert message_list1 == message_list2

    #user 2 logs out
    auth.auth_logout(token)

    #user 3 logs in 
    user = auth.auth_login('jane@gmail.com', 'youshallpass')
    token = user.get('token')

    #user 3 joins both the channe;s
    channel.channel_join(token,ch1.get('channel_id'))
    channel.channel_join(token,ch2.get('channel_id'))

    #user 3 searches for 1234
    message_list1 = ['1234','1234']
    message_list2 = search.search(token,'1234')

    assert message_list2 == message_list1
