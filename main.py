#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
import vk_api
import requests
import time
import threading
import os

from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from random import randint

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
			longpoll = VkBotLongPoll(vk_session, "178327076")
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

	while True:
		try:
			for e in torem:
				events.remove(e)
			torem = []
			for event in events: # Parsing through every event
				torem.append(event)
				print(event)

		except Exception as e:
			print(f"Shit happened: {e}")

if __name__ == '__main__':
	token = loadtokens()
	threading.Thread(target=main, args=[token]).start()