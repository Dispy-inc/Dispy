from dispy import *
import creds

def message_create(msg):
    print(msg.content)

bot = Bot(creds.token)
bot.eventlink(10)
bot.start()