# file to store all data
# structure based on project spec

data = {
    'users': [
        # {
        #     'u_id' : 1,
        #     'name_first' : 'John',
        #     'name_last' : 'Smith',
        #     'handle' : 'johnsmith',
        #     'email' : 'johnsmith@gmail.com',
        #     'password' : 'youshallpass',
        #     'is_global_owner' : True
        #     'permission_id' : 2
        # },
    ],
    'channels': [ 
        # {
        #     'channel_id' : 1,
        #     'name' : 'tut 5',
        #     'is_public' : True,
        #     'all_members' : [
        #         {'u_id' : 1, 'name_first' : 'John', 'name_last' : 'Smith'},
        #         {'u_id' : 1, 'name_first' : 'Lucy', 'name_last' : 'Luck'}, ....
        #     ],
        #     'owner_members' : [
        #         {'u_id' : 1, 'name_first' : 'John', 'name_last' : 'Smith'}, ....
        #     ], 
        #     'messages' : [
        #         { 'message_id' : 123,
        #           'u_id' : 111,
        #           'message' : 'abc',
        #           'time_created': 202010011603
        #         }
        #     ]
        # }
    ],
    'tok_uid' : {
        #     12345:32
    },
    # keeps track of the highest message_id (last message to have been sent)
    'last_m_id' : 0
}
