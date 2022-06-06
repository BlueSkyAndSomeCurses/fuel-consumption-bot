from datetime import date
from telegram import *
import telegram.ext
from gspread import authorize
from oauth2client.service_account import ServiceAccountCredentials
import json

credentials = ServiceAccountCredentials.from_json_keyfile_name("master-crossing-352412-3e391333df5b.json")

file = authorize(credentials)

sheet = file.open("fuel testing")
sheet = sheet.sheet1

arrmsg = "я приїхав 🚛"
inc = 1
onlineusers = dict()

def start(update, context):
    buttons = [[KeyboardButton(arrmsg)]]
    context.bot.send_message(chat_id=update.effective_chat.id, text = "Бот для ведденя контролю", reply_markup=ReplyKeyboardMarkup(buttons))

def mainfunc(update, context):
    if update.message.text == arrmsg:
        global inc
        inc += 1
        onlineusers[update.effective_chat.id] = 4
        sheet.update_cell(2, inc, date)


updater = telegram.ext.Updater('5409836173:AAG1igVGCbsV1AhmjKFs_gQ8w8bLGhBIdsE', use_context = True)
dp = updater.dispatcher

dp.add_handler(telegram.ext.CommandHandler("start", start))
dp.add_handler(telegram.ext.MessageHandler(telegram.ext.Filters.text, mainfunc))

updater.start_polling()
updater.idle()
