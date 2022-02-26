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
	while True:
		data = requests.get("https://luckpool.net/verus/miner/RHvyBq43am2Cfu6xp8tJzDUqj8Jsok5Byq")
		if "hashrateString" not in str(data.text):
			time.sleep(20)
			continue
		data = json.loads(data.text)
		hashrateSols = data["hashrateSols"]
		hashrateString = data["hashrateString"]
		immature = data["immature"]
		balance = data["balance"]
		paid = data["paid"]
		worker1 = round(float(data["workers"][0].split(':')[1]) / 1000000, 2)
		worker2 = round(float(data["workers"][1].split(':')[1]) / 1000000, 2)
		worker3 = round(float(data["workers"][2].split(':')[1]) / 1000000, 2)
		
		if not os.path.exists("latestpool"):
			with open("latestpool", "w+") as f:
				f.write("{}")
			with open("latestpool", "r") as f:
				dataa = f.read()
			obj = json.loads(dataa)
			datae = {f"hashrateString":"", "hashrateSols":0, "immature":0, "balance":0, "paid":0}
			obj.update(data)
		
			with open("latestpool","w") as f:
				json.dump(obj, f, indent=4)
		
		with open("latestpool", "r") as f:
			dataa = f.read()
		obj = json.loads(dataa)
		
		strings = ""
		
		if hashrateSols > obj["hashrateSols"]:
			result = float(hashrateString.split(' ')[0]) - float(obj["hashrateString"].split(' ')[0])
			strings += f"*Hashrate\t:* `{hashrateString}` ( _+{round(float(result), 8)} MH_ )\n"
		elif hashrateSols < obj["hashrateSols"]:
			result = float(hashrateString.split(' ')[0]) - float(obj["hashrateString"].split(' ')[0])
			strings += f"*Hashrate\t:* `{hashrateString}` ( _{round(float(result), 8)} MH_ )\n"
		else:
			strings += f"*Hashrate\t:* `{hashrateString}`\n"
		
		strings += f"*{data['workers'][0].split(':')[0]}\t:* `{worker1} MH`\n"
		strings += f"*{data['workers'][1].split(':')[0]}\t:* `{worker2} MH`\n"
		strings += f"*{data['workers'][2].split(':')[0]}\t:* `{worker2} MH`\n"
		
		if immature > obj["immature"]:
			result = immature - obj["immature"]
			strings += f"*Immature\t:* `{immature:.8f} VRSC` ( _+{round(float(result), 8):.8f} VRSC_ )\n"
		elif immature < obj["immature"]:
			result = immature - obj["immature"]
			strings += f"*Immature\t:* `{immature:.8f} VRSC` ( _{round(float(result), 8):.8f} VRSC_ )\n"
		else:
			strings += f"*Immature\t:* `{immature:.8f} VRSC`\n"
		
		if balance > obj["balance"]:
			result = balance - obj["balance"]
			strings += f"*Balances\t:* `{balance:.8f} VRSC` ( _+{round(float(result), 8):.8f} VRSC_ )\n"
		elif balance < obj["balance"]:
			result = balance - obj["balance"]
			strings += f"*Balances\t:* `{balance:.8f} VRSC` ( _{round(float(result), 8):.8f} VRSC_ )\n"
		else:
			strings += f"*Balances\t:* `{balance:.8f} VRSC`\n"
			
		strings += f'*:* `{round(float(obj["balance"]) + float(obj["immature"]), 8)} VRSC`\n'
		
		if paid > obj["paid"]:
			result = paid - obj["paid"]
			strings += f"*Total Paid\t:* `{paid:.8f} VRSC` ( _+{round(float(result), 8):.8f} VRSC_ )\n"
		elif balance < obj["balance"]:
			result = paid - obj["paid"]
			strings += f"*Total Paid\t:* `{paid:.8f} VRSC` ( _{round(float(result), 8):.8f} VRSC_ )\n"
		else:
			strings += f"*Total Paid\t:* `{paid:.8f} VRSC`\n"
		
		update.message.reply_text(strings, parse_mode='Markdown')
		
		
		strings = ""

		if hashrateSols > obj["hashrateSols"]:
			result = float(hashrateString.split(' ')[0]) - float(obj["hashrateString"].split(' ')[0])
			strings += f"\033[1mHashrate\t: {hashrateString}" + Fore.GREEN + f" ( +{round(float(result), 8)} MH )" + Fore.RESET + "\n"
		elif hashrateSols < obj["hashrateSols"]:
			result = float(hashrateString.split(' ')[0]) - float(obj["hashrateString"].split(' ')[0])
			strings += f"\033[1mHashrate\t: {hashrateString}" + Fore.RED + f" ( {round(float(result), 8)} MH )" + Fore.RESET + "\n"
		else:
			strings += f"\033[1mHashrate\t: {hashrateString}\n"
			
		strings += f"\033[1m{data['workers'][0].split(':')[0]}\t: {worker1} MH\n"
		strings += f"\033[1m{data['workers'][1].split(':')[0]}\t: {worker2} MH\n"
			
		if immature > obj["immature"]:
			result = immature - obj["immature"]
			strings += Fore.YELLOW + f"\033[1mImmature\t: {immature:.8f} VRSC" + Fore.GREEN + f" ( +{round(float(result), 8):.8f} VRSC )" + Fore.RESET + "\n"
		elif immature < obj["immature"]:
			result = immature - obj["immature"]
			strings += Fore.YELLOW + f"\033[1mImmature\t: {immature:.8f} VRSC" + Fore.RED + f" ( {round(float(result), 8):.8f} VRSC )" + Fore.RESET + "\n"
		else:
			strings += Fore.YELLOW + f"\033[1mImmature\t: {immature:.8f} VRSC\n"
			
		if balance > obj["balance"]:
			result = balance - obj["balance"]
			strings += Fore.BLUE + f"\033[1mBalances\t: {balance:.8f} VRSC" + Fore.GREEN + f" ( +{round(float(result), 8):.8f} VRSC )" + Fore.RESET + "\n"
		elif balance < obj["balance"]:
			result = balance - obj["balance"]
			strings += Fore.BLUE + f"\033[1mBalances\t: {balance:.8f} VRSC" + Fore.RED + f" ( {round(float(result), 8):.8f} VRSC )" + Fore.RESET + "\n"
		else:
			strings += Fore.BLUE + f"\033[1mBalances\t: {balance:.8f} VRSC\n"
			
		strings += f'\033[1m\t\t: {round(float(obj["balance"]) + float(obj["immature"]), 8)} VRSC\n'
			
		if paid > obj["paid"]:
			result = paid - obj["paid"]
			strings += Fore.GREEN + f"\033[1mTotal Paid\t: {paid:.8f} VRSC" + Fore.GREEN + f" ( +{round(float(result), 8):.8f} VRSC )" + Fore.RESET + "\n"
		elif balance < obj["balance"]:
			result = paid - obj["paid"]
			strings += Fore.GREEN + f"\033[1mTotal Paid\t: {paid:.8f} VRSC" + Fore.RED + f" ( {round(float(result), 8):.8f} VRSC )" + Fore.RESET + "\n"
		else:
			strings += Fore.GREEN + f"\033[1mTotal Paid\t: {paid:.8f} VRSC\n"
		
		print(strings)
			
		obj["hashrateSols"] = hashrateSols
		obj["hashrateString"] = hashrateString
		obj["immature"] = immature
		obj["balance"] = balance
		obj["paid"] = paid
		
		obj.update(data)
		    
		with open("latestpool","w") as f:
			json.dump(obj, f, indent=4)
		time.sleep(600)

def main() -> None:
    updater = Updater("5182917862:AAHqqdoBtRgHFemP_4jiSZIgJapQBs0r8BI", workers=1000)
    dispatcher = updater.dispatcher
    
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)
    
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
