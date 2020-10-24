import re
from data import data
  
regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
def check_email(email):  

    if(re.search(regex,email)):  
        return True 
          
    else:  
        return False
def clear_data():
    data['users'] = []
    data['channels'] = []
    data['tok_uid'] = {}
    
# True if user ID is valid, False otherwise
def is_valid_uid(u_id):
    for uid in data['users']:
        if uid['u_id'] == u_id:
            return True
    return False

def get_user_info(u_id):
    for user in data['users']:
        if user['u_id'] == u_id:
            return {'u_id' : u_id, 'email' : user['email'], 'name_first' : user['name_first'], 'name_last' : user['name_last'], 'handle_str': user['handle']}
