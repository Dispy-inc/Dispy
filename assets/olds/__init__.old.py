import sys
sys.dont_write_bytecode = True
import websocket
import json
import threading
from ...dispy.dispy.utilites import *

callinglist = {}
afterlist = {}
stopheartbeating = threading.Event()

class IntentsError(Exception):
	def __init__(self, message):
		super().__init__(message)
		self.message = message

class UnfinishFeature(Exception):
	def __init__(self, message):
		super().__init__(message)
		self.message = message

def heartbeat(interval, ws):
	while not stopheartbeating.is_set():
		stopheartbeating.wait(interval)
		if not stopheartbeating.is_set():
			heartbeat_content = {
				'op': 1,
				'd': 'null'
			}
			send_ws(ws,heartbeat_content)
		else:
			break

def after_tasks(function, delay):
	while not stopheartbeating.is_set():
		stopheartbeating.wait(delay)
		if not stopheartbeating.is_set():
			function()

class time():
	def sleep(delay):
		sleep = threading.Event()
		sleep.wait(delay)
		del sleep

def event_reroute(ws):
	while not stopheartbeating.is_set():
		message = ws.recv()
		response = json.loads(message)
		if 't' in response and response['t'] != None:
			for tocall in callinglist.items():
				if response['t'] == tocall[0]:
					tocall[1](dict_to_obj(response['d']))

class Bot:
	def __init__(self,token) -> None:
		self.token = token
		self.ws = websocket.WebSocket()
		self.status = False


	def config(self):
		pass


	def eventlink(self,function: callable,event_name: str):
		"""Link a discord gateway event to a python function.

      Parameters:
       function (callable): The function that should be call when the event is triggered.
       event_name (str): This is the event that will trigger the defined function. Event names are UPPER-CASED with under_scores joining each word in the name.
		"""
		assert callable(function), "The first argument must be callable."
		callinglist.update({event_name:function})


	def end(self):
		"""Disconnect the bot.
		"""
		ws = self.ws
		stopheartbeating.set()
		self.status = False
		ws.close(1000,'shutdown following a request')
		print("Closed")


	def start(self):
		"""Will log-in the bot and start the connection with the discord gateway.
		"""
		ws = self.ws
		ws.connect('wss://gateway.discord.gg/?v=10&encording=json')
		self.status = True
		heartbeat_interval = recv(ws)['d']['heartbeat_interval'] / 1000
		threading.Thread(target=heartbeat, args=(heartbeat_interval, ws)).start()

		payload = {
			'op': 2,
			'd': {
				'token': self.token,
				'intents': 131071,
				'properties': {
					'os': 'linux',
					'browser': 'dispy-lib',
					'device': 'dispy-lib'
				}
			}
		}

		send_ws(ws,payload)
		threading.Thread(target=event_reroute, args=(ws,),daemon=True).start()
		for sending in afterlist.items():
			threading.Thread(target=after_tasks, args=(sending[1], sending[0]),daemon=True)
		
