---
icon: robot-astromech
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

# Create a bot

***

In this guide, you will be explained how to register you bot to discord and invite it on your server.

{% hint style="info" %}
You can completly skip this part if you've already taken the token of the bot and invite it to the server.
{% endhint %}

{% hint style="info" %}
A video tutorial will soon be done to help beginner.
{% endhint %}

{% stepper %}
{% step %}
### Go into your [discord developer portal](https://discord.com/developers/applications)

Login if needed.
{% endstep %}

{% step %}
### Create your application

Click **"New Application"** on the discord developer portal and name your application (it will **not** be used as the bot name).
{% endstep %}

{% step %}
### Define your bot

Go into the **"Bot"** section on your left, in here, you can change the profil picture and username of your bot.
{% endstep %}

{% step %}
### Give it the right to read messages

Before you continue, you need to give your bot the ability to do some things, go down a little bit until you see the **"Privileged Gateway Intents"** category (Just before bot permissions).&#x20;

You need to check the 3 options ("Presence Intent", "Server Members Intent" and "Message Content Intent").

This will give your bot the ability to read messages (for example) and this is very pratical lol.

_**Warning:** If your bot is added on more that 100 servers, you will not be able to have theses ability anymore, to regain them, you will need to go in the "App Verification" section on your left. But if you're doing only testing or a custom bot for a server, you don't need those._
{% endstep %}

{% step %}
### Get your token!

To make the bot do things and be aware of things happening, you need to have his token. You can simply get it by resetting it in the **"Bot"** section (The **"Reset Token"** button).

_**Warning:** Your token is like your social security number (Not at this point but you get it), you need to keep it private, do not share it even with best friends. With your token, someone could destroy any server that the bot is on._
{% endstep %}

{% step %}
### Invite your bot on your server

Next, go into the **"0Auth2"** section on your left (right above the bot section).

Go down a little bit in at the end of the page, in **"OAuth2 URL Generator"**. You need to select **"bot"** in the scopes.

Go down a little bit again, in the **"Bot permissions"** field, select **"Administrator"**.

You can change the default permissions of your bot by whatever you want but it is recommended to put administrator for testing.

Now, at the bottom, there is a **"Generated URL"** field containing the URL you need to invite your bot on any server. You can just open it in your browser and select you discord server to invite it, be aware you need to be administrator on the server your inviting your bot to.
{% endstep %}

{% step %}
### And you're done!

Congrat! Your bot is ready to go!

What's next? Learn how to use the dispy lib with python and make your bot go online.
{% endstep %}
{% endstepper %}
