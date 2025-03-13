---
icon: '1'
layout:
  title:
    visible: true
  description:
    visible: true
  tableOfContents:
    visible: true
  outline:
    visible: true
  pagination:
    visible: false
---

# Ready print

{% hint style="info" %}
This page is under construction!
{% endhint %}

***

Print when the bot is online on discord. Don't forgot to replace 'your\_token' with your actual token.

<pre class="language-python"><code class="lang-python"><strong>from dispy import Bot
</strong>
token = 'your_token'
bot = Bot(token)

@bot.once('READY')
def on_ready(msg):
   print('READY')

bot.run()
</code></pre>
