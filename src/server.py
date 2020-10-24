import sys
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from error import InputError

#####
import auth
import channel
import channels
import user
import message
import search
####

def defaultHandler(err):
    response = err.get_response()
    print('response', err, err.get_response())
    response.data = dumps({
        "code": err.code,
        "name": "System Error",
        "message": err.get_description(),
    })
    response.content_type = 'application/json'
    return response

APP = Flask(__name__)
CORS(APP)

APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, defaultHandler)

# Example
@APP.route("/echo", methods=['GET'])
def echo():
    data = request.args.get('data')
    if data == 'echo':
   	    raise InputError(description='Cannot echo "echo"')
    return dumps({
        'data': data
    })


## our routes    
  
@APP.route("/auth/register", methods=['POST'])
def auth_register_http():
    
    data = request.get_json()
    
    r = auth.auth_register(data['email'], data['password'], data['name_first'], data['name_last'])

    return dumps(r)
    
    
@APP.route("/channels/create", methods=['POST'])
def channels_create_http():

    data = request.get_json()
    r = channels.channels_create(data['token'], data['name'], data['is_public'])
    
    return dumps(r)


@APP.route("/channel/details", methods=['GET'])
def channel_details_http():

    token = request.args.get('token')
    channel_id = request.args.get('channel_id')
    
    r = channel.channel_details(token, int(channel_id))

    return dumps(r)


@APP.route("/channel/join", methods=['POST'])
def channel_join_http():

    data = request.get_json()
    
    # call channel_join with given {token, channel_id}
    r = channel.channel_join(data['token'], data['channel_id'])
    
    return dumps(r)

@APP.route("/channel/leave", methods=['POST'])
def channel_leave_http():

    data = request.get_json()
    
    # call channel_leave with given {token, channel_id}
    r = channel.channel_leave(data['token'], data['channel_id'])
    
    return dumps(r)


@APP.route("/channel/addowner", methods=['POST'])
def channel_addowner_http():

    data = request.get_json()
    
    # call channel_addowner with given {token, channel_id, u_id}
    r = channel.channel_addowner(data['token'], data['channel_id'], data['u_id'])
    
    return dumps(r)


@APP.route("/channel/removeowner", methods=['POST'])
def channel_removeowner_http():

    data = request.get_json()
    
    # call channel_removeowner with given {token, channel_id, u_id}
    r = channel.channel_removeowner(data['token'], data['channel_id'], data['u_id'])
    
    return dumps(r)


@APP.route("/message/send", methods=['POST'])
def message_send_http():

    data = request.get_json()
    
    # call message_send with given {token, channel_id, message}
    r = message.message_send(data['token'], data['channel_id'], data['message'])
    
    return dumps(r)

@APP.route("/message/remove", methods=['DELETE'])
def message_remove_http():

    data = request.get_json()
    
    # call message_remove with given {token, message_id}
    r = message.message_remove(data['token'], data['message_id'])
    
    return dumps(r)
    

@APP.route("/channel/messages", methods=['GET'])
def channel_messages_http():

    token = request.args.get('token')
    channel_id = request.args.get('channel_id')
    start = request.args.get('start')
    
    r = channel.channel_messages(token, int(channel_id), int(start))

    return dumps(r)

@APP.route("/message/edit", methods=['POST'])
def message_edit_http():

    data = request.get_json()

    r = message.message_edit(data['token'], data['message_id'], data['message'])

    return dumps(r)

@APP.route("/search", methods=['GET'])
def channel_search_http():

    token = request.args.get('token')
    message = request.args.get('message')
    
    r = search.search(token,message)

    return dumps(r)



if __name__ == "__main__":
    APP.run(port=0) # Do not edit this port
