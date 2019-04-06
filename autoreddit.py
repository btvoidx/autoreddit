# -*- coding: utf-8 -*-
# Main code 
import vk_api
import requests
import time

#   Settings   ##############################################
group_id = -180517625
album_id = 261824317
max_posts = 24
max_retries = max_posts * 4
time_between = 3600
#############################################################

#   Persistent vars   #######################################
info = {
	"version": "0.2.11",
	"author": "vk.com/btvoidx"
}
headers = {
	"User-Agent": "Python Automatic posts grabber (by /u/btvoidx)"
}
#############################################################

# Uploading photo to VK is very annoying process. Why i just cant add images to post using urls?
def uploadPhoto(vk, url, group_id, album_id):
	destination = vk.photos.getUploadServer(album_id=album_id, group_id=abs(group_id))

	image = requests.get(url, stream=True)
	data = ("image.jpg", image.raw, image.headers['Content-Type'])
	meta = requests.post(destination['upload_url'], files={'photo': data}).json()
	photo = vk.photos.save(group_id=group_id, album_id=album_id, **meta)[0]
	return photo

# Make sure script can download image with url.
def validateURL(url):
	url = url.replace("://imgur.com", "://i.imgur.com")
	if url.split(".")[-1] not in ["png", "jpg", "jpeg", "gif"]:
		url = url + ".png"
	return url

def retried(retries):
	retries = retries + 1
	return retries

def loadtokens(file):
	token = open(file).read()
	return token

# Main function. Needs some code improvements.
def main(user_token, subreddit):
	post_time = int(time.time()) + 120 # Adding 120 seconds because i running this script 2 minutes before *:00. My host is very busy doing all tasks at *:00
	retries = 0

	vk_session = vk_api.VkApi(
		token=user_token
	)
	vk = vk_session.get_api()

	vk.groups.edit(group_id=abs(group_id), photos=2) # Open group photos so script can add new photos to album.

	got_r = True
	while got_r:
		try:
			r = requests.get("https://www.reddit.com/r/{}/top.json?sort=hot&limit={}&raw_json=1".format(subreddit, max_posts), headers=headers)
			got_r = False
		except:
			if retried(retries) > max_retries:
				return "Good job, your bot stopped working!"
			print("Unable to grab reddit posts.")
			time.sleep(5)

	counter = 0
	for post in r.json()["data"]["children"]:
		counter = counter + 1
		got_p_u = True
		got_p_p = True
		try:
			# I like how this string ruins my tabs.
			print("""
Post {} of {}:
Subreddit: {};
Title: {};
From: {};
Image URL: {}.

				""".format(
					counter, max_posts,
					post["data"]["subreddit"].encode("utf-8"),
					post["data"]["title"].encode("utf-8"),
					post["data"]["author"].encode("utf-8"),
					post["data"]["url"].encode("utf-8")
				)
			)
		except:
			print("Something went wrong. Trying to continue without printing about post.")

		message = "{}\n\n/u/{}".format(post["data"]["title"].encode("utf-8"), post["data"]["author"].encode("utf-8"))
		post_time = post_time + time_between

		while got_p_u:
			try:
				newurl = validateURL(post["data"]["url"])
				image = uploadPhoto(vk, newurl, abs(group_id), album_id)
				image = "photo" + group_id + "_" + str(image["id"])
				got_p_u = False
			except:
				if retried(retries) > max_retries:
					return "Good job, your bot stopped working!"
				print("Unable to upload photo to VK, {}".format(post["data"]["url"]))
				time.sleep(5)

		while got_p_p:
			try:
				vk.wall.post(owner_id=group_id, message=message.decode("utf-8"), publish_date=post_time, attachments=image)
				got_p_p = False
			except:
				if retried(retries) > max_retries:
					return "Good job, your bot stopped working!"

				print("Unable to schedule post." + message.decode("utf-8"))
				time.sleep(5)

	vk.groups.edit(group_id=abs(group_id), photos=0) # Close group photos so noone can see what we added today. (But there is a bug. Anyone can still see added photos on news page)

if __name__ == '__main__':
	token = loadtokens("tokens.ignore")
	main(token, "mildlyinteresting")