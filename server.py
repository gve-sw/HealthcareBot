#!/usr/bin/python
from flask import Flask, request, abort
from webexteamssdk import WebexTeamsAPI
import json

app = Flask(__name__)
api_webexTeams = WebexTeamsAPI()

@app.route('/webhook',methods=['POST'])
def webhook():
  if request.method == 'POST':
      print('holla')
      incoming_message  = request.json
      #parse post reqest for message id and room id
      inc_msg_id  = incoming_message['data']['id']
      inc_room_id = incoming_message['data']['roomId']

      #reqest the txt of the message id
      inc_msg_txt = api_webexTeams.messages.get(inc_msg_id).text

      api_webexTeams.messages.create(inc_room_id,text='respose'+inc_msg_txt)

      print(inc_msg_txt)

      return '', 200
  else:
      abort(400)

if __name__ == '__main__':
   app.run()