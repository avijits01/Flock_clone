from data import data
from error import InputError
from helper_functions import check_email

import hashlib

def auth_login(email, password):

    tok_uid = data['tok_uid']
    if not check_email(email):
        raise InputError 
    users_data = data['users']

    email_registered = False
    for user in users_data:
        if email == user['email']:
            email_registered = True

    if not email_registered:
        raise InputError()
    
    # create a hash for provided password 
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    
    for user in users_data:
        if email == user['email']:
            if password_hash != user['password']:
                raise InputError()
                
                
    for user in users_data:
        if email == user['email']:
            if password_hash == user['password']:
                user_id = user['u_id']     
                user_token = user['email']  
                tok_uid[user_token] = user_id
    return {
        'u_id': user_id,
        'token': user_token,
    }



def auth_logout(token):
    users_data = data['users']
    ## tok_uid = data['tok_uid']
    for user in users_data:
        if token == user['email']:
            del data['tok_uid'][token]
            return {
                'is_success': True,
            }
    return {
        'is_success': False,
    }       
    

def auth_register(email, password, name_first, name_last):

    if not check_email(email):
        raise InputError()

    users_data = data['users']
    tok_uid = data['tok_uid']
    for user in users_data:
        if email == user['email']:
            raise InputError()

    if len(password) < 6 :
        raise InputError()

    if len(name_first) < 1 or len(name_first) > 50:
        raise InputError()
    if len(name_last) < 1 or len(name_last) > 50:
        raise InputError()

    u_id = len(users_data) + 1
    handle = (name_first + name_last).lower()[0:20]
    # users have regular global permissions by default
    permission_id = 2
    # first user to register becomes a global owner
    if len(users_data) == 0:
        permission_id = 1
    user = {
            'u_id' : u_id,
            'name_first' : name_first,
            'name_last' : name_last,
            'handle' : handle,
            'email' : email,
            # store hash of password 
            'password' : hashlib.sha256(password.encode()).hexdigest(),
            'permission_id' : permission_id
        }
    #for earlier iteration token is user's email
    tok_uid[user['email']] = u_id
    data['users'].append(user)
    return {
        'u_id': user['u_id'],
        'token': user['email'],
    }

