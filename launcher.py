#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
import requests
from os import system, chdir, getcwd

repo = "btvoidx/autoreddit"
filename = "main.py"
chdir(getcwd() + "/autoreddit/")

with open(filename) as f:
	current = f.read()
	downloaded = requests.get("https://raw.githubusercontent.com/{}/master/{}".format(repo, filename)).text

	if current == downloaded:
		system("python3.7 {}".format(filename))
	else:
		f.close()
		f = open(filename, "w")
		f.write(downloaded)

		system("python3.7 {}".format(filename))