
from error import InputError, AccessError
from data import data
import random
from channel import channel_details, get_user_info
from data import data


def channels_list(token):
    tok_uid = data.get('tok_uid')
    channels = data.get('channels')
    if token is None:
        print('Not logged in')
    else:
        channels_2 = []
        uid = tok_uid.get(token) 

        for i in channels:
            id = i.get('channel_id')
            #will give access error if other user tried to access
            try:
                diction = channel_details(token,id)
            except:
                continue
            members = diction.get('all_members')
            for j in members:
                check_id = j.get('u_id')

                if check_id is uid:
                    print(f'Channel {i}')

                    ch_name = i.get('name')
                    #name = diction.get('name')
                    owners = diction.get('owner_members')
                    members = diction.get('all_members')

                    channels_2.append({'channel_id':id,'name':ch_name})

                    print(f'Name of the channel {ch_name}')
                    print(f'Owners of the channel {owners}')
                    print(f'Members of the channel {members}')
        
        #for tests
        return {'channels':channels_2}
    

def channels_listall(token):
    ## tok_uid = data.get('tok_uid')
    channels = data.get('channels')
    if token is None:
        print('Not logged in')
    else:
        ## uid = tok_uid.get(token) 
        channels_2 = []
        
        for i in channels:
            name = i.get('name')
            id = i.get('channel_id')

            print (f'Name of channel {name} ')
            print (f'Id of channel {id}')

            diction = channel_details(token,id)

            user_name = diction.get('name')
            owners = diction.get('owner_members')
            members = diction.get('all_members')

            channels_2.append({'channel_id':id,'name':name})
            print(f'Name of the channel {user_name}')
            print(f'Owners of the channel {owners}')
            print(f'Members of the channel {members}')


    return {'channels':channels_2}

def channels_create(token, name, is_public):
#check len(name) is greater than 20
    if len(name) > 20:
        raise InputError()

#get unique channel_id
    channel_id = random.randint(1,1000)
    for x in data['channels']:
        if channel_id == x['channel_id']:
            channel_id = random.randint(1000,2000)

    
    # make channel
    new_channel = {
        'channel_id' : channel_id,
        'name' : name,
        'is_public' : is_public,
        'all_members' : [],
        'owner_members' : [],
        'messages' : []
    }
    
    data['channels'].append(new_channel)

    
## add authorised user to list of channel owners
    # get user id from token
    u_id = data['tok_uid'][token]
    
    # get user dictionary
    user = get_user_info(u_id)
    
    new_i = len(data['channels']) - 1
    data['channels'][new_i]['all_members'].append(user)
    data['channels'][new_i]['owner_members'].append(user)
    
    return {
        'channel_id' : channel_id
    }
