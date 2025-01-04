---
icon: arrow-down-to-bracket
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

# Installation

***

This is the introduction guide on how to install and import dispy for your own project.

## Installation

### Prerequisites

Dispy will work with Python 3.12 or higher, it hasn't been tested with lower versions.

The required library's are in the [requirement](https://github.com/JamesMinoucha/Dispy/blob/main/requirements.txt) file on the github repository.

### Installation

{% tabs %}
{% tab title="Windows" %}
```bash
pip install dispy-bot
```
{% endtab %}

{% tab title="Linux" %}
```bash
pip3 install dispy-bot
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
pip install dispy-bot
```

And voilà, you have a working (i think) env to work with dispy! you can simply do `deactivate` when you have finished.
{% endtab %}

{% tab title="Linux" %}
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
pip3 install dispy-bot
```

And voilà, you have a working (i think) env to work with dispy! you can simply do `deactivate` when you have finished.
{% endtab %}
{% endtabs %}
