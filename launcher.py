#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
import requests
from os import system as run

repo = "btvoidx/autoreddit"
file = "main.py"

with open(file) as f:
	current = f.read()
	downloaded = requests.get("https://raw.githubusercontent.com/{}/master/{}".format(repo, file)).text

	if current == downloaded:
		run("python3.7 {}".format(file))
	else:
		f.close()
		f = open(file, "w")
		f.write(downloaded)

		run("python3.7 {}".format(file))