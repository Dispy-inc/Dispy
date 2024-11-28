from dispy.types.variable import Snowflake, Timestamp
from dispy.types.user import User
from dispy.modules.rest_api import result
from pydantic import BaseModel, create_model, Field
import asyncio
from typing import Optional, Type, Any, Tuple, Dict, List
from copy import deepcopy
from pydantic.fields import FieldInfo

def partial_model(model: Type[BaseModel]):
    def make_field_optional(field: FieldInfo, default: Any = None) -> Tuple[Any, FieldInfo]:
        new = deepcopy(field)
        new.default = default
        new.annotation = Optional[field.annotation]  # type: ignore
        return new.annotation, new
    return create_model(
        f'Partial{model.__name__}',
        __base__=model,
        __module__=model.__module__,
        **{
            field_name: make_field_optional(field_info)
            for field_name, field_info in model.__fields__.items()
        }
    )

#X = Type not implemented

@partial_model
class Message(BaseModel):
    id: Snowflake
    channel_id: Snowflake
    author: User
    content: str
    timestamp: Timestamp
    edited_timestamp: Timestamp
    tts: bool
    mention_everyone: bool
    mentions: List[User]
    mention_roles: List[dict] #X
    mention_channels: Dict[dict, Any] #X
    attachments: List[dict] #X
    embeds: List[dict] #X
    reactions: Dict[dict, Any] #X
    nonce: bool | int
    pinned: bool
    webhook_id: Snowflake
    type: int
    activity: dict #X
    application: dict #X
    application_id: Snowflake
    flags: int
    message_reference: dict #X
    message_snapshots: Dict[dict, Any] #X
    referenced_message: dict
    interaction_metadata: dict #X
    interaction: dict #X
    thread: dict #X
    components: List[dict] #X
    sticker_items: Dict[dict, Any] #X
    stickers: Dict[dict, Any] #X
    position: int
    role_subscription_data: dict #X
    resolved: dict #X
    poll: dict #X
    call: dict #X
    api_: Any = Field(exclude=True)

    def __init__(self, **data):
        super().__init__(**data)
        self._api = data.get('api_')
        self._loop = self._api._loop
        self.__request__ = self._api.__request__

    def reply(self,content=None,**kwargs) -> result["Message"]:
        """
        Reply to the message.
        """
        future = self._loop.create_future()
        
        async def _asynchronous(content, **kwargs):
            payload = {
                "message_reference": {
                    "channel_id": self.channel_id,
                    "message_id": self.id,
                    "type": 0
                },
                "type": 19
            }

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
            
            result = await self.__request__('post', f'channels/{self.channel_id}/messages', payload) # no_traceback
            future.set_result(result)
        
        asyncio.run_coroutine_threadsafe(_asynchronous(content, **kwargs),loop=self._loop)
        return result[Message](future,self._api,Message)
    
    def delete(self) -> result[None]:
        """
        Delete the message.
        """
        future = self._loop.create_future()
        
        async def _asynchronous(channel_id,message_id):
            result = await self.__request__('delete', f'channels/{channel_id}/messages/{message_id}') # no_traceback
            future.set_result(result)
        
        asyncio.run_coroutine_threadsafe(_asynchronous(self.channel_id, self.id), self._loop)
        return result[None](future,self)