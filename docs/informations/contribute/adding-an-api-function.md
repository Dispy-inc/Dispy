---
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

# Adding an API function

***

In this contribute section, it will be explain how to add a function to the API.

If you don't know how to make a pull request (Demand to change the code), you may see this [explaination](./#how-to-make-a-pull-request).

{% stepper %}
{% step %}
#### Research

Before you code a new function for Dispy, you need to know exactly how to do it.

In the [documentation](https://discord.com/developers/docs/intro) of discord, you can find every possible API requests, e.g. [Request to create a message](https://discord.com/developers/docs/resources/message#create-message). You will need theses informations to continue.
{% endstep %}

{% step %}
#### Amount

In Dispy, your function can be in multiple place, e.g. to create a message:

* bot.create\_message() which need all arguments
* message.reply() which need content and a message object
* channel.send() which need content and a channel object

An API function need to be present on types that has the necessary informations and on the bot object.
{% endstep %}

{% step %}
#### Where

The API function for the bot object are located in **dispy.modules.**_**rest\_api.py**_.

For an object (e.g. Message), they are located in **dispy.types** and the file which contain the definition of the object. If the object doesn't exist, follow this guide[^1].
{% endstep %}

{% step %}
#### Introduction

If the object doesn't have the `_api = None` argument, you need to add it at the end of all the type definition. With this you can call the \_\_request\_\_ object.

You need to import these two thing (if they are not already imported):

```python
from dispy.modules.rest_api import result
import asyncio
```
{% endstep %}

{% step %}
#### Create the Function

When creating a function, you need to follow some rules to be sure your pull request will be accepted.

* If the API request return something, it need to has a type object (If it doesn't exist, create it using this guide[^2]) or put 'None' if nothing is returned
* It need to be asynchronous.
* It need to be using the internal function of Dispy (`result` & `__request__`)
* The line using \_\_request\_\_ need to have the comment `# no_traceback` at the end.
* Your function need to have a description.
* Your function need to return a result object and it need to be set when the request send a response. Use the damn template x).

Template:

```python
def function(self, argument=None, **kwargs) -> result[<Type>]:
    """
    Description
    """
    future = self._api._loop.create_future()
    
    async def _asynchronous():
        payload = {}
        
        # Your code here!
        
        result = await self._api.__request__('<method>', f'<path>', payload) # no_traceback
        future.set_result(result)
    
    asyncio.run_coroutine_threadsafe(_asynchronous(), self._api._loop)
    return result[<Type>](future,self._api,<Type>)
```

**What's to change in the template**

1. There is 3 `<Type>` to replace with the return type object, you can put 'None'.
2. You need to change `<method>` to the method used in the API request, e.g. Post, patch, delete.
3. And `<path>`, you replace by the API path given by the Discord documentation.

{% hint style="danger" %}
If your function need to has an argument called **"embeds"**, you need to define it manually inside your \_asynchronous function and give it inside the **run\_coroutine\_threadsafe**. Don't ask me why, ask asyncio.
{% endhint %}
{% endstep %}

{% step %}
Testing

It is important to test your functions before doing a pull request. Please.
{% endstep %}
{% endstepper %}

And you're done! Time to open a pull request

[^1]: There is no guide yet.

    Ask the developer :)

[^2]: There is no guide yet.

    Ask the developer :)
