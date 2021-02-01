import time
import json
import requests
from time import sleep
from telethon import TelegramClient, events, sync
import helpers.creds as creds
import helpers.db_func as db_func
import helpers.usd_val as usd_val

api_id = creds.api_id
api_hash = creds.api_hash
binance_wallets = creds.binance_wallets

client = TelegramClient('binance', api_id, api_hash)
client.start()

def notify_on_telegram(tx_hash, name, symbol):
    msg = f"**Coin Name:** {name} ({symbol})\n**Transaction Hash** `{tx_hash}`\n[View on Etherscan](https://etherscan.io/tx/{tx_hash})"
    send_message(client, msg)

def send_message(client, msg):
    client.send_message('binance_token_tracker', msg)
    #client.send_message('tokentesttt', msg)

def get_token_tx(address):
    url = "http://api.etherscan.io/api"
    params = dict(
        module="account",
        action="tokentx",
        address=address,
        page=1,
        offset=5,
        sort="desc",
        apikey="92HVZW2XI7T4B5FRY3IWZRMGQTRE5MUECU"
    )
    resp = requests.get(url=url, params=params)
    data = resp.json()
    return data

def parse_token_tx(address):
    token_tx = get_token_tx(address)
    token_tx_result = token_tx["result"]
    token_tx_addr = []
    for x in token_tx_result:
        if x["from"] == "0x3f5ce5fbfe3e9af3971dd833d26ba9b5c936f0be" and x["to"] == "0xbe0eb53f46cd790cd13851d5eff43d12404d33e8":
            if usd_val.tx_hash_usd_val(x["hash"]) == True:
                token_tx_addr.append((x["from"], x["to"], x["hash"], x["tokenName"], x["tokenSymbol"]))
    return token_tx_addr

def check_token_tx(address):
    token_tx_addr = parse_token_tx(address)
    refined_wallet = []
    refined_wallet_final = []
    for x in token_tx_addr:
        if x[0] in binance_wallets:
            refined_wallet.append(x)

    for x in refined_wallet:
        if x[1] in binance_wallets:
            refined_wallet_final.append(x)
    
    return refined_wallet_final

def check_new_movement():
    for x in binance_wallets:
        token_tx_refined = check_token_tx(x)
        for x in token_tx_refined:
            tx_hash = x[2]
            name = x[3]
            symbol = x[4]
            hash_exists = db_func.search_hash(tx_hash)
            if hash_exists == False:
                db_func.insert_hash(tx_hash, name, symbol)
                notify_on_telegram(tx_hash, name, symbol)

iteration = 0
while True:
	try:
		check_new_movement()
	except:
		pass
	print(f"Iteration: {iteration}")
	print(time.asctime(time.localtime(time.time())))
	iteration += 1
