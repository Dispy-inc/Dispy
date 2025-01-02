from typing import Callable

class SlashCommandBuilder:
    """
    You can build a command like an EmbedBuilder, template to get started:
    ```py
    command = (CommandBuilder()
        .setTitle('command')
        .setDescription('Very interesting description')
    )
    ```
    """
    def __init__(self):
        self.args = {}
    def get(self):
        content = {}
        content.update(self.args)
        content['type'] = 1
        return content
    
    def set(self):
        """Will define the slash command."""
    def link(self,function: Callable = None):
        """Link the slash command to a function and set() it automaticly if not already done."""
    
    def setName(self, name: str):
        self.args['name'] = name
        return self  
    def setDescription(self, description: str):
        self.args['description'] = description
        return self  