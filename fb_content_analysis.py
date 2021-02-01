import requests
from bs4 import BeautifulSoup

def content_analysis_facebook(username):
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

	return (total_likes, total_talking, fb_grade, fb_like_rank, fb_talk_rank)
