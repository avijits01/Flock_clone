from data import data
from error import InputError
from helper_functions import check_email, is_valid_uid, get_user_info
def user_profile(token, u_id):
    
    #InputError: User with u_id is not a valid user
    if not is_valid_uid(u_id):
        raise InputError()

    # Get user information from help functions 
    user_info = get_user_info(u_id)

    return {
        'user': user_info,
    }


def user_profile_setname(token, name_first, name_last):
    if len(name_first) < 1 or len(name_first) > 50:
        raise InputError()
    if len(name_last) < 1 or len(name_last) > 50:
        raise InputError()
    user_data = data['users']

    # Find target user
    active_users = data['tok_uid']
    target_u_id = active_users[token]

    target_user = {}
    for user in user_data:
        if user['u_id'] == target_u_id:
            target_user = user

    target_user['name_first'] = name_first
    target_user['name_last'] = name_last
    return {
    }

def user_profile_setemail(token, email):
    if not check_email(email):
        raise InputError()

    users_data = data['users']
    for user in users_data:
        if email == user['email']:
            raise InputError()
    # Find target user
    active_users = data['tok_uid']
    target_u_id = active_users[token]

    target_user = {}
    for user in users_data:
        if user['u_id'] == target_u_id:
            target_user = user

    target_user['email'] = email
    
    return {
    }

def user_profile_sethandle(token, handle_str):
    
    #InputError: handle_str is not between 3 and 20 characters
    if len(handle_str) < 3 or len(handle_str) > 20:
        raise InputError()
    
    #InputError: handle is already used by another user
    for user in data['users']: 
        if handle_str == user['handle']:
            raise InputError()
    
    #get authorised user id
    u_id_caller = data['tok_uid'][token]

    #Update the authorised user's handle
    target_user = {}
    for user in data['users']:
        if user['u_id'] == u_id_caller:
            target_user = user

    target_user['handle'] = handle_str
    
    return {
    }
