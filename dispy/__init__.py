from .dispy import events
from .dispy.intents import *
from .dispy.rest_api import *
from .dispy.utilites import *
from collections.abc import Callable
from future.utils import raise_
import aiohttp
import asyncio
import os
import sys

class MyException(Exception): pass

debug_enabled = False
def debug(*args, **kwargs):
   if debug_enabled: print(*args, **kwargs)

every_intents = get_every_intents()
direct_intents = get_direct_intents()
not_direct_intents = get_inverse_direct_intents()

# Customs Error
class errors:
   class AuthentificationError(Exception):
      def __init__(self, message):
         super().__init__(message)
         self.message = message
   class TooMany(Exception):
      def __init__(self, message):
         super().__init__(message)
         self.message = message
   class EventError(Exception):
      def __init__(self, message):
         super().__init__(message)
         self.message = message

class Bot:
   def __init__(self,token=None,intents=37377) -> None:
      self.token = token
      self.status = 0
      self.heartbeat_interval = None
      self.handlers = {}
      self.max_handlers = 5
      self.ws = None
      self.intent = intents
      with open(os.path.dirname(__file__)+'\\error_codes.json', 'r') as file:
         self.error_codes = json.load(file)
   def config(self,token=None):
      if self.status != 0:
         raise errors.AuthentificationError('Changing bot config during it execution is not possible.')
      if token != None: self.token = token
   
   # Called when the gateway receive an discord event (not a gateway opcode)
   async def __sendevent__(self,eventname,args):
      tasks = []
      for key, handler in self.handlers.items():
         if key == eventname:
            if eventname in not_direct_intents:
               if handler['is_direct'] and 'guild_id' in args: return False
               if not handler['is_direct'] and 'guild_id' not in args: return False
              
            tasks.append(asyncio.to_thread(handler['function'], args))
      await asyncio.gather(*tasks)

   # Gateway receive function
   async def __recv__(self):
      async for msg in self.ws:
         data = json.loads(msg.data)

         if data['op'] == 10: # Identification and heartbeat set
            self.heartbeat_interval = data['d']['heartbeat_interval'] / 1000
            
            asyncio.create_task(self.__heartbeat__())
            debug('Identification')
            await self.__identify__()
         elif data['op'] == 11: # Heartbeat received
            debug('Heartbeat Received')
         else: # Events
            if data['t'] != None:
               debug(f'Event received: {data['t']}: \n {json.dumps(data,indent=2)}')
               await self.__sendevent__(data['t'],dict_to_obj(data['d']))
            else:
               debug(json.dumps(data,indent=2))

   # Used to identify the bot with the token
   async def __identify__(self):
      for event in self.handlers.keys():
         pass
      payload = {
               'op': 2,
               'd': {
                  'token': self.token,
                  'intents': self.intent,
                  'properties': {
                     'os': 'linux',
                     'browser': 'dispy-lib',
                     'device': 'dispy-lib'
                  }
               }
            }
      await self.ws.send_json(payload)

   # This function send an event ( Will need to be heavily modified when resume will be added :`) )
   async def __heartbeat__(self):
      while True:
         await asyncio.sleep(self.heartbeat_interval)
         heartbeat_payload = {
            "op": 1,
            "d": 'null'
         }
         debug('Heartbeat Sended')
         await self.ws.send_json(heartbeat_payload)

   # Launch the gateway between discord and the client
   def start(self):
      async def start():
         session = aiohttp.ClientSession()
         async with session.ws_connect('wss://gateway.discord.gg/?v=10&encording=json') as ws:
            self.ws = ws
            await self.__recv__()
         await session.close()
      
      # \/ This shit is not the definition of great coding but i dont care, and this work
      async def main():
         await asyncio.gather(start())
      
      asyncio.run(main())
   
   # Function to link a gateway event to a function in the user code
   def eventlink(self,event_name: str, function: Callable):
      try:
         if event_name in every_intents:
            is_direct = event_name in direct_intents
            event_name = event_name[7:] if is_direct else event_name

            if sum(1 for v in self.handlers.values() if v == event_name) < self.max_handlers:
               self.handlers.update({
                  event_name: {
                     "function": function,
                     "is_direct": is_direct
                  }
               })

            else: 
               raise TypeError("test")
         else:
            raise ValueError("test")
      except ValueError as e:
         raise_(ValueError, None, sys.exc_info()[2])