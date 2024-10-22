---
icon: arrow-down-to-bracket
---

# Introduction

This is the introduction guide on how to install and import dispy for your own project.

{% hint style="warning" %}
Please note that the installation process can be different between users, you will need to know how your system is making python work.
{% endhint %}

## Installation

***

### Prerequisites

Dispy will work with Python 3.12 or higher, it hasn't been tested with lower versions.

The required library's are in the [requirement](../../../requirements.txt) file on the github repository.

### Installation

Dispo isn't yet on pypi, so you will need to install it via the github repo, this command will install it:

{% tabs %}
{% tab title="Windows" %}
```bash
pip install git+https://github.com/JamesMinoucha/Dispy.git
```
{% endtab %}

{% tab title="Linux" %}
{% hint style="danger" %}
<mark style="color:red;">The linux documentation is not yet tested, dispy will be stress test on linux later.</mark>
{% endhint %}

```bash
pip3 install git+https://github.com/JamesMinoucha/Dispy.git
```

Maybe you will need to add sudo to your command.
{% endtab %}
{% endtabs %}

### Virtual Environments (for nerds) <a href="#virtual-environments" id="virtual-environments"></a>

I hate these shit, but here's how to do it for nerds lol.

For starter, please make sure you have python and pip updated & installed, i will not explain it here.

{% tabs %}
{% tab title="Windows" %}
#### Creating the environment

{% code fullWidth="false" %}
```bash
python -m venv bot-env
```
{% endcode %}

#### Activating the environment

```bash
bot-env\Scripts\activate.bat
```

#### Importing the library

```bash
pip install git+https://github.com/JamesMinoucha/Dispy.git
```

And voilà, you have a working (i think) env to work with dispy! you can simply do `deactivate` when you have finished.
{% endtab %}

{% tab title="Linux" %}
{% hint style="danger" %}
<mark style="color:red;">The linux documentation is not yet tested, dispy will be stress test on linux later.</mark>
{% endhint %}

#### Creating the environment

```bash
python3 -m venv bot-env
```

#### Activating the environment

```bash
source bot-env/bin/activate
```

#### Importing the library

```bash
pip3 install git+https://github.com/JamesMinoucha/Dispy.git
```

And voilà, you have a working (i think) env to work with dispy! you can simply do `deactivate` when you have finished.
{% endtab %}
{% endtabs %}

## Importing

***

When using dispy, it is recommended to `import *` because the main functionality are in the same place. Here's a example code assuming that you have made a bot on the discord developer panel, otherwise see the [guide](setup-your-bot-on-discord.md) on how to create a discord bot:

```python
from dispy import *

token = 'your_token'
bot = Bot(token)

def on_message(msg):
   if msg.author.bot: return False
   send_message(msg.channel_id,token,embeds=[
      Embed(
         title="Message created!",
         description=f"Content: {msg.content}"
   )])

def on_ready(msg):
   print('READY')

bot.on(on_message,"MESSAGE_CREATE")
bot.once(on_ready,"READY")
bot.start()
```

In this example, when a message is created, a embed will be send in the same channel showing the content of the message. No intents needed, dispy will calculate it automaticly.

Well done! You have successfully installed and import dispy for your project.

