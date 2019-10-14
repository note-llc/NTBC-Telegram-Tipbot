import json
import codecs
import requests
from bs4 import BeautifulSoup, SoupStrainer
import re
import subprocess
from telegram.ext.dispatcher import run_async
from telegram.ext import Updater
from html import escape

updater = Updater(token='BOT_TOKEN')
dispatcher = updater.dispatcher

import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
					level=logging.INFO)

def commands(bot, update):
	user = update.message.from_user.username
	bot.send_message(chat_id=update.message.chat_id, text="Initiating commands /tip & /withdraw have a specfic format,\n use them like so:" + "\n \n Parameters: \n <user> = target user to tip \n <amount> = amount of NoteBlockChain to utilise \n <address> = NoteBlockChain address to withdraw to \n \n Tipping format: \n /tip <user> <amount> \n \n Withdrawing format: \n /withdraw <address> <amount>")

def help(bot, update):
	bot.send_message(chat_id=update.message.chat_id, text="The following commands are at your disposal: /hi , /commands , /deposit , /tip , /withdraw or /balance")

def deposit(bot, update):
	user = update.message.from_user.username
	if user is None:
		bot.send_message(chat_id=update.message.chat_id, text="Please set a telegram username in your profile settings!")
	else:
		address = "root/telegrambot/Metropolitan/src/METROd"
		result = subprocess.run([address,"getaccountaddress",user],stdout=subprocess.PIPE)
		clean = (result.stdout.strip()).decode("utf-8")
		bot.send_message(chat_id=update.message.chat_id, text="@{0} your depositing address is: {1}".format(user,clean))

def tip(bot,update):
	user = update.message.from_user.username
	target = update.message.text[5:]
	amount =  target.split(" ")[1]
	target =  target.split(" ")[0]
	if user is None:
		bot.send_message(chat_id=update.message.chat_id, text="Please set a telegram username in your profile settings!")
	else:
		machine = "@NoTeM"
		if target == machine:
			bot.send_message(chat_id=update.message.chat_id, text="HODL.")
		elif "@" in target:
			target = target[1:]
			user = update.message.from_user.username
			core = "/usr/local/bin/notebcd"
			result = subprocess.run([core,"getbalance",user],stdout=subprocess.PIPE)
			balance = float((result.stdout.strip()).decode("utf-8"))
			amount = float(amount)
			if balance < amount:
				bot.send_message(chat_id=update.message.chat_id, text="@{0} you have insufficent funds.".format(user))
			elif target == user:
				bot.send_message(chat_id=update.message.chat_id, text="You can't tip yourself!")
			else:
				balance = str(balance)
				amount = str(amount)
				tx = subprocess.run([core,"move",user,target,amount],stdout=subprocess.PIPE)
				bot.send_message(chat_id=update.message.chat_id, text="@{0} tipped @{1} of {2} DEAL".format(user, target, amount))
		else:
			bot.send_message(chat_id=update.message.chat_id, text="Error that user is not applicable.")

def balance(bot,update):
	user = update.message.from_user.username
	if user is None:
		bot.send_message(chat_id=update.message.chat_id, text="Please set a telegram username in your profile settings!")
	else:
		core = "/usr/local/bin/notebcd"
		result = subprocess.run([core,"getbalance",user],stdout=subprocess.PIPE)
		clean = (result.stdout.strip()).decode("utf-8")
		balance  = float(clean)
		balance =  str(round(balance,3))
		bot.send_message(chat_id=update.message.chat_id, text="@{0} your current balance is: {1} DEAL ".format(user,balance))



def withdraw(bot,update):
	user = update.message.from_user.username
	if user is None:
		bot.send_message(chat_id=update.message.chat_id, text="Please set a telegram username in your profile settings!")
	else:
		target = update.message.text[9:]
		address = target[:35]
		address = ''.join(str(e) for e in address)
		target = target.replace(target[:35], '')
		amount = float(target)
		core = "/usr/local/bin/notebcd"
		result = subprocess.run([core,"getbalance",user],stdout=subprocess.PIPE)
		clean = (result.stdout.strip()).decode("utf-8")
		balance = float(clean)
		if balance < amount:
			bot.send_message(chat_id=update.message.chat_id, text="@{0} you have insufficent funds.".format(user))
		else:
			amount = str(amount)
			tx = subprocess.run([core,"sendfrom",user,address,amount],stdout=subprocess.PIPE)
			bot.send_message(chat_id=update.message.chat_id, text="@{0} has successfully withdrew to address: {1} of {2} DEAL" .format(user,address,amount))

def hi(bot,update):
	user = update.message.from_user.username
	bot.send_message(chat_id=update.message.chat_id, text="Hello @{0}, Let's make a DEAL!".format(user))

def rain(bot,update):
  bot.send_message(chat_id=update.message.chat_id, text="Stake for a rainy day!")

def price(bot,update):
	data = requests.get('https://icqbase.com/page/api?method=singleinfo&marketid=69').json()['return'][0]

	satsPrice = data['lasttradeprice']
	change = data['change']
	volume24 = data['24BaseVolume']

	priceInfo = '''\
	Price: {0} BTC
	Change: {1}%
	24/Total Vol.: {2} BTC'''.format(satsPrice, change, volume24)

	bot.send_message(chat_id=update.message.chat_id, text=priceInfo)

from telegram.ext import CommandHandler

commands_handler = CommandHandler('commands', commands)
dispatcher.add_handler(commands_handler)

rain_handler = CommandHandler('rain', rain)
dispatcher.add_handler(rain_handler)

hi_handler = CommandHandler('hi', hi)
dispatcher.add_handler(hi_handler)

withdraw_handler = CommandHandler('withdraw', withdraw)
dispatcher.add_handler(withdraw_handler)

deposit_handler = CommandHandler('deposit', deposit)
dispatcher.add_handler(deposit_handler)

tip_handler = CommandHandler('tip', tip)
dispatcher.add_handler(tip_handler)

balance_handler = CommandHandler('balance', balance)
dispatcher.add_handler(balance_handler)

help_handler = CommandHandler('help', help)
dispatcher.add_handler(help_handler)

price_handler = CommandHandler('price', price)
dispatcher.add_handler(price_handler)

updater.start_polling()

