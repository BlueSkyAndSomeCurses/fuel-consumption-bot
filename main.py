import datetime
from telegram import *
import telegram.ext
from gspread import authorize
from oauth2client.service_account import ServiceAccountCredentials
import json
import pytz

credentials = ServiceAccountCredentials.from_json_keyfile_name("JSON FILE") #put name of the json file here instead of "JSON FILE"

file = authorize(credentials)

sheet = file.open("fuel testing")
sheet = sheet.sheet1


arrmsg = "я приїхав 🚛"
inc = 1
onlineusers = dict()

def driver(update, context, user):
    sheet.update_cell(onlineusers[user][0], onlineusers[user][1], update.message.text)
    context.bot.send_message(chat_id=user, text = "Вкажіть маршрут")
    onlineusers[user][1]+=1    

def route(update, context, user):
    sheet.update_cell(onlineusers[user][0], onlineusers[user][1], update.message.text)
    context.bot.send_message(chat_id=user, text = "Заправка денна")
    onlineusers[user][1]+=1    

def refill(update, context, user):
    sheet.update_cell(onlineusers[user][0], onlineusers[user][1], update.message.text)
    context.bot.send_message(chat_id=user, text = "Номер паливної картки")
    onlineusers[user][1]+=1    

def fuelcard(update, context, user):
    sheet.update_cell(onlineusers[user][0], onlineusers[user][1], update.message.text)
    context.bot.send_message(chat_id=user, text = "Вид палива ДП/ДП+")
    onlineusers[user][1]+=1    

def fueltype(update, context, user):
    sheet.update_cell(onlineusers[user][0], onlineusers[user][1], update.message.text)
    context.bot.send_message(chat_id=user, text = "Кінцевий пробіг")
    onlineusers[user][1]+=1    

def result(update, context, user):
    sheet.update_cell(onlineusers[user][0], onlineusers[user][1], update.message.text)
    context.bot.send_message(chat_id=user, text = "Залишок")
    onlineusers[user][1]+=1    

def remainder(update, context, user):
    sheet.update_cell(onlineusers[user][0], onlineusers[user][1], update.message.text)
    context.bot.send_message(chat_id=user, text = "Вага вантажу")
    onlineusers[user][1]+=1    

def weight(update, context, user):
    sheet.update_cell(onlineusers[user][0], onlineusers[user][1], update.message.text)
    context.bot.send_message(chat_id=user, text = "Кількість клієнтів")
    onlineusers[user][1]+=1    

def clientsamount(update, context, user):
    sheet.update_cell(onlineusers[user][0], onlineusers[user][1], update.message.text)
    context.bot.send_message(chat_id=user, text = "Дякую")
    onlineusers.pop(user)

func = [driver, route, refill, fuelcard, fueltype,result, remainder, weight, clientsamount]

def start(update, context):
    buttons = [[KeyboardButton(arrmsg)]]
    context.bot.send_message(chat_id=update.effective_chat.id, text = "Бот для ведденя контролю", reply_markup=ReplyKeyboardMarkup(buttons))

def mainfunc(update, context):
    user = update.effective_chat.id
    if update.message.text == arrmsg:
        global inc
        inc += 1
        onlineusers[user] = [inc, 4] 
        sheet.update_cell(onlineusers[user][0], 2, str(datetime.date.today()))
        sheet.update_cell(onlineusers[user][0], 3, str(datetime.datetime.now(pytz.timezone('Europe/Kiev')).strftime("%H:%M")))
        context.bot.send_message(chat_id=user, text = "Вкажіть своє ім'я")
        return
    func[onlineusers[user][1]-4](update,context,user)
    

updater = telegram.ext.Updater('TOKEN', use_context = True)
#put your telegram bot token instead of 'TOKEN'
dp = updater.dispatcher

dp.add_handler(telegram.ext.CommandHandler("start", start))
dp.add_handler(telegram.ext.MessageHandler(telegram.ext.Filters.text, mainfunc))

updater.start_polling()
updater.idle()
