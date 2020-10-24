import other
import channel
import auth
import channels

## is_valid_channel ##

def test_valid_channel():
    other.clear()
    # False for non-existent channel_id
    assert not channel.is_valid_channel(0)

    # True for existing channel_id
    u0 = auth.auth_register('charlie@gmail.com', 'youshallpass', 'Charlie', 'Barry')
    c1 = channels.channels_create(u0['token'], 'public channel', True)
    
    assert channel.is_valid_channel(c1['channel_id'])
    

## is_valid_uid ##

def test_valid_uid():
    other.clear()
    # False for non-existent u_id
    assert not channel.is_valid_uid(0)

    # True for existing u_id
    u0 = auth.auth_register('charlie@gmail.com', 'youshallpass', 'Charlie', 'Barry')
    assert channel.is_valid_uid(u0['u_id'])

## is_channel_member ##

def test_channel_member_false():
    other.clear()
    # False for non member
    u0 = auth.auth_register('charlie@gmail.com', 'youshallpass', 'Charlie', 'Barry')    
    u1 = auth.auth_register('elizabeth@gmail.com', 'youshallpass', 'Elizabeth', 'Alexander')
    c1 = channels.channels_create(u0['token'], 'public channel', True)
    
    # u1 is not a member of c1
    assert not channel.is_channel_member(u1['u_id'], c1['channel_id'])

    # True for channel member (regular or owner)
    # u0 is a member of c1
    assert channel.is_channel_member(u0['u_id'], c1['channel_id'])


## is_channel_owner ##
    
def test_channel_owner_false():
    other.clear()
    # False for non owner
    u0 = auth.auth_register('charlie@gmail.com', 'youshallpass', 'Charlie', 'Barry')
    u1 = auth.auth_register('elizabeth@gmail.com', 'youshallpass', 'Elizabeth', 'Alexander')
    c1 = channels.channels_create(u0['token'], 'public channel', True)
    channel.channel_join(u1['token'], c1['channel_id'])
    
    # u1 is a member of c1 but not an owner
    assert not channel.is_channel_owner(u1['u_id'], c1['channel_id'])
    
    # True for channel owner
    assert channel.is_channel_owner(u0['u_id'], c1['channel_id'])


## is_public_channel

def test_public_channel_false():
    other.clear()
    # False if channel is private
    u0 = auth.auth_register('charlie@gmail.com', 'youshallpass', 'Charlie', 'Barry')
    c1 = channels.channels_create(u0['token'], 'public channel', False)
    assert not channel.is_public_channel(c1['channel_id'])
    
    # True if channel is public
    c2 = channels.channels_create(u0['token'], 'private channel', True)
    assert channel.is_public_channel(c2['channel_id'])


## is_global_owner ##

def test_global_owner_false():
    other.clear()
    # False if user has regular global permissions (id 2)
    u0 = auth.auth_register('charlie@gmail.com', 'youshallpass', 'Charlie', 'Barry')
    u1 = auth.auth_register('elizabeth@gmail.com', 'youshallpass', 'Elizabeth', 'Alexander')
    
    # u1 is a regular member (not first to register)
    assert not channel.is_global_owner(u1['u_id'])
    
    # True if user is a global owner (id 1)
    assert channel.is_global_owner(u0['u_id'])


## get_user_info ##

# Returns {u_id, name_first, name_last) for a given user
def test_user_info():
    other.clear()
    u0 = auth.auth_register('charlie@gmail.com', 'youshallpass', 'Charlie', 'Barry')
    
    assert channel.get_user_info(u0['u_id']) == {
        'u_id' : u0['u_id'],
        'name_first': 'Charlie',
        'name_last': 'Barry'
    }


## get_channel_info ##

# Returns {name, owner_members, all_members) for a given channel
def test_channel_info():
    other.clear()

    u0 = auth.auth_register('charlie@gmail.com', 'youshallpass', 'Charlie', 'Barry')
    c1 = channels.channels_create(u0['token'], 'public channel', True)
    
    u0_info = channel.get_user_info(u0['u_id'])
    
    assert channel.get_channel_info(c1['channel_id']) == {
        'name': 'public channel',
        'all_members': [u0_info],
        'owner_members': [u0_info]
    }

# UNCOMMENT when message branch is merged
'''
## get_message_details ##

def test_message_details():
    other.clear()
    
    # Returns {} is message_id does not exist
    assert message.get_message_details(0) == {}
    
    # Returns {u_id, channel_id, message} otherwise
    u0 = auth.auth_register('charlie@gmail.com', 'youshallpass', 'Charlie', 'Barry')
    c1 = channels.channels_create(u0['token'], 'public channel', True)
    
    m_id = message.message_send(u0['token'], c1['channel_id'], 'hi')
    assert message.get_message_details(m_id['message_id']) == {
        'u_id': u0['u_id'],
        'channel_id': c1['channel_id'],
        'message': 'hi'
    }
'''



