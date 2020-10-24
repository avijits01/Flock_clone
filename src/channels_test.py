from data import data
import auth
from auth import auth_login
import channels
import channel
import data
import helper_functions


    
 
def test_channels_list():
    #dictionary of token and uid when user logs in and the element removes when he logs out


    helper_functions.clear_data()
    user1_email = '1234@gmail.com'
    user1_password = 'asdfghjk'
    user1_firstname = 'USER'
    user1_lastname = '1'
    
    diction = auth.auth_register(user1_email,user1_password,user1_firstname,user1_lastname)
    token = diction.get('token')
    id_dict = channels.channels_create(token,user1_firstname,True)

    channel_id = id_dict.get('channel_id')
    channels.channels_create(token,user1_firstname,True)

    chan = channels.channels_list(token)
    chan = chan.get('channels')
    assert channel_id!= None
    assert chan!=None
    assert True

def test_channels_list_1channel():
    #dictionary of token and uid when user logs in and the element removes when he logs out

    helper_functions.clear_data()
    user1_email = '1234@gmail.com'
    user1_password = 'asdfghjk'
    user1_firstname = 'USER'
    user1_lastname = '1'
    
    diction = auth.auth_register(user1_email,user1_password,user1_firstname,user1_lastname)
    token = diction.get('token')
    ## uid = diction.get('u_id')
    id_dict = channels.channels_create(token,user1_firstname,True)

    channel_id = id_dict.get('channel_id')

    chan = channels.channels_list(token)
    chan = chan.get('channels')
    assert chan == [{'channel_id':channel_id,'name':user1_firstname}]

def test_channels_list_2channel():
    #dictionary of token and uid when user logs in and the element removes when he logs out

    helper_functions.clear_data()
    user1_email = '1234@gmail.com'
    user1_password = 'asdfghjk'
    user1_firstname = 'USER'
    user1_lastname = '1'
    
    diction = auth.auth_register(user1_email,user1_password,user1_firstname,user1_lastname)
    token = diction.get('token')
    ## uid = diction.get('u_id')
    id_dict = channels.channels_create(token,user1_firstname,True)

    channel_id1 = id_dict.get('channel_id')

    id_dict2 = channels.channels_create(token,'asdfg',True)

    channel_id2 = id_dict2.get('channel_id')
    
    chan = channels.channels_list(token)
    chan = chan.get('channels')
    assert chan == [{'channel_id':channel_id1,'name':user1_firstname},
    {'channel_id':channel_id2,'name':'asdfg'}]

#one channel is made by another user
def test_channels_list_3channel():
    #dictionary of token and uid when user logs in and the element removes when he logs out

    helper_functions.clear_data()
    user1_email = '1234@gmail.com'
    user1_password = 'asdfghjk'
    user1_firstname = 'USER'
    user1_lastname = '1'

    ## user2_email = '12@gmail.com'
    ## user2_password = 'asghjk'
    ## user2_firstname = 'ASDFG'
    ## user2_lastname = '123'
    
    diction1 = auth.auth_register(user1_email,user1_password,user1_firstname,user1_lastname)
    ## diction2 = auth.auth_register(user2_email,user2_password,user2_firstname,user2_lastname)

    token1 = diction1.get('token')
    ## uid = diction1.get('u_id')
    ## token2 = diction2.get('token')

    id_dict = channels.channels_create(token1,user1_firstname,True)

    channel_id1 = id_dict.get('channel_id')

    id_dict2 = channels.channels_create(token1,'asdfg',True)

    channel_id2 = id_dict2.get('channel_id')

    #another user created this channel
    ## id_dict3 = channels.channels_create(token2,'asdfgh',True)
    
    chan = channels.channels_list(token1)
    chan = chan.get('channels')
    assert chan == [{'channel_id':channel_id1,'name':user1_firstname},
    {'channel_id':channel_id2,'name':'asdfg'}]

def test_channels_listall():
    helper_functions.clear_data()
    user1_email = '1234@gmail.com'
    user1_password = 'asdfghjk'
    user1_firstname = 'USER'
    user1_lastname = '1'

    diction = auth.auth_register(user1_email,user1_password,user1_firstname,user1_lastname)
    token = diction.get('token')
    ## id_dict = channels.channels_create(token,user1_firstname,True)

    ## channel_id = id_dict.get('channel_id')
    channels.channels_create(token,user1_firstname,True)
    

    chan = channels.channels_listall(token)
    chan = chan.get('channels')
    assert chan!=None
    assert True

def test_channels_listall_1channel():
    #dictionary of token and uid when user logs in and the element removes when he logs out

    helper_functions.clear_data()
    user1_email = '1234@gmail.com'
    user1_password = 'asdfghjk'
    user1_firstname = 'USER'
    user1_lastname = '1'
    
    diction = auth.auth_register(user1_email,user1_password,user1_firstname,user1_lastname)
    token = diction.get('token')
    ## uid = diction.get('u_id')
    id_dict = channels.channels_create(token,user1_firstname,True)

    channel_id = id_dict.get('channel_id')

    chan = channels.channels_listall(token)
    chan = chan.get('channels')
    assert chan == [{'channel_id':channel_id,'name':user1_firstname}]

def test_channels_listall_2channel():
    #dictionary of token and uid when user logs in and the element removes when he logs out

    helper_functions.clear_data()
    user1_email = '1234@gmail.com'
    user1_password = 'asdfghjk'
    user1_firstname = 'USER'
    user1_lastname = '1'
    
    diction = auth.auth_register(user1_email,user1_password,user1_firstname,user1_lastname)
    token = diction.get('token')
    ## uid = diction.get('u_id')
    id_dict = channels.channels_create(token,user1_firstname,True)

    channel_id1 = id_dict.get('channel_id')

    id_dict2 = channels.channels_create(token,'asdfg',True)

    channel_id2 = id_dict2.get('channel_id')
    
    chan = channels.channels_listall(token)
    chan = chan.get('channels')
    assert chan == [{'channel_id':channel_id1,'name':user1_firstname},
    {'channel_id':channel_id2,'name':'asdfg'}]


#to check channel list only returns channel in which user is there
def test_channels_list2():
   
   # uid = tok_uid.get(12334) 

    helper_functions.clear_data()
    user1_email = '1234@gmail.com'
    user1_password = 'asdfghjk'
    user1_firstname = 'USER'
    user1_lastname = '1'

    diction = auth.auth_register(user1_email,user1_password,user1_firstname,user1_lastname)
    token = diction.get('token')
    uid = diction.get('u_id')
    ## id_dict = channels.channels_create(token,user1_firstname,True)

    chans = channels.channels_list(token)
    chans = chans.get('channels')

    for i in chans:
        id = i.get('channel_id')
        diction = channel.channel_details(token,id) #also be implemented with handling access error
        diction = diction.get('all_members')
        for j in diction:
            assert j.get('u_id') == uid

def test_chennels_create():
    from channels import channels_create

    helper_functions.clear_data()
    user1_email = '1234@gmail.com'
    user1_password = 'asdfghjk'
    user1_firstname = 'USER'
    user1_lastname = '1'

    diction = auth.auth_register(user1_email,user1_password,user1_firstname,user1_lastname)
    token = diction.get('token')

    name = 'Group5'
    is_public = True
    channel_ID = channels_create(token, name, is_public)
    assert(channel_ID != None)
    assert(len(name) <= 20)
#check whether data has put into data.py



    
    


            

           

   




    

