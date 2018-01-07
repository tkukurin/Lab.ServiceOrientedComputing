import json
import logging
from channels import Group
from channels.sessions import channel_session
from api.models import Tweet
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
from channels.auth import channel_session_user, channel_session_user_from_http 

"""
session_key = '8cae76c505f15432b48c8292a7dd0e54'

session = Session.objects.get(session_key=session_key)
session_data = session.get_decoded()
print session_data
uid = session_data.get('_auth_user_id')
user = User.objects.get(id=uid)
"""

@channel_session
@channel_session_user_from_http
def ws_connect(message):
    print("conn", message.http_session.__dir__())    
    s = Session.objects.get(pk=message.http_session.session_key)
    print(s)
    print(s.get_decoded())
    tweets = Tweet.objects.get(user_id=user_id)
    Group(user_id).add(message.reply_channel)
    #message.channel_session['user_id'] = room.label


@channel_session
@channel_session_user
def ws_receive(message):
    print("receive", message.content)
    user_id = message['user_id']
    content = json.loads(message['text'])
    if content:
        tweet = Tweet.objects.create(owner=user_id, content=content)
        message.reply_channel.send({
          'text': content,
        })


@channel_session
@channel_session_user
def ws_disconnect(message):
    print("disconn", message.content)
    try:
        label = message.channel_session['room']
        _ = Room.objects.get(label=label)
        Group(Room.room_id_from_label(label)).discard(message.reply_channel)

    except (KeyError, Room.DoesNotExist):
        pass