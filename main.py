#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
import vk_api
import requests
import time
import threading
import os

from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from random import randint

from mildlylib import *

#from googletrans import Translator
#translator = Translator(service_urls=["translate.google.com"])

events = []

def random_id(): #Random number for random_id
	return randint(0, 9223372036854775807)

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
			log(f"An error occurred: {e}.", "ERROR")

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
					is_auto = False
					is_ad = False
					if event.obj.text.split("\n")[-1][0:3] == "/u/": # If this is an automatic publication
						is_auto = True

					if event.obj.marked_as_ads == 0: # If post is ad-free
						is_ad = True

					if not is_auto and not is_ad: # Mail about this post if it ad-free and not automatic.
						for peer_id in [2000000001]:
							message = localization.new_post + localization.mailing_notification
							vk.messages.send(peer_id=peer_id, random_id=random_id(), message=message, attachment=f"wall{event.obj.owner_id}_{event.obj.id}")


		except Exception as e:
			log(f"Shit happened: {e}", "ERROR")

if __name__ == '__main__':
	token = os.environ["group-token"]
	threading.Thread(target=main, args=[token]).start()