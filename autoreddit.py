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
retries = 0
info = {
	"version": "0.3.0",
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

def failproof(function, failtext):
	global retries
	while True:
		try:
			return function
		except:
			retries = retries + 1
			if retries > max_retries:
				return False
			print(failtext)
			time.sleep(3)

def loadtokens(file):
	token = open(file).read()
	return token

# Main function. Needs some code improvements.
def main(user_token, subreddit):
	post_time = int(time.time()) + 120 # Adding 120 seconds because i running this script 2 minutes before *:00. My host is very busy doing all tasks at *:00

	vk_session = vk_api.VkApi(
		token=user_token
	)
	vk = vk_session.get_api()

	vk.groups.edit(group_id=abs(group_id), photos=2) # Open group photos so script can add new photos to album.

	r = failproof(
		requests.get("https://www.reddit.com/r/{}/top.json?sort=hot&limit={}&raw_json=1".format(subreddit, max_posts), headers=headers),
		"Reddit data grab failed."
	)

	counter = 0
	for post in r.json()["data"]["children"]:
		counter = counter + 1
		# I don't use here failproof() because script CAN work without printing result. It's not a big problem if it can't.
		try:
			print("Post {} of {}:\nSubreddit: {};\nTitle: {};\nFrom: {};\nImage URL: {}.\n".format(
				counter, max_posts,
				post["data"]["subreddit"].encode("utf-8"),
				post["data"]["title"].encode("utf-8"),
				post["data"]["author"].encode("utf-8"),
				post["data"]["url"].encode("utf-8")
			)
		)
		except:
			print("Can't print result of post {}. Trying to continue.".format(counter))

		message = "{}\n\n/u/{}".format(post["data"]["title"].encode("utf-8"), post["data"]["author"].encode("utf-8"))
		post_time = post_time + time_between

		
		newurl = failproof(
			validateURL(post["data"]["url"]),
			"URL validation failed."
		)
		image = failproof(
			uploadPhoto(vk, newurl, abs(group_id), album_id),
			"Failed to upload photo to VK."
		)
		image = "photo" + str(group_id) + "_" + str(image["id"])

	
		failproof(
			vk.wall.post(owner_id=group_id, message=message.decode("utf-8"), publish_date=post_time, attachments=image),
			"Unable to schedule post." + message.decode("utf-8")
		)
		

	vk.groups.edit(group_id=abs(group_id), photos=0) # Close group photos so noone can see what we added today. (But there is a bug. Anyone can still see added photos on news page)

if __name__ == '__main__':
	token = loadtokens("tokens.ignore")
	main(token, "mildlyinteresting")