# -*- coding: utf-8 -*-
import vk_api
import requests
import time

#   Settings   ##############################################
group_id = "-180517625"
group_id_cache = "180517625"
album_id = "261824317"
max_posts = 24
max_retries = max_posts * 4
time_between = 3600

user_token="9c13eb6698fca9f01add63ed27e34b7aeea299a458393bb4075b1c1d4e32f867d599300ce9483cddc5675"
group_token="ab18b179bca28b68b8e9cc44d3354ff958887804dace0b1b30c382690009da00f90e306e5ab15dbc16e64"
#############################################################

#   Persistent vars   #######################################
info = {"version": "0.2.9 beta", "author": "btvoidx"}
headers = {
	"User-Agent": "Python Automatic posts grabber (by /u/btvoidx)"
}
#############################################################

def uploadPhoto(vk, url, group_id, album_id):
	destination = vk.photos.getUploadServer(album_id=album_id, group_id=group_id_cache)

	image = requests.get(url, stream=True)
	data = ("image.jpg", image.raw, image.headers['Content-Type'])
	meta = requests.post(destination['upload_url'], files={'photo': data}).json()
	photo = vk.photos.save(group_id=group_id, album_id=album_id, **meta)[0]
	return photo

def validateURL(url):
	url = url.replace("://imgur.com", "://i.imgur.com")
	if url.split(".")[-1] not in ["png", "jpg", "jpeg", "gif"]:
		url = url + ".png"
	return url

def retried(retries):
	retries = retries + 1
	return retries

def main(subreddit):
	post_time = int(time.time()) + 120
	retries = 0

	vk_session = vk_api.VkApi(
		token=user_token
	)
	vk = vk_session.get_api()

	vk.groups.edit(group_id=group_id_cache, photos=2)

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
				image = uploadPhoto(vk, newurl, group_id_cache, album_id)
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

	vk.groups.edit(group_id=group_id_cache, photos=0)

if __name__ == '__main__':
	main("mildlyinteresting")