import auth
import pytest
import other
from error import InputError, AccessError

##############################
#      users_all tests       #
##############################

def test_users_all_single():
    other.clear()
    
    # register and view a single user
    u0 = auth.auth_register('king@gmail.com', 'youshallpass', 'King', 'Kingson')
    u0_info = {
        'u_id': u0['u_id'], 'email': 'king@gmail.com',
        'name_first': 'King', 'name_last': 'Kingson', 'handle_str': 'kingkingson'
    }
    
    users_list = other.users_all(u0['token'])
    assert users_list == {'users': [u0_info]}

def test_users_all_several():

    other.clear()

    # register several new users
    u1 = auth.auth_register('1_123@gmail.com','111111','Xuewen','Fan')
    u2 = auth.auth_register('2_123@gmail.com','222222','Nancy','North')
    u3 = auth.auth_register('king@gmail.com', 'youshallpass', 'King', 'Kingson')

    u1_info = {
        'u_id': u1['u_id'], 'email': '1_123@gmail.com',
        'name_first': 'Xuewen', 'name_last': 'Fan', 'handle_str': 'xuewenfan'
    }

    u2_info = {
        'u_id': u2['u_id'], 'email': '2_123@gmail.com',
        'name_first': 'Nancy', 'name_last': 'North', 'handle_str': 'nancynorth'
    }

    u3_info = {
        'u_id': u3['u_id'], 'email': 'king@gmail.com',
        'name_first': 'King', 'name_last': 'Kingson', 'handle_str': 'kingkingson'
    }

    # all three users should appear (in order of registration)
    users_list = other.users_all(u1['token'])  

    assert users_list == {'users': [u1_info, u2_info, u3_info]}


###############################################
#      admin_userpermission_change tests      #
###############################################

# InputError: u_id does not refer to a valid user
def test_userpermission_input_err():
    other.clear()
    
    u0 = auth.auth_register('king@gmail.com', 'youshallpass', 'King', 'Kingson')    
    
    # call function with invalid id 0
    with pytest.raises(InputError):
        assert other.admin_userpermission_change(u0['token'], 0, 1)
    
    
# InputError: permission_id does not refer to a value permission
def test_userpermission_input_err2():
    other.clear()
    
    u0 = auth.auth_register('king@gmail.com', 'youshallpass', 'King', 'Kingson')    
    u1 = auth.auth_register('elizabeth@gmail.com', 'youshallpass', 'Elizabeth', 'Alexander')
    
    # call function with invalid permission 3
    with pytest.raises(InputError):
        assert other.admin_userpermission_change(u0['token'], u1['u_id'], 3)


# AccessError: authorised user is not a global owner
def test_userpermission_access_err():
    other.clear()
    
    u0 = auth.auth_register('king@gmail.com', 'youshallpass', 'King', 'Kingson')    
    u1 = auth.auth_register('elizabeth@gmail.com', 'youshallpass', 'Elizabeth', 'Alexander')
    
    # u1 (regular user) tries to change u0's permissions
    with pytest.raises(AccessError):
        assert other.admin_userpermission_change(u1['token'], u0['u_id'], 2)


'''
# no errors: user's global permissions are changed
def test_userpermission_standard():
    other.clear()
    
    u0 = auth.auth_register('king@gmail.com', 'youshallpass', 'King', 'Kingson')    
    u1 = auth.auth_register('elizabeth@gmail.com', 'youshallpass', 'Elizabeth', 'Alexander')
    
    # u0 (global owner) changes u1's permission to owner (id 1)
    admin_userpermission_change(u0['token'], u1['u_id'], 1)
'''





