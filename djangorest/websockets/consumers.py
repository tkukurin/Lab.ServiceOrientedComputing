import json
from channels import Group
from channels.sessions import channel_session
from channels.auth import channel_session_user_from_http

@channel_session_user_from_http
def ws_connect(message):
  message.reply_channel.send({ 'accept': True })
  message.channel_session['username'] = str(message.user)
  Group('chat').add(message.reply_channel)


@channel_session
def ws_receive(message):
  content = json.loads(message.content.get('text'))
  username = message.channel_session.get('username', 'anonymous')
  
  Group("chat").send({
    'text': json.dumps({
      'username': username,
      'message': content.get('message', ''),
    }),
  })


@channel_session
def ws_disconnect(message):
  Group("chat").discard(message.reply_channel)