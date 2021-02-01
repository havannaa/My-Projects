import mysql.connector

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

def insert_user(email, passwd, code):
	sql = "INSERT INTO `user` (`id`, `email`, `passwd`, `code`, `done`, `fbs1`, `fbs1tf`, `fbs1tp`, `fbs1tg`, `fbc1`, `fbc1tf`, `fbc1tp`, `fbc1tg`, `fbc2`, `fbc3`, `fbc4`, `fbc5`, `tws1`, `tws1tf`, `tws1tp`, `tws1tg`, `twc1`, `twc1tf`, `twc1tp`, `twc1tg`, `twc2`, `twc3`, `twc4`, `twc5`, `ins1`, `ins1tf`, `ins1tp`, `ins1tg`, `inc1`, `inc1tf`, `inc1tp`, `inc1tg`, `inc2`, `inc3`, `inc4`, `inc5`, `tbs1`, `tbs1tf`, `tbs1tp`, `tbs1tg`, `tbc1`, `tbc1tf`, `tbc1tp`, `tbc1tg`, `tbc2`, `tbc3`, `tbc4`, `tbc5`, `fbc2tf`, `fbc2tp`, `fbc3tf`, `fbc3tp`, `fbc4tf`, `fbc4tp`, `fbc5tf`, `fbc5tp`, `twc2tf`, `twc2tp`, `twc3tf`, `twc3tp`, `twc4tf`, `twc4tp`, `twc5tf`, `twc5tp`, `inc2tf`, `inc2tp`, `inc3tf`, `inc3tp`, `inc4tf`, `inc4tp`, `inc5tf`, `inc5tp`, `tbc2tf`, `tbc2tp`, `tbc3tf`, `tbc3tp`, `tbc4tf`, `tbc4tp`, `tbc5tf`, `tbc5tp`) VALUES (NULL, '{0}', '{1}', '{2}', '0', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '');".format(email, passwd, code)
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
