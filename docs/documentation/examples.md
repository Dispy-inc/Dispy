---
icon: copy
---

# Examples

***

{% hint style="danger" %}
These examples assume that you have the **Message Content** privileged intent enabled. Follow step 4 on the [Create a bot](readme/setup-your-bot-on-discord.md) guide.
{% endhint %}

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

To test your command, simply send `!help` in a channel that the bot has access to.

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

This is a basic example of the embed functionality, to see your embed, simply send `!help` in a channel that the bot has access to.

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

