#!/usr/bin/python
from flask import Flask, request, abort
from webexteamssdk import WebexTeamsAPI
import json
import os
import pymongo

app = Flask(__name__)
api_webexTeams = WebexTeamsAPI()
BOT_PERSON_EMAIL = os.environ['WEBEXTEAMS_BOT_PERSON_EMAIL']
MONGO_URL = os.environ['MONGODB_URI']

SEED_DATA = [
    {
        'decade': '1970s',
        'artist': 'Debby Boone',
        'song': 'You Light Up My Life',
        'weeksAtOne': 10
    },
    {
        'decade': '1980s',
        'artist': 'Olivia Newton-John',
        'song': 'Physical',
        'weeksAtOne': 10
    },
    {
        'decade': '1990s',
        'artist': 'Mariah Carey',
        'song': 'One Sweet Day',
        'weeksAtOne': 16
    }
]


@app.route('/webhook',methods=['POST'])
def webhook():
  if request.method == 'POST':
      incoming_message  = request.json
      #parse post reqest for message id and room id
      inc_msg_id  = incoming_message['data']['id']
      inc_room_id = incoming_message['data']['roomId']
      inc_person_email = incoming_message['data']['personEmail']

      print(BOT_PERSON_EMAIL)
      print(inc_person_email)

      client = pymongo.MongoClient(MONGO_URL)
      db = client.get_default_database()
      songs = db['songs']
      songs.insert_many(SEED_DATA)
      query = {'song': 'One Sweet Day'}
      songs.update(query, {'$set': {'artist': 'Mariah Carey ft. Boyz II Men'}})
      cursor = songs.find({'weeksAtOne': {'$gte': 10}}).sort('decade', 1)
      for doc in cursor:
        print ('In the %s, %s by %s topped the charts for %d straight weeks.' %
               (doc['decade'], doc['song'], doc['artist'], doc['weeksAtOne']))
      db.drop_collection('songs')
      client.close()
      
      #check if this is a message sent by the bot 
      if inc_person_email==BOT_PERSON_EMAIL:
        return '', 200
      else:
        

        #reqest the txt of the message id
        inc_msg_txt = api_webexTeams.messages.get(inc_msg_id).text

        api_webexTeams.messages.create(inc_room_id,text='respose'+inc_msg_txt)

        print(inc_msg_txt)

        return '', 200
  else:
      abort(400)

if __name__ == '__main__':
      
      app.run()