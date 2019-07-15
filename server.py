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

client = pymongo.MongoClient(MONGO_URL)
db = client.get_default_database()
requests_log = db['requests_log']
messages_log = db['messages_log']

def convert_to_dict(obj):
  """
  A function takes in a custom object and returns a dictionary representation of the object.
  This dict representation includes meta data such as the object's module and class names.
  """
  
  #  Populate the dictionary with object meta data 
  obj_dict = {
    "__class__": obj.__class__.__name__,
    "__module__": obj.__module__
  }
  
  #  Populate the dictionary with object properties
  obj_dict.update(obj.__dict__)
  
  return obj_dict['_json_data']


@app.route('/webhook',methods=['POST'])
def webhook():
  if request.method == 'POST':
      incoming_message  = request.json
      #print(incoming_message)
      #requests_log.insert_one(incoming_message)
      #parse post reqest for message id and room id
      inc_msg_id  = incoming_message['data']['id']
      inc_room_id = incoming_message['data']['roomId']
      inc_person_email = incoming_message['data']['personEmail']

      incoming_message['_id']=incoming_message['data']['id']
      #requests_log.insert_one(incoming_message)
      #print(BOT_PERSON_EMAIL)
      #print(inc_person_email)

      #check if this is a message sent by the bot 
      if inc_person_email==BOT_PERSON_EMAIL:
        return '', 200
      else:
        

        #reqest the txt of the message id
        inc_msg = api_webexTeams.messages.get(inc_msg_id)

        #insert into Mogoddb
        s= json.loads(json.dumps(inc_msg,default=convert_to_dict))
        s['_id']=s['id']
        messages_log.insert_one(s)


        api_webexTeams.messages.create(inc_room_id,text='respose'+inc_msg.text)

        #print(inc_msg_txt)

        return '', 200
  else:
      abort(400)

if __name__ == '__main__':
    try :
        app.run()
    except:
      #log the exceptionq
      print('exception')
    finally:
      print('closing DB')
      client.close()