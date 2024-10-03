from dispy import *
import creds
# /\ Create a creds.py in your bot folder, and put a token variable in it.

bot = Bot(token=creds.token)

def say_hello(msg):
   if msg.author.bot: return False
   if any(element in msg.content for element in ['hello','hola','helo','hey','hi','salut','bonjour']):
      send_message('Hello!',msg.channel_id,creds.token)
   
def ready(args):
   print('READY')

bot.eventlink('READY',ready)
bot.eventlink('MESSAGE_CREATE',say_hello)
bot.start()