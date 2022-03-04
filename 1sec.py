import logging, requests, random, json, os, time

os.system("sudo apt-get update")
os.system("sudo apt install python3-pip -y")
os.system("sudo pip3 install python-telegram-bot")

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext
from telegram.ext.dispatcher import run_async
from colorama import Fore, init as color_ama
color_ama(autoreset=True)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)

@run_async
def start(update, context):
	list = requests.get("https://www.1secmail.com/api/v1/?action=genRandomMailbox&count=100").json()
	msg = "\n".join(list)
	update.message.reply_text(f"`{msg}`", parse_mode='Markdown')
	for x in list:
		email = x.split("@")[0].strip()
		password = x.split("@")[1].strip()
		update.message.reply_text(f"{email}@{password} Waiting...")
		while True:
			check = requests.get(f"https://www.1secmail.com/api/v1/?action=getMessages&login={email}&domain={password}").json()
			if len(check) != 0:
				a = requests.get(f"https://www.1secmail.com/api/v1/?action=readMessage&login={email}&domain={password}&id={check[0]['id']}")
				a = a.text.split(',')[16].split('confirmation_token=')[1].split('&amp;locale=id')[0]
				requests.get(f"https://run.qwiklabs.com/users/confirmation?confirmation_token={a}")
				update.message.reply_text(f"{email}@{password} is confirm!!")
				break
			
def stop(update, context):
	update.message.reply_text("stopped")
	os.system("sudo reboot")
				
def main() -> None:
    updater = Updater("5166018106:AAHPY5g634qaDCLzvJdmYcFsJsoo2LBAWhU", workers=1000)
    dispatcher = updater.dispatcher
    
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)
    
    stop_handler = CommandHandler('stop', stop)
    dispatcher.add_handler(stop_handler)
    
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()