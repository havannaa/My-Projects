import mysql.connector
from random import randint
from datetime import datetime

def get_current_time():
    return str(datetime.now().strftime("%c"))

def generate_referral_code_personal():
    return str(randint(100000, 999999))

def connect():
    mydb = mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        passwd='',
        database='sip'
    )
    return mydb

for x in user_check_login('2'):
    print(x)
for x in user_check_login(2):
    print(x)
    mydb = connect()
    mycursor = mydb.cursor()
    mycursor.execute(sql)

    myresult = mycursor.fetchall()

    mycursor.close()
    mydb.close()

    return myresult

def insert(sql):
    mydb = connect()
    mycursor = mydb.cursor()
    mycursor.execute(sql)
    mydb.commit()

    mycursor.close()
    mydb.close()

def update(sql):
    mydb = connect()
    mycursor = mydb.cursor()
    mycursor.execute(sql)
    mydb.commit()

    mycursor.close()
    mydb.close()

def get_new_btc_wallet():
    sql = f"SELECT `id`, `wallet`,`private` FROM `btc_wallet` WHERE is_used='' LIMIT 1;"
    myresult = select(sql)[0]
    row_id = myresult[0]
    public = myresult[1]
    private = myresult[2]
    return (row_id, public, private)

def update_btc_wallet_used(row_id):
    sql = f"UPDATE `btc_wallet` SET `is_used` = 'used' WHERE `btc_wallet`.`id` = {row_id};"
    update(sql)

def get_new_eth_wallet():
    sql = f"SELECT `id`, `wallet`,`private` FROM `eth_wallet` WHERE is_used='' LIMIT 1;"
    myresult = select(sql)[0]
    row_id = myresult[0]
    public = myresult[1]
    private = myresult[2]
    return (row_id, public, private)

def update_eth_wallet_used(row_id):
    sql = f"UPDATE `eth_wallet` SET `is_used` = 'used' WHERE `eth_wallet`.`id` = {row_id};"
    update(sql)


def register_post_check_mail(email):
    sql = f"SELECT `user_id`,`full_name` FROM `users` WHERE email='{email}';"
    myresult = select(sql)
    myresult_len = len(myresult)
    if myresult_len != 0:
        return True
    else:
        return False

def register_post(full_name, email, password, referral_code):
    check_mail = register_post_check_mail(email)
    if check_mail == False:
        referral_code_personal = generate_referral_code_personal()
        account_creation_time = get_current_time()
        btc_wallet = get_new_btc_wallet()
        update_btc_wallet_used(btc_wallet[0])
        eth_wallet = get_new_eth_wallet()
        update_eth_wallet_used(eth_wallet[0])
        sql = f"INSERT INTO `users` (`user_id`, `full_name`, `email`, `password`, `referral_code`, `referral_code_personal`, `joined_date`, `dob`, `address`, `city`, `region`, `country`, `postal_code`, `phone`, `account_balance`, `wlt_addr_btc`, `wlt_addr_btc_pvt`, `wlt_btc_amount`, `wlt_addr_eth`, `wlt_addr_eth_pvt`, `wlt_eth_amount`) VALUES (NULL, '{full_name}', '{email}', '{password}', '{referral_code}', '{referral_code_personal}', '{account_creation_time}', '', '', '', '', '', '', '', '0', '{btc_wallet[1]}', '{btc_wallet[2]}', '0', '{eth_wallet[1]}', '{eth_wallet[2]}', '0');"
        insert(sql)
        return True
    else:
        return False
    
def user_new_investment(user_id, amount, plan):
    investment_start_time = get_current_time()
    sql = f"INSERT INTO `investments` (`inv_id`, `user_id`, `date`, `amount`, `inv_plan`, `status`) VALUES (NULL, '{user_id}', '{investment_start_time}', '{amount}', '{plan}', 'Running');"
    insert(sql)

def user_check_investment(user_id):
    sql = f"SELECT `date`,`amount`,`inv_plan`,`status` FROM `investments` WHERE user_id='{user_id}';"
    myresult = select(sql)
    return myresult

def user_new_deposit(user_id, tx_type, amount, amount_usd, tx_addr, tx_hash, tx_status):
    tx_time = get_current_time()
    sql = f"INSERT INTO `deposits` (`deposit_id`, `user_id`, `date`, `tx_type`, `tx_amount`, `tx_amount_usd`, `tx_address`, `tx_hash`, `tx_status`) VALUES (NULL, '{user_id}', '{tx_time}', '{tx_type}', '{amount}', '{amount_usd}', '{tx_addr}', '{tx_hash}', '{tx_status}');"
    insert(sql)

def user_check_deposit(user_id):
    sql = f"SELECT `date`,`tx_type`,`tx_amount`,`tx_amount_usd`,`tx_address`,`tx_hash`,`tx_status` FROM `deposits` WHERE `user_id`='{user_id}';"
    myresult = select(sql)
    return myresult

def user_new_withdraw(user_id, tx_type, amount, amount_usd, tx_addr, tx_hash, tx_status):
    tx_time = get_current_time()
    sql = f"INSERT INTO `withdrawls` (`wtdl_id`, `user_id`, `date`, `tx_type`, `tx_amount`, `tx_amount_usd`, `tx_address`, `tx_hash`, `tx_status`) VALUES (NULL, '{user_id}', '{tx_time}', '{tx_type}', '{amount}', '{amount_usd}', '{tx_addr}', '{tx_hash}', '{tx_status}');"
    insert(sql)

def user_check_withdraw(user_id):
    sql = f"SELECT `date`,`tx_type`,`tx_amount`,`tx_amount_usd`,`tx_address`,`tx_hash`,`tx_status` FROM `withdrawls` WHERE `user_id`={user_id};"
    myresult = select(sql)
    return myresult

def user_new_login(user_id, ip, location, browser, platform):
    login_time = get_current_time()
    sql = f"INSERT INTO `logins` (`login_id`, `user_id`, `date`, `ip`, `location`, `browser`, `platform`) VALUES (NULL, '{user_id}', '{login_time}', '{ip}', '{location}', '{browser}', '{platform}');"
    insert(sql)

def user_check_login(user_id):
    sql = f"SELECT `date`,`ip`,`location`,`browser`,`platform` FROM `logins` WHERE `user_id`={user_id};"
    myresult = select(sql)
    return myresult

