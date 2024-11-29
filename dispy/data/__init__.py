from dispy.data.errors import errors
from dispy.data.intents import intents
from dispy.modules.intents import intents_variable

class data:
    def __init__(self):
        self.errors = errors
        self.intents = intents_variable(intents)