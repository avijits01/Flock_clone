
import pytest
import user
import auth
from error import InputError
from data import data
from helper_functions import clear_data

##################################
#       user_profile tests       #
##################################

def test_user_profile_invalid_input():
    clear_data()
    
    #setup one user
    user_a = auth.auth_register('abc123@gmail.com', 'password123', 'Firstname', 'Lastname')
    
    #input with wrong uid will raise inputerror
    with pytest.raises(InputError):
        assert user.user_profile(user_a['token'], 000000)

def test_user_profile_valid1():
    clear_data()
    
    #setup one user
    user_b = auth.auth_register('abc123@gmail.com', 'password123', 'Firstname', 'Lastname')
    user.user_profile_sethandle(user_b['token'], 'handle123')
    
    assert user.user_profile(user_b['token'], user_b['u_id']) == {'user': {'u_id' : user_b['u_id'], 'email' : 'abc123@gmail.com', 'name_first' : 'Firstname', 'name_last' : 'Lastname', 'handle_str': 'handle123'}}

def test_user_profile_valid2():
    clear_data()
    
    #setup one user
    user_c = auth.auth_register('abc123@gmail.com', 'password123', 'Firstname', 'Lastname')
    user.user_profile_sethandle(user_c['token'], 'handle123')
    
    #resetup details
    user.user_profile_setname(user_c['token'], 'Burt', 'Fan')
    user.user_profile_setemail(user_c['token'], 'burt123@gmail.com')
    user.user_profile_sethandle(user_c['token'], 'handle456')
    
    assert user.user_profile(user_c['token'], user_c['u_id']) == {'user': {'u_id' : user_c['u_id'], 'email' : 'burt123@gmail.com', 'name_first' : 'Burt', 'name_last' : 'Fan', 'handle_str': 'handle456'}}
    
##################################
#   user_profile_setname tests   #
##################################

def test_user_name_valid1():
    clear_data()
    user1_email = 'user1@google.com'
    user1_password = '1234567'
    user1_firstname = 'User'
    user1_lastname = 'One'

    user1 = auth.auth_register(user1_email, user1_password, user1_firstname, user1_lastname)
    user1_u_id = user1['u_id']
    user1_token = user1['token']
    
    user_first = 'Yuetong'
    user_last = 'chen'
    user_token = user1_token
    user_uid = user1_u_id
    user.user_profile_setname(user_token, user_first, user_last)
    user_data = user.user_profile(user_token, user_uid)
    user_info = user_data['user']
    assert user_info['name_first'] == 'Yuetong'
    assert user_info['name_last'] ==  'chen'

def test_user_name_valid2():
    clear_data()
    user2_email = 'user2@google.com'
    user2_password = '12345678'
    user2_firstname = 'User'
    user2_lastname = 'Two'
    user2 = auth.auth_register(user2_email, user2_password, user2_firstname, user2_lastname)
    user2_u_id = user2['u_id']
    user2_token = user2['token']

    user_first = '1212chen'
    user_last = 'chen__'
    user_token = user2_token
    user_uid = user2_u_id
    user.user_profile_setname(user_token, user_first, user_last)
    user_data = user.user_profile(user_token, user_uid)
    user_info = user_data['user']
    assert user_info['name_first'] == '1212chen'
    assert user_info['name_last'] == 'chen__'

def test_user_name_valid3():
    clear_data()
    user3_email = 'user3@google.com'
    user3_password = '12345678df'
    user3_firstname = 'User'
    user3_lastname = 'Three'
    user3 = auth.auth_register(user3_email, user3_password, user3_firstname, user3_lastname)
    user3_u_id = user3['u_id']
    user3_token = user3['token']
    user_first = '1212chen@@11'
    user_last = 'chen__98sd'
    user_token = user3_token
    user_uid = user3_u_id
    user.user_profile_setname(user_token, user_first, user_last)
    user_data = user.user_profile(user_token, user_uid)
    user_info = user_data['user']
    assert user_info['name_first'] == '1212chen@@11'
    assert user_info['name_last'] == 'chen__98sd'
def test_user_name_firstInvalid():
    clear_data()
    user1_token = 'tokenw'
    user1_first = ''
    user1_last = 'ccceu'
    with pytest.raises(InputError):
        user.user_profile_setname(user1_token, user1_first, user1_last)

def test_user_name_lastInvalid():
    clear_data()
    user2_token = 'tokenw'
    user2_first = 'dfdfiui'
    user2_last = ''
    with pytest.raises(InputError):
        user.user_profile_setname(user2_token, user2_first, user2_last)

def test_user_name_firstInvalid_50():
    clear_data()
    user3_token = 'tokenw'
    user3_first = '123456778812345677881234567788123456778812345677881234567788'
    user3_last = 'ccceu'
    with pytest.raises(InputError):
        user.user_profile_setname(user3_token, user3_first, user3_last)

def test_user_name_lastInvalid_50():
    clear_data()
    user4_token = 'tokenw'
    user4_last = '123456778812345677881234567788123456778812345677881234567788'
    user4_first = 'ccceu'
    with pytest.raises(InputError):
        user.user_profile_setname(user4_token, user4_first, user4_last)

##################################
#   user_profile_setemail tests  #
##################################

def test_user_email_valid1():
    clear_data()
    user5_email = 'user2@google.com'
    user5_password = '12345678'
    user5_firstname = 'User'
    user5_lastname = 'Five'
    user5 = auth.auth_register(user5_email, user5_password, user5_firstname, user5_lastname)
    user5_u_id = user5['u_id']
    user5_token = user5['token']
    user_token = user5_token
    user_email = 'user1@qq.com'
    user_uid = user5_u_id
    user.user_profile_setemail(user_token, user_email)
    user_data = user.user_profile(user_token, user_uid)
    user_info = user_data['user']
    assert user_info['email'] == 'user1@qq.com'

def test_user_invalid_email():
    user1_token = 'ttt1k'
    user1_email = 'sddsds'
    with pytest.raises(InputError):
        user.user_profile_setemail(user1_token, user1_email)

def test_user_used_email():
    clear_data()
    user_email = 'user@gamil.com'
    user_password = '1qqqqqqq'
    user_firstname = 'User'
    user_lastname = 'use'
    new_user = auth.auth_register(user_email, user_password, user_firstname, user_lastname) 
    user_token = new_user['token']
    user_new_email = 'user@gamil.com'
    
    with pytest.raises(InputError):
        user.user_profile_setemail(user_token, user_new_email)
        
##################################
#  user_profile_sethandle tests  #
##################################

def test_user_profile_sethandle_invalid_input_too_short():
    clear_data()
    
    #setup one user
    user_a = auth.auth_register('abc123@gmail.com', 'password123', 'Firstname', 'Lastname')
    #input with a too short handle
    with pytest.raises(InputError):
        user.user_profile_sethandle(user_a['token'], '12')

def test_user_profile_sethandle_invalid_input_too_long():
    clear_data()
    
    #setup one user
    user_b = auth.auth_register('abc123@gmail.com', 'password123', 'Firstname', 'Lastname')
    #input with a too long handle
    with pytest.raises(InputError):
        user.user_profile_sethandle(user_b['token'], '123456789012345678901')

def test_user_profile_sethandle_invalid_input_repeat():
    clear_data()
    
    #setup one user
    user_c = auth.auth_register('abc123@gmail.com', 'password123', 'Firstname', 'Lastname')
    user.user_profile_sethandle(user_c['token'], 'handle123')
    #input with a used handle
    with pytest.raises(InputError):
        user.user_profile_sethandle(user_c['token'], 'handle123')

def test_user_profile_sethandle_valid1():
    clear_data()
    
    #setup one user
    user_d = auth.auth_register('abc123@gmail.com', 'password123', 'Firstname', 'Lastname')
    user.user_profile_sethandle(user_d['token'], 'handle123')
    #find handle in dict and check the correctness
    user_data = user.user_profile(user_d['token'], user_d['u_id'])
    user_info = user_data['user']
    assert user_info['handle_str'] == 'handle123'

def test_user_profile_sethandle_valid2():
    clear_data()
    
    #setup one user
    user_e = auth.auth_register('abc123@gmail.com', 'password123', 'Firstname', 'Lastname')
    user.user_profile_sethandle(user_e['token'], 'handle123')
    #resetup handle
    user.user_profile_sethandle(user_e['token'], 'handle456')
    #find handle in dict and check the correctness
    user_data = user.user_profile(user_e['token'], user_e['u_id'])
    user_info = user_data['user']
    assert user_info['handle_str'] == 'handle456'
    
