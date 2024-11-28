#"-1": [
#   "READY",
#   "RESUMED",
#   "VOICE_SERVER_UPDATE",
#   "USER_UPDATE",
#   "INTERACTION_CREATE",
#   "ALL"
#],

class intents_variable:
    def __init__(self,intents) -> None:
        intents_list = intents.copy()
        del intents_list['-1']
        self.__intents_list__ = intents_list

        self.intents = {key for nested_dict in intents.values() for key in nested_dict}
        self.direct_intents = intents["12"] + intents["13"] + intents["14"] + intents["25"]
        self.direct_intents_opposed = [intents["0"][9]] + intents["9"][:3] + intents["10"] + intents["11"] + intents["24"]
    def get_intents(self,eventname) -> list:
        parents = []
        for parent_id, events in self.__intents_list__.items():
            if eventname in events:
                parents.append(parent_id)
        return parents
    def get_child(self,id):
        return list(self.__intents_list__.values())[id]