import os
import stripe
from millify import millify
import cgi
import mysql.connector
from db_func import *
from growth_func import *
from amazon_func import *
from mail_func import *
from misc_func import *
from content_func import *
from flask import Flask, render_template, url_for, request, make_response, redirect, render_template_string, jsonify
from random import randint
import random
import json
import subprocess
import urllib.request
import requests
from bs4 import BeautifulSoup
from math import ceil
from datetime import date, timedelta
from time import time
import pdfkit
from flask_uploads import UploadSet, configure_uploads, IMAGES

app = Flask(__name__)

#photos = UploadSet("photos", IMAGES)

#app.config["UPLOADED_PHOTOS_DEST"] = "/var/www/FlaskApp/FlaskApp/static/pictures"
#configure_uploads(app, photos)


app.config["APPLICATION_ROOT"] = "/"
UPLOAD_FOLDER = "/var/www/FlaskApp/FlaskApp/static/pictures/"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

stripe_keys ={
	"secret_key": "sk_test_fKAGkiOkzQ1Sya8FKVyTzzKL00sqT9yfGs",
	"publishable_key": "pk_test_rn4jUhQpScyhcnGrDlYDfDVr001XIdMQMe"
}

stripe.api_key = stripe_keys['secret_key']

products = [
{
	"id": 1,
	"name": "Basic Monthly",
	"description": "Basic Subscription, 1 Month Duration",
	"amount": 399
},
{
	"id": 2,
	"name": "Basic Annually",
	"description": "Basic Subscription, 12 Months Duration",
	"amount": 4389
},
{
	"id": 3,
	"name": "Standard Monthly",
	"description": "Standard Subscription, One Month Duration",
	"amount": 899
},
{
	"id": 4,
	"name": "Standard Annually",
	"description": "Standard Subscription, 12 Months Duration",
	"amount": 9889
},
{
	"id": 5,
	"name": "Professional Monthly",
	"description": "Professional Subscription, One Month Duration",
	"amount": 2999
},
{
	"id": 6,
	"name": "Professional Annually",
	"description": "Professional Subscription, 12 Months Duration",
	"amount": 32989
},
]

def get_product(product_id):
	return products[product_id-1]

def handle_array(mys):
	mys = mys.replace("[", "").replace("]", "").replace(",", ":").replace(" ", "")
	return mys

# integer conversion and math functions
def get_last_five_days():
	dates = []
	i = 0
	while i < 5:
		dates.append((date.today()- timedelta(days=i)).strftime('%Y-%m-%d'))
		i = i + 1
	dates.reverse()
	return dates

millnames = ['','k','m','b','t']

"""
def millify(n):
	n = float(n)
	millidx = max(0,min(len(millnames)-1, int(math.floor(0 if n == 0 else math.log10(abs(n))/3))))
	return '{:.0f}{}'.format(n / 10**(3 * millidx), millnames[millidx])
"""

def get_random():
	return randint(100000, 999999)

def get_random_engmt():
	return randint(30, 42)

def followers_by_media(soc_arr):
	try:
		num_fb = int(soc_arr[0])
	except:
		num_fb = 0
	try:
		num_tw = int(soc_arr[1])
	except:
		num_tw = 0
	try:
		num_insta = int(soc_arr[2])
	except:
		num_insta = 0
	total = num_fb + num_tw + num_insta
	try:
		perc_fb = ceil((num_fb/total)*100)
	except:
		perc_fb = 0
	try:
		perc_tw = ceil((num_tw/total)*100)
	except:
		perc_tw = 0
	try:
		perc_insta = ceil((num_insta/total)*100)
	except:
		perc_insta = 0
	if perc_fb == 100:
		perc_fb = 98
	elif perc_tw == 100:
		perc_tw = 98
	elif perc_insta == 100:
		perc_insta = 98
		
	return (perc_fb, perc_tw, perc_insta)

def get_self_profile_stats(soc_arr):
	print(get_fb_likes(soc_arr[0]))
	return (millify(get_fb_likes(soc_arr[0]), precision=2), millify(get_twitter_stats(soc_arr[1]), precision=2), millify(get_insta_stats(soc_arr[2]), precision=2), millify(get_youtube_stats(soc_arr[3]), precision=2))

@app.route("/")
def index():
	email = request.cookies.get("uemail")
	if email != None:
		user_log = 1
	else:
		user_log = 0
	return render_template("index.html", user_log=user_log)

@app.route("/dashboard/")
def dashboard():
	email = request.cookies.get("uemail")
	if email != None:
		image_uploaded_before = False
		uid = get_id_email(email)
		image_name = str(uid)+".jpg"
		pathname = "/var/www/FlaskApp/FlaskApp/static/pictures/" + image_name
		if os.path.exists(pathname):
			image_uploaded_before = True

		print(image_uploaded_before)
		print(image_name)

		db_results = fetch_all_single_record(email)
		last_five = get_last_five_days()
		foll_media = followers_by_media([db_results["fbs1tf"], db_results["tws1tf"], db_results["ins1tf"]])
		owner_profile = [db_results["fbs1"], millify(db_results["fbs1tf"], precision=2), millify(db_results["fbs1tp"], precision=2), str(get_random_engmt())+"%", db_results["tws1"], millify(db_results["tws1tf"], precision=2), millify(db_results["tws1tp"], precision=2), str(get_random_engmt())+"%", db_results["ins1"], millify(db_results["ins1tf"], precision=2), millify(db_results["ins1tp"], precision=2), str(get_random_engmt())+"%", db_results["tbs1"], millify(db_results["tbs1tf"], precision=2), millify(db_results["tbs1tp"], precision=2), str(get_random_engmt())+"%"]
		#self_stats = [millify(db_results["fbs1tf"]), millify(db_results["tws1tf"]), millify(db_results["ins1tf"]), millify(db_results["tbs1tf"])]
		self_stats = [millify(db_results["fbs1tf"], precision=2), millify(db_results["tws1tf"], precision=2), millify(db_results["ins1tf"], precision=2), millify(db_results["tbs1tf"], precision=2)]
		growth = []
		growth.extend(str_to_lst(db_results["fbs1tg"]))
		growth.extend(str_to_lst(db_results["tws1tg"]))
		growth.extend(str_to_lst(db_results["ins1tg"]))
		user_stats = get_user_stats(email)
		notif = get_notif(email)
		print("before stats")
		print(str(user_stats))
		print("after stats")
		subs_stats = get_user_stats(email)[1]
		if subs_stats == "Basic":
			total_input = 5
		elif subs_stats == "Trial":
			total_input = 0
		elif subs_stats == "Standard":
			total_input = 25
		elif subs_stats == "Professional":
			total_input = 100
		return render_template("dashboard.html", self_stats=self_stats, foll_media=foll_media, owner_profile=owner_profile, last_five=last_five, growth=growth, user_stats=user_stats, uid=uid, image_uploaded_before=image_uploaded_before, uploaded_image="pictures/"+image_name, total_input=total_input, notif=notif)
	else:
		return render_template("login.html")
	"""
	foll_media = [67, 19, 14]
	return render_template("dashboard.html", self_stats=self_stats, foll_media=foll_media)
	"""

@app.route("/fb_follower_growth/")
def fb_follower_growth():
	email = request.cookies.get("uemail")
	if email != None:
		image_uploaded_before = False
		uid = get_id_email(email)
		image_name = str(uid)+".jpg"
		pathname = "/var/www/FlaskApp/FlaskApp/static/pictures/" + image_name
		if os.path.exists(pathname):
			image_uploaded_before = True
		db_results = fetch_all_single_record(email)
		last_five = get_last_five_days()
		foll_media = [millify(db_results["fbs1tf"], precision=2), millify(db_results["fbs1tp"], precision=2), str(get_random_engmt())+"%"]
		datam1 = []
		datam2 = []
		datam1.extend(str_to_lst(db_results["fbs1tg"]))
		datam2.extend(str_to_lst(db_results["fbc1tg"]))

		datam3 = []
		datam4 = []

		temp_data_arr = str_to_lst(db_results["fbs1tg"])
		for x in temp_data_arr:
			datam3.append(ceil(x/24))

		temp_data_arr = str_to_lst(db_results["fbc1tg"])
		for x in temp_data_arr:
			datam4.append(ceil(x/24))

		subs_stats = get_user_stats(email)[1]
		if subs_stats == "Basic":
			total_input = 5
		elif subs_stats == "Trial":
			total_input = 0
		elif subs_stats == "Standard":
			total_input = 25
		elif subs_stats == "Professional":
			total_input = 100
		user_stats = get_user_stats(email)
		notif = get_notif(email)
		return render_template("fb_follower_growth.html", datam1=datam1, datam2=datam2, foll_media=foll_media, last_five=last_five, datam3=datam3, datam4=datam4, image_uploaded_before=image_uploaded_before, uploaded_image="pictures/"+image_name, total_input=total_input, user_stats=user_stats, notif=notif)
	else:
		return render_template("login.html")

@app.route("/fb_competitor_growth/")
def fb_competitor_growth():
	email = request.cookies.get("uemail")
	if email != None:
		image_uploaded_before = False
		uid = get_id_email(email)
		image_name = str(uid)+".jpg"
		pathname = "/var/www/FlaskApp/FlaskApp/static/pictures/" + image_name
		if os.path.exists(pathname):
			image_uploaded_before = True
		db_results = fetch_all_single_record(email)
		last_five = get_last_five_days()
		foll_media = [millify(db_results["fbs1tf"], precision=2), millify(db_results["fbs1tp"], precision=2), str(get_random_engmt())+"%"]
		datam1 = []
		datam2 = []
		datam1.extend(str_to_lst(db_results["fbs1tg"]))
		datam2.extend(str_to_lst(db_results["fbc1tg"]))
		profile_data = []
		profile_data.append("@"+db_results["fbs1"])
		profile_data.append("@"+db_results["fbc1"])
		profile_data.append("@"+db_results["fbc2"])
		profile_data.append("@"+db_results["fbc3"])
		profile_data.append("@"+db_results["fbc4"])
		profile_data.append("@"+db_results["fbc5"])
		profile_data.append(millify(db_results["fbs1tf"], precision=2))
		profile_data.append(millify(db_results["fbc1tf"], precision=2))
		profile_data.append(millify(db_results["fbc2tf"], precision=2))
		profile_data.append(millify(db_results["fbc3tf"], precision=2))
		profile_data.append(millify(db_results["fbc4tf"], precision=2))
		profile_data.append(millify(db_results["fbc5tf"], precision=2))
		profile_data.append(millify(db_results["fbs1tp"], precision=2))
		profile_data.append(millify(db_results["fbc1tp"], precision=2))
		profile_data.append(millify(db_results["fbc2tp"], precision=2))
		profile_data.append(millify(db_results["fbc3tp"], precision=2))
		profile_data.append(millify(db_results["fbc4tp"], precision=2))
		profile_data.append(millify(db_results["fbc5tp"], precision=2))
		profile_data.append(str(get_random_engmt())+"%")
		profile_data.append(str(get_random_engmt())+"%")
		profile_data.append(str(get_random_engmt())+"%")
		profile_data.append(str(get_random_engmt())+"%")
		profile_data.append(str(get_random_engmt())+"%")
		profile_data.append(str(get_random_engmt())+"%")
		subs_stats = get_user_stats(email)[1]
		if subs_stats == "Basic":
			total_input = 5
		elif subs_stats == "Trial":
			total_input = 0
		elif subs_stats == "Standard":
			total_input = 25
		elif subs_stats == "Professional":
			total_input = 100
		user_stats = get_user_stats(email)
		notif = get_notif(email)
		return render_template("fb_competitor_growth.html", datam1=datam1, datam2=datam2, foll_media=foll_media, last_five=last_five, profile_data=profile_data, image_uploaded_before=image_uploaded_before, uploaded_image="pictures/"+image_name, total_input=total_input, user_stats=user_stats, notif=notif)
	else:
		return render_template("login.html")

@app.route("/fb_content_engagement/")
def fb_content_engagement():
	email = request.cookies.get("uemail")
	if email != None:
		image_uploaded_before = False
		uid = get_id_email(email)
		image_name = str(uid)+".jpg"
		pathname = "/var/www/FlaskApp/FlaskApp/static/pictures/" + image_name
		if os.path.exists(pathname):
			image_uploaded_before = True
		db_results = fetch_fbcon(email)
		fb_con = [db_results["fbcon_total_likes"], db_results["fbcon_total_talking"], db_results["fbcon_fb_grade"], db_results["fbcon_fb_like_rank"], db_results["fbcon_fb_talk_rank"], db_results["fbcon_page_description"], db_results["fbcon_page_grade"], db_results["fbcon_likes_rank"], db_results["fbcon_talking_about_rank"]]
		subs_stats = get_user_stats(email)[1]
		if subs_stats == "Basic":
			total_input = 5
		elif subs_stats == "Trial":
			total_input = 0
		elif subs_stats == "Standard":
			total_input = 25
		elif subs_stats == "Professional":
			total_input = 100
		subs_stats = get_user_stats(email)[1]
		if subs_stats == "Basic":
			total_input = 5
		elif subs_stats == "Trial":
			total_input = 0
		elif subs_stats == "Standard":
			total_input = 25
		elif subs_stats == "Professional":
			total_input = 100
		user_stats = get_user_stats(email)
		notif = get_notif(email)
		return render_template("fb_content_engagement.html", fb_con=fb_con, image_uploaded_before=image_uploaded_before, uploaded_image="pictures/"+image_name, total_input=total_input, user_stats=user_stats, notif=notif)
	else:
		return render_template("login.html")

@app.route("/fb_hashtag_analysis/")
def fb_hashtag_analysis():
	email = request.cookies.get("uemail")
	if email != None:
		image_uploaded_before = False
		uid = get_id_email(email)
		image_name = str(uid)+".jpg"
		pathname = "/var/www/FlaskApp/FlaskApp/static/pictures/" + image_name
		if os.path.exists(pathname):
			image_uploaded_before = True
		subs_stats = get_user_stats(email)[1]
		if subs_stats == "Basic":
			total_input = 5
		elif subs_stats == "Trial":
			total_input = 0
		elif subs_stats == "Standard":
			total_input = 25
		elif subs_stats == "Professional":
			total_input = 100
		user_stats = get_user_stats(email)
		notif = get_notif(email)
		return render_template("fb_hashtag_analysis.html", image_uploaded_before=image_uploaded_before, uploaded_image="pictures/"+image_name, total_input=total_input, user_stats=user_stats, notif=notif)
	else:
		return render_template("login.html")

@app.route("/fb_content_performance/")
def fb_content_performance():
	email = request.cookies.get("uemail")
	if email != None:
		image_uploaded_before = False
		uid = get_id_email(email)
		image_name = str(uid)+".jpg"
		pathname = "/var/www/FlaskApp/FlaskApp/static/pictures/" + image_name
		if os.path.exists(pathname):
			image_uploaded_before = True
		subs_stats = get_user_stats(email)[1]
		if subs_stats == "Basic":
			total_input = 5
		elif subs_stats == "Trial":
			total_input = 0
		elif subs_stats == "Standard":
			total_input = 25
		elif subs_stats == "Professional":
			total_input = 100
		user_stats = get_user_stats(email)
		notif = get_notif(email)
		return render_template("fb_content_performance.html", image_uploaded_before=image_uploaded_before, uploaded_image="pictures/"+image_name, total_input=total_input, user_stats=user_stats, notif=notif)
	else:
		return render_template("login.html")


@app.route("/tw_follower_growth/")
def tw_follower_growth():
	email = request.cookies.get("uemail")
	if email != None:
		image_uploaded_before = False
		uid = get_id_email(email)
		image_name = str(uid)+".jpg"
		pathname = "/var/www/FlaskApp/FlaskApp/static/pictures/" + image_name
		if os.path.exists(pathname):
			image_uploaded_before = True
		db_results = fetch_all_single_record(email)
		last_five = get_last_five_days()
		foll_media = [millify(db_results["tws1tf"], precision=2), millify(db_results["tws1tp"], precision=2), str(get_random_engmt())+"%"]
		datam1 = []
		datam2 = []
		datam1.extend(str_to_lst(db_results["tws1tg"]))
		datam2.extend(str_to_lst(db_results["twc1tg"]))
		subs_stats = get_user_stats(email)[1]
		if subs_stats == "Basic":
			total_input = 5
		elif subs_stats == "Trial":
			total_input = 0
		elif subs_stats == "Standard":
			total_input = 25
		elif subs_stats == "Professional":
			total_input = 100
		user_stats = get_user_stats(email)
		notif = get_notif(email)
		return render_template("tw_follower_growth.html", datam1=datam1, datam2=datam2, foll_media=foll_media, last_five=last_five, image_uploaded_before=image_uploaded_before, uploaded_image="pictures/"+image_name, total_input=total_input, user_stats=user_stats, notif=notif)
	else:
		return render_template("login.html")

@app.route("/tw_competitor_growth/")
def tw_competitor_growth():
	email = request.cookies.get("uemail")
	if email != None:
		image_uploaded_before = False
		uid = get_id_email(email)
		image_name = str(uid)+".jpg"
		pathname = "/var/www/FlaskApp/FlaskApp/static/pictures/" + image_name
		if os.path.exists(pathname):
			image_uploaded_before = True
		db_results = fetch_all_single_record(email)
		last_five = get_last_five_days()
		foll_media = [millify(db_results["tws1tf"], precision=2), millify(db_results["tws1tp"], precision=2), str(get_random_engmt())+"%"]
		datam1 = []
		datam2 = []
		datam1.extend(str_to_lst(db_results["tws1tg"]))
		datam2.extend(str_to_lst(db_results["twc1tg"]))
		profile_data = []
		profile_data.append("@"+db_results["tws1"])
		profile_data.append("@"+db_results["twc1"])
		profile_data.append("@"+db_results["twc2"])
		profile_data.append("@"+db_results["twc3"])
		profile_data.append("@"+db_results["twc4"])
		profile_data.append("@"+db_results["twc5"])
		profile_data.append(millify(db_results["tws1tf"], precision=2))
		profile_data.append(millify(db_results["twc1tf"], precision=2))
		profile_data.append(millify(db_results["twc2tf"], precision=2))
		profile_data.append(millify(db_results["twc3tf"], precision=2))
		profile_data.append(millify(db_results["twc4tf"], precision=2))
		profile_data.append(millify(db_results["twc5tf"], precision=2))
		profile_data.append(millify(db_results["tws1tp"], precision=2))
		profile_data.append(millify(db_results["twc1tp"], precision=2))
		profile_data.append(millify(db_results["twc2tp"], precision=2))
		profile_data.append(millify(db_results["twc3tp"], precision=2))
		profile_data.append(millify(db_results["twc4tp"], precision=2))
		profile_data.append(millify(db_results["twc5tp"], precision=2))
		profile_data.append(str(get_random_engmt())+"%")
		profile_data.append(str(get_random_engmt())+"%")
		profile_data.append(str(get_random_engmt())+"%")
		profile_data.append(str(get_random_engmt())+"%")
		profile_data.append(str(get_random_engmt())+"%")
		profile_data.append(str(get_random_engmt())+"%")
		subs_stats = get_user_stats(email)[1]
		if subs_stats == "Basic":
			total_input = 5
		elif subs_stats == "Trial":
			total_input = 0
		elif subs_stats == "Standard":
			total_input = 25
		elif subs_stats == "Professional":
			total_input = 100
		user_stats = get_user_stats(email)
		notif = get_notif(email)
		return render_template("tw_competitor_growth.html", datam1=datam1, datam2=datam2, foll_media=foll_media, last_five=last_five, profile_data=profile_data, image_uploaded_before=image_uploaded_before, uploaded_image="pictures/"+image_name, total_input=total_input, user_stats=user_stats, notif=notif)
	else:
		return render_template("login.html")

@app.route("/tw_content_engagement/")
def tw_content_engagement():
	email = request.cookies.get("uemail")
	if email != None:
		image_uploaded_before = False
		uid = get_id_email(email)
		image_name = str(uid)+".jpg"
		pathname = "/var/www/FlaskApp/FlaskApp/static/pictures/" + image_name
		if os.path.exists(pathname):
			image_uploaded_before = True
		db_results = fetch_twcon(email)
		tw_con = [db_results["twcon_total_retweet"], db_results["twcon_total_reply"], db_results["twcon_total_mentions"], db_results["twcon_total_hashtags"], db_results["twcon_total_links"], db_results["twcon_total_tweets"], db_results["twcon_total_following"], db_results["twcon_total_followers"]]
		subs_stats = get_user_stats(email)[1]
		if subs_stats == "Basic":
			total_input = 5
		elif subs_stats == "Trial":
			total_input = 0
		elif subs_stats == "Standard":
			total_input = 25
		elif subs_stats == "Professional":
			total_input = 100
		user_stats = get_user_stats(email)
		notif = get_notif(email)
		return render_template("tw_content_engagement.html", tw_con=tw_con, image_uploaded_before=image_uploaded_before, uploaded_image="pictures/"+image_name, total_input=total_input, user_stats=user_stats, notif=notif)
	else:
		return render_template("login.html")

@app.route("/tw_hashtag_analysis/")
def tw_hashtag_analysis():
	email = request.cookies.get("uemail")
	if email != None:
		image_uploaded_before = False
		uid = get_id_email(email)
		image_name = str(uid)+".jpg"
		pathname = "/var/www/FlaskApp/FlaskApp/static/pictures/" + image_name
		if os.path.exists(pathname):
			image_uploaded_before = True
		db_results = fetch_twcon(email)
		twcon_usernames_count = eval(db_results["twcon_usernames_count"])
		twcon_hashtags_count = eval(db_results["twcon_hashtags_count"])
		twcon_new_hashtags = []
		for x in twcon_hashtags_count:
			if len(x[0]) < 15:
				twcon_new_hashtags.append(x)
		username_count = len(twcon_usernames_count)
		hashtag_count = len(twcon_new_hashtags)
		tw_con = [twcon_usernames_count, twcon_new_hashtags, username_count, hashtag_count]
		subs_stats = get_user_stats(email)[1]
		if subs_stats == "Basic":
			total_input = 5
		elif subs_stats == "Trial":
			total_input = 0
		elif subs_stats == "Standard":
			total_input = 25
		elif subs_stats == "Professional":
			total_input = 100
		user_stats = get_user_stats(email)
		notif = get_notif(email)
		return render_template("tw_hashtag_analysis.html", tw_con=tw_con, image_uploaded_before=image_uploaded_before, uploaded_image="pictures/"+image_name, total_input=total_input, user_stats=user_stats, notif=notif)
	else:
		return render_template("login.html")

@app.route("/tw_content_performance/")
def tw_content_performance():
	email = request.cookies.get("uemail")
	if email != None:
		image_uploaded_before = False
		uid = get_id_email(email)
		image_name = str(uid)+".jpg"
		pathname = "/var/www/FlaskApp/FlaskApp/static/pictures/" + image_name
		if os.path.exists(pathname):
			image_uploaded_before = True
		subs_stats = get_user_stats(email)[1]
		if subs_stats == "Basic":
			total_input = 5
		elif subs_stats == "Trial":
			total_input = 0
		elif subs_stats == "Standard":
			total_input = 25
		elif subs_stats == "Professional":
			total_input = 100
		user_stats = get_user_stats(email)
		notif = get_notif(email)
		return render_template("tw_content_performance.html", image_uploaded_before=image_uploaded_before, uploaded_image="pictures/"+image_name, total_input=total_input, user_stats=user_stats, notif=notif)
	else:
		return render_template("login.html")

@app.route("/tw_sentiment_analysis/")
def tw_sentiment_analysis():
	email = request.cookies.get("uemail")
	if email != None:
		image_uploaded_before = False
		uid = get_id_email(email)
		image_name = str(uid)+".jpg"
		pathname = "/var/www/FlaskApp/FlaskApp/static/pictures/" + image_name
		if os.path.exists(pathname):
			image_uploaded_before = True
		subs_stats = get_user_stats(email)[1]
		if subs_stats == "Basic":
			total_input = 5
		elif subs_stats == "Trial":
			total_input = 0
		elif subs_stats == "Standard":
			total_input = 25
		elif subs_stats == "Professional":
			total_input = 100
		user_stats = get_user_stats(email)
		notif = get_notif(email)
		return render_template("tw_sentiment_analysis.html", image_uploaded_before=image_uploaded_before, uploaded_image="pictures/"+image_name, total_input=total_input, user_stats=user_stats, notif=notif)
	else:
		return render_template("login.html")


@app.route("/insta_follower_growth/")
def insta_follower_growth():
	email = request.cookies.get("uemail")
	"""
		datam1 = follower_growth_insta(fetch_self_profiles(email)[2])
		datam2 = follower_growth_insta(fetch_comp_profiles(email)[2])
		return render_template("insta_follower_growth.html", datam1=datam1, datam2=datam2)
	else:
		return render_template("login.html")
	"""
	if email != None:
		image_uploaded_before = False
		uid = get_id_email(email)
		image_name = str(uid)+".jpg"
		pathname = "/var/www/FlaskApp/FlaskApp/static/pictures/" + image_name
		if os.path.exists(pathname):
			image_uploaded_before = True
		db_results = fetch_all_single_record(email)
		last_five = get_last_five_days()
		foll_media = [millify(db_results["ins1tf"], precision=2), millify(db_results["ins1tp"], precision=2), str(get_random_engmt())+"%"]
		datam1 = []
		datam2 = []
		datam1.extend(str_to_lst(db_results["ins1tg"]))
		datam2.extend(str_to_lst(db_results["inc1tg"]))
		subs_stats = get_user_stats(email)[1]
		if subs_stats == "Basic":
			total_input = 5
		elif subs_stats == "Trial":
			total_input = 0
		elif subs_stats == "Standard":
			total_input = 25
		elif subs_stats == "Professional":
			total_input = 100
		user_stats = get_user_stats(email)
		notif = get_notif(email)
		return render_template("insta_follower_growth.html", datam1=datam1, datam2=datam2, foll_media=foll_media, last_five=last_five, image_uploaded_before=image_uploaded_before, uploaded_image="pictures/"+image_name, total_input=total_input, user_stats=user_stats, notif=notif)
	else:
		return render_template("login.html")

@app.route("/insta_competitor_growth/")
def insta_competitor_growth():
	email = request.cookies.get("uemail")
	if email != None:
		image_uploaded_before = False
		uid = get_id_email(email)
		image_name = str(uid)+".jpg"
		pathname = "/var/www/FlaskApp/FlaskApp/static/pictures/" + image_name
		if os.path.exists(pathname):
			image_uploaded_before = True
		db_results = fetch_all_single_record(email)
		last_five = get_last_five_days()
		foll_media = [millify(db_results["ins1tf"], precision=2), millify(db_results["ins1tp"], precision=2), str(get_random_engmt())+"%"]
		datam1 = []
		datam2 = []
		datam1.extend(str_to_lst(db_results["ins1tg"]))
		datam2.extend(str_to_lst(db_results["inc1tg"]))
		profile_data = []
		profile_data.append("@"+db_results["ins1"])
		profile_data.append("@"+db_results["inc1"])
		profile_data.append("@"+db_results["inc2"])
		profile_data.append("@"+db_results["inc3"])
		profile_data.append("@"+db_results["inc4"])
		profile_data.append("@"+db_results["inc5"])
		profile_data.append(millify(db_results["ins1tf"], precision=2))
		profile_data.append(millify(db_results["inc1tf"], precision=2))
		profile_data.append(millify(db_results["inc2tf"], precision=2))
		profile_data.append(millify(db_results["inc3tf"], precision=2))
		profile_data.append(millify(db_results["inc4tf"], precision=2))
		profile_data.append(millify(db_results["inc5tf"], precision=2))
		profile_data.append(millify(db_results["ins1tp"], precision=2))
		profile_data.append(millify(db_results["inc1tp"], precision=2))
		profile_data.append(millify(db_results["inc2tp"], precision=2))
		profile_data.append(millify(db_results["inc3tp"], precision=2))
		profile_data.append(millify(db_results["inc4tp"], precision=2))
		profile_data.append(millify(db_results["inc5tp"], precision=2))
		profile_data.append(str(get_random_engmt())+"%")
		profile_data.append(str(get_random_engmt())+"%")
		profile_data.append(str(get_random_engmt())+"%")
		profile_data.append(str(get_random_engmt())+"%")
		profile_data.append(str(get_random_engmt())+"%")
		profile_data.append(str(get_random_engmt())+"%")
		subs_stats = get_user_stats(email)[1]
		if subs_stats == "Basic":
			total_input = 5
		elif subs_stats == "Trial":
			total_input = 0
		elif subs_stats == "Standard":
			total_input = 25
		elif subs_stats == "Professional":
			total_input = 100
		user_stats = get_user_stats(email)
		notif = get_notif(email)
		return render_template("insta_competitor_growth.html", datam1=datam1, datam2=datam2, foll_media=foll_media, last_five=last_five, profile_data=profile_data, image_uploaded_before=image_uploaded_before, uploaded_image="pictures/"+image_name, total_input=total_input, user_stats=user_stats, notif=notif)
	else:
		return render_template("login.html")

@app.route("/insta_content_engagement/")
def insta_content_engagement():
	email = request.cookies.get("uemail")
	if email != None:
		image_uploaded_before = False
		uid = get_id_email(email)
		image_name = str(uid)+".jpg"
		pathname = "/var/www/FlaskApp/FlaskApp/static/pictures/" + image_name
		if os.path.exists(pathname):
			image_uploaded_before = True
		db_results = fetch_instacon(email)
		insta_con = [db_results["instacon_total_followers"], db_results["instacon_total_followees"], db_results["instacon_mediacount"], db_results["instacon_userid"], db_results["instacon_biography"], db_results["instacon_full_name"], db_results["instacon_external_url"], db_results["instacon_has_public_story"], db_results["instacon_has_viewable_story"], db_results["instacon_is_private"], db_results["instacon_is_verified"], db_results["instacon_profile_pic_url"], db_results["instacon_total_likes"], db_results["instacon_total_comments"]]
		subs_stats = get_user_stats(email)[1]
		if subs_stats == "Basic":
			total_input = 5
		elif subs_stats == "Trial":
			total_input = 0
		elif subs_stats == "Standard":
			total_input = 25
		elif subs_stats == "Professional":
			total_input = 100
		user_stats = get_user_stats(email)
		notif = get_notif(email)
		return render_template("insta_content_engagement.html", insta_con=insta_con, image_uploaded_before=image_uploaded_before, uploaded_image="pictures/"+image_name, total_input=total_input, user_stats=user_stats, notif=notif)
	else:
		return render_template("login.html")

@app.route("/insta_hashtag_analysis/")
def insta_hashtag_analysis():
	email = request.cookies.get("uemail")
	if email != None:
		image_uploaded_before = False
		uid = get_id_email(email)
		image_name = str(uid)+".jpg"
		pathname = "/var/www/FlaskApp/FlaskApp/static/pictures/" + image_name
		if os.path.exists(pathname):
			image_uploaded_before = True
		db_results = fetch_instacon(email)
		hashtags = eval(db_results["instacon_hashtags"])
		mentions = eval(db_results["instacon_mentions"])
		engmt_hashtag = []
		engmt_mention = []
		len_hashtag = len(hashtags)
		len_mention = len(mentions)
		for x in range(0, len(hashtags)):
			engmt_hashtag.append(str(randint(30, 50))+"%")
		for x in range(0, len(mentions)):
			engmt_mention.append(str(randint(30, 50))+"%")
		subs_stats = get_user_stats(email)[1]
		if subs_stats == "Basic":
			total_input = 5
		elif subs_stats == "Trial":
			total_input = 0
		elif subs_stats == "Standard":
			total_input = 25
		elif subs_stats == "Professional":
			total_input = 100
		user_stats = get_user_stats(email)
		notif = get_notif(email)
		return render_template("insta_hashtag_analysis.html", hashtags=hashtags, mentions=mentions, engmt_hashtag=engmt_hashtag, engmt_mention=engmt_mention, len_hashtag=len_hashtag, len_mention=len_mention, image_uploaded_before=image_uploaded_before, uploaded_image="pictures/"+image_name, total_input=total_input, user_stats=user_stats, notif=notif)
	else:
		return render_template("login.html")

@app.route("/insta_content_performance/")
def insta_content_performance():
	email = request.cookies.get("uemail")
	if email != None:
		image_uploaded_before = False
		uid = get_id_email(email)
		image_name = str(uid)+".jpg"
		pathname = "/var/www/FlaskApp/FlaskApp/static/pictures/" + image_name
		if os.path.exists(pathname):
			image_uploaded_before = True
		subs_stats = get_user_stats(email)[1]
		if subs_stats == "Basic":
			total_input = 5
		elif subs_stats == "Trial":
			total_input = 0
		elif subs_stats == "Standard":
			total_input = 25
		elif subs_stats == "Professional":
			total_input = 100
		user_stats = get_user_stats(email)
		notif = get_notif(email)
		return render_template("insta_content_performance.html", image_uploaded_before=image_uploaded_before, uploaded_image="pictures/"+image_name, total_input=total_input, user_stats=user_stats, notif=notif)
	else:
		return render_template("login.html")


@app.route("/tube_subscriber_growth/")
def tube_subscriber_growth():
	email = request.cookies.get("uemail")
	if email != None:
		image_uploaded_before = False
		uid = get_id_email(email)
		image_name = str(uid)+".jpg"
		pathname = "/var/www/FlaskApp/FlaskApp/static/pictures/" + image_name
		if os.path.exists(pathname):
			image_uploaded_before = True
		subs_stats = get_user_stats(email)[1]
		if subs_stats == "Basic":
			total_input = 5
		elif subs_stats == "Trial":
			total_input = 0
		elif subs_stats == "Standard":
			total_input = 25
		elif subs_stats == "Professional":
			total_input = 100
		user_stats = get_user_stats(email)
		notif = get_notif(email)
		return render_template("tube_subscriber_growth.html", image_uploaded_before=image_uploaded_before, uploaded_image="pictures/"+image_name, total_input=total_input, user_stats=user_stats, notif=notif)
	else:
		return render_template("login.html")

@app.route("/tube_competitor_growth/")
def tube_competitor_growth():
	email = request.cookies.get("uemail")
	if email != None:
		image_uploaded_before = False
		uid = get_id_email(email)
		image_name = str(uid)+".jpg"
		pathname = "/var/www/FlaskApp/FlaskApp/static/pictures/" + image_name
		if os.path.exists(pathname):
			image_uploaded_before = True
		db_results = fetch_tbcomp(email)
		db_results["tbs1tf"] = millify(db_results["tbs1tf"], precision=2)
		db_results["tbs1tp"] = millify(db_results["tbs1tp"], precision=2)
		db_results["tbc1tf"] = millify(db_results["tbc1tf"], precision=2)
		db_results["tbc1tp"] = millify(db_results["tbc1tp"], precision=2)
		db_results["tbc2tf"] = millify(db_results["tbc2tf"], precision=2)
		db_results["tbc2tp"] = millify(db_results["tbc2tp"], precision=2)
		db_results["tbc3tf"] = millify(db_results["tbc3tf"], precision=2)
		db_results["tbc3tp"] = millify(db_results["tbc3tp"], precision=2)
		db_results["tbc4tf"] = millify(db_results["tbc4tf"], precision=2)
		db_results["tbc4tp"] = millify(db_results["tbc4tp"], precision=2)
		db_results["tbc5tf"] = millify(db_results["tbc5tf"], precision=2)
		db_results["tbc5tp"] = millify(db_results["tbc5tp"], precision=2)
		db_results["tbs1engmt"] = str(int(db_results["tbs1engmt"]))+"%"
		subs_stats = get_user_stats(email)[1]
		if subs_stats == "Basic":
			total_input = 5
		elif subs_stats == "Trial":
			total_input = 0
		elif subs_stats == "Standard":
			total_input = 25
		elif subs_stats == "Professional":
			total_input = 100
		user_stats = get_user_stats(email)
		notif = get_notif(email)
		return render_template("tube_competitor_growth.html", db_results=db_results, image_uploaded_before=image_uploaded_before, uploaded_image="pictures/"+image_name, total_input=total_input, user_stats=user_stats, notif=notif)
	else:
		return render_template("login.html")

@app.route("/tube_content_engagement/")
def tube_content_engagement():
	email = request.cookies.get("uemail")
	if email != None:
		image_uploaded_before = False
		uid = get_id_email(email)
		image_name = str(uid)+".jpg"
		pathname = "/var/www/FlaskApp/FlaskApp/static/pictures/" + image_name
		if os.path.exists(pathname):
			image_uploaded_before = True
		db_results = fetch_tubecon(email)
		tubecon = [db_results["tubecon_sub_count_rank"], db_results["tubecon_video_view_rank"], db_results["tubecon_sub_count"], db_results["tubecon_channel_title"], db_results["tubecon_video_view"], db_results["tubecon_annual_earning_potential"], db_results["tubecon_channel_category"], db_results["tubecon_joined_date"], db_results["tubecon_total_uploaded_videos"], db_results["tubecon_last_two_week_video_views"], db_results["tubecon_last_two_week_estimated_earnings"], str(abs(int(db_results["tubecon_last_two_week_video_uploaded"])))]
		subs_stats = get_user_stats(email)[1]
		if subs_stats == "Basic":
			total_input = 5
		elif subs_stats == "Trial":
			total_input = 0
		elif subs_stats == "Standard":
			total_input = 25
		elif subs_stats == "Professional":
			total_input = 100
		user_stats = get_user_stats(email)
		notif = get_notif(email)
		return render_template("tube_content_engagement.html", tubecon=tubecon, image_uploaded_before=image_uploaded_before, uploaded_image="pictures/"+image_name, total_input=total_input, user_stats=user_stats, notif=notif)
	else:
		return render_template("login.html")


@app.route("/social_fb/")
def social_fb():
	email = request.cookies.get("uemail")
	if email != None:
		image_uploaded_before = False
		uid = get_id_email(email)
		image_name = str(uid)+".jpg"
		pathname = "/var/www/FlaskApp/FlaskApp/static/pictures/" + image_name
		if os.path.exists(pathname):
			image_uploaded_before = True
		profiles = fetch_fb(email)

		subs_stats = get_user_stats(email)[1]
		if subs_stats == "Basic":
			total_input = 5
		elif subs_stats == "Trial":
			total_input = 0
		elif subs_stats == "Standard":
			total_input = 25
		elif subs_stats == "Professional":
			total_input = 100
		user_stats = get_user_stats(email)
		notif = get_notif(email)
		return render_template("social_fb.html", profiles=profiles, image_uploaded_before=image_uploaded_before, uploaded_image="pictures/"+image_name, total_input=total_input, user_stats=user_stats, notif=notif)
	else:
		return render_template("login.html")

@app.route("/social_tw/")
def social_tw():
	email = request.cookies.get("uemail")
	if email != None:
		image_uploaded_before = False
		uid = get_id_email(email)
		image_name = str(uid)+".jpg"
		pathname = "/var/www/FlaskApp/FlaskApp/static/pictures/" + image_name
		if os.path.exists(pathname):
			image_uploaded_before = True
		subs_stats = get_user_stats(email)[1]
		if subs_stats == "Basic":
			total_input = 5
		elif subs_stats == "Trial":
			total_input = 0
		elif subs_stats == "Standard":
			total_input = 25
		elif subs_stats == "Professional":
			total_input = 100
		profiles = fetch_tw(email)
		user_stats = get_user_stats(email)
		notif = get_notif(email)
		return render_template("social_tw.html", profiles=profiles, image_uploaded_before=image_uploaded_before, uploaded_image="pictures/"+image_name, total_input=total_input, user_stats=user_stats, notif=notif)
	else:
		return render_template("login.html")

@app.route("/social_insta/")
def social_insta():
	email = request.cookies.get("uemail")
	if email != None:
		image_uploaded_before = False
		uid = get_id_email(email)
		image_name = str(uid)+".jpg"
		pathname = "/var/www/FlaskApp/FlaskApp/static/pictures/" + image_name
		if os.path.exists(pathname):
			image_uploaded_before = True
		profiles = fetch_in(email)
		subs_stats = get_user_stats(email)[1]
		if subs_stats == "Basic":
			total_input = 5
		elif subs_stats == "Trial":
			total_input = 0
		elif subs_stats == "Standard":
			total_input = 25
		elif subs_stats == "Professional":
			total_input = 100
		user_stats = get_user_stats(email)
		notif = get_notif(email)
		return render_template("social_insta.html", profiles=profiles, image_uploaded_before=image_uploaded_before, uploaded_image="pictures/"+image_name, total_input=total_input, user_stats=user_stats, notif=notif)
	else:
		return render_template("login.html")

@app.route("/social_tube/")
def social_tube():
	email = request.cookies.get("uemail")
	if email != None:
		image_uploaded_before = False
		uid = get_id_email(email)
		image_name = str(uid)+".jpg"
		pathname = "/var/www/FlaskApp/FlaskApp/static/pictures/" + image_name
		if os.path.exists(pathname):
			image_uploaded_before = True
		profiles = fetch_tb(email)
		subs_stats = get_user_stats(email)[1]
		if subs_stats == "Basic":
			total_input = 5
		elif subs_stats == "Trial":
			total_input = 0
		elif subs_stats == "Standard":
			total_input = 25
		elif subs_stats == "Professional":
			total_input = 100
		user_stats = get_user_stats(email)
		notif = get_notif(email)
		return render_template("social_tube.html", profiles=profiles, image_uploaded_before=image_uploaded_before, uploaded_image="pictures/"+image_name, total_input=total_input, user_stats=user_stats, notif=notif)
	else:
		return render_template("login.html")

@app.route("/social_fb_standard/")
def social_fb_standard():
	email = request.cookies.get("uemail")
	if email != None:
		image_uploaded_before = False
		uid = get_id_email(email)
		image_name = str(uid)+".jpg"
		pathname = "/var/www/FlaskApp/FlaskApp/static/pictures/" + image_name
		if os.path.exists(pathname):
			image_uploaded_before = True
		profiles = fetch_fb(email)

		subs_stats = get_user_stats(email)[1]
		if subs_stats == "Basic":
			total_input = 5
		elif subs_stats == "Trial":
			total_input = 0
		elif subs_stats == "Standard":
			total_input = 25
		elif subs_stats == "Professional":
			total_input = 100
		user_stats = get_user_stats(email)
		notif = get_notif(email)
		return render_template("social_fb_standard.html", profiles=profiles, image_uploaded_before=image_uploaded_before, uploaded_image="pictures/"+image_name, total_input=total_input, user_stats=user_stats, notif=notif)
	else:
		return render_template("login.html")

@app.route("/social_tw_standard/")
def social_tw_standard():
	email = request.cookies.get("uemail")
	if email != None:
		image_uploaded_before = False
		uid = get_id_email(email)
		image_name = str(uid)+".jpg"
		pathname = "/var/www/FlaskApp/FlaskApp/static/pictures/" + image_name
		if os.path.exists(pathname):
			image_uploaded_before = True
		profiles = fetch_fb(email)

		subs_stats = get_user_stats(email)[1]
		if subs_stats == "Basic":
			total_input = 5
		elif subs_stats == "Trial":
			total_input = 0
		elif subs_stats == "Standard":
			total_input = 25
		elif subs_stats == "Professional":
			total_input = 100
		user_stats = get_user_stats(email)
		notif = get_notif(email)
		return render_template("social_tw_standard.html", profiles=profiles, image_uploaded_before=image_uploaded_before, uploaded_image="pictures/"+image_name, total_input=total_input, user_stats=user_stats, notif=notif)
	else:
		return render_template("login.html")

@app.route("/social_insta_standard/")
def social_insta_standard():
	email = request.cookies.get("uemail")
	if email != None:
		image_uploaded_before = False
		uid = get_id_email(email)
		image_name = str(uid)+".jpg"
		pathname = "/var/www/FlaskApp/FlaskApp/static/pictures/" + image_name
		if os.path.exists(pathname):
			image_uploaded_before = True
		profiles = fetch_fb(email)

		subs_stats = get_user_stats(email)[1]
		if subs_stats == "Basic":
			total_input = 5
		elif subs_stats == "Trial":
			total_input = 0
		elif subs_stats == "Standard":
			total_input = 25
		elif subs_stats == "Professional":
			total_input = 100
		user_stats = get_user_stats(email)
		notif = get_notif(email)
		return render_template("social_insta_standard.html", profiles=profiles, image_uploaded_before=image_uploaded_before, uploaded_image="pictures/"+image_name, total_input=total_input, user_stats=user_stats, notif=notif)
	else:
		return render_template("login.html")

@app.route("/social_tube_standard/")
def social_tube_standard():
	email = request.cookies.get("uemail")
	if email != None:
		image_uploaded_before = False
		uid = get_id_email(email)
		image_name = str(uid)+".jpg"
		pathname = "/var/www/FlaskApp/FlaskApp/static/pictures/" + image_name
		if os.path.exists(pathname):
			image_uploaded_before = True
		profiles = fetch_fb(email)

		subs_stats = get_user_stats(email)[1]
		if subs_stats == "Basic":
			total_input = 5
		elif subs_stats == "Trial":
			total_input = 0
		elif subs_stats == "Standard":
			total_input = 25
		elif subs_stats == "Professional":
			total_input = 100
		user_stats = get_user_stats(email)
		notif = get_notif(email)
		return render_template("social_tube_standard.html", profiles=profiles, image_uploaded_before=image_uploaded_before, uploaded_image="pictures/"+image_name, total_input=total_input, user_stats=user_stats, notif=notif)
	else:
		return render_template("login.html")

@app.route("/social_fb_professional/")
def social_fb_professional():
	email = request.cookies.get("uemail")
	if email != None:
		image_uploaded_before = False
		uid = get_id_email(email)
		image_name = str(uid)+".jpg"
		pathname = "/var/www/FlaskApp/FlaskApp/static/pictures/" + image_name
		if os.path.exists(pathname):
			image_uploaded_before = True
		profiles = fetch_fb(email)

		subs_stats = get_user_stats(email)[1]
		if subs_stats == "Basic":
			total_input = 5
		elif subs_stats == "Trial":
			total_input = 0
		elif subs_stats == "Standard":
			total_input = 25
		elif subs_stats == "Professional":
			total_input = 100
		user_stats = get_user_stats(email)
		notif = get_notif(email)
		return render_template("social_fb_professional.html", profiles=profiles, image_uploaded_before=image_uploaded_before, uploaded_image="pictures/"+image_name, total_input=total_input, user_stats=user_stats, notif=notif)
	else:
		return render_template("login.html")

@app.route("/social_tw_professional/")
def social_tw_professional():
	email = request.cookies.get("uemail")
	if email != None:
		image_uploaded_before = False
		uid = get_id_email(email)
		image_name = str(uid)+".jpg"
		pathname = "/var/www/FlaskApp/FlaskApp/static/pictures/" + image_name
		if os.path.exists(pathname):
			image_uploaded_before = True
		profiles = fetch_fb(email)

		subs_stats = get_user_stats(email)[1]
		if subs_stats == "Basic":
			total_input = 5
		elif subs_stats == "Trial":
			total_input = 0
		elif subs_stats == "Standard":
			total_input = 25
		elif subs_stats == "Professional":
			total_input = 100
		user_stats = get_user_stats(email)
		notif = get_notif(email)
		return render_template("social_tw_professional.html", profiles=profiles, image_uploaded_before=image_uploaded_before, uploaded_image="pictures/"+image_name, total_input=total_input, user_stats=user_stats, notif=notif)
	else:
		return render_template("login.html")

@app.route("/social_insta_professional/")
def social_insta_professional():
	email = request.cookies.get("uemail")
	if email != None:
		image_uploaded_before = False
		uid = get_id_email(email)
		image_name = str(uid)+".jpg"
		pathname = "/var/www/FlaskApp/FlaskApp/static/pictures/" + image_name
		if os.path.exists(pathname):
			image_uploaded_before = True
		profiles = fetch_fb(email)

		subs_stats = get_user_stats(email)[1]
		if subs_stats == "Basic":
			total_input = 5
		elif subs_stats == "Trial":
			total_input = 0
		elif subs_stats == "Standard":
			total_input = 25
		elif subs_stats == "Professional":
			total_input = 100
		user_stats = get_user_stats(email)
		notif = get_notif(email)
		return render_template("social_insta_professional.html", profiles=profiles, image_uploaded_before=image_uploaded_before, uploaded_image="pictures/"+image_name, total_input=total_input, user_stats=user_stats, notif=notif)
	else:
		return render_template("login.html")

@app.route("/social_tube_professional/")
def social_tube_professional():
	email = request.cookies.get("uemail")
	if email != None:
		image_uploaded_before = False
		uid = get_id_email(email)
		image_name = str(uid)+".jpg"
		pathname = "/var/www/FlaskApp/FlaskApp/static/pictures/" + image_name
		if os.path.exists(pathname):
			image_uploaded_before = True
		profiles = fetch_fb(email)

		subs_stats = get_user_stats(email)[1]
		if subs_stats == "Basic":
			total_input = 5
		elif subs_stats == "Trial":
			total_input = 0
		elif subs_stats == "Standard":
			total_input = 25
		elif subs_stats == "Professional":
			total_input = 100
		user_stats = get_user_stats(email)
		notif = get_notif(email)
		return render_template("social_tube_professional.html", profiles=profiles, image_uploaded_before=image_uploaded_before, uploaded_image="pictures/"+image_name, total_input=total_input, user_stats=user_stats, notif=notif)
	else:
		return render_template("login.html")

@app.route("/login/")
def login():
	email = request.cookies.get("uemail")
	if email == None:
		return render_template("login.html")
	else:
		#return render_template("dashboard.html")
		return render_template("login.html")

@app.route("/recoverpw/")
def recoverpw():
	email = request.cookies.get("uemail")
	if email == None:
		return render_template("recoverpw.html")
	else:
		return render_template("dashboard.html")

@app.route("/register/")
def register():
	email = request.cookies.get("uemail")
	if email == None:
		return render_template("register.html")
	else:
		image_uploaded_before = False
		uid = get_id_email(email)
		image_name = str(uid)+".jpg"
		pathname = "/var/www/FlaskApp/FlaskApp/static/pictures/" + image_name
		if os.path.exists(pathname):
			image_uploaded_before = True
		db_results = fetch_all_single_record(email)
		last_five = get_last_five_days()
		foll_media = followers_by_media([db_results["fbs1tf"], db_results["tws1tf"], db_results["ins1tf"]])
		owner_profile = [db_results["fbs1"], millify(db_results["fbs1tf"], precision=2), millify(db_results["fbs1tp"], precision=2), str(get_random_engmt())+"%", db_results["tws1"], millify(db_results["tws1tf"], precision=2), millify(db_results["tws1tp"], precision=2), str(get_random_engmt())+"%", db_results["ins1"], millify(db_results["ins1tf"], precision=2), millify(db_results["ins1tp"], precision=2), str(get_random_engmt())+"%", db_results["tbs1"], millify(db_results["tbs1tf"], precision=2), millify(db_results["tbs1tp"], precision=2), str(get_random_engmt())+"%"]
		#self_stats = [millify(db_results["fbs1tf"]), millify(db_results["tws1tf"]), millify(db_results["ins1tf"]), millify(db_results["tbs1tf"])]
		self_stats = [millify(db_results["fbs1tf"], precision=2), millify(db_results["tws1tf"], precision=2), millify(db_results["ins1tf"], precision=2), millify(db_results["tbs1tf"], precision=2)]
		growth = []
		growth.extend(str_to_lst(db_results["fbs1tg"]))
		growth.extend(str_to_lst(db_results["tws1tg"]))
		growth.extend(str_to_lst(db_results["ins1tg"]))
		subs_stats = get_user_stats(email)[1]
		if subs_stats == "Basic":
			total_input = 5
		elif subs_stats == "Trial":
			total_input = 0
		elif subs_stats == "Standard":
			total_input = 25
		elif subs_stats == "Professional":
			total_input = 100
		return (render_template("dashboard.html", self_stats=self_stats, foll_media=foll_media, owner_profile=owner_profile, last_five=last_five, growth=growth, image_uploaded_before=image_uploaded_before, uploaded_image="pictures/"+image_name, total_input=total_input))

@app.route("/verify/", methods=["post", "get"])
def verify():
	email = request.form["email"]
	password = request.form["password"]
	if check_user_login(email, password) == 1:
		image_uploaded_before = False
		uid = get_id_email(email)
		image_name = str(uid)+".jpg"
		pathname = "/var/www/FlaskApp/FlaskApp/static/pictures/" + image_name
		if os.path.exists(pathname):
			image_uploaded_before = True
		db_results = fetch_all_single_record(email)
		last_five = get_last_five_days()
		foll_media = followers_by_media([db_results["fbs1tf"], db_results["tws1tf"], db_results["ins1tf"]])
		### check millify bug here
		print("-------")
		print(db_results["fbs1tf"])
		millify(db_results["fbs1tf"], precision=2)
		millify(db_results["fbs1tp"], precision=2)
		print("-------")
		print(db_results["fbs1tp"])
		millify(db_results["tws1tf"], precision=2)
		print("-------")
		print(db_results["tws1tf"])
		millify(db_results["tws1tp"], precision=2)
		print("-------")
		print(db_results["tws1tp"])
		millify(db_results["ins1tf"], precision=2)
		millify(db_results["ins1tp"], precision=2)

		owner_profile = [db_results["fbs1"], millify(db_results["fbs1tf"], precision=2), millify(db_results["fbs1tp"], precision=2), str(get_random_engmt())+"%", db_results["tws1"], millify(db_results["tws1tf"], precision=2), millify(db_results["tws1tp"], precision=2), str(get_random_engmt())+"%", db_results["ins1"], millify(db_results["ins1tf"], precision=2), millify(db_results["ins1tp"], precision=2), str(get_random_engmt())+"%", db_results["tbs1"], millify(db_results["tbs1tf"], precision=2), millify(db_results["tbs1tp"], precision=2), str(get_random_engmt())+"%"]
		#self_stats = [millify(db_results["fbs1tf"]), millify(db_results["tws1tf"]), millify(db_results["ins1tf"]), millify(db_results["tbs1tf"])]
		self_stats = [millify(db_results["fbs1tf"], precision=2), millify(db_results["tws1tf"], precision=2), millify(db_results["ins1tf"], precision=2), millify(db_results["tbs1tf"], precision=2)]
		growth = []
		growth.extend(str_to_lst(db_results["fbs1tg"]))
		growth.extend(str_to_lst(db_results["tws1tg"]))
		growth.extend(str_to_lst(db_results["ins1tg"]))
		user_stats = get_user_stats(email)
		if user_stats[3] < 0:
			return redirect(url_for("index"))
		subs_stats = get_user_stats(email)[1]
		if subs_stats == "Basic":
			total_input = 5
		elif subs_stats == "Trial":
			total_input = 0
		elif subs_stats == "Standard":
			total_input = 25
		elif subs_stats == "Professional":
			total_input = 100
		user_stats = get_user_stats(email)
		notif = get_notif(email)
		resp =  make_response(render_template("dashboard.html", self_stats=self_stats, foll_media=foll_media, owner_profile=owner_profile, last_five=last_five, growth=growth, user_stats=user_stats, image_uploaded_before=image_uploaded_before, uploaded_image="pictures/"+image_name, total_input=total_input, notif=notif))
		resp.set_cookie("uemail", email)
		return resp
	else:
		return render_template("login_fallback.html")
	return "user checked"

@app.route("/add_user/", methods=["post", "get"])
def add_user():
	email = request.form["email"]
	password = request.form["password"]
	resp_user_check = check_user(email)
	if resp_user_check == 0:
		rndm = get_random()
		day_started = str(int(time()))
		insert_user(email, password, rndm, day_started)
		email = str(email)
		password = str(password)
		rndm = str(rndm)
		str_0 = "https://socialmine.net/email_verify?email={0}&code={1}".format(email, rndm)
		send_verify_email(email, str_0)
		return render_template("register_fallback.html")
	else:
		return render_template("register_fallback.html")

@app.route("/email_verify", methods=["post", "get"])
def email_verify():
	email = str(request.args.get("email"))
	code = str(request.args.get("code"))
	if check_done(email, code) == 1:
		update_done(email)
		resp = make_response(render_template("dashboard.html"))
		resp.set_cookie("uemail", email)
		return resp
	else:
		return render_template("login.html")

@app.route("/recover/", methods=["post", "get"])
def recover():
	email = str(request.form["email"])
	if get_pass(str(email)) != 0:
		passwd = str(get_pass(email))
		str_01 = "Email: " + email + "\n" + "Password: " + passwd
		sending_mail_forget(email, str_01)
		return render_template("login.html")
	else:
		return render_template("login.html")
@app.route("/logout/")
def logout():
	resp = make_response(render_template("login.html"))
	resp.delete_cookie("uemail")
	return resp

@app.route("/check_cookie/")
def check_cookie():
	uemail = request.cookies.get("uemail")
	return ("uemail: {0}".format(uemail))

@app.route("/rt_update_fb/", methods=["post", "get"])
def rt_update_fb():
	uemail = request.cookies.get("uemail")
	fbs1 = str(request.form["fbs1"]).replace("@", "")
	fbc1 = str(request.form["fbc1"]).replace("@", "")
	fbc2 = str(request.form["fbc2"]).replace("@", "")
	fbc3 = str(request.form["fbc3"]).replace("@", "")
	fbc4 = str(request.form["fbc4"]).replace("@", "")
	fbc5 = str(request.form["fbc5"]).replace("@", "")

	fbs1tf, fbs1tp, fbs1tg = follower_growth_facebook(fbs1)
	fbs1tg = handle_array(str(fbs1tg))
	update_self_fb_params(uemail, fbs1tf, fbs1tp, fbs1tg)

	fbc1tf, fbc1tp, fbc1tg = follower_growth_facebook(fbc1)
	fbc1tg = handle_array(str(fbc1tg))
	update_comp_fb_params(uemail, fbc1tf, fbc1tp, fbc1tg)

	update_fb(fbs1, fbc1, fbc2, fbc3, fbc4, fbc5, uemail)

	fbc2tf, fbc2tp, temp = follower_growth_facebook(fbc2)
	fbc3tf, fbc3tp, temp = follower_growth_facebook(fbc3)
	fbc4tf, fbc4tp, temp = follower_growth_facebook(fbc4)
	fbc5tf, fbc5tp, temp = follower_growth_facebook(fbc5)

	update_fb_comp2(fbc2tf, fbc2tp, fbc3tf, fbc3tp, fbc4tf, fbc4tp, fbc5tf, fbc5tp, uemail)

	fbcon_total_likes, fbcon_total_talking, fbcon_fb_grade, fbcon_fb_like_rank, fbcon_fb_talk_rank, fbcon_page_description, fbcon_page_grade, fbcon_likes_rank, fbcon_talking_about_rank = content_analysis_facebook(fbs1)

	update_fbcomp(fbcon_total_likes, fbcon_total_talking, fbcon_fb_grade, fbcon_fb_like_rank, fbcon_fb_talk_rank, fbcon_page_description, fbcon_page_grade, fbcon_likes_rank, fbcon_talking_about_rank, uemail)

	return redirect(url_for("social_fb"))

@app.route("/rt_update_tw/", methods=["post", "get"])
def rt_update_tw():
	uemail = request.cookies.get("uemail")
	tws1 = str(request.form["tws1"]).replace("@", "")
	twc1 = str(request.form["twc1"]).replace("@", "")
	twc2 = str(request.form["twc2"]).replace("@", "")
	twc3 = str(request.form["twc3"]).replace("@", "")
	twc4 = str(request.form["twc4"]).replace("@", "")
	twc5 = str(request.form["twc5"]).replace("@", "")

	tws1tf, tws1tp, tws1tg = follower_growth_twitter(tws1)
	tws1tg = handle_array(str(tws1tg))
	update_self_tw_params(uemail, tws1tf, tws1tp, tws1tg)

	twc1tf, twc1tp, twc1tg = follower_growth_twitter(twc1)
	twc1tg = handle_array(str(twc1tg))
	update_comp_tw_params(uemail, twc1tf, twc1tp, twc1tg)

	twc2tf, twc2tp, temp = follower_growth_twitter(twc2)
	twc3tf, twc3tp, temp = follower_growth_twitter(twc3)
	twc4tf, twc4tp, temp = follower_growth_twitter(twc4)
	twc5tf, twc5tp, temp = follower_growth_twitter(twc5)

	update_tw_comp2(twc2tf, twc2tp, twc3tf, twc3tp, twc4tf, twc4tp, twc5tf, twc5tp, uemail)

	update_tw(tws1, twc1, twc2, twc3, twc4, twc5, uemail)

	twcon_total_retweet, twcon_total_reply, twcon_total_mentions, twcon_total_hashtags, twcon_total_links, twcon_usernames_count, twcon_hashtags_count, twcon_total_tweets, twcon_total_following, twcon_total_followers = content_analysis_twitter(tws1)
	twcon_usernames_count = str(twcon_usernames_count).replace("'", "\\'")
	twcon_hashtags_count = str(twcon_hashtags_count).replace("'", "\\'")

	update_twcomp(twcon_total_retweet, twcon_total_reply, twcon_total_mentions, twcon_total_hashtags, twcon_total_links, twcon_usernames_count, twcon_hashtags_count, twcon_total_tweets, twcon_total_following, twcon_total_followers, uemail)

	return redirect(url_for("social_tw"))

@app.route("/rt_update_in/", methods=["post", "get"])
def rt_update_in():
	uemail = request.cookies.get("uemail")
	ins1 = str(request.form["ins1"]).replace("@", "")
	inc1 = str(request.form["inc1"]).replace("@", "")
	inc2 = str(request.form["inc2"]).replace("@", "")
	inc3 = str(request.form["inc3"]).replace("@", "")
	inc4 = str(request.form["inc4"]).replace("@", "")
	inc5 = str(request.form["inc5"]).replace("@", "")

	ins1tf, ins1tp, ins1tg = follower_growth_insta(ins1)
	ins1tg = handle_array(str(ins1tg))
	update_self_in_params(uemail, ins1tf, ins1tp, ins1tg)

	inc1tf, inc1tp, inc1tg = follower_growth_insta(inc1)
	inc1tg = handle_array(str(inc1tg))
	update_comp_in_params(uemail, inc1tf, inc1tp, inc1tg)

	inc2tf, inc2tp, temp = follower_growth_insta(inc2)
	inc3tf, inc3tp, temp = follower_growth_insta(inc3)
	inc4tf, inc4tp, temp = follower_growth_insta(inc4)
	inc5tf, inc5tp, temp = follower_growth_insta(inc5)

	update_in_comp2(inc2tf, inc2tp, inc3tf, inc3tp, inc4tf, inc4tp, inc5tf, inc5tp, uemail)

	update_in(ins1, inc1, inc2, inc3, inc4, inc5, uemail)

	instacon_total_followers, instacon_total_followees, instacon_mediacount, instacon_userid, instacon_biography, instacon_full_name, instacon_external_url, instacon_has_public_story, instacon_has_viewable_story, instacon_is_private, instacon_is_verified, instacon_profile_pic_url, instacon_total_likes, instacon_total_comments, instacon_hashtags, instacon_mentions = content_analysis_instaloader(ins1)

	instacon_hashtags = str(instacon_hashtags).replace("'", "\\'")
	instacon_mentions = str(instacon_mentions).replace("'", "\\'")

	update_instacomp(instacon_total_followers, instacon_total_followees, instacon_mediacount, instacon_userid, instacon_biography, instacon_full_name, instacon_external_url, instacon_has_public_story, instacon_has_viewable_story, instacon_is_private, instacon_is_verified, instacon_profile_pic_url, instacon_total_likes, instacon_total_comments, instacon_hashtags, instacon_mentions, uemail)

	return redirect(url_for("social_insta"))

@app.route("/rt_update_tb/", methods=["post", "get"])
def rt_update_tb():
	uemail = request.cookies.get("uemail")
	tbs1 = str(request.form["tbs1"]).replace("@", "")
	tbc1 = str(request.form["tbc1"]).replace("@", "")
	tbc2 = str(request.form["tbc2"]).replace("@", "")
	tbc3 = str(request.form["tbc3"]).replace("@", "")
	tbc4 = str(request.form["tbc4"]).replace("@", "")
	tbc5 = str(request.form["tbc5"]).replace("@", "")

	tbs1tf, tbs1tp = follower_growth_tube(tbs1)

	update_self_tb_params(uemail, tbs1tf, tbs1tp, 0)

	tbc1tf, tbc1tp = follower_growth_tube(tbc1)

	update_comp_tb_params(uemail, tbc1tf, tbc1tp, 0)

	tbc2tf, tbc2tp = follower_growth_tube(tbc2)
	tbc3tf, tbc3tp = follower_growth_tube(tbc3)
	tbc4tf, tbc4tp = follower_growth_tube(tbc4)
	tbc5tf, tbc5tp = follower_growth_tube(tbc5)

	update_tb_comp2(tbc2tf, tbc2tp, tbc3tf, tbc3tp, tbc4tf, tbc4tp, tbc5tf, tbc5tp, uemail)

	update_tb(tbs1, tbc1, tbc2, tbc3, tbc4, tbc5, uemail)

	tubecon_sub_count_rank, tubecon_video_view_rank, tubecon_sub_count, tubecon_channel_title, tubecon_video_view, tubecon_annual_earning_potential, tubecon_channel_category, tubecon_joined_date, tubecon_total_uploaded_videos, tubecon_last_two_week_video_views, tubecon_last_two_week_estimated_earnings, tubecon_last_two_week_video_uploaded = content_analysis_youtube(tbs1)

	update_tubecomp(tubecon_sub_count_rank, tubecon_video_view_rank, tubecon_sub_count, tubecon_channel_title, tubecon_video_view, tubecon_annual_earning_potential, tubecon_channel_category, tubecon_joined_date, tubecon_total_uploaded_videos, tubecon_last_two_week_video_views, tubecon_last_two_week_estimated_earnings, tubecon_last_two_week_video_uploaded, uemail)

	return redirect(url_for("social_tube"))
	
@app.route("/shop/")
def shop():
	amz_recent = amaz_get_recent()
	return render_template("shop/index.html", amz_recent=amz_recent)

@app.route("/shop_search/", methods=["POST", "GET"])
def shop_search():
	product_search = request.args.get("trending_product")
	list_product_title, list_product_price, list_product_link, list_product_image = get_amazon(product_search)
	if len(list_product_title) == 0:
		amz_recent = amaz_get_recent()
		return render_template("shop/index.html", amz_recent=amz_recent)
	else:
		return render_template("shop/shop-fullwidth.html", product_link=list_product_link, product_image=list_product_image, product_title=list_product_title, product_price=list_product_price)

@app.route("/test/")
def test():
	return "test page"

@app.route("/anim/")
def anim():
	return render_template("anim.html")

@app.route("/animtt/")
def animtt():
	return render_template("anim2.html")

@app.route("/stripe/")
def strp():
	return render_template("strp.html", key=stripe_keys["publishable_key"])

@app.route("/charge/", methods=["POST"])
def charge():
	email = request.cookies.get("uemail")
	product = get_product(int(request.json['product']))
	print("print product: " + str(product))
	response = jsonify('error')
	response.status_code = 500
	if product:
		try:
			product = get_product(int(request.json['product']))
			customer = stripe.Customer.create(
				email=email,
				source=request.json['token']
			)
			stripe.Charge.create(
				customer=customer.id,
				amount=product['amount'],
				currency='usd',
				description=product['description']
			)

			product_id = product["id"]
			if product_id == 1:
				upgrade_basic_monthly(email)
			elif product_id == 2:
				upgrade_basic_annually(email)
			elif product_id == 3:
				upgrade_standard_monthly(email)
			elif product_id == 4:
				upgrade_standard_annually(email)
			elif product_id == 5:
				upgrade_professional_monthly(email)
			elif product_id == 6:
				upgrade_professional_annually(email)

		except stripe.error.StripeError:
			return response
	return response

@app.route("/basic_monthly/")
def basic_monthly():
	email = request.cookies.get("uemail")
	if email != None:
		image_uploaded_before = False
		uid = get_id_email(email)
		image_name = str(uid)+".jpg"
		pathname = "/var/www/FlaskApp/FlaskApp/static/pictures/" + image_name
		if os.path.exists(pathname):
			image_uploaded_before = True

		product = products[0]
		if product:
			product["amount_in_dollar"] = product["amount"] / 100
		subs_stats = get_user_stats(email)[1]
		if subs_stats == "Basic":
			total_input = 5
		elif subs_stats == "Trial":
			total_input = 0
		elif subs_stats == "Standard":
			total_input = 25
		elif subs_stats == "Professional":
			total_input = 100
		return render_template("basic_monthly.html", key=stripe_keys["publishable_key"], product=product, image_uploaded_before=image_uploaded_before, uploaded_image="pictures/"+image_name, total_input=total_input)
	else:
		return render_template("login.html")

@app.route("/basic_annually/")
def basic_annually():
	email = request.cookies.get("uemail")
	if email != None:
		image_uploaded_before = False
		uid = get_id_email(email)
		image_name = str(uid)+".jpg"
		pathname = "/var/www/FlaskApp/FlaskApp/static/pictures/" + image_name
		if os.path.exists(pathname):
			image_uploaded_before = True

		product = products[1]
		if product:
			product["amount_in_dollar"] = product["amount"] / 100
		subs_stats = get_user_stats(email)[1]
		if subs_stats == "Basic":
			total_input = 5
		elif subs_stats == "Trial":
			total_input = 0
		elif subs_stats == "Standard":
			total_input = 25
		elif subs_stats == "Professional":
			total_input = 100
		user_stats = get_user_stats(email)
		notif = get_notif(email)
		return render_template("basic_annually.html", key=stripe_keys["publishable_key"], product=product, image_uploaded_before=image_uploaded_before, uploaded_image="pictures/"+image_name, total_input=total_input, user_stats=user_stats, notif=notif)
	else:
		return render_template("login.html")

@app.route("/standard_monthly/")
def standard_monthly():
	email = request.cookies.get("uemail")
	if email != None:
		image_uploaded_before = False
		uid = get_id_email(email)
		image_name = str(uid)+".jpg"
		pathname = "/var/www/FlaskApp/FlaskApp/static/pictures/" + image_name
		if os.path.exists(pathname):
			image_uploaded_before = True

		product = products[2]
		if product:
			product["amount_in_dollar"] = product["amount"] / 100
		subs_stats = get_user_stats(email)[1]
		if subs_stats == "Basic":
			total_input = 5
		elif subs_stats == "Trial":
			total_input = 0
		elif subs_stats == "Standard":
			total_input = 25
		elif subs_stats == "Professional":
			total_input = 100
		user_stats = get_user_stats(email)
		notif = get_notif(email)
		return render_template("standard_monthly.html", key=stripe_keys["publishable_key"], product=product, image_uploaded_before=image_uploaded_before, uploaded_image="pictures/"+image_name, total_input=total_input, user_stats=user_stats, notif=notif)
	else:
		return render_template("login.html")

@app.route("/standard_annually/")
def standard_annually():
	email = request.cookies.get("uemail")
	if email != None:
		image_uploaded_before = False
		uid = get_id_email(email)
		image_name = str(uid)+".jpg"
		pathname = "/var/www/FlaskApp/FlaskApp/static/pictures/" + image_name
		if os.path.exists(pathname):
			image_uploaded_before = True

		product = products[3]
		if product:
			product["amount_in_dollar"] = product["amount"] / 100
		subs_stats = get_user_stats(email)[1]
		if subs_stats == "Basic":
			total_input = 5
		elif subs_stats == "Trial":
			total_input = 0
		elif subs_stats == "Standard":
			total_input = 25
		elif subs_stats == "Professional":
			total_input = 100
		user_stats = get_user_stats(email)
		notif = get_notif(email)
		return render_template("standard_annually.html", key=stripe_keys["publishable_key"], product=product, image_uploaded_before=image_uploaded_before, uploaded_image="pictures/"+image_name, total_input=total_input, user_stats=user_stats, notif=notif)
	else:
		return render_template("login.html")

@app.route("/professional_monthly/")
def professional_monthly():
	email = request.cookies.get("uemail")
	if email != None:
		image_uploaded_before = False
		uid = get_id_email(email)
		image_name = str(uid)+".jpg"
		pathname = "/var/www/FlaskApp/FlaskApp/static/pictures/" + image_name
		if os.path.exists(pathname):
			image_uploaded_before = True

		product = products[4]
		if product:
			product["amount_in_dollar"] = product["amount"] / 100
		subs_stats = get_user_stats(email)[1]
		if subs_stats == "Basic":
			total_input = 5
		elif subs_stats == "Trial":
			total_input = 0
		elif subs_stats == "Standard":
			total_input = 25
		elif subs_stats == "Professional":
			total_input = 100
		user_stats = get_user_stats(email)
		notif = get_notif(email)
		return render_template("professional_monthly.html", key=stripe_keys["publishable_key"], product=product, image_uploaded_before=image_uploaded_before, uploaded_image="pictures/"+image_name, total_input=total_input, user_stats=user_stats, notif=notif)
	else:
		return render_template("login.html")

@app.route("/professional_annually/")
def professional_annually():
	email = request.cookies.get("uemail")
	if email != None:
		image_uploaded_before = False
		uid = get_id_email(email)
		image_name = str(uid)+".jpg"
		pathname = "/var/www/FlaskApp/FlaskApp/static/pictures/" + image_name
		if os.path.exists(pathname):
			image_uploaded_before = True

		product = products[5]
		if product:
			product["amount_in_dollar"] = product["amount"] / 100
		subs_stats = get_user_stats(email)[1]
		if subs_stats == "Basic":
			total_input = 5
		elif subs_stats == "Trial":
			total_input = 0
		elif subs_stats == "Standard":
			total_input = 25
		elif subs_stats == "Professional":
			total_input = 100
		user_stats = get_user_stats(email)
		notif = get_notif(email)
		return render_template("professional_annually.html", key=stripe_keys["publishable_key"], product=product, image_uploaded_before=image_uploaded_before, uploaded_image="pictures/"+image_name, total_input=total_input, user_stats=user_stats, notif=notif)
	else:
		return render_template("login.html")

@app.route("/file_success/")
def file_success():
	email = request.cookies.get("uemail")
	if request.method == 'POST': 
		f = request.files['file'] 
		f.save(email+".jpg") 
		return redirect(url_for("dashboard"))

@app.route("/pdff/<name>/<location>")
def pdff(name, location):
	rendered = render_template("pdf_template.html", name=name, location=location)

	css = ['/var/www/FlaskApp/FlaskApp/main.css']

	pdf = pdfkit.from_string(rendered, False, css=css)

	response = make_response(pdf)
	response.headers['Content-Type'] = "application/pdf"
	response.headers['Content-Disposition'] = "inline; filename=report.pdf"

	return response

@app.route("/boot/")
def boot():
	email = request.cookies.get("uemail")
	if email != None:

		rendered = render_template("boot.html")

		pdf = pdfkit.from_string(rendered, False)

		response = make_response(pdf)
		response.headers['Content-Type'] = "application/pdf"
		response.headers['Content-Disposition'] = "inline; filename=report.pdf"

		return response

	else:
		return render_template("login.html")

@app.route("/tube_generate_report/")
def tube_generate_report():
	email = request.cookies.get("uemail")
	if email != None:
		db_results = fetch_tubecon(email)
		tubecon = [db_results["tubecon_sub_count_rank"], db_results["tubecon_video_view_rank"], db_results["tubecon_sub_count"], db_results["tubecon_channel_title"], db_results["tubecon_video_view"], db_results["tubecon_annual_earning_potential"], db_results["tubecon_channel_category"], db_results["tubecon_joined_date"], db_results["tubecon_total_uploaded_videos"], db_results["tubecon_last_two_week_video_views"], db_results["tubecon_last_two_week_estimated_earnings"], str(abs(int(db_results["tubecon_last_two_week_video_uploaded"])))]

		db_results = fetch_tbcomp(email)

		db_results["tbs1tf"] = millify(db_results["tbs1tf"], precision=2)
		db_results["tbs1tp"] = millify(db_results["tbs1tp"], precision=2)
		db_results["tbc1tf"] = millify(db_results["tbc1tf"], precision=2)
		db_results["tbc1tp"] = millify(db_results["tbc1tp"], precision=2)
		db_results["tbc2tf"] = millify(db_results["tbc2tf"], precision=2)
		db_results["tbc2tp"] = millify(db_results["tbc2tp"], precision=2)
		db_results["tbc3tf"] = millify(db_results["tbc3tf"], precision=2)
		db_results["tbc3tp"] = millify(db_results["tbc3tp"], precision=2)
		db_results["tbc4tf"] = millify(db_results["tbc4tf"], precision=2)
		db_results["tbc4tp"] = millify(db_results["tbc4tp"], precision=2)
		db_results["tbc5tf"] = millify(db_results["tbc5tf"], precision=2)
		db_results["tbc5tp"] = millify(db_results["tbc5tp"], precision=2)
		db_results["tbs1engmt"] = str(int(db_results["tbs1engmt"]))+"%"

		rendered = render_template("tube_generate_report.html", db_results=db_results, tubecon=tubecon)

		pdf = pdfkit.from_string(rendered, False)

		response = make_response(pdf)
		response.headers['Content-Type'] = "application/pdf"
		response.headers['Content-Disposition'] = "inline; filename=YouTube_Report(SocialMine.net).pdf"

		return response
	else:
		return render_template("login.html")

@app.route("/tw_generate_report/")
def tw_generate_report():
	email = request.cookies.get("uemail")
	if email != None:
		db_results = fetch_all_single_record(email)
		foll_media = [millify(db_results["tws1tf"], precision=2), millify(db_results["tws1tp"], precision=2), str(get_random_engmt())+"%"]

		profile_data = []
		profile_data.append("@"+db_results["tws1"])
		profile_data.append("@"+db_results["twc1"])
		profile_data.append("@"+db_results["twc2"])
		profile_data.append("@"+db_results["twc3"])
		profile_data.append("@"+db_results["twc4"])
		profile_data.append("@"+db_results["twc5"])
		profile_data.append(millify(db_results["tws1tf"], precision=2))
		profile_data.append(millify(db_results["twc1tf"], precision=2))
		profile_data.append(millify(db_results["twc2tf"], precision=2))
		profile_data.append(millify(db_results["twc3tf"], precision=2))
		profile_data.append(millify(db_results["twc4tf"], precision=2))
		profile_data.append(millify(db_results["twc5tf"], precision=2))
		profile_data.append(millify(db_results["tws1tp"], precision=2))
		profile_data.append(millify(db_results["twc1tp"], precision=2))
		profile_data.append(millify(db_results["twc2tp"], precision=2))
		profile_data.append(millify(db_results["twc3tp"], precision=2))
		profile_data.append(millify(db_results["twc4tp"], precision=2))
		profile_data.append(millify(db_results["twc5tp"], precision=2))
		profile_data.append(str(get_random_engmt())+"%")
		profile_data.append(str(get_random_engmt())+"%")
		profile_data.append(str(get_random_engmt())+"%")
		profile_data.append(str(get_random_engmt())+"%")
		profile_data.append(str(get_random_engmt())+"%")
		profile_data.append(str(get_random_engmt())+"%")

		db_results = fetch_twcon(email)
		tw_cont = [db_results["twcon_total_retweet"], db_results["twcon_total_reply"], db_results["twcon_total_mentions"], db_results["twcon_total_hashtags"], db_results["twcon_total_links"], db_results["twcon_total_tweets"], db_results["twcon_total_following"], db_results["twcon_total_followers"]]

		twcon_usernames_count = eval(db_results["twcon_usernames_count"])
		twcon_hashtags_count = eval(db_results["twcon_hashtags_count"])
		twcon_new_hashtags = []
		for x in twcon_hashtags_count:
			if len(x[0]) < 15:
				twcon_new_hashtags.append(x)
		username_count = len(twcon_usernames_count)
		hashtag_count = len(twcon_new_hashtags)
		tw_con = [twcon_usernames_count, twcon_new_hashtags, username_count, hashtag_count]

		rendered = render_template("tw_generate_report.html", foll_media=foll_media, profile_data=profile_data, tw_con=tw_con, tw_cont=tw_cont)

		pdf = pdfkit.from_string(rendered, False)

		response = make_response(pdf)
		response.headers['Content-Type'] = "application/pdf"
		response.headers['Content-Disposition'] = "inline; filename=Twitter_Report(SocialMine.net).pdf"

		return response
	else:
		return render_template("login.html")

@app.route("/fb_generate_report/")
def fb_generate_report():
	email = request.cookies.get("uemail")
	if email != None:

		db_results = fetch_all_single_record(email)
		foll_media = [millify(db_results["fbs1tf"], precision=2), millify(db_results["fbs1tp"], precision=2), str(get_random_engmt())+"%"]

		profile_data = []
		profile_data.append("@"+db_results["fbs1"])
		profile_data.append("@"+db_results["fbc1"])
		profile_data.append("@"+db_results["fbc2"])
		profile_data.append("@"+db_results["fbc3"])
		profile_data.append("@"+db_results["fbc4"])
		profile_data.append("@"+db_results["fbc5"])
		profile_data.append(millify(db_results["fbs1tf"], precision=2))
		profile_data.append(millify(db_results["fbc1tf"], precision=2))
		profile_data.append(millify(db_results["fbc2tf"], precision=2))
		profile_data.append(millify(db_results["fbc3tf"], precision=2))
		profile_data.append(millify(db_results["fbc4tf"], precision=2))
		profile_data.append(millify(db_results["fbc5tf"], precision=2))
		profile_data.append(millify(db_results["fbs1tp"], precision=2))
		profile_data.append(millify(db_results["fbc1tp"], precision=2))
		profile_data.append(millify(db_results["fbc2tp"], precision=2))
		profile_data.append(millify(db_results["fbc3tp"], precision=2))
		profile_data.append(millify(db_results["fbc4tp"], precision=2))
		profile_data.append(millify(db_results["fbc5tp"], precision=2))
		profile_data.append(str(get_random_engmt())+"%")
		profile_data.append(str(get_random_engmt())+"%")
		profile_data.append(str(get_random_engmt())+"%")
		profile_data.append(str(get_random_engmt())+"%")
		profile_data.append(str(get_random_engmt())+"%")
		profile_data.append(str(get_random_engmt())+"%")

		db_results = fetch_fbcon(email)
		fb_con = [db_results["fbcon_total_likes"], db_results["fbcon_total_talking"], db_results["fbcon_fb_grade"], db_results["fbcon_fb_like_rank"], db_results["fbcon_fb_talk_rank"], db_results["fbcon_page_description"], db_results["fbcon_page_grade"], db_results["fbcon_likes_rank"], db_results["fbcon_talking_about_rank"]]

		rendered = render_template("fb_generate_report.html", foll_media=foll_media, profile_data=profile_data, fb_con=fb_con)

		pdf = pdfkit.from_string(rendered, False)

		response = make_response(pdf)
		response.headers['Content-Type'] = "application/pdf"
		response.headers['Content-Disposition'] = "inline; filename=Facebook_Report(SocialMine.net).pdf"

		return response

	else:
		return render_template("login.html")

@app.route("/insta_generate_report/")
def insta_generate_report():
	email = request.cookies.get("uemail")
	if email != None:
		db_results = fetch_all_single_record(email)
		foll_media = [millify(db_results["ins1tf"], precision=2), millify(db_results["ins1tp"], precision=2), str(get_random_engmt())+"%"]

		profile_data = []
		profile_data.append("@"+db_results["ins1"])
		profile_data.append("@"+db_results["inc1"])
		profile_data.append("@"+db_results["inc2"])
		profile_data.append("@"+db_results["inc3"])
		profile_data.append("@"+db_results["inc4"])
		profile_data.append("@"+db_results["inc5"])
		profile_data.append(millify(db_results["ins1tf"], precision=2))
		profile_data.append(millify(db_results["inc1tf"], precision=2))
		profile_data.append(millify(db_results["inc2tf"], precision=2))
		profile_data.append(millify(db_results["inc3tf"], precision=2))
		profile_data.append(millify(db_results["inc4tf"], precision=2))
		profile_data.append(millify(db_results["inc5tf"], precision=2))
		profile_data.append(millify(db_results["ins1tp"], precision=2))
		profile_data.append(millify(db_results["inc1tp"], precision=2))
		profile_data.append(millify(db_results["inc2tp"], precision=2))
		profile_data.append(millify(db_results["inc3tp"], precision=2))
		profile_data.append(millify(db_results["inc4tp"], precision=2))
		profile_data.append(millify(db_results["inc5tp"], precision=2))
		profile_data.append(str(get_random_engmt())+"%")
		profile_data.append(str(get_random_engmt())+"%")
		profile_data.append(str(get_random_engmt())+"%")
		profile_data.append(str(get_random_engmt())+"%")
		profile_data.append(str(get_random_engmt())+"%")
		profile_data.append(str(get_random_engmt())+"%")

		db_results = fetch_instacon(email)
		insta_con = [db_results["instacon_total_followers"], db_results["instacon_total_followees"], db_results["instacon_mediacount"], db_results["instacon_userid"], db_results["instacon_biography"], db_results["instacon_full_name"], db_results["instacon_external_url"], db_results["instacon_has_public_story"], db_results["instacon_has_viewable_story"], db_results["instacon_is_private"], db_results["instacon_is_verified"], db_results["instacon_profile_pic_url"], db_results["instacon_total_likes"], db_results["instacon_total_comments"]]

		db_results = fetch_instacon(email)
		hashtags = eval(db_results["instacon_hashtags"])
		mentions = eval(db_results["instacon_mentions"])
		engmt_hashtag = []
		engmt_mention = []
		len_hashtag = len(hashtags)
		len_mention = len(mentions)
		for x in range(0, len(hashtags)):
			engmt_hashtag.append(str(randint(30, 50))+"%")
		for x in range(0, len(mentions)):
			engmt_mention.append(str(randint(30, 50))+"%")

		rendered = render_template("insta_generate_report.html", foll_media=foll_media, profile_data=profile_data, insta_con=insta_con, hashtags=hashtags, mentions=mentions, engmt_hashtag=engmt_hashtag, engmt_mention=engmt_mention, len_hashtag=len_hashtag, len_mention=len_mention)

		pdf = pdfkit.from_string(rendered, False)

		response = make_response(pdf)
		response.headers['Content-Type'] = "application/pdf"
		response.headers['Content-Disposition'] = "inline; filename=Instagram_Report(SocialMine.net).pdf"

		return response

	else:
		return render_template("login.html")

@app.route("/uploadpics/", methods=["POST"])
def uploadpics():
	email = request.cookies.get("uemail")
	uid = (request.form["uid"])
	image_name = str(uid)+".jpg"
	print("dickhead " + str(image_name))
	pathname = "/var/www/FlaskApp/FlaskApp/static/pictures/" + image_name
	if request.method == "POST":
		if os.path.exists(pathname):
			os.remove(pathname)
		file = request.files["file"]
		file.save(os.path.join(app.config["UPLOAD_FOLDER"], image_name))
		return redirect(url_for("dashboard"))
if __name__ == "__main__":
	app.run(host="0.0.0.0", debug=True, port=80)
