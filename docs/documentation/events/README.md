---
hidden: true
icon: calculator-simple
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

# Events

{% hint style="info" %}
This page is under construction!
{% endhint %}

***

When using `bot.on()` and `bot.once()`, you can connect a event that discord has to your code. For example, you can link the creation of a message to a function in your code.

There is multiple ways of connecting a discord event to your function. Here's some examples :

#### The basic way

<pre class="language-python"><code class="lang-python">def your_function(msg: Message, user: User):
    # Do something
<strong>    
</strong>bot.on('MESSAGE_CREATE',your_function)
</code></pre>

#### The decorator way

```python
@bot.on('MESSAGE_CREATE')
def your_function(msg: Message, user: User):
    # Do something
```

#### The lazy way (Clearly the best)

```python
@bot.on()
def message_create(msg: Message, user: User):
    # Do something
```

_We don't speak about the shit way (`bot.on(function=message_create)`)._

### Small detail

For simplicity (and to keep my sanity), i preferred to separate DIRECT and normal messages, i used this because it is more simple to code with that and the automatic intents selection is more optimized.
