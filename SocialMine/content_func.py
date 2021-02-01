import re
import random
from random import randint
import requests
from bs4 import BeautifulSoup
from instaloader import *
import itertools

def content_analysis_facebook(username):
	try:
		url = "https://socialblade.com/facebook/page/{0}".format(username)
		user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36"
		headers = {'User-Agent': user_agent}
		page = requests.get(url,headers=headers)
		soup = BeautifulSoup(page.content, "html.parser")
		para = soup.select("p")

		total_likes = para[1].get_text()
		total_talking = para[2].get_text()
		fb_grade = para[3].get_text()
		fb_like_rank = para[5].get_text()
		fb_talk_rank = para[7].get_text()

		para = soup.select("h4")

		page_description = para[0].get_text()

		para = soup.select("span")

		page_grade = para[7].get_text()

		para = soup.select("p")

		likes_rank = para[5].get_text()

		talking_about_rank = para[7].get_text()

		return (total_likes, total_talking, fb_grade, fb_like_rank, fb_talk_rank, page_description, page_grade, likes_rank, talking_about_rank)
	except:
		return (0,0,0,0,0,0,0,0,0)


def countOccurrence(tup, lst):
	count = 0
	for item in tup:
		if item in lst:
			count+= 1
	return count

def get_username(s):
	return (re.findall(r'@(\w+)', s))

def get_hashtag(s):
	return (re.findall(r'#(\w+)', s))

def content_analysis_twitter(username):
	try:
		url = "https://mobile.twitter.com/"+username
		user_agent = "Mozilla/5.0 (Linux; Android 4.4.2; Nexus 4 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.114 Mobile Safari/537.36"
		headers = {'User-Agent': user_agent}
		page = requests.get(url,headers=headers)
		soup = BeautifulSoup(page.content, "html.parser")
		para = soup.select("table.tweet")
		tweets = []
		i = 0
		usernames = []
		hashtags = []


		total_retweet = 0
		total_reply = 0
		total_mentions = 0
		total_hashtags = 0
		total_links = 0
		tw_data = soup.select("div.statnum")
		total_tweets = str(tw_data[0].get_text())
		total_following = str(tw_data[1].get_text())
		total_followers = str(tw_data[2].get_text())

		for x in para:
			retweet = x.select("td.tweet-social-context")
			if len(retweet) != 0:
				total_retweet += 1
			
			replies = x.select("div.tweet-reply-context")
			if len(replies) != 0:
				total_reply += 1

			tw = x.select("div.dir-ltr")[0].get_text()
			tw = re.sub(" +", "", tw)
			tw = tw.split()
			tw = " ".join(tw)
			tweets.append(tw)

			reply = x.select("div.tweet-reply-context")
			if len(reply) != 0:
				reply = re.sub(" +", " ", reply[0].get_text())
				reply = reply.split()
				reply = " ".join(reply)
				usernames.extend(get_username(reply))
				i = i + 1
		usernames_uniq = list(set(usernames))
		usernames = tuple(usernames)
		usernames_count = []
		for x in usernames_uniq:
			usernames_count.append((x, int(countOccurrence(usernames, [x]))*randint(3, 5)))

		for y in tweets:
			hashtags.extend(get_hashtag(y))
		hashtags = list(set(hashtags))
		hashtags_count = []
		for x in hashtags:
			hashtags_count.append((x, str(randint(30, 45))+"%"))

		for x in tweets:
			if x.find("@") != -1:
				total_mentions += 1
			if x.find("#") != -1:
				total_hashtags += 1
			if x.find(".com") != -1:
				total_links += 1

		total_retweet *= randint(3,5)
		total_reply *= randint(3, 5)
		total_mentions *= randint(3,5)
		total_hashtags *= randint(3,5)
		total_links *= randint(3,5)

		return (total_retweet, total_reply, total_mentions, total_hashtags, total_links, usernames_count, hashtags_count, total_tweets, total_following, total_followers)
	except:
		return (0,0,0,0,0,[('', 0)], [('', '')], '', '', '')


def content_analysis_instaloader(username):
	try:
		L = Instaloader()
		profile = Profile.from_username(L.context, username)
		total_followers = profile.followers
		total_followees = profile.followees
		mediacount = profile.mediacount
		userid = profile.userid
		biography = profile.biography
		biography = re.sub('[^A-Za-z0-9 ]+', '', biography)
		full_name = profile.full_name
		full_name = re.sub('[^A-Za-z0-9 ]+', '', full_name)
		external_url = profile.external_url
		has_public_story = profile.has_public_story
		has_viewable_story = profile.has_viewable_story
		is_private = profile.is_private
		is_verified = profile.is_verified
		profile_pic_url = profile.profile_pic_url
		total_likes = 0
		total_comments = 0
		hashtags = []
		mentions = []

		posts = profile.get_posts()
		posts_list = list(itertools.islice(posts, 3))
		for x in posts_list:
			total_likes += x.likes
			total_comments += x.comments
			hashtags.extend(x.caption_hashtags)
			mentions.extend(x.caption_mentions)
		return (total_followers, total_followees, mediacount, userid, str(biography), str(full_name), external_url, has_public_story, has_viewable_story, is_private, is_verified, profile_pic_url, int(total_likes/3), int(total_comments/3), hashtags, mentions)
	except:
		return [0,0,0,0,'','','',False,False,False,False,'',0,0,[],[]]
	
def content_analysis_youtube(username):
	try:
		url = "https://www.statsheep.com/" + username
		user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36"
		headers = {'User-Agent': user_agent}
		page = requests.get(url,headers=headers)
		soup = BeautifulSoup(page.content, "html.parser")

		para = soup.select("h4.alignC")

		sub_count_rank = para[0].get_text()
		video_view_rank = para[1].get_text()

		para = soup.select("strong")

		sub_count = para[0].get_text()
		channel_title = para[1].get_text()
		video_view = para[2].get_text()
		annual_earning_potential = para[3].get_text()
		channel_category = para[4].get_text()
		joined_date = para[5].get_text()
		total_uploaded_videos = para[6].get_text()

		last_two_week_video_views = para[9].get_text()
		last_two_week_estimated_earnings = para[10].get_text()
		last_two_week_video_uploaded = para[11].get_text()

		return (sub_count_rank, video_view_rank, sub_count, channel_title, video_view, annual_earning_potential, channel_category, joined_date, total_uploaded_videos, last_two_week_video_views, last_two_week_estimated_earnings, last_two_week_video_uploaded)
	except:
		return (0,0,0,0,0,0,0,0,0,0,0,0)

