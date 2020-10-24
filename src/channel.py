from error import InputError, AccessError
from data import data

def channel_invite(token, channel_id, u_id):
    
    #get authorised user id
    u_id_caller = data['tok_uid'][token]
    
    #InputError: channel_id does not refer to a valid channel.
    if not is_valid_channel(channel_id):
        raise InputError()
    
    #InputError: u_id does not refer to a valid user
    elif not is_valid_uid(u_id):
        raise InputError()
        
    #AccessError: the authorised user is not already a member of the channel
    elif not is_channel_member(u_id_caller, channel_id):
        raise AccessError()
 
    user_info = get_user_info(u_id)
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            channel['all_members'].append(user_info)
    return {
    }

def channel_details(token, channel_id):
    
    #InputError: channel_id does not refer to a valid channel.
    if not is_valid_channel(channel_id):
        raise InputError()
    
    #get authorised user id
    u_id_caller = data['tok_uid'][token]
    
    #AccessError: the authorised user is not already a member of the channel
    if not is_channel_member(u_id_caller, channel_id):
        raise AccessError()
    
     
    channel_info = get_channel_info(channel_id)
    return channel_info
    

def channel_messages(token, channel_id, start):

    # InputError: invalid channel id
    if not is_valid_channel(channel_id):
        raise InputError('Invalid channel ID')

    # get user id
    u_id = data['tok_uid'][token]
    
    # InputError: start is greater than total number of messages
    for i in data['channels']:
        if i['channel_id'] == channel_id:
            if len(i['messages']) - 1 < start:
                raise InputError('no message at start index')
    
    # AccessError: authorised user not a member of channel
    if not is_channel_member(u_id, channel_id):
        raise AccessError('Authorised user is not a member of channel')


    messages = []
    for channel in data['channels']:
        if channel['channel_id'] != channel_id:
            continue 
        
        # if the end of messages is not reached at index start + 50
        # display all 50 messages and set end to start + 50
        if (len(channel['messages']) - start) > 50:
            for message_index in range(start, start + 50):
                messages.append(
                    {
                        'message_id' : channel['messages'][message_index]['message_id'],
                        'u_id' : u_id,
                        'message': channel['messages'][message_index]['message'],
                        'time_created' : channel['messages'][message_index]['time_created']
                    }
                )


            return {'messages' : messages, 'start' : start, 'end' : start + 50}
        
        else:
            # if the least recent message is reached
            # display all messages before start and set end to -1
            for message_index in range(start, len(channel['messages'])):
                messages.append(
                    {
                        'message_id' : channel['messages'][message_index]['message_id'],
                        'u_id' : u_id,
                        'message': channel['messages'][message_index]['message'],
                        'time_created' : channel['messages'][message_index]['time_created']
                    }
                )


            return {'messages' : messages, 'start' : start, 'end' : -1}

        

##########################
#    helper functions    #
##########################

# True if channel ID is valid, False otherwise
def is_valid_channel(channel_id):
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            return True
    return False

# True if user ID is valid, False otherwise
def is_valid_uid(u_id):
    for uid in data['users']:
        if uid['u_id'] == u_id:
            return True
    return False

# True if user is a member of the channel, False otherwise
def is_channel_member(u_id, channel_id):
    # find channel
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            # search for user in all_members
            for member in channel['all_members']:
                if member['u_id'] == u_id:
                    return True
            return False

# True if user is an owner of the channel, False otherwise
def is_channel_owner(u_id, channel_id):
    # find channel
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            # search for user in owner_members
            for member in channel['owner_members']:
                if member['u_id'] == u_id:
                    return True
            return False 

# True if channel is public, False otherwise
def is_public_channel(channel_id):
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            if channel['is_public'] == True:
                return True
            return False

# True if user is global owner, False otherwise
def is_global_owner(u_id):
    for user in data['users']:
        if user['u_id'] == u_id:
            if user['permission_id'] == 1:
                return True
            return False

# Returns {u_id, name_first, name_last) for a given user
def get_user_info(u_id):
    for user in data['users']:
        if user['u_id'] == u_id:
            return {'u_id' : u_id, 'name_first' : user['name_first'], 'name_last' : user['name_last']}

#Returns {name, owner_members, all_members) for a given channel
def get_channel_info(channel_id):
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            return {'name' : channel['name'], 'owner_members' : channel['owner_members'], 'all_members' : channel['all_members']}

##########################
#    implementations     #
##########################
def channel_leave(token, channel_id):

    # get user's u_id
    u_id = data['tok_uid'][token]

    # InputError: invalid channel ID
    if not is_valid_channel(channel_id):
        raise InputError('Channel ID does not refer to a valid channel')
    
    # AccessError: authorised user is not a member of the channel
    elif not is_channel_member(u_id, channel_id):
        raise AccessError('Authorised user is not a member of the channel')
    
    # no errors: user is removed from all_members and owner_members (if applicable)
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            # find user dictionary
            for member in channel['all_members']:
                if member['u_id'] == u_id:
                    # remove user dictionary from all_members
                    channel['all_members'].remove(member)
            # if user is also owner, remove from owner_members
            if is_channel_owner(u_id, channel_id):
                for owner in channel['owner_members']:
                    if owner['u_id'] == u_id:
                        channel['owner_members'].remove(owner)

    return { }

def channel_join(token, channel_id):
    
    # get user's u_id
    u_id = data['tok_uid'][token]

    # InputError: invalid channel ID
    if not is_valid_channel(channel_id):
        raise InputError('Channel ID does not refer to a valid channel')
    
    # AccessError: channel ID refers to a channel that is private AND user is not global owner
    elif not is_public_channel(channel_id) and not is_global_owner(u_id):
        raise AccessError('Channel is private and user is not a global owner')
    
    # no errors: user is already a member of channel, nothing happens
    if is_channel_member(u_id, channel_id):
        return { }
    
    # no errors: user is global owner (can join public and private channels)
    elif is_global_owner(u_id):
        user_info = get_user_info(u_id)
        # find channel
        for channel in data['channels']:
            if channel['channel_id'] == channel_id:
                # add user to both members and owners lists
                channel['all_members'].append(user_info)
                channel['owner_members'].append(user_info)
   

    # no errors: user is regular user and channel is public
    else: 
        user_info = get_user_info(u_id)
        for channel in data['channels']:
            if channel['channel_id'] == channel_id:
                # add user to members list
                channel['all_members'].append(user_info)
    
    return { }

def channel_addowner(token, channel_id, u_id):
    
    # InputError: invalid channel ID
    if not is_valid_channel(channel_id):
        raise InputError('Channel ID does not refer to a valid channel')
    
    # InputError: user with u_id is already an owner of channel
    if is_channel_owner(u_id, channel_id):
        raise InputError('User is already a channel owner')
    
    # get u_id of authorised user
    u_id_caller = data['tok_uid'][token]
    
    # AccessError: user is not an owner of this channel AND not a global owner
    if not is_channel_owner(u_id_caller, channel_id) and not is_global_owner(u_id_caller):
        raise AccessError('User is not an owner of channel and not a global owner')
    
    # no errors: user is not an owner of this channel BUT is a global owner
    # or: authorised user is an owner of channel
    else:
        # find channel
        for channel in data['channels']:
            if channel['channel_id'] == channel_id:
                # add u with u_id to the list of owners and members (if applicable)
                user_info = get_user_info(u_id)
                # owners list
                channel['owner_members'].append(user_info)
                # members list
                if not is_channel_member(u_id, channel_id):
                    channel['all_members'].append(user_info)


    return { }

def channel_removeowner(token, channel_id, u_id):
    
    # InputError: invalid channel ID
    if not is_valid_channel(channel_id):
        raise InputError('Channel ID does not refer to a valid channel')
    
    # InputError: user with u_id is not an owner of the channel
    elif not is_channel_owner(u_id, channel_id):
        raise InputError('User is not an owner of the channel')
        
    # get u_id of authorised user
    u_id_caller = data['tok_uid'][token]
    
    # AccessError: user is not an owner of this channel AND not a global owner
    if not is_channel_owner(u_id_caller, channel_id) and not is_global_owner(u_id_caller):
        raise AccessError('Authorised user is not an owner of channel and not a global owner')    
    
    # no errors: authorised user is not an owner of the channel BUT is a global owner
    # or: authorised user is an owner of the channel
    else:
        # find channel
        for channel in data['channels']:
            if channel['channel_id'] == channel_id:
                # remove user from owners_members list
                for owner in channel['owner_members']:
                    if owner['u_id'] == u_id:
                        channel['owner_members'].remove(owner)
    
    return { }

