import requests
from bs4 import BeautifulSoup
from random import randint
import random

# latest product fetch
def amaz_parse(para):
	title = para.select("div.p13n-sc-truncate.p13n-sc-line-clamp-2")[0].get_text().strip()
	alink = "https://www.amazon.com" + para.select("a.a-link-normal")[0].get("href")
	image = para.select("img")[0].get("src")
	price = para.select("span.p13n-sc-price")[0].get_text().strip()
	return (title, alink, image, price)
def amaz_get_recent():
	page = requests.get("https://www.amazon.com/Best-Sellers/zgbs/wireless/ref=zg_bs_nav_0")
	soup = BeautifulSoup(page.content, "html.parser")
	para = soup.select("li.zg-item-immersion")
	lst_prod = []
	for x in para:
		prod = amaz_parse(x)
		lst_prod.append(prod)
	random.shuffle(lst_prod)
	return lst_prod

# amazon functions
def fetch_tags(para):
	try:
		product_title = para.select("span.a-size-medium.a-color-base.a-text-normal")[0].get_text()
		product_price = para.select("span.a-offscreen")[0].get_text()
		alink = para.select("a.a-link-normal")[0]
		product_link = "https://www.amazon.com" + str((alink.get("href")))
		product_image = para.select("img.s-image")[0].get("src")
		return (product_title, product_price, product_link, product_image)
	except:
		return 0

def get_amazon(product_name):
	try:
		page = requests.get("https://www.amazon.com/s?k="+product_name)
		soup = BeautifulSoup(page.content, "html.parser")

		para = soup.select("div.a-section.a-spacing-medium")
		list_product_title = []
		list_product_price = []
		list_product_link = []
		list_product_image = []
		for x in para:
			fetched = fetch_tags(x)
			if fetched != 0:
				product_title, product_price, product_link, product_image = fetched
				list_product_title.append(product_title)
				list_product_price.append(product_price)
				list_product_link.append(product_link)
				list_product_image.append(product_image)

		list_product_title.reverse()
		list_product_price.reverse()
		list_product_link.reverse()
		list_product_image.reverse()

		return (list_product_title, list_product_price, list_product_link, list_product_image)
	except:
		return ([], [], [], [])

