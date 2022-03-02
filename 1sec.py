from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext
from telegram.ext.dispatcher import run_async
from colorama import Fore, init as color_ama
color_ama(autoreset=True)

import logging, requests, random, json, os, time
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)

@run_async
def start(update, context):
	list = requests.get("https://www.1secmail.com/api/v1/?action=genRandomMailbox&count=30").json()
	msg = "\n".join(list)
	update.message.reply_text(f"`{msg}`", parse_mode='Markdown')
	for x in list:
		if os.path.exists("stop"):
			update.message.reply_text("stopped")
			exit(0)
		email = x.split("@")[0].strip()
		password = x.split("@")[1].strip()
		msg = update.message.reply_text(f"{email}@{password} Waiting...")
		with open(f'msgid', 'w') as f:
			f.write(str(msg))
		
		while True:
			check = requests.get(f"https://www.1secmail.com/api/v1/?action=getMessages&login={email}&domain={password}").json()
			if len(check) != 0:
				a = requests.get(f"https://www.1secmail.com/api/v1/?action=readMessage&login={email}&domain={password}&id={check[0]['id']}")
				a = a.text.split(',')[16].split('confirmation_token=')[1].split('&amp;locale=id')[0]
				requests.get(f"https://run.qwiklabs.com/users/confirmation?confirmation_token={a}")
				with open(f'msgid', 'r') as f:
					msgid = f.read()
				for x in str(msgid).split(', '):
					if 'message_id' in x:
						msgid = x.split(' ')[1]
						break
				context.bot.edit_message(chat_id=update.message.chat_id, message_id=int(msgid), text=f"{email}@{password} is confirm!!")
				break
			
def stop(update, context):
	with open("stop", "a+") as f:
		f.write(" ")

def main() -> None:
    updater = Updater("5166018106:AAH07UP_b23T-dCtFiypamXYhvFukdXs4Ec", workers=1000)
    dispatcher = updater.dispatcher
    
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)
    
    stop_handler = CommandHandler('stop', stop)
    dispatcher.add_handler(stop_handler)
    
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()