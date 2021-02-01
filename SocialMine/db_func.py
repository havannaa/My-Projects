import mysql.connector
import datetime
import time

def connect():
	mydb = mysql.connector.connect(
		host="localhost",
		user="root",
		passwd="1111",
		database="app"
	)
	return mydb

def execute_query_insert(sql):
	mydb = connect()
	mycursor = mydb.cursor()
	mycursor.execute(sql)
	mydb.commit()

def execute_query_update(sql):
	mydb = connect()
	mycursor = mydb.cursor()
	mycursor.execute(sql)
	mydb.commit()

def execute_query_select(sql):
	mydb = connect()
	mycursor = mydb.cursor()
	mycursor.execute(sql)
	myresult = mycursor.fetchall()
	return myresult

def update_fb(fbs1, fbc1, fbc2, fbc3, fbc4, fbc5, email):
	sql = "UPDATE `user` SET `fbs1` = '{0}', `fbc1` = '{1}', `fbc2` = '{2}', `fbc3` = '{3}', `fbc4` = '{4}', `fbc5` = '{5}' WHERE `user`.`email` = '{6}';".format(fbs1, fbc1, fbc2, fbc3, fbc4, fbc5, email)
	execute_query_update(sql)

def update_fb_comp2(fbc2tf, fbc2tp, fbc3tf, fbc3tp, fbc4tf, fbc4tp, fbc5tf, fbc5tp, email):
	sql = "UPDATE `user` SET `fbc2tf` = '{0}', `fbc2tp` = '{1}', `fbc3tf` = '{2}', `fbc3tp` = '{3}', `fbc4tf` = '{4}', `fbc4tp` = '{5}' , `fbc5tf` = '{6}', `fbc5tp` = '{7}' WHERE `user`.`email` = '{8}';".format(fbc2tf, fbc2tp, fbc3tf, fbc3tp, fbc4tf, fbc4tp, fbc5tf, fbc5tp, email)
	execute_query_update(sql)

def update_tw_comp2(twc2tf, twc2tp, twc3tf, twc3tp, twc4tf, twc4tp, twc5tf, twc5tp, email):
	sql = "UPDATE `user` SET `twc2tf` = '{0}', `twc2tp` = '{1}', `twc3tf` = '{2}', `twc3tp` = '{3}', `twc4tf` = '{4}', `twc4tp` = '{5}' , `twc5tf` = '{6}', `twc5tp` = '{7}' WHERE `user`.`email` = '{8}';".format(twc2tf, twc2tp, twc3tf, twc3tp, twc4tf, twc4tp, twc5tf, twc5tp, email)
	execute_query_update(sql)

def update_in_comp2(inc2tf, inc2tp, inc3tf, inc3tp, inc4tf, inc4tp, inc5tf, inc5tp, email):
	sql = "UPDATE `user` SET `inc2tf` = '{0}', `inc2tp` = '{1}', `inc3tf` = '{2}', `inc3tp` = '{3}', `inc4tf` = '{4}', `inc4tp` = '{5}' , `inc5tf` = '{6}', `inc5tp` = '{7}' WHERE `user`.`email` = '{8}';".format(inc2tf, inc2tp, inc3tf, inc3tp, inc4tf, inc4tp, inc5tf, inc5tp, email)
	execute_query_update(sql)

def update_tb_comp2(tbc2tf, tbc2tp, tbc3tf, tbc3tp, tbc4tf, tbc4tp, tbc5tf, tbc5tp, email):
	sql = "UPDATE `user` SET `tbc2tf` = '{0}', `tbc2tp` = '{1}', `tbc3tf` = '{2}', `tbc3tp` = '{3}', `tbc4tf` = '{4}', `tbc4tp` = '{5}' , `tbc5tf` = '{6}', `tbc5tp` = '{7}' WHERE `user`.`email` = '{8}';".format(tbc2tf, tbc2tp, tbc3tf, tbc3tp, tbc4tf, tbc4tp, tbc5tf, tbc5tp, email)
	execute_query_update(sql)

def update_tw(tws1, twc1, twc2, twc3, twc4, twc5, email):
	sql = "UPDATE `user` SET `tws1` = '{0}', `twc1` = '{1}', `twc2` = '{2}', `twc3` = '{3}', `twc4` = '{4}', `twc5` = '{5}' WHERE `user`.`email` = '{6}';".format(tws1, twc1, twc2, twc3, twc4, twc5, email)
	execute_query_update(sql)

def update_in(ins1, inc1, inc2, inc3, inc4, inc5, email):
	sql = "UPDATE `user` SET `ins1` = '{0}', `inc1` = '{1}', `inc2` = '{2}', `inc3` = '{3}', `inc4` = '{4}', `inc5` = '{5}' WHERE `user`.`email` = '{6}';".format(ins1, inc1, inc2, inc3, inc4, inc5, email)
	execute_query_update(sql)

def update_tb(tbs1, tbc1, tbc2, tbc3, tbc4, tbc5, email):
	sql = "UPDATE `user` SET `tbs1` = '{0}', `tbc1` = '{1}', `tbc2` = '{2}', `tbc3` = '{3}', `tbc4` = '{4}', `tbc5` = '{5}' WHERE `user`.`email` = '{6}';".format(tbs1, tbc1, tbc2, tbc3, tbc4, tbc5, email)
	execute_query_update(sql)

def fetch_self_profiles(email):
	sql = "SELECT fbs1, tws1, ins1, tbs1 FROM `user` WHERE email='{0}'".format(email)
	myresult = list(execute_query_select(sql)[0])
	return myresult

def fetch_comp_profiles(email):
	sql = "SELECT fbc1, twc1, inc1, tbc1 FROM `user` WHERE email='{0}'".format(email)
	myresult = list(execute_query_select(sql)[0])
	return myresult

def fetch_fb(email):
	sql = "SELECT fbs1, fbc1, fbc2, fbc3, fbc4, fbc5 FROM user WHERE email='{0}'".format(email)
	myresult = list(execute_query_select(sql)[0])
	return myresult

def fetch_tw(email):
	sql = "SELECT tws1, twc1, twc2, twc3, twc4, twc5 FROM user WHERE email='{0}'".format(email)
	myresult = list(execute_query_select(sql)[0])
	return myresult

def fetch_in(email):
	sql = "SELECT ins1, inc1, inc2, inc3, inc4, inc5 FROM user WHERE email='{0}'".format(email)
	myresult = list(execute_query_select(sql)[0])
	return myresult

def fetch_tb(email):
	sql = "SELECT tbs1, tbc1, tbc2, tbc3, tbc4, tbc5 FROM user WHERE email='{0}'".format(email)
	myresult = list(execute_query_select(sql)[0])
	return myresult

def insert_user(email, passwd, code, day_started):
	sql = "INSERT INTO `user` (`id`, `email`, `passwd`, `code`, `done`, `user_type`, `day_started`, `package_length`, `fbs1`, `fbs1tf`, `fbs1tp`, `fbs1tg`, `fbc1`, `fbc1tf`, `fbc1tp`, `fbc1tg`, `fbc2`, `fbc3`, `fbc4`, `fbc5`, `tws1`, `tws1tf`, `tws1tp`, `tws1tg`, `twc1`, `twc1tf`, `twc1tp`, `twc1tg`, `twc2`, `twc3`, `twc4`, `twc5`, `ins1`, `ins1tf`, `ins1tp`, `ins1tg`, `inc1`, `inc1tf`, `inc1tp`, `inc1tg`, `inc2`, `inc3`, `inc4`, `inc5`, `tbs1`, `tbs1tf`, `tbs1tp`, `tbs1tg`, `tbc1`, `tbc1tf`, `tbc1tp`, `tbc1tg`, `tbc2`, `tbc3`, `tbc4`, `tbc5`, `fbc2tf`, `fbc2tp`, `fbc3tf`, `fbc3tp`, `fbc4tf`, `fbc4tp`, `fbc5tf`, `fbc5tp`, `twc2tf`, `twc2tp`, `twc3tf`, `twc3tp`, `twc4tf`, `twc4tp`, `twc5tf`, `twc5tp`, `inc2tf`, `inc2tp`, `inc3tf`, `inc3tp`, `inc4tf`, `inc4tp`, `inc5tf`, `inc5tp`, `tbc2tf`, `tbc2tp`, `tbc3tf`, `tbc3tp`, `tbc4tf`, `tbc4tp`, `tbc5tf`, `tbc5tp`, `fbcon_total_likes`, `fbcon_total_talking`, `fbcon_fb_grade`, `fbcon_fb_like_rank`, `fbcon_fb_talk_rank`, `fbcon_page_description`, `fbcon_page_grade`, `fbcon_likes_rank`, `fbcon_talking_about_rank`, `twcon_total_retweet`, `twcon_total_reply`, `twcon_total_mentions`, `twcon_total_hashtags`, `twcon_total_links`, `twcon_usernames_count`, `twcon_hashtags_count`, `twcon_total_tweets`, `twcon_total_following`, `twcon_total_followers`, `instacon_total_followers`, `instacon_total_followees`, `instacon_mediacount`, `instacon_userid`, `instacon_biography`, `instacon_full_name`, `instacon_external_url`, `instacon_has_public_story`, `instacon_has_viewable_story`, `instacon_is_private`, `instacon_is_verified`, `instacon_profile_pic_url`, `instacon_total_likes`, `instacon_total_comments`, `instacon_hashtags`, `instacon_mentions`, `tubecon_sub_count_rank`, `tubecon_video_view_rank`, `tubecon_sub_count`, `tubecon_channel_title`, `tubecon_video_view`, `tubecon_annual_earning_potential`, `tubecon_channel_category`, `tubecon_joined_date`, `tubecon_total_uploaded_videos`, `tubecon_last_two_week_video_views`, `tubecon_last_two_week_estimated_earnings`, `tubecon_last_two_week_video_uploaded`) VALUES (NULL, '{0}', '{1}', '{2}', '0', '1', '{3}', '5', 'null', '0', '0', '0:0:0:0:0', 'null', '0', '0', '0:0:0:0:0', 'null', 'null', 'null', 'null', 'null', '0', '0', '0:0:0:0:0', 'null', '0', '0', '0:0:0:0:0', 'null', 'null', 'null', 'null', 'null', '0', '0', '0:0:0:0:0', 'null', '0', '0', '0:0:0:0:0', 'null', 'null', 'null', 'null', 'null', '0', '0', '0', 'null', '0', '0', '0', 'null', 'null', 'null', 'null', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '[(\\'null\\', 0)]', '[(\\'null\\', \\'0%\\')]', '0', '0', '0', '0', '0', '0', '0', 'null', 'null', 'null', 'null', 'False', 'False', 'False', 'null', '0', '0', '[\\'null\\']', '[\\'null\\']', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0');".format(email, passwd, code, day_started)
	print(sql)
	execute_query_insert(sql)

def check_done(email, code):
	sql = "SELECT `id`, `done` FROM `user` WHERE email='{0}' AND code={1}".format(email, code)
	myresult = int(list(execute_query_select(sql)[0])[1])
	return myresult

def get_pass(email):
	sql = "SELECT `id`, `passwd` FROM `user` WHERE email='{0}'".format(email)
	myresult = list(execute_query_select(sql)[0])[1]
	return myresult

def update_done(email):
	sql = "UPDATE `user` SET `done` = '1' WHERE `user`.`email` = '{0}';".format(email)
	execute_query_update(sql)

def check_user(email):
	sql = "SELECT * FROM user WHERE email='{0}'".format(email)
	myresult = execute_query_select(sql)
	return len(myresult)

def check_user_login(email, passwd):
	sql = "SELECT * FROM user WHERE `email`='{0}' AND passwd='{1}'".format(email, passwd)
	myresult = execute_query_select(sql)
	return len(myresult)

def update_self_fb_params(email, fbs1tf, fbs1tp, fbs1tg):
	sql = "UPDATE `user` SET `fbs1tf` = '{0}', `fbs1tp` = '{1}', `fbs1tg` = '{2}' WHERE `user`.`email` = '{3}';".format(fbs1tf, fbs1tp, fbs1tg, email)
	execute_query_update(sql)

def update_comp_fb_params(email, fbc1tf, fbc1tp, fbc1tg):
	sql = "UPDATE `user` SET `fbc1tf` = '{0}', `fbc1tp` = '{1}', `fbc1tg` = '{2}' WHERE `user`.`email` = '{3}';".format(fbc1tf, fbc1tp, fbc1tg, email)
	execute_query_update(sql)

def update_self_tw_params(email, tws1tf, tws1tp, tws1tg):
	sql = "UPDATE `user` SET `tws1tf` = '{0}', `tws1tp` = '{1}', `tws1tg` = '{2}' WHERE `user`.`email` = '{3}';".format(tws1tf, tws1tp, tws1tg, email)
	execute_query_update(sql)

def update_comp_tw_params(email, twc1tf, twc1tp, twc1tg):
	sql = "UPDATE `user` SET `twc1tf` = '{0}', `twc1tp` = '{1}', `twc1tg` = '{2}' WHERE `user`.`email` = '{3}';".format(twc1tf, twc1tp, twc1tg, email)
	execute_query_update(sql)

def update_self_in_params(email, ins1tf, ins1tp, ins1tg):
	sql = "UPDATE `user` SET `ins1tf` = '{0}', `ins1tp` = '{1}', `ins1tg` = '{2}' WHERE `user`.`email` = '{3}';".format(ins1tf, ins1tp, ins1tg, email)
	execute_query_update(sql)

def update_comp_in_params(email, inc1tf, inc1tp, inc1tg):
	sql = "UPDATE `user` SET `inc1tf` = '{0}', `inc1tp` = '{1}', `inc1tg` = '{2}' WHERE `user`.`email` = '{3}';".format(inc1tf, inc1tp, inc1tg, email)
	execute_query_update(sql)

def update_self_tb_params(email, tbs1tf, tbs1tp, tbs1tg):
	sql = "UPDATE `user` SET `tbs1tf` = '{0}', `tbs1tp` = '{1}', `tbs1tg` = '{2}' WHERE `user`.`email` = '{3}';".format(tbs1tf, tbs1tp, tbs1tg, email)
	execute_query_update(sql)

def update_comp_tb_params(email, tbc1tf, tbc1tp, tbc1tg):
	sql = "UPDATE `user` SET `tbc1tf` = '{0}', `tbc1tp` = '{1}', `tbc1tg` = '{2}' WHERE `user`.`email` = '{3}';".format(tbc1tf, tbc1tp, tbc1tg, email)
	execute_query_update(sql)

def update_comp_fb(fbc2tf, fbc2tp, fbc3tf, fbc3tp, fbc4tf, fbc4tp, fbc5tf, fbc5tp, email):
	sql = "UPDATE `user` SET `fbc2tf` = '{0}', `fbc2tp` = '{1}', `fbc3tf` = '{2}', `fbc3tp` = '{3}', `fbc4tf` = '{4}', `fbc4tp` = '{5}', `fbc5tf` = '{6}', `fbc5tp` = '{7}' WHERE `user`.`email` = '{8}';".format(fbc2tf, fbc2tp, fbc3tf, fbc3tp, fbc4tf, fbc4tp, fbc5tf, fbc5tp, email)
	execute_query_update(sql)

def update_comp_tw(twc2tf, twc2tp, twc3tf, twc3tp, twc4tf, twc4tp, twc5tf, twc5tp, email):
	sql = "UPDATE `user` SET `twc2tf` = '{0}', `twc2tp` = '{1}', `twc3tf` = '{2}', `twc3tp` = '{3}', `twc4tf` = '{4}', `twc4tp` = '{5}', `twc5tf` = '{6}', `twc5tp` = '{7}' WHERE `user`.`email` = '{8}';".format(twc2tf, twc2tp, twc3tf, twc3tp, twc4tf, twc4tp, twc5tf, twc5tp, email)
	execute_query_update(sql)

def update_comp_in(inc2tf, inc2tp, inc3tf, inc3tp, inc4tf, inc4tp, inc5tf, inc5tp, email):
	sql = "UPDATE `user` SET `inc2tf` = '{0}', `inc2tp` = '{1}', `inc3tf` = '{2}', `inc3tp` = '{3}', `inc4tf` = '{4}', `inc4tp` = '{5}', `inc5tf` = '{6}', `inc5tp` = '{7}' WHERE `user`.`email` = '{8}';".format(inc2tf, inc2tp, inc3tf, inc3tp, inc4tf, inc4tp, inc5tf, inc5tp, email)
	execute_query_update(sql)

def update_comp_tb(tbc2tf, tbc2tp, tbc3tf, tbc3tp, tbc4tf, tbc4tp, tbc5tf, tbc5tp, email):
	sql = "UPDATE `user` SET `tbc2tf` = '{0}', `tbc2tp` = '{1}', `tbc3tf` = '{2}', `tbc3tp` = '{3}', `tbc4tf` = '{4}', `tbc4tp` = '{5}', `tbc5tf` = '{6}', `tbc5tp` = '{7}' WHERE `user`.`email` = '{8}';".format(tbc2tf, tbc2tp, tbc3tf, tbc3tp, tbc4tf, tbc4tp, tbc5tf, tbc5tp, email)
	execute_query_update(sql)

def fetch_all_single_record(email):
	sql = "SELECT * FROM `user` WHERE email='{0}'".format(email)
	myresult = execute_query_select(sql)[0]
	db_results={"id":myresult[0],"email":myresult[1],"passwd":myresult[2],"code":myresult[3],"done":myresult[4],"user_type":myresult[5],"day_started":myresult[6],"package_length":myresult[7],"fbs1":myresult[8],"fbs1tf":myresult[9],"fbs1tp":myresult[10],"fbs1tg":myresult[11],"fbc1":myresult[12],"fbc1tf":myresult[13],"fbc1tp":myresult[14],"fbc1tg":myresult[15],"fbc2":myresult[16],"fbc3":myresult[17],"fbc4":myresult[18],"fbc5":myresult[19],"tws1":myresult[20],"tws1tf":myresult[21],"tws1tp":myresult[22],"tws1tg":myresult[23],"twc1":myresult[24],"twc1tf":myresult[25],"twc1tp":myresult[26],"twc1tg":myresult[27],"twc2":myresult[28],"twc3":myresult[29],"twc4":myresult[30],"twc5":myresult[31],"ins1":myresult[32],"ins1tf":myresult[33],"ins1tp":myresult[34],"ins1tg":myresult[35],"inc1":myresult[36],"inc1tf":myresult[37],"inc1tp":myresult[38],"inc1tg":myresult[39],"inc2":myresult[40],"inc3":myresult[41],"inc4":myresult[42],"inc5":myresult[43],"tbs1":myresult[44],"tbs1tf":myresult[45],"tbs1tp":myresult[46],"tbs1tg":myresult[47],"tbc1":myresult[48],"tbc1tf":myresult[49],"tbc1tp":myresult[50],"tbc1tg":myresult[51],"tbc2":myresult[52],"tbc3":myresult[53],"tbc4":myresult[54],"tbc5":myresult[55],"fbc2tf":myresult[56],"fbc2tp":myresult[57],"fbc3tf":myresult[58],"fbc3tp":myresult[59],"fbc4tf":myresult[60],"fbc4tp":myresult[61],"fbc5tf":myresult[62],"fbc5tp":myresult[63],"twc2tf":myresult[64],"twc2tp":myresult[65],"twc3tf":myresult[66],"twc3tp":myresult[67],"twc4tf":myresult[68],"twc4tp":myresult[69],"twc5tf":myresult[70],"twc5tp":myresult[71],"inc2tf":myresult[72],"inc2tp":myresult[73],"inc3tf":myresult[74],"inc3tp":myresult[75],"inc4tf":myresult[76],"inc4tp":myresult[77],"inc5tf":myresult[78],"inc5tp":myresult[79],"tbc2tf":myresult[80],"tbc2tp":myresult[81],"tbc3tf":myresult[82],"tbc3tp":myresult[83],"tbc4tf":myresult[84],"tbc4tp":myresult[85],"tbc5tf":myresult[86],"tbc5tp":myresult[87],"fbcon_total_likes":myresult[88],"fbcon_total_talking":myresult[89],"fbcon_fb_grade":myresult[90],"fbcon_fb_like_rank":myresult[91],"fbcon_fb_talk_rank":myresult[92],"fbcon_page_description":myresult[93],"fbcon_page_grade":myresult[94],"fbcon_likes_rank":myresult[95],"fbcon_talking_about_rank":myresult[96],"twcon_total_retweet":myresult[97],"twcon_total_reply":myresult[98],"twcon_total_mentions":myresult[99],"twcon_total_hashtags":myresult[100],"twcon_total_links":myresult[101],"twcon_usernames_count":myresult[102],"twcon_hashtags_count":myresult[103],"twcon_total_tweets":myresult[104],"twcon_total_following":myresult[105],"twcon_total_followers":myresult[106],"instacon_total_followers":myresult[107],"instacon_total_followees":myresult[108],"instacon_mediacount":myresult[109],"instacon_userid":myresult[110],"instacon_biography":myresult[111],"instacon_full_name":myresult[112],"instacon_external_url":myresult[113],"instacon_has_public_story":myresult[114],"instacon_has_viewable_story":myresult[115],"instacon_is_private":myresult[116],"instacon_is_verified":myresult[117],"instacon_profile_pic_url":myresult[118],"instacon_total_likes":myresult[119],"instacon_total_comments":myresult[120],"instacon_hashtags":myresult[121],"instacon_mentions":myresult[122],"tubecon_sub_count_rank":myresult[123],"tubecon_video_view_rank":myresult[124],"tubecon_sub_count":myresult[125],"tubecon_channel_title":myresult[126],"tubecon_video_view":myresult[127],"tubecon_annual_earning_potential":myresult[128],"tubecon_channel_category":myresult[129],"tubecon_joined_date":myresult[130],"tubecon_total_uploaded_videos":myresult[131],"tubecon_last_two_week_video_views":myresult[132],"tubecon_last_two_week_estimated_earnings":myresult[133],"tubecon_last_two_week_video_uploaded":myresult[134]}
	return db_results

def fetch_fbcon(email):
	sql = "SELECT fbcon_total_likes, fbcon_total_talking, fbcon_fb_grade, fbcon_fb_like_rank, fbcon_fb_talk_rank, fbcon_page_description, fbcon_page_grade, fbcon_likes_rank, fbcon_talking_about_rank FROM user WHERE user.email='{0}'".format(email)
	myresult = execute_query_select(sql)[0]
	db_results={"fbcon_total_likes":myresult[0], "fbcon_total_talking":myresult[1], "fbcon_fb_grade":myresult[2], "fbcon_fb_like_rank":myresult[3], "fbcon_fb_talk_rank":myresult[4], "fbcon_page_description":myresult[5], "fbcon_page_grade":myresult[6], "fbcon_likes_rank":myresult[7], "fbcon_talking_about_rank":myresult[8]}
	return db_results

def fetch_twcon(email):
	sql = "SELECT twcon_total_retweet, twcon_total_reply, twcon_total_mentions, twcon_total_hashtags, twcon_total_links, twcon_usernames_count, twcon_hashtags_count, twcon_total_tweets, twcon_total_following, twcon_total_followers FROM user WHERE user.email='{0}'".format(email)
	myresult = execute_query_select(sql)[0]
	db_results={"twcon_total_retweet":myresult[0], "twcon_total_reply":myresult[1], "twcon_total_mentions":myresult[2], "twcon_total_hashtags":myresult[3], "twcon_total_links":myresult[4], "twcon_usernames_count":myresult[5], "twcon_hashtags_count":myresult[6], "twcon_total_tweets":myresult[7], "twcon_total_following":myresult[8], "twcon_total_followers":myresult[9]}
	return db_results

def fetch_instacon(email):
	sql = "SELECT instacon_total_followers, instacon_total_followees, instacon_mediacount, instacon_userid, instacon_biography, instacon_full_name, instacon_external_url, instacon_has_public_story, instacon_has_viewable_story, instacon_is_private, instacon_is_verified, instacon_profile_pic_url, instacon_total_likes, instacon_total_comments, instacon_hashtags, instacon_mentions FROM user WHERE user.email='{0}'".format(email)
	myresult = execute_query_select(sql)[0]
	db_results={"instacon_total_followers":myresult[0], "instacon_total_followees":myresult[1], "instacon_mediacount":myresult[2], "instacon_userid":myresult[3], "instacon_biography":myresult[4], "instacon_full_name":myresult[5], "instacon_external_url":myresult[6], "instacon_has_public_story":myresult[7], "instacon_has_viewable_story":myresult[8], "instacon_is_private":myresult[9], "instacon_is_verified":myresult[10], "instacon_profile_pic_url":myresult[11], "instacon_total_likes":myresult[12], "instacon_total_comments":myresult[13], "instacon_hashtags":myresult[14], "instacon_mentions":myresult[15]}
	return db_results

def fetch_tubecon(email):
	sql = "SELECT tubecon_sub_count_rank, tubecon_video_view_rank, tubecon_sub_count, tubecon_channel_title, tubecon_video_view, tubecon_annual_earning_potential, tubecon_channel_category, tubecon_joined_date, tubecon_total_uploaded_videos, tubecon_last_two_week_video_views, tubecon_last_two_week_estimated_earnings, tubecon_last_two_week_video_uploaded FROM user WHERE user.email='{0}'".format(email)
	myresult = execute_query_select(sql)[0]
	db_results={"tubecon_sub_count_rank":myresult[0], "tubecon_video_view_rank":myresult[1], "tubecon_sub_count":myresult[2], "tubecon_channel_title":myresult[3], "tubecon_video_view":myresult[4], "tubecon_annual_earning_potential":myresult[5], "tubecon_channel_category":myresult[6], "tubecon_joined_date":myresult[7], "tubecon_total_uploaded_videos":myresult[8], "tubecon_last_two_week_video_views":myresult[9], "tubecon_last_two_week_estimated_earnings":myresult[10], "tubecon_last_two_week_video_uploaded":myresult[11]}
	return db_results

def fetch_tbcomp(email):
	sql = "SELECT tbs1, tbs1tf, FLOOR(RAND()*(40-25+1)+25), tbc1, tbc1tf, tbc1tp, tbc2, tbc2tf, tbc2tp, tbc3, tbc3tf, tbc3tp, tbc4, tbc4tf, tbc4tp, tbc5, tbc5tf, tbc5tp, tbs1tp FROM user WHERE user.email='{0}'".format(email)
	myresult = execute_query_select(sql)[0]
	db_results={"tbs1":myresult[0], "tbs1tf":myresult[1], "tbs1engmt":myresult[2], "tbc1":myresult[3], "tbc1tf":myresult[4], "tbc1tp":myresult[5], "tbc2":myresult[6], "tbc2tf":myresult[7], "tbc2tp":myresult[8], "tbc3":myresult[9], "tbc3tf":myresult[10], "tbc3tp":myresult[11], "tbc4":myresult[12], "tbc4tf":myresult[13], "tbc4tp":myresult[14], "tbc5":myresult[15], "tbc5tf":myresult[16], "tbc5tp":myresult[17], "tbs1tp":myresult[18]}
	return db_results

def update_fbcomp(fbcon_total_likes, fbcon_total_talking, fbcon_fb_grade, fbcon_fb_like_rank, fbcon_fb_talk_rank, fbcon_page_description, fbcon_page_grade, fbcon_likes_rank, fbcon_talking_about_rank, email):
	sql = "UPDATE `user` SET `fbcon_total_likes` = '{0}', `fbcon_total_talking` = '{1}', `fbcon_fb_grade` = '{2}', `fbcon_fb_like_rank` = '{3}', `fbcon_fb_talk_rank` = '{4}', `fbcon_page_description` = '{5}', `fbcon_page_grade` = '{6}', `fbcon_likes_rank` = '{7}', `fbcon_talking_about_rank` = '{8}' WHERE `user`.`email` = '{9}';".format(fbcon_total_likes, fbcon_total_talking, fbcon_fb_grade, fbcon_fb_like_rank, fbcon_fb_talk_rank, fbcon_page_description, fbcon_page_grade, fbcon_likes_rank, fbcon_talking_about_rank, email)
	execute_query_update(sql)

def update_twcomp(twcon_total_retweet, twcon_total_reply, twcon_total_mentions, twcon_total_hashtags, twcon_total_links, twcon_usernames_count, twcon_hashtags_count, twcon_total_tweets, twcon_total_following, twcon_total_followers, email):
	sql = "UPDATE `user` SET `twcon_total_retweet` = '{0}', `twcon_total_reply` = '{1}', `twcon_total_mentions` = '{2}', `twcon_total_hashtags` = '{3}', `twcon_total_links` = '{4}', `twcon_usernames_count` = '{5}', `twcon_hashtags_count` = '{6}', `twcon_total_tweets` = '{7}', `twcon_total_following` = '{8}', `twcon_total_followers` = '{9}' WHERE `user`.`email` = '{10}';".format(twcon_total_retweet, twcon_total_reply, twcon_total_mentions, twcon_total_hashtags, twcon_total_links, twcon_usernames_count, twcon_hashtags_count, twcon_total_tweets, twcon_total_following, twcon_total_followers, email)
	execute_query_insert(sql)

def update_instacomp(instacon_total_followers, instacon_total_followees, instacon_mediacount, instacon_userid, instacon_biography, instacon_full_name, instacon_external_url, instacon_has_public_story, instacon_has_viewable_story, instacon_is_private, instacon_is_verified, instacon_profile_pic_url, instacon_total_likes, instacon_total_comments, instacon_hashtags, instacon_mentions, email):
	sql = "UPDATE `user` SET `instacon_total_followers` = '{0}', `instacon_total_followees` = '{1}', `instacon_mediacount` = '{2}', `instacon_userid` = '{3}', `instacon_biography` = '{4}', `instacon_full_name` = '{5}', `instacon_external_url` = '{6}', `instacon_has_public_story` = '{7}', `instacon_has_viewable_story` = '{8}', `instacon_is_private` = '{9}', `instacon_is_verified` = '{10}', `instacon_profile_pic_url` = '{11}', `instacon_total_likes` = '{12}', `instacon_total_comments` = '{13}', `instacon_hashtags` = '{14}', `instacon_mentions` = '{15}' WHERE `user`.`email` = '{16}';".format(instacon_total_followers, instacon_total_followees, instacon_mediacount, instacon_userid, instacon_biography, instacon_full_name, instacon_external_url, instacon_has_public_story, instacon_has_viewable_story, instacon_is_private, instacon_is_verified, instacon_profile_pic_url, instacon_total_likes, instacon_total_comments, instacon_hashtags, instacon_mentions, email)
	execute_query_update(sql)

def update_tubecomp(tubecon_sub_count_rank, tubecon_video_view_rank, tubecon_sub_count, tubecon_channel_title, tubecon_video_view, tubecon_annual_earning_potential, tubecon_channel_category, tubecon_joined_date, tubecon_total_uploaded_videos, tubecon_last_two_week_video_views, tubecon_last_two_week_estimated_earnings, tubecon_last_two_week_video_uploaded, email):
	sql = "UPDATE `user` SET `tubecon_sub_count_rank` = '{0}', `tubecon_video_view_rank` = '{1}', `tubecon_sub_count` = '{2}', `tubecon_channel_title` = '{3}', `tubecon_video_view` = '{4}', `tubecon_annual_earning_potential` = '{5}', `tubecon_channel_category` = '{6}', `tubecon_joined_date` = '{7}', `tubecon_total_uploaded_videos` = '{8}', `tubecon_last_two_week_video_views` = '{9}', `tubecon_last_two_week_estimated_earnings` = '{10}', `tubecon_last_two_week_video_uploaded` = '{11}' WHERE `user`.`email` = '{12}';".format(tubecon_sub_count_rank, tubecon_video_view_rank, tubecon_sub_count, tubecon_channel_title, tubecon_video_view, tubecon_annual_earning_potential, tubecon_channel_category, tubecon_joined_date, tubecon_total_uploaded_videos, tubecon_last_two_week_video_views, tubecon_last_two_week_estimated_earnings, tubecon_last_two_week_video_uploaded, email)
	execute_query_update(sql)
def get_user_stats(email):
	sql = "SELECT email, user_type, day_started, package_length FROM `user` WHERE email='{0}'".format(email)
	myresult = list(execute_query_select(sql)[0])
	email = myresult[0]
	user_type = int(myresult[1])
	day_started = datetime.datetime.fromtimestamp(int(myresult[2]))
	now = datetime.datetime.fromtimestamp(time.time())
	package_length = int(myresult[3])
	time_diff = (now-day_started).days
	time_left = package_length - time_diff
	if user_type == 0:
		user_type = "Admin"
	elif user_type == 1:
		user_type = "Trial"
	elif user_type == 2:
		user_type = "Basic"
	elif user_type == 3:
		user_type = "Standard"
	elif user_type == 4:
		user_type = "Professional"


	time_month = int(time_left / 30)
	time_days = time_left - (time_month*30)

	time_left = "You have {0} months and {1} days left".format(time_month, time_days)

	return (email, user_type, time_left, time_days)

def upgrade_basic_monthly(email):
	time_now = int(time.time())
	user_type = 2
	package_length = 30
	sql = "UPDATE `user` SET `user_type` = '{0}', `day_started` = '{1}', `package_length` = '{2}' WHERE `user`.`email` = '{3}';".format(user_type, time_now, package_length, email)
	execute_query_update(sql)
	print("upgrade_basic_monthly")
def upgrade_basic_annually(email):
	time_now = int(time.time())
	user_type = 2
	package_length = 365
	sql = "UPDATE `user` SET `user_type` = '{0}', `day_started` = '{1}', `package_length` = '{2}' WHERE `user`.`email` = '{3}';".format(user_type, time_now, package_length, email)
	execute_query_update(sql)
	print("upgrade_basic_annually")
def upgrade_standard_monthly(email):
	time_now = int(time.time())
	user_type = 3
	package_length = 30
	sql = "UPDATE `user` SET `user_type` = '{0}', `day_started` = '{1}', `package_length` = '{2}' WHERE `user`.`email` = '{3}';".format(user_type, time_now, package_length, email)
	execute_query_update(sql)
	print("upgrade_standard_monthly")
def upgrade_standard_annually(email):
	time_now = int(time.time())
	user_type = 3
	package_length = 365
	sql = "UPDATE `user` SET `user_type` = '{0}', `day_started` = '{1}', `package_length` = '{2}' WHERE `user`.`email` = '{3}';".format(user_type, time_now, package_length, email)
	execute_query_update(sql)
	print("upgrade_standard_annually")
def upgrade_professional_monthly(email):
	time_now = int(time.time())
	user_type = 4
	package_length = 30
	sql = "UPDATE `user` SET `user_type` = '{0}', `day_started` = '{1}', `package_length` = '{2}' WHERE `user`.`email` = '{3}';".format(user_type, time_now, package_length, email)
	execute_query_update(sql)
	print("upgrade_professional_monthly")
def upgrade_professional_annually(email):
	time_now = int(time.time())
	user_type = 4
	package_length = 365
	sql = "UPDATE `user` SET `user_type` = '{0}', `day_started` = '{1}', `package_length` = '{2}' WHERE `user`.`email` = '{3}';".format(user_type, time_now, package_length, email)
	execute_query_update(sql)
	print("upgrade_professional_annually")
def get_id_email(email):
	sql = "SELECT id, email FROM `user` WHERE email='{0}'".format(email)
	myresult = list(execute_query_select(sql)[0])
	return myresult[0]

def get_notif(email):
	sql = "SELECT fbs1tf, fbc1tf, fbc2tf, fbc3tf, fbc4tf, fbc5tf, tws1tf, twc1tf, twc2tf, twc3tf, twc4tf, twc5tf, ins1tf, inc1tf, inc2tf, inc3tf, inc4tf, inc5tf, tbs1tf, tbc1tf, tbc2tf, tbc3tf, tbc4tf, tbc5tf from user WHERE email='{0}'".format(email)
	try:
		fbs1tf, fbc1tf, fbc2tf, fbc3tf, fbc4tf, fbc5tf, tws1tf, twc1tf, twc2tf, twc3tf, twc4tf, twc5tf, ins1tf, inc1tf, inc2tf, inc3tf, inc4tf, inc5tf, tbs1tf, tbc1tf, tbc2tf, tbc3tf, tbc4tf, tbc5tf = list(execute_query_select(sql))[0]
		fb_lst = [fbs1tf, fbc1tf, fbc2tf, fbc3tf, fbc4tf, fbc5tf]
		tw_lst = [tws1tf, twc1tf, twc2tf, twc3tf, twc4tf, twc5tf]
		in_lst = [ins1tf, inc1tf, inc2tf, inc3tf, inc4tf, inc5tf]
		tb_lst = [tbs1tf, tbc1tf, tbc2tf, tbc3tf, tbc4tf, tbc5tf]

		fb_lst.sort()
		tw_lst.sort()
		in_lst.sort()
		tb_lst.sort()

		fbn = "Your rank is " + str(fb_lst.index(fbs1tf)+1) + " among Facebook Competitors"
		twn = "Your rank is " + str(tw_lst.index(tws1tf)+1) + " among Twitter Competitors"
		inn = "Your rank is " + str(in_lst.index(ins1tf)+1) + " among Instagram Competitors"
		tbn = "Your rank is " + str(tb_lst.index(tbs1tf)+1) + " among YouTube Competitors"
		notif = [fbn, twn, inn, tbn]
		return notif
	except:
		return None

