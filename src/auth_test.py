import auth
import pytest
from helper_functions import clear_data
from error import InputError
from data import data

#test login

def test_login_valid_1():
    clear_data()
    user1_email = 'user1@google.com'
    user1_password = '1234567'
    user1_firstname = 'User'
    user1_lastname = 'One'

    # User1 register
    user1_reg = auth.auth_register(user1_email, user1_password, user1_firstname, user1_lastname)
    # User1 login
    user1_log = auth.auth_login(user1_email, user1_password)
    assert user1_log['token'] == user1_reg['token']
    assert user1_log['u_id'] == user1_reg['u_id']
    


def test_login_valid_2():
    clear_data()
    user2_email = 'asdjkj123@gmail.com'
    user2_password = 'cytsah12378'
    user2_firstname = 'User'
    user2_lastname = 'Two'

    # User1 register
    user2_reg = auth.auth_register(user2_email, user2_password, user2_firstname, user2_lastname)
    # User1 login
    user2_log = auth.auth_login(user2_email, user2_password)
    assert user2_log['token'] == user2_reg['token']
    assert user2_log['u_id'] == user2_reg['u_id']

def test_login_valid_3():
    clear_data()
    user3_email = 'ahjhjhjhjh@gmail.com'
    user3_password = '###444$$$skj.'
    user3_firstname = 'User'
    user3_lastname = 'Three'

    # User1 register
    user3_reg = auth.auth_register(user3_email, user3_password, user3_firstname, user3_lastname)
    # User1 login
    user3_log = auth.auth_login(user3_email, user3_password)
    assert user3_log['token'] == user3_reg['token']
    assert user3_log['u_id'] == user3_reg['u_id']
  
def test_login_invalid_email():
    clear_data()
    user_email = 'cyttt.com'
    user_password = '12345678'
    with pytest.raises(InputError):
        auth.auth_login(user_email, user_password)     
def test_login_unregistered():
    clear_data()
    user_email = 'z5237321@ad.com'
    user_password = '12345678'
    with pytest.raises(InputError):
        auth.auth_login(user_email, user_password)
def test_login_not_match_password():
    clear_data()
    user_email = 'z5237321@ad.com'
    user_password = '87654321'
    with pytest.raises(InputError):
        auth.auth_login(user_email, user_password)
def test_login_empty_email():
    clear_data()
    user_email = ''
    user_password = '87654321'
    with pytest.raises(InputError):
        auth.auth_login(user_email, user_password) 
def test_login_empty_password():
    clear_data()
    user_email = 'z5237321@ad.com'
    user_password = ''
    with pytest.raises(InputError):
        auth.auth_login(user_email, user_password)

#test logout

def test_logout_valid_1():
    clear_data()
    user1_email = 'user1@google.com'
    user1_password = '1234567'
    user1_firstname = 'User'
    user1_lastname = 'One'

    # User1 register
    auth.auth_register(user1_email, user1_password, user1_firstname, user1_lastname)

    # User1 login
    user1 = auth.auth_login(user1_email, user1_password)
    user1_token = user1['token']

    # User1 logout
    user1_logout = auth.auth_logout(user1_token)

    assert user1_logout['is_success']

    


def test_logout_valid_2():
    clear_data()
    user2_email = 'user2@google.com'
    user2_password = '12345678'
    user2_firstname = 'User'
    user2_lastname = 'Two'
     # User1 register
    auth.auth_register(user2_email, user2_password, user2_firstname, user2_lastname)

    # User1 login
    user2 = auth.auth_login(user2_email, user2_password)
    user2_token = user2['token']

    # User1 logout
    user2_logout = auth.auth_logout(user2_token)

    assert user2_logout['is_success']
def test_logout_valid_3():
    clear_data()
    user3_email = 'user3@google.com'
    user3_password = '123456789'
    user3_firstname = 'User'
    user3_lastname = 'Three'
    # User1 register
    auth.auth_register(user3_email, user3_password, user3_firstname, user3_lastname)

    # User1 login
    user3 = auth.auth_login(user3_email, user3_password)
    user3_token = user3['token']

    # User1 logout
    user3_logout = auth.auth_logout(user3_token)

    assert user3_logout['is_success']

def test_logout_invalid_1():
    clear_data()
    invalid_token = 'invalidtoken'
    user1_logout = auth.auth_logout(invalid_token)
    assert not user1_logout['is_success']

def test_logout_invalid_2():
    clear_data()
    invalid_token = '?'
    user2_logout = auth.auth_logout(invalid_token)
    assert not user2_logout['is_success']

def test_logout_invalid_3():
    clear_data()
    invalid_token = '0'
    user3_logout = auth.auth_logout(invalid_token)
    assert not user3_logout['is_success']

# test register

def test_register_valid1():
    clear_data()
    user1_email = 'user1@google.com'
    user1_password = '1234567'
    user1_firstname = 'User'
    user1_lastname = 'One'

    user1 = auth.auth_register(user1_email, user1_password, user1_firstname, user1_lastname)
    user1_u_id = user1['u_id']
    user1_token = user1['token']

    assert user1_u_id == 1
    assert user1_token == user1_email

def test_register_valid2():
    clear_data()
    user2_email = 'user2@google.com'
    user2_password = '12345678'
    user2_firstname = 'User'
    user2_lastname = 'Two'
    user2 = auth.auth_register(user2_email, user2_password, user2_firstname, user2_lastname)
    user2_u_id = user2['u_id']
    user2_token = user2['token']

    assert user2_u_id == 1
    assert user2_token == user2_email

def test_register_valid3():
    clear_data()
    user3_email = 'user3@google.com'
    user3_password = '123456789'
    user3_firstname = 'User'
    user3_lastname = 'Three'
    # User3 register
    user3 = auth.auth_register(user3_email, user3_password, user3_firstname, user3_lastname)
    user3_u_id = user3['u_id']
    user3_token = user3['token']

    assert user3_u_id == 1
    assert user3_token == user3_email

def test_register_invalid_email():
    clear_data()
    user_email = 'user.com'
    user_password = '12344566'
    user_firstname = 'User'
    user_lastname = 'user'
    with pytest.raises(InputError):
        auth.auth_register(user_email, user_password, user_firstname, user_lastname)     

def test_register_invalid_password():
    clear_data()
    user_email = 'user@gamil.com'
    user_password = '1'
    user_firstname = 'User'
    user_lastname = 'user'
    with pytest.raises(InputError):
        auth.auth_register(user_email, user_password, user_firstname, user_lastname)   

def test_register_invalid_firstname():
    clear_data()
    user_email = 'user@gamil.com'
    user_password = '12345667'
    user_firstname = ''
    user_lastname = 'user'
    with pytest.raises(InputError):
        auth.auth_register(user_email, user_password, user_firstname, user_lastname)   

def test_register_invalid_lastname():
    clear_data()
    user_email = 'user@gamil.com'
    user_password = '1qqqqqqqqq'
    user_firstname = 'User'
    user_lastname = ''
    with pytest.raises(InputError):
        auth.auth_register(user_email, user_password, user_firstname, user_lastname)   

def test_register_used_email():
    clear_data()
    user_email = 'user@gamil.com'
    user_password = '1qqqqqqq'
    user_firstname = 'User'
    user_lastname = 'use'
    auth.auth_register(user_email, user_password, user_firstname, user_lastname)   
    user1_email = 'user@gamil.com'
    user1_password = 'qqqqqqqq'
    user1_firstname = 'User'
    user1_lastname = 'use'

    with pytest.raises(InputError):
        auth.auth_register(user1_email, user1_password, user1_firstname, user1_lastname)   

def test_register_invalid_lastname_50():
    clear_data()
    user_email = 'user@gamil.com'
    user_password = '1qqqqqqqqq'
    user_firstname = 'User'
    user_lastname = '123456778812345677881234567788123456778812345677881234567788'
    with pytest.raises(InputError):
        auth.auth_register(user_email, user_password, user_firstname, user_lastname)

def test_register_invalid_first_50():
    clear_data()
    user_email = 'user@gamil.com'
    user_password = '1qqqqqqqqq'
    user_firstname = '123456778812345677881234567788123456778812345677881234567788'
    user_lastname = 'User'
    with pytest.raises(InputError):
        auth.auth_register(user_email, user_password, user_firstname, user_lastname)
