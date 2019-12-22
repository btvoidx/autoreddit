#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
import vk_api
import requests
import time
import threading
import os

from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from random import randint

#from googletrans import Translator
#translator = Translator(service_urls=["translate.google.com"])

events = []

def log(text, logtype):
	string = "[{}/{}]: {}".format(threading.current_thread().name, logtype, text)
	print(string)

def random_id(): #Random number for random_id
	return randint(0, 9223372036854775807)

def loadtokens():
	return os.environ["group-token"]

def failsafe(function, contin=False, *args):
	while contin:
		try:
			return function(*args)
		except Exception as e:
			log(f"An error occurred while executing {function}: {e}", "ERROR")

def eventloop(vk_session):
	while True:
		try:
			longpoll = VkBotLongPoll(vk_session, "180517625")
			log("Connected to longpoll", "TRACE")
		except:
			continue

		try:
			for event in longpoll.listen():
				events.append(event)
		except Exception as e:
			log(f"An error occurred: {e}", "ERROR")

def main(token):
	vk_session = vk_api.VkApi(
		token=token
	)
	vk = vk_session.get_api()
	threading.Thread(target=eventloop, args=[vk_session]).start()
	torem = []

	while True:
		try:
			for e in torem:
				events.remove(e)
			torem = []
			for event in events: # Parsing through every event
				torem.append(event)
				if event.type == VkBotEventType.WALL_POST_NEW:
					if False: #event.obj.text.split("\n")[-1][0:3] == "/u/": # Verifying that this is legit auto-post
						tr = translator.translate(text=event.obj.text.split("\n")[0], dest="ru", src="en").text
						message = f"Примерный перевод с помощью Google Translate:\n{tr}"
						vk.wall.createComment(owner_id=event.obj.owner_id, post_id=event.obj.id, message=message)
						log(f"New post just got translated. Post id: {event.obj.id}", "TRACE")

		except Exception as e:
			log(f"Shit happened: {e}", "ERROR")

if __name__ == '__main__':
	token = loadtokens()
	threading.Thread(target=main, args=[token]).start()