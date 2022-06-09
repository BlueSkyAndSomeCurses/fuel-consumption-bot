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
routes = dict()

cars = [
    [[InlineKeyboardButton("Volvo AT1609BI", callback_data = "Volvo AT1609BI")],
    [InlineKeyboardButton("Volvo AT2463AI", callback_data = "Volvo AT2463AI")],
    [InlineKeyboardButton("MB AT9564BH", callback_data = "MB AT9564BH")],
    [InlineKeyboardButton("MB AT2569AB", callback_data = "MB AT2569AB")],
    [InlineKeyboardButton("MB AT7143AI", callback_data = "MB AT7143AI")],
    [InlineKeyboardButton("Вперед", callback_data = "forward")]
    ],
    [[InlineKeyboardButton("MB AT0638AP", callback_data = "MB AT0638AP")],
    [InlineKeyboardButton("MB BC9613CH", callback_data = "MB BC9613CH")],
    [InlineKeyboardButton("MB AT2133AP", callback_data = "MB AT2133AP")],
    [InlineKeyboardButton("MB AT9780AP", callback_data = "MB AT9780AP")],
    [InlineKeyboardButton("MB AT8993BT", callback_data = "MB AT8993BT")],
    [InlineKeyboardButton("Назад", callback_data = "back"), InlineKeyboardButton("Вперед", callback_data = "forward")]
    ],
    [[InlineKeyboardButton("Renault AT4191AE", callback_data = "Renault AT4191AE")],
    [InlineKeyboardButton("Renault AT1778EA", callback_data = "Renault AT1778EA")],
    [InlineKeyboardButton("Renault AT1779EA", callback_data = "Renault AT1779EA")],
    [InlineKeyboardButton("Renault AT4974EI", callback_data = "Renault AT4974EI")],
    [InlineKeyboardButton("Renault AT1784EI", callback_data = "Renault AT1784EI")],
    [InlineKeyboardButton("Назад", callback_data = "back")]
    ],
    
    ]

rots = open("rot.txt", "r").readlines()


for i in range(len(rots)):
    rots[i] = rots[i][0:-1]
    routes[rots[i].replace(" ","").replace("-","").lower()] = rots[i]

print(routes)
rots.clear()

count = 1
while datasheet.cell(count, 1).value:
    database[datasheet.cell(count,1).value] = [datasheet.cell(count,2).value,datasheet.cell(count,3).value, count] 
    count+=1



def binarysearch(word, left, right):
    mid = (left+right)//2
    looking = lower(round[mid].replace(" ", ""))
    if word > routes[mid]:
        return binarysearch(word, mid+1, right)
    elif word < round[mid]:
        return binarysearch(word, left, mid -1)
    else:
        return routes[mid]



def driver(update, context, user):
    msg = update.message.text
    sheet.update_cell(onlineusers[user][0], onlineusers[user][1], msg)
    database[user][0] = msg
    datasheet.update_cell(database[user][2], 2, msg)
    onlineusers[user][1]+=1    
    onlineusers[user].append(0)
    context.bot.send_message(chat_id=update.effective_chat.id, text = "Вкажіть назву авто", reply_markup=InlineKeyboardMarkup(cars[0]))

def carChoosing(update, context):
    user = update.effective_user.username
    query = update.callback_query.data


    if "back" in query:
        onlineusers[user][2]-=1
        context.bot.edit_message_reply_markup(chat_id=update.effective_chat.id, message_id = update.callback_query.message.message_id, reply_markup=InlineKeyboardMarkup(cars[onlineusers[user][2]]))
    elif "forward" in query:
        onlineusers[user][2]+=1
        context.bot.edit_message_reply_markup(chat_id=update.effective_chat.id, message_id = update.callback_query.message.message_id, reply_markup=InlineKeyboardMarkup(cars[onlineusers[user][2]]))
        
    else:
        sheet.update_cell(onlineusers[user][0], 5, query)
        database[user][1] = query
        datasheet.update_cell(database[user][2], 3, query)
        context.bot.send_message(chat_id=update.effective_chat.id, text = "Вкажіть Маршрут")
        onlineusers[user][1]+=1    
        
        

def error(update,context,user):
    update.message.reply_text("Виберіть машину!")
    context.bot.send_message(chat_id=update.effective_chat.id, text = "Вкажіть назву авто", reply_markup=InlineKeyboardMarkup(cars[0]))

def route(update, context, user):
    text = (update.message.text).replace(" ","").replace("-","").lower()  
    print(text)
    if text in routes:
        sheet.update_cell(onlineusers[user][0], 6, routes[text])
    update.message.reply_text("Заправка денна")
    onlineusers[user][1]+=1    

def refill(update, context, user):
    sheet.update_cell(onlineusers[user][0], 7, update.message.text)
    update.message.reply_text("Номер паливної картки")
    onlineusers[user][1]+=1    

def fuelcard(update, context, user):
    sheet.update_cell(onlineusers[user][0], 8, update.message.text)
    context.bot.send_message(chat_id=update.effective_chat.id, text = "Вид палива", reply_markup=ReplyKeyboardMarkup([[KeyboardButton("ДП")],[KeyboardButton("ДП+")],[KeyboardButton("A95")],[KeyboardButton("A95+")]]))
    onlineusers[user][1]+=1    

def fueltype(update, context, user):
    text = update.message.text
    if text == "ДП" or text=="ДП+" or text == "A95" or text == "A95+":
        sheet.update_cell(onlineusers[user][0], 9, text)
        update.message.reply_text("Кінцевий пробіг")
        onlineusers[user][1]+=1    
        return
    context.bot.send_message(chat_id=update.effective_chat.id, text = "Виберіть вид палива із запропонованих", reply_markup=ReplyKeyboardMarkup([[KeyboardButton("ДП")],[KeyboardButton("ДП+")],[KeyboardButton("A95")],[KeyboardButton("A95+")]]))
    

def result(update, context, user):
    sheet.update_cell(onlineusers[user][0], 10, update.message.text)
    update.message.reply_text("Залишок")
    onlineusers[user][1]+=1    

def remainder(update, context, user):
    sheet.update_cell(onlineusers[user][0], 11, update.message.text)
    update.message.reply_text("Кількість клієнтів")
    onlineusers[user][1]+=1    

def clientsamount(update, context, user):
    sheet.update_cell(onlineusers[user][0], 12, update.message.text)
    context.bot.send_message(chat_id=update.effective_chat.id, text = "Дякую", reply_markup=ReplyKeyboardMarkup([[arrmsg]]))
    onlineusers.pop(user)

func = [driver, error, route, refill, fuelcard, fueltype,result, remainder,  clientsamount]

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
dp.add_handler(telegram.ext.CallbackQueryHandler(carChoosing))

updater.start_polling()
updater.idle()
