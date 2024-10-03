import sys
sys.dont_write_bytecode = True
import json

def recv(ws):
   response = ws.recv()
   if response:
      return json.loads(response)
   
def send_ws(ws,content):
   ws.send(json.dumps(content))

class dict_to_obj(dict):
    def __getattr__(self, attr):
        value = self.get(attr)
        if isinstance(value, dict):
            return dict_to_obj(value)
        return value