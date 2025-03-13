---
icon: copy
---

# Examples

***

### Base Template

This is how the base code of your bot should like, but I recommend hiding the token better.

```python
from dispy import Bot

token = 'your_token'
bot = Bot(token)

@bot.once('READY')
def on_ready():
   print('READY')

bot.run()
```

### Help Command

You can try your command by sending !help into a channel that the bot has access to. Please note that you need to have the Message Content Privileged Intent, follow [step 4 on the Create a bot guide](readme/setup-your-bot-on-discord.md).

```python
from dispy import Bot
from dispy.types import (
   Message,
   User
)

token = 'your_token'
bot = Bot(token)

@bot.once('READY')
def on_ready():
   print('READY')
   
@bot.on('MESSAGE_CREATE')
def on_message(msg: Message, user: User):
   if msg.content == '!help':
      msg.reply('My commands are:\n- !help - List the commands')

bot.run()
```

### Embed Example

From the Help Command Example.

```python
from dispy import Bot, EmbedBuilder
from dispy.types import (
   Message,
   User
)

token = 'your_token'
bot = Bot(token)

@bot.once('READY')
def on_ready():
    print('READY')
   
@bot.on('MESSAGE_CREATE')
def on_message(msg: Message, user: User):
    if msg.content == '!help':
        helpCommand = (EmbedBuilder()
            .setTitle('Commands List')
            .setColor('blue')
            .addField('!help', 'List the commands')
        )
        msg.reply(embeds=helpCommand)

bot.run()
```

