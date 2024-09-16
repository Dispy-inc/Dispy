import json

def receive_ws(ws):
   response = ws.recv()
   if response:
      return json.loads(response)
   
def send_ws(ws,content):
   ws.send(json.dumps(content))