import aiohttp
import asyncio
import json
from dispy.dispy.utilites import dict_to_obj

base_url = 'https://discord.com/api/v10/'
token = None

async def async_send_message(content, channel_id, __token__):
    payload = {
        'content': content
    }
    headers = {
        'authorization': f'Bot {__token__}',
        'content-type': 'application/json'
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(f'{base_url}channels/{channel_id}/messages', json=payload, headers=headers) as response:
            if response.status != 200:
                raise ConnectionError('Impossible to send a request to the discord API')
            else:
                response_data = await response.json()
                return dict_to_obj(response_data)
            
def send_message(content,channel_id,__token__):
   async def main():
      await asyncio.gather(async_send_message(content,channel_id,__token__))
   
   asyncio.run(main())