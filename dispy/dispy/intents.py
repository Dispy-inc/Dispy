import json
import os

# Direct message now start with DIRECT_
# Direct message poll now start with DIRECT_






#  0[9] 9[3 premier] 10 11
#  12 13 14



with open(os.path.dirname(__file__)+'\\intents.json', 'r') as file:
   intents_list = json.load(file)

def get_intents(event_name):
    parents = []
    for parent_id, events in intents_list.items():
        if event_name in events:
            parents.append(parent_id)
    return parents

def get_inverse_direct_intents() -> list:
    return [intents_list["0"][9]] + intents_list["9"][:3] + intents_list["10"] + intents_list["11"]
def get_direct_intents() -> list:
    return intents_list["12"] + intents_list["13"] + intents_list["14"]

def get_every_intents() -> list:
    return {key for nested_dict in intents_list.values() for key in nested_dict}