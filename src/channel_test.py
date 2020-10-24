import pytest
from data import data
from error import InputError, AccessError
import auth
import channel
import channels
import other

import message

def starter():
    # clear all data
    other.clear()
    
    # register four users
    # user 0 is a global owner
    u0 = auth.auth_register('king@gmail.com', 'youshallpass', 'King', 'Kingson')
    u1 = auth.auth_register('elizabeth@gmail.com', 'youshallpass', 'Elizabeth', 'Alexander')
    u2 = auth.auth_register('jane@gmail.com', 'youshallpass', 'Jane', 'Anton')
    u3 = auth.auth_register('charlie@gmail.com', 'youshallpass', 'Charlie', 'Barry')
    # u = {u_id, token}

    # user 3 creates a public channel
    c1 = channels.channels_create(u3['token'], 'public channel', True)
    # user 3 creates a private channel 
    c2 = channels.channels_create(u3['token'], 'private channel', False)
    # c = { channel_id }
    
    return [u0, u1, u2, u3, c1, c2]

##############################
#   channel_invite tests     #
##############################

#(token, channel_id, u_id)
#InputError: channel_id does not refer to a valid channel
def test_invite_input_error_invaild_channel():  
    info = starter()
    u1, u3 = info[1], info[3]
    with pytest.raises(InputError):
        assert channel.channel_invite(u3['token'], 000000, u1['u_id'])
    
#InputError: u_id does not refer to a valid user
def test_invite_input_error_invalid_user():  
    info = starter()
    u3, c1 = info[3], info[4]
    with pytest.raises(InputError):
        assert channel.channel_invite(u3['token'], c1['channel_id'], 000000)

#AccessError: the authorised user is not already a member of the channel
def test_invite_access_error():  
    info = starter()
    u1, u2, c1 = info[1], info[2], info[4]
    with pytest.raises(AccessError):
        assert channel.channel_invite(u1['token'], c1['channel_id'], u2['u_id'])

##############################
#   channel_details tests    #
##############################

#(token, channel_id)
#InputError: Channel ID is not a valid channel
def test_details_input_error_invaild_channel():
    info = starter()
    u1 = info[1]
    with pytest.raises(InputError):
        assert channel.channel_details(u1['token'], 000000)


#AccessError: Authorised user is not a member of channel with channel_id
def test_details_access_error_invaild_member():
    info = starter()
    u1, c1 = info[1], info[4]
    with pytest.raises(AccessError):
        assert channel.channel_details(u1['token'], c1['channel_id'])     

##############################
#     channel_join tests     #
##############################

# InputError: invalid channel ID (assuming no channel ID is 0)
def test_join_input_err():
    info = starter()
    u1 = info[1]
    with pytest.raises(InputError):
        assert channel.channel_join(u1['token'], 0)  

# AccessError: channel is private and authorised user is not a global owner
def test_join_access_err():
    info = starter()
    u1, c2 = info[1], info[5]
    with pytest.raises(AccessError):
        # user 1 (regular user) attempts to join private channel 
        assert channel.channel_join(u1['token'], c2['channel_id'])

# no errors: user is already a member of channel (nothing happens)
def test_join_already_member():
    info = starter()
    u1, u3, c1 = info[1], info[3], info[4]
    
    # store user information
    u3_info = {'u_id' : u3['u_id'], 'name_first': 'Charlie', 'name_last' : 'Barry'}
    u1_info = {'u_id' : u1['u_id'], 'name_first' : 'Elizabeth', 'name_last' : 'Alexander'}
    
    # user 1 joins public channel 
    channel.channel_join(u1['token'], c1['channel_id'])
    # user 1 joins public channel again
    channel.channel_join(u1['token'], c1['channel_id'])
    details = channel.channel_details(u1['token'], c1['channel_id'])
    # user 1 should have only have one instance in all_members
    assert details['all_members'] == [u3_info, u1_info]

# no errors: channel is private and authorised user is a global owner
def test_join_access_global_owner():
    info = starter()
    u0, u3, c2 = info[0], info[3], info[5]
    
    # store user information
    u3_info = {'u_id' : u3['u_id'], 'name_first': 'Charlie', 'name_last' : 'Barry'}
    u0_info = {'u_id' : u0['u_id'], 'name_first' : 'King', 'name_last' : 'Kingson'}
    
    # user 0 (global owner) joins private channel 
    channel.channel_join(u0['token'], c2['channel_id'])
    details = channel.channel_details(u0['token'], c2['channel_id'])
    
    # user 0 should appear in both channel owners and channel members lists
    assert details['all_members'] == [u3_info, u0_info]
    assert details['owner_members'] == [u3_info, u0_info]

# no errors: channel is public and authorised user is a global owner
def test_join_access_global_owner2():
    info = starter()
    u0, u3, c1 = info[0], info[3], info[4]
    
    # store user information
    u3_info = {'u_id' : u3['u_id'], 'name_first': 'Charlie', 'name_last' : 'Barry'}
    u0_info = {'u_id' : u0['u_id'], 'name_first' : 'King', 'name_last' : 'Kingson'}
    
    # user 0 (global owner) joins public channel 
    channel.channel_join(u0['token'], c1['channel_id'])
    details = channel.channel_details(u0['token'], c1['channel_id'])
    
    # user 0 should appear in both channel owners and channel members list
    assert details['all_members'] == [u3_info, u0_info]
    assert details['owner_members'] == [u3_info, u0_info]

# no errors: channel is public and authorised user is a regular user
def test_join_standard():
    info = starter()
    u1, u2, u3, c1 = info[1], info[2], info[3], info[4]
    
    # store user information
    u3_info = {'u_id' : u3['u_id'], 'name_first': 'Charlie', 'name_last' : 'Barry'}
    u1_info = {'u_id' : u1['u_id'], 'name_first' : 'Elizabeth', 'name_last' : 'Alexander'}
    u2_info = {'u_id' : u2['u_id'], 'name_first' : 'Jane', 'name_last' : 'Anton'}
    
    # user 1 joins public channel 
    channel.channel_join(u1['token'], c1['channel_id'])
    details = channel.channel_details(u1['token'], c1['channel_id'])
    # user 1 should appear in channel members list
    assert details['all_members'] == [u3_info, u1_info]
    # user 1 should NOT be in channel owners list
    assert details['owner_members'] == [u3_info]
    
    # user 2 joins public channel
    channel.channel_join(u2['token'], c1['channel_id'])
    details = channel.channel_details(u2['token'], c1['channel_id'])
    # both users 1 and 2 should appear in list of channel members
    assert details['all_members'] == [u3_info, u1_info, u2_info] 
    # users 1 and 2 should NOT appear in channel owners list
    assert details['owner_members'] == [u3_info]



##############################
#    channel_leave tests     #
##############################

# InputError: invalid channel ID (assmuing no channel ID is 0)
def test_leave_input_err():
    info = starter()
    u1 = info[1]
    with pytest.raises(InputError):
        assert channel.channel_leave(u1['token'], 0)

# AccessError: authorised user not a member of channel
def test_leave_access_err():
    info = starter()
    u1, c1 = info[1], info[4]
    with pytest.raises(AccessError):
        # user 1 attempts to leave channel she is not a member of 
        assert channel.channel_leave(u1['token'], c1['channel_id'])


# no errors: global owner leaves channel they are a member of 
def test_leave_global_owner():
    info = starter()
    u0, u3, c1 = info[0], info[3], info[4]
    
    # get user information
    u3_info = {'u_id' : u3['u_id'], 'name_first': 'Charlie', 'name_last' : 'Barry'}
    
    # user 0 (global owner) joins public channel (is now both member and owner of channel)
    channel.channel_join(u0['token'], c1['channel_id'])
    # user 0 leaves that channel
    channel.channel_leave(u0['token'], c1['channel_id'])
    # user 0 should have been removed from both channel members and owners lists
    details = channel.channel_details(u3['token'], c1['channel_id'])
    assert details['all_members'] == [u3_info]
    assert details['owner_members'] == [u3_info]

# no errors: a channel owner (not global owner) leaves channel they are a member of
def test_leave_channel_owner():
    info = starter()
    u1, u3, c1 = info[1], info[3], info[4]
    
    # get user information
    u3_info = {'u_id' : u3['u_id'], 'name_first': 'Charlie', 'name_last' : 'Barry'}
    
    # user 3 adds user 1 as a channel owner (an automatically as member)
    channel.channel_addowner(u3['token'], c1['channel_id'], u1['u_id'])
    # user 1 leaves the channel
    channel.channel_leave(u1['token'], c1['channel_id'])
    # user 1 should have been removed from both channel members and owners lists
    details = channel.channel_details(u3['token'], c1['channel_id'])
    assert details['all_members'] == [u3_info]
    assert details['owner_members'] == [u3_info]
    

# no errors: regular user leaves channel they are a member of 
def test_leave_standard():
    info = starter()
    u1, u2, u3, c1 = info[1], info[2], info[3], info[4]
    
    # get user information
    u3_info = {'u_id' : u3['u_id'], 'name_first': 'Charlie', 'name_last' : 'Barry'}
    u2_info = {'u_id' : u2['u_id'], 'name_first' : 'Jane', 'name_last' : 'Anton'}
    
    # users 1 and 2 join public channel
    channel.channel_join(u1['token'], c1['channel_id'])
    channel.channel_join(u2['token'], c1['channel_id'])
    # user 1 leaves the channel
    channel.channel_leave(u1['token'], c1['channel_id'])
    # only user 2 should remain as a member of channel
    details = channel.channel_details(u2['token'], c1['channel_id'])
    assert details['all_members'] == [u3_info, u2_info]


################################
#    channel_addowner tests    #
################################

# InputError: invalid channel ID (assmuing no channel ID is 0)
def test_addowner_input_err():
    info = starter()
    u0, u1 = info[0], info[1]
    with pytest.raises(InputError):
        assert channel.channel_addowner(u0['token'], 0, u1['u_id'])

# InputError: user with u_id is already an owner of channel (global owner version)
def test_addowner_input_err2():
    info = starter()
    u0, c1 = info[0], info[4]
    # global owner user 0 joins public channel and is added as owner of channel
    channel.channel_join(u0['token'], c1['channel_id'])
    # user 0 attempts to add himself as owner of channel
    with pytest.raises(InputError):
        assert channel.channel_addowner(u0['token'], c1['channel_id'], u0['u_id'])

# InputError: user with u_id is already an owner of channel (regular owner version)
def test_addowner_input_err3():
    info = starter()
    u3, c1 = info[3], info[4]
    
    # user 3 (channel creater and thus owner) attempts to add himself as owner of channel
    with pytest.raises(InputError):
        assert channel.channel_addowner(u3['token'], c1['channel_id'], u3['u_id'])
        

# AccessError: authorised user is not a global owner or an owner of this channel
def test_addowner_access_err():
    info = starter()
    u1, u2, c1 = info[1], info[2], info[4]
    
    # user 1 joins public channel
    channel.channel_join(u1['token'], c1['channel_id'])
    # user 1 (only a channel member) attempts to add user 2 as a channel owner
    with pytest.raises(AccessError):
        assert channel.channel_addowner(u1['token'], c1['channel_id'], u2['u_id'])

# no errors: authorised user is a global owner but not a member of this channel
def test_addowner_global_owner():
    info = starter()
    u0, u1, u3, c1 = info[0], info[1], info[3], info[4]
    
    # get user information
    u3_info = {'u_id' : u3['u_id'], 'name_first': 'Charlie', 'name_last' : 'Barry'}
    u1_info = {'u_id' : u1['u_id'], 'name_first' : 'Elizabeth', 'name_last' : 'Alexander'}
    
    # user 0 (global owner) adds user 1 as an owner of public channel
    channel.channel_addowner(u0['token'], c1['channel_id'], u1['u_id'])
    # user 1 should appear in both channel members and owners lists
    details = channel.channel_details(u1['token'], c1['channel_id'])
    assert details['all_members'] == [u3_info, u1_info]
    assert details['owner_members'] == [u3_info, u1_info]

# no errors: authorised user is a channel owner and u_id is not already an owner
def test_addowner_standard():
    info = starter()
    u0, u1, u3, c1 = info[0], info[1], info[3], info[4]
    
    # get user information
    u3_info = {'u_id' : u3['u_id'], 'name_first': 'Charlie', 'name_last' : 'Barry'}
    u0_info = {'u_id' : u0['u_id'], 'name_first' : 'King', 'name_last' : 'Kingson'}
    u1_info = {'u_id' : u1['u_id'], 'name_first' : 'Elizabeth', 'name_last' : 'Alexander'}
    
    # global owner user 0 joins public channel and is added as owner of channel
    channel.channel_join(u0['token'], c1['channel_id'])
    # user 0 adds user 1 as an owner of the channel
    channel.channel_addowner(u0['token'], c1['channel_id'], u1['u_id'])
    # user 1 should appear in both channel members and owners lists
    details = channel.channel_details(u0['token'], c1['channel_id'])
    assert details['owner_members'] == [u3_info, u0_info, u1_info]
    assert details['all_members'] == [u3_info, u0_info, u1_info]
    

    

###################################
#    channel_removeowner tests    #
###################################

# InputError: invalid channel ID (assmuing no channel ID is 0)
def test_removeowner_input_err():
    info = starter()
    u0 = info[0]
    with pytest.raises(InputError):
        assert channel.channel_removeowner(u0['token'], 0, u0['u_id'])

# InputError: user with u_id is not an owner of channel
def test_removeowner_input_err2():
    info = starter()
    u1, u3, c1 = info[1], info[3], info[4]

    # user 1 joins the channel (not a channel owner)
    channel.channel_join(u1['token'], c1['channel_id'])
    # user 3 attempts to remove user 1 as owner of channel
    with pytest.raises(InputError):
        assert channel.channel_removeowner(u3['token'], c1['channel_id'], u1['u_id'])
    
# AccessError: authorised user is not a global owner or owner of the channel
def test_removeowner_access_err():
    info = starter()
    u1, u2, u3, c1 = info[1], info[2], info[3], info[4]

    # user 3 adds user 2 as a channel owner
    channel.channel_addowner(u3['token'], c1['channel_id'], u2['u_id'])    
    # user 1 joins public channel (not a channel owner)
    channel.channel_join(u1['token'], c1['channel_id'])
    # user 1 (only a regular channel member) attempts to remove user 2 as an owner
    with pytest.raises(AccessError):
        assert channel.channel_removeowner(u1['token'], c1['channel_id'], u2['u_id'])

# no errors: authorised user is a global owner but not an owner of this channel
def test_removeowner_global_owner():
    info = starter()
    u0, u2, u3, c1 = info[0], info[2], info[3], info[4]
    
    # get user information
    u3_info = {'u_id' : u3['u_id'], 'name_first': 'Charlie', 'name_last' : 'Barry'}
    u2_info = {'u_id' : u2['u_id'], 'name_first' : 'Jane', 'name_last' : 'Anton'}

    # user 3 adds user 2 as a channel owner
    channel.channel_addowner(u3['token'], c1['channel_id'], u2['u_id']) 

    # user 0 removes user 2 as channel owner (user 2 is still a member)
    channel.channel_removeowner(u0['token'], c1['channel_id'], u2['u_id'])
    
    details = channel.channel_details(u2['token'], c1['channel_id'])
    assert details['owner_members'] == [u3_info]
    assert details['all_members'] == [u3_info, u2_info]

# no errors: user with u_id is removed as owner from the channel by a regular channel owner
def test_removeowner_standard():
    info = starter()
    u1, u2, u3, c1 = info[1], info[2], info[3], info[4]
    
    # get user information
    u2_info = {'u_id' : u2['u_id'], 'name_first' : 'Jane', 'name_last' : 'Anton'}
    u3_info = {'u_id' : u3['u_id'], 'name_first': 'Charlie', 'name_last' : 'Barry'}
    
    # user 3 adds user 1 as an owner
    channel.channel_addowner(u3['token'], c1['channel_id'], u1['u_id'])
    # user 3 adds user 2 as an owner
    channel.channel_addowner(u3['token'], c1['channel_id'], u2['u_id'])  

    # user 2 removes user 1 as owner
    channel.channel_removeowner(u2['token'], c1['channel_id'], u1['u_id'])
    # user 1 should not be in owners list
    details = channel.channel_details(u2['token'], c1['channel_id'])
    assert details['owner_members'] == [u3_info, u2_info]
    
    # user 2 removes herself as channel owner
    channel.channel_removeowner(u2['token'], c1['channel_id'], u2['u_id'])
    # channel should have one owner now
    details = channel.channel_details(u2['token'], c1['channel_id'])
    assert details['owner_members'] == [u3_info]
    
    
###################################
#      channel_messages tests     #
###################################

# InputError: invalid channel ID
def test_messages_input_err():

    info = starter()
    u3 = info[3]
    
    with pytest.raises(InputError):
        assert channel.channel_messages(u3['token'], 0, 0)

# InputError: start is greater than total number of messages in channel
    info = starter()
    u3, c1 = info[3], info[4]
    
    with pytest.raises(InputError):
        # user 3 attempts to get message at index 0 from a channel with no messages
        assert channel.channel_messages(u3['token'], c1['channel_id'], 0)

# AccessError: authorised user is not a member of the channel
    info = starter()
    u1, c1 = info[1], info[4]
    
    with pytest.raises(AccessError):
        assert channel.channel_messages(u1['token'], c1['channel_id'], -1)

# no errors: reaches least recent message
def test_messages_neg_end():
    info = starter()
    u3, c1 = info[3], info[4]
    
    # user 3 sends 50 messages to c1
    for i in range(0, 50):
        message.message_send(u3['token'], c1['channel_id'], f"message {i}")
    
    # user 3 displays messages from index 0 (most recent)
    c1_messages = channel.channel_messages(u3['token'], c1['channel_id'], 0)
    
    assert len(c1_messages['messages']) == 50
    assert c1_messages['start'] == 0
    assert c1_messages['end'] == -1
       

# no errors: does not reach the least recent message
def test_messages_pos_end():
    info = starter()
    u3, c1 = info[3], info[4]
    
    # user 3 sends 100 messages to c1
    for i in range(0, 100):
        message.message_send(u3['token'], c1['channel_id'], f"message {i}")
    
    # user 3 displays messages from index 10
    c1_messages = channel.channel_messages(u3['token'], c1['channel_id'], 10)
    
    assert len(c1_messages['messages']) == 50
    assert c1_messages['start'] == 10
    assert c1_messages['end'] == 60






