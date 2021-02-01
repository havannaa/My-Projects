from telethon import TelegramClient, events, sync
from time import sleep

api_id = 505928
api_hash = "0d6f4b42df8b428678d648d95498cd65"

client = TelegramClient('session_name', api_id, api_hash)

client.start()

'''
ent = client.get_messages("@realoriginalferrari");

print(ent[0].id)
print(ent[0].message)

client.send_message('cricket_project', ent[0].message);
'''

current_id = 0
while (True):
	sleep(1);
	try:
		ent = client.get_messages("@realoriginalferrari")
		msg_id = ent[0].id
		msg_content = ent[0].message
		editted = (ent[0].edit_date == None)
		lst = ['%','Ferrari','Offer','Bookie','Widraw','Joinchat','http','Book','Ahuja','Join','Offer','Guarantee','W.me','Withdraw','Guarantee','Christmas','Minimum','Id','Try', 'Fake']

		matched = 0
		for l in lst:
			if (l.lower() in msg_content.lower()):
				matched = 1

		if (current_id != msg_id):
			if matched != 1:
				message = client.send_message('cricket_project', msg_content)
				if (editted == False):
					print('message editted')
					client.edit_message('cricket_project', message.id, msg_content)
		current_id = msg_id
		print(current_id, msg_id)
	except:
		pass

