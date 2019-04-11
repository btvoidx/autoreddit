#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
import requests
from os import system as run

repo = "btvoidx/autoreddit"
filename = "main.py"
filepath = "autoreddit/main.py"

with open(filepath) as f:
	current = f.read()
	downloaded = requests.get("https://raw.githubusercontent.com/{}/master/{}".format(repo, filename)).text

	if current == downloaded:
		run("python3.7 {}".format(filepath))
	else:
		f.close()
		f = open(filepath, "w")
		f.write(downloaded)

		run("python3.7 {}".format(filepath))