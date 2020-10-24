# COMP1531 Major Project

## Changelog

* Oct 3, 2020 channel and channels updated
* Sep 27, 2020 channel updated
* Sep 26, 2020 auth updated

## Contents
  1. auth
  2. channel
  3. channels
  4. message
  5. user
  6. search

## 1. auth:

* auth_login function: When usre enter an empty email or an empty password. It will return Input error
* token: token is like primary key that can identify user. In auth_register function, user inputs email password and name. It will return a valid token. Invalid token is like '?' or '0' because of wrong input. Therefore it also cannot logout successfully
* login and logout: Logout is successful only user has already login successfully.
* login and register: Login is successful only user has already login successfuly.

## 2. channel:
- When a global owner joins (using channel_join) a channel, they are added to both all_members and owner_members lists.
- A global owner is not automatically an owner or member of any channel until they join (channel_join) or are invited (channel_invite).
- Channel_details will show 'all_memebers' in the order of joining or being invited.
- Channel_messages will show 50 messages at once or until the least recent message is shown (if the channel does not have a sufficient number of messages).
- If a user who is not a member of a channel is added as a channel owner (channel_addowner), they are added to both all_members and owner_members lists. i.e. they do not need to join as members before being made owners.
- A global owner can manipulate channel owner data (via channel_addowner and channel_removeowner) even if they are not a member of that channel.
- Channel owners can remove themselves or other owners from the owner_members list (channel_removeowner).
- The channel_removeowner function only removes the user with u_id as an owner. The user will still remain in the all_members list until they leave the channel.
- If a user joins a channel they are already a member of (channel_join), nothing happens (no errors are produced, but a duplicate instance of the user is not added to the all_members list).

## 3. channels:
- Channels_list will show the details of all channels which the authorised user is a member of.
- Channels_listall will show the details of all channels in the Flockr.
- A user who creates a channel (channels_create) is made an owner of the channel.

## 4. message:
- If a user is a global owner and not part of a channel, they have permission to remove messages from that channel via message_remove.
- If a user is a global owner and not part of a channel, they do not have permission to send messages to that channel (message_send) until they join (channel_join).

## 5. other:
- Global owners can change their own permissions (admin_userpermission_change).
- No errors are produced if admin_userpermission_change does not alter the user's previous permissions (e.g. if a user with permission_id 1 is given permission_id 1 again).
