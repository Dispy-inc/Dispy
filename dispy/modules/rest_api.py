import aiohttp
import asyncio
import json
import threading
from dispy.modules import dict_to_obj
from typing import Generic, TypeVar, Type, Unpack

# 888888ba  oo                               
# 88    `8b ``                               
# 88     88 dP .d8888b.    88d888b. dP    dP 
# 88     88 88 Y8ooooo.    88'  `88 88    88 
# 88    .8P 88       88 ,, 88.  .88 88.  .88 
# 8888888P  dP `88888P' 88 88Y888P' `8888P88 
#                          88            .88 
#                          dP        d8888P  

# Developed by ✯James French✯ with ❤
# Licensed with GPLv3

T = TypeVar('T')

class result(Generic[T]):
    """
    Represent the response of the request you've done.
    Use .get() to get variables, this will pause the execution of your code until the response is given.
    """
    def __init__(self, future: asyncio.Future[T], api, cls: Type[T] = None):
        self.future = future
        self.api = api
        self.loop = self.api._loop
        self._cls = cls
    
    def __class_getitem__(cls, item):
        cls._cls = item
        return cls
    
    def get(self) -> T:
        """
        Will block the code execution until response is given.
        """
        async def asynchronous() -> T:
            return await self.future
        
        future_result = asyncio.run_coroutine_threadsafe(asynchronous(), self.loop)
        result = future_result.result(timeout=7)
        return self._cls(**result, api_=self.api) if 'api_' in Message.__annotations__ and self._cls else self._cls(**result)

from dispy.types.message import Message

class __internal__(Generic[T]):
    def  __init__(self,token,error_handler) -> None:
        self._token = token
        self._header = {
            'authorization': f'Bot {self._token}',
            'content-type': 'application/json'
        }
        self._loop = asyncio.new_event_loop()
        self._base_url = 'https://discord.com/api/v10/'
        self._error = error_handler
        threading.Thread(target=self.run_loop, daemon=True).start()
    def run_loop(self):
        asyncio.set_event_loop(self._loop)
        self._loop.run_forever() # no_traceback

    class _encoder(json.JSONEncoder):
        def default(self, obj):
            # Check if the object has '_value' to see if it is safe to serialize it
            if hasattr(obj, '_value'):
                return obj._value
            return super().default(obj)

    async def __request__(self,function,path,payload=None):
        args = {}
        if payload:
            serialized_payload = json.dumps(payload, cls=self._encoder)
            args['json'] = json.loads(serialized_payload)
        async with aiohttp.ClientSession() as session:
            try:
                async with getattr(session, function)(f'{self._base_url}{path}', headers=self._header, **args) as response:
                    if response.status not in [200, 204]:
                        error = json.loads(await response.text())
                        self._error.summon("request_failed",stop=False,code=response.status,error=error["message"])
                    else:
                        if response.status != 204:
                            response_data = await response.json()
                            return dict_to_obj(response_data)
                        else:
                            return None
            except Exception as e:
                self._error.summon("dispy_request_error",stop=False,error=e)

    #--------------------------------------------------------------------------------------#
    #                                       Requests                                       #
    #--------------------------------------------------------------------------------------#

    def create_message(self,content=None,channel_id=None, **kwargs: Unpack[Message]) -> result[Message]:
        """
        Create a message.
        """
        future = self._loop.create_future()

        async def _asynchronous(content,channel_id, **kwargs):
            payload = {}

            # Embed
            embeds = kwargs.get('embeds',None)
            if embeds is not None:
                if not isinstance(embeds, list):
                    embeds = [embeds]
                kwargs['embeds'] = embeds

            if kwargs:
                payload.update(kwargs)
            if content:
                payload.update({"content": content})
            
            result = await self.__request__('post', f'channels/{channel_id}/messages', payload) # no_traceback
            future.set_result(result)
        
        asyncio.run_coroutine_threadsafe(_asynchronous(content,channel_id, **kwargs),self._loop)
        return result[Message](future,self,Message)

    def delete_message(self,channel_id,message_id) -> result[None]:
        """
        Delete a specific message.
        """
        future = self._loop.create_future()

        async def _asynchronous(channel_id,message_id):
            result = await self.__request__('delete', f'channels/{channel_id}/messages/{message_id}') # no_traceback
            future.set_result(result)
        
        asyncio.run_coroutine_threadsafe(_asynchronous(channel_id, message_id), self._loop)
        return result[None](future,self)