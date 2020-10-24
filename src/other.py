from data import data
from error import InputError, AccessError
from channel import is_valid_uid

# set data back to its original state
def clear():
    data['users'] = []
    data['channels'] = []
    data['tok_uid'] = {}


def users_all(token):
    
    users_list = []
    for user in data['users']:
        # get required user info
        user_data = {
            'u_id': user['u_id'],
            'email': user['email'],
            'name_first': user['name_first'],
            'name_last': user['name_last'],
            'handle_str': user['handle']
        }
        
        # add to list
        users_list.append(user_data)
    
    return {'users': users_list}


def admin_userpermission_change(token, u_id, permission_id):

    # InputError: user id is invalid
    if not is_valid_uid(u_id):
        raise InputError(description='User with u_id does not exist')

    # InputError: permission_id is invalid (not 1 or 2)
    if permission_id != 1 and permission_id != 2:
        raise InputError(description='permission_id must be 1 or 2')
   
    # get authorised user's id
    u_id_caller = data['tok_uid'][token]
     
    # AccessError: authorised user is not a global owner (permission_id is 2)   
    for user in data['users']:
        if user['u_id'] == u_id_caller:
            print(user['permission_id'])
            if user['permission_id'] == 2:
                raise AccessError(description='Regular users cannot alter global permissions')
    
    # else, update user's permission_id
    for user in data['users']:
        if user['u_id'] == u_id:
            user['permission_id'] = permission_id
    

