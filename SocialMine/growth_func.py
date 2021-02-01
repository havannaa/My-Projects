import math
import requests
from bs4 import BeautifulSoup

def follower_growth_insta(username):
	try:
		url = "https://socialblade.com/instagram/user/"+username
		user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36"
		headers = {'User-Agent': user_agent}
		page = requests.get(url,headers=headers)
		soup = BeautifulSoup(page.content, "html.parser")
		total_follower = int(str(soup.select("div.YouTubeUserTopInfo")[1].select("span")[1].get_text()).replace(",", ""))
		total_media = int(str(soup.select("div.YouTubeUserTopInfo")[0].select("span")[1].get_text()).replace(",", ""))
		followers = []

		followers.append(abs(int(str(soup.select("div")[447].select("span")[0].get_text()).replace(",", ""))))
		followers.append(abs(int(str(soup.select("div")[429].select("span")[0].get_text()).replace(",", ""))))
		followers.append(abs(int(str(soup.select("div")[421].select("span")[0].get_text()).replace(",", ""))))
		followers.append(abs(int(str(soup.select("div")[408].select("span")[0].get_text()).replace(",", ""))))
		followers.append(abs(int(str(soup.select("div")[462].select("span")[0].get_text()).replace(",", ""))))

		return (total_follower, total_media, followers)
	except:
		return (0, 0, [0,0,0,0,0])

def follower_growth_twitter(username):
	try:
		url = "https://socialblade.com/twitter/user/"+username
		user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36"
		headers = {'User-Agent': user_agent}
		page = requests.get(url,headers=headers)
		soup = BeautifulSoup(page.content, "html.parser")
		total_follower = int(str(soup.select("div.YouTubeUserTopInfo")[0].select("span")[1].get_text()).replace(",", ""))
		total_media = int(str(soup.select("div.YouTubeUserTopInfo")[3].select("span")[1].get_text()).replace(",", ""))

		followers = []

		para = soup.select("div")

		followers.append(abs(int(str(para[405].select("span")[0].get_text()).replace(",", ""))))
		followers.append(abs(int(str(para[392].select("span")[0].get_text()).replace(",", ""))))
		followers.append(abs(int(str(para[381].select("span")[0].get_text()).replace(",", ""))))
		followers.append(abs(int(str(para[369].select("span")[0].get_text()).replace(",", ""))))
		followers.append(abs(int(str(para[356].select("span")[0].get_text()).replace(",", ""))))
		return (total_follower, total_media, followers)
	except:
		return (0, 0, [0,0,0,0,0])

def follower_growth_facebook(username):
	try:
		url = "https://socialblade.com/facebook/page/"+username
		user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36"
		headers = {'User-Agent': user_agent}
		page = requests.get(url,headers=headers)
		soup = BeautifulSoup(page.content, "html.parser")
		total_follower = int(str(soup.select("p")[1].get_text()).replace("page likes", "").replace(",", "").strip())
		total_activity = int(str(soup.select("p")[2].get_text()).replace("talking about this", "").replace(",", "").strip())
		followers = []
		para = soup.select("div")

		followers.append(abs(int(str(para[257].select("span")[0].get_text()).replace(",", ""))))
		followers.append(abs(int(str(para[367].select("span")[0].get_text()).replace(",", ""))))
		followers.append(abs(int(str(para[356].select("span")[0].get_text()).replace(",", ""))))
		followers.append(abs(int(str(para[345].select("span")[0].get_text()).replace(",", ""))))
		followers.append(abs(int(str(para[334].select("span")[0].get_text()).replace(",", ""))))

		return (total_follower, total_activity, followers)
	except:
		return (0, 0, [0,0,0,0,0])

def follower_growth_tube(username):
	try:
		url = "https://socialblade.com/youtube/user/"+username
		user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36"
		headers = {'User-Agent': user_agent}
		page = requests.get(url,headers=headers)
		soup = BeautifulSoup(page.content, "html.parser")
		total_media = int(str(soup.select("div.YouTubeUserTopInfo")[0].select("span")[1].get_text()).replace(",", "").strip())
		total_follower = (str(soup.select("div.YouTubeUserTopInfo")[1].select("span")[1].get_text()).replace(",", "").strip())

		last_char = total_follower[-1]
		total_follower = float(total_follower.replace(last_char, ""))
		if last_char == "K":
			total_follower = int(total_follower*1000)
		elif last_char == "M":
			total_follower = int(total_follower*1000000)
		else:
			total_follower = int(total_follower)
			
		return (total_media, total_follower)
	except:
		return (0, 0)

"""
print("Instagram")
print(follower_growth_insta("enca"))
print("Twitter")
print(follower_growth_twitter("binance"))
print("Facebook")
print(follower_growth_facebook("binance"))
print("YouTube")
print(follower_growth_tube("mrbeast6000"))
"""
