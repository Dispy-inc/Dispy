import websocket
import json
import threading
import time
from .dispy.utilites import *

class IntentsError(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message

def heartbeat(interval, ws):
   while True:
      time.sleep(interval)
      heartbeat_content = {
         'op': 1,
         'd': 'null'
      }
      send_ws(ws,heartbeat_content)

def event_reroute(ws, response):
   response = json.loads(response)
   if 't' in response and response['t'] != None:
         print(response['t'])
   elif response['op'] == 11:
      print('HEARTBEAT')

class Bot:
   def __init__(self,token) -> None:
      self.token = token
   def eventlink(self,function):
      assert callable(function), "The first argument must be callable."
   def start(self):
      ws = websocket.WebSocket()
      ws.connect('wss://gateway.discord.gg/?v=10&encording=json')
      heartbeat_interval = receive_ws(ws)['d']['heartbeat_interval'] / 1000
      threading.Thread(target=heartbeat, args=(heartbeat_interval, ws)).start()

      payload = {
         'op': 2,
         'd': {
            'token': self.token,
            'intents': 131071,
            'properties': {
               'os': 'linux',
               'browser': 'dispy-lib',
               'device': 'dispy-lib'
            }
         }
      }

      send_ws(ws,payload)
      while True:
         message = ws.recv()
         event_reroute(ws, message)
      
