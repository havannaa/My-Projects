from instaloader import *
import itertools

def content_analysis_instaloader(username):
	L = Instaloader()
	profile = Profile.from_username(L.context, username)
	total_followers = profile.followers
	total_followees = profile.followees
	mediacount = profile.mediacount
	userid = profile.userid
	biography = profile.biography
	full_name = profile.full_name
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
	return (total_followers, total_followees, mediacount, userid, biography, full_name, external_url, has_public_story, has_viewable_story, is_private, is_verified, profile_pic_url, int(total_likes/3), int(total_comments/3), hashtags, mentions)
	
print(content_analysis_instaloader("dualipa"))
