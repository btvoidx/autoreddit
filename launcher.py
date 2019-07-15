#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
import requests
from os import system, chdir, getcwd

repo = "btvoidx/mildlybot"
files = ["main.py", "launcher.py"]
chdir(getcwd() + "/autoreddit/")

for filename in files:
	with open(filename) as f:
		current = f.read()
		downloaded = requests.get(f"https://raw.githubusercontent.com/{repo}/master/{filename}").text

		if current == downloaded:
			print(f"{filename} is up to date.")
		else:
			print(f"{filename} can be updated. Updating...")
			f.close()
			f = open(filename, "w")
			f.write(downloaded)
			print(f"{filename} was updated.")

		f.close()

system(f"python3.7 {files[0]}")