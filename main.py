from datetime import datetime, date
from telegram import *
import telegram.ext
from gspread import authorize
from oauth2client.service_account import ServiceAccountCredentials
import json
import pytz

credentials = ServiceAccountCredentials.from_json_keyfile_name("master-crossing-352412-3e391333df5b.json") #put name of the json file here instead of "JSON FILE"

file = authorize(credentials)

sheet = file.open("fuel testing")
datasheet = sheet.worksheet("database")
sheet = sheet.sheet1



arrmsg = "я приїхав 🚛"
inc = int(datasheet.cell(1,7).value)
onlineusers = dict()
database = dict()

count = 1
while datasheet.cell(count, 1).value:
    database[datasheet.cell(count,1).value] = [datasheet.cell(count,2).value,datasheet.cell(count,3).value, count] 
    count+=1





def driver(update, context, user):
    msg = update.message.text
    sheet.update_cell(onlineusers[user][0], onlineusers[user][1], msg)
    database[user][0] = msg
    datasheet.update_cell(database[user][2], 2, msg)
    update.message.reply_text("Вкажіть назву авто")
    onlineusers[user][1]+=1    

def car(update, context, user):
    msg = update.message.text
    sheet.update_cell(onlineusers[user][0], onlineusers[user][1], msg)
    database[user][0] = msg
    datasheet.update_cell(database[user][2], 3, msg)
    update.message.reply_text("Вкажіть маршрут")
    onlineusers[user][1]+=1    

def route(update, context, user):
    sheet.update_cell(onlineusers[user][0], onlineusers[user][1], update.message.text)
    update.message.reply_text("Заправка денна")
    onlineusers[user][1]+=1    

def refill(update, context, user):
    sheet.update_cell(onlineusers[user][0], onlineusers[user][1], update.message.text)
    update.message.reply_text("Номер паливної картки")
    onlineusers[user][1]+=1    

def fuelcard(update, context, user):
    sheet.update_cell(onlineusers[user][0], onlineusers[user][1], update.message.text)
    context.bot.send_message(chat_id=update.effective_chat.id, text = "Вид палива", reply_markup=ReplyKeyboardMarkup([[KeyboardButton("ДП")],[KeyboardButton("ДП+")],[KeyboardButton("A95")],[KeyboardButton("A95+")]]))
    onlineusers[user][1]+=1    

def fueltype(update, context, user):
    sheet.update_cell(onlineusers[user][0], onlineusers[user][1], update.message.text)
    update.message.reply_text("Кінцевий пробіг")
    onlineusers[user][1]+=1    

def result(update, context, user):
    sheet.update_cell(onlineusers[user][0], onlineusers[user][1], update.message.text)
    update.message.reply_text("Залишок")
    onlineusers[user][1]+=1    

def remainder(update, context, user):
    sheet.update_cell(onlineusers[user][0], onlineusers[user][1], update.message.text)
    update.message.reply_text("Кількість клієнтів")
    onlineusers[user][1]+=1    

def clientsamount(update, context, user):
    sheet.update_cell(onlineusers[user][0], onlineusers[user][1], update.message.text)
    context.bot.send_message(chat_id=update.effective_chat.id, text = "Дякую", reply_markup=ReplyKeyboardMarkup([[arrmsg]]))
    onlineusers.pop(user)

func = [driver, car, route, refill, fuelcard, fueltype,result, remainder,  clientsamount]

def start(update, context):
    buttons = [[KeyboardButton(arrmsg)]]
    context.bot.send_message(chat_id=update.effective_chat.id, text = "Бот для ведденя контролю", reply_markup=ReplyKeyboardMarkup(buttons))


def mainfunc(update, context):
    user = update.effective_user.username

    if update.message.text == arrmsg:
        global inc
        inc += 1
        onlineusers[user] = [inc, 4] 
        sheet.update_cell(onlineusers[user][0], 2, str(date.today()))
        sheet.update_cell(onlineusers[user][0], 3, str(datetime.now(pytz.timezone('Europe/Kiev')).strftime("%H:%M")))
        if user in database:
            sheet.update_cell(onlineusers[user][0], 4, database[user][0])
            sheet.update_cell(onlineusers[user][0], 5, database[user][1])
            onlineusers[user][1]= 6
            update.message.reply_text("Вкажіть маршрут")
        else:    
            update.message.reply_text("Вкажіть своє ім'я")
            count = int(datasheet.cell(1,8).value)
            database[user] = ["","", count]
            datasheet.update_cell(count,1, user)
            count+=1

            datasheet.update_cell(1,8, str(count))

        datasheet.update_cell(1,7, str(inc))
        return
    func[onlineusers[user][1]-4](update,context,user)

    

updater = telegram.ext.Updater('5409836173:AAG1igVGCbsV1AhmjKFs_gQ8w8bLGhBIdsE', use_context = True)
#put your telegram bot token instead of 'TOKEN'
dp = updater.dispatcher

dp.add_handler(telegram.ext.CommandHandler("start", start))
dp.add_handler(telegram.ext.MessageHandler(telegram.ext.Filters.text,  mainfunc))

updater.start_polling()
updater.idle()
