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
    database[datasheet.cell(count,1).value] = [datasheet.cell(count,2).value,datasheet.cell(count,3).value, count, [datasheet.cell(count, 4).value], [datasheet.cell(count,5).value]] 
    count+=1

def endMessage(update, context,user):
    typeddata = onlineusers[user][2]
    
    message = "Перевірте чи все введено правильно, у разі потреби зміни даних, натисніть відповідну цифру\n"

    if user in database:
        message += "3) Маршрут: " + typeddata[2] + "\n4) Заправка денна: " + typeddata[3] + "\n5) Номер паливної картки: " + typeddata[4] + "\n6) Вид палива: " + typeddata[5] + "\n7) Кінцевий пробіг: " + typeddata[6] +"\n8) Залишок палива: " + typeddata[7] + "\n9) Кількість клієнтів: " + typeddata[8]
        context.bot.send_message(chat_id=update.effective_chat.id, text = message, reply_markup=ReplyKeyboardMarkup([[KeyboardButton("3"),KeyboardButton("4"),KeyboardButton("5"),KeyboardButton("6")],[KeyboardButton("7"),KeyboardButton("8"),KeyboardButton("9")], [KeyboardButton("Все файно")]]))
    else:
        message += "1) Водій: " + typeddata[0] + "\n2) Авто: " + typeddata[1] + "\n3) Маршрут: " + typeddata[2] + "\n4) Заправка денна: " + typeddata[3] + "\n5) Номер паливної картки: " + typeddata[4] + "\n6) Вид палива: " + typeddata[5] + "\n7) Кінцевий пробіг: " + typeddata[6] +"\n8) Залишок палива: " + typeddata[7] + "\n9) Кількість клієнтів: " + typeddata[8]
        context.bot.send_message(chat_id=update.effective_chat.id, text = message, reply_markup=ReplyKeyboardMarkup([[KeyboardButton("1"),KeyboardButton("2"),KeyboardButton("3"),KeyboardButton("4")],[KeyboardButton("5"),KeyboardButton("6"),KeyboardButton("7"),KeyboardButton("8")], [KeyboardButton("9")],[KeyboardButton("Все файно")]]))

def driver(update, context, user):
    onlineusers[user][2][0] = update.message.text
    onlineusers[user][1]+=1    
    onlineusers[user].append(0)
    context.bot.send_message(chat_id=update.effective_chat.id, text = "Вкажіть назву авто", reply_markup=InlineKeyboardMarkup(cars[0]))

def changeDriver(update, context, user):
    onlineusers[user][2][0] = update.message.text
    onlineusers[user][1] = 9 
    endMessage(update, context, user) 
    

def carChoosing(update, context):
    user = update.effective_user.username
    query = update.callback_query.data


    if "back" in query:
        onlineusers[user][3]-=1
        context.bot.edit_message_reply_markup(chat_id=update.effective_chat.id, message_id = update.callback_query.message.message_id, reply_markup=InlineKeyboardMarkup(cars[onlineusers[user][3]]))
    elif "forward" in query:
        onlineusers[user][3]+=1
        context.bot.edit_message_reply_markup(chat_id=update.effective_chat.id, message_id = update.callback_query.message.message_id, reply_markup=InlineKeyboardMarkup(cars[onlineusers[user][3]]))
        
    else:
        onlineusers[user][2][1] = query
        if onlineusers[user][1]==11:
            onlineusers[user][1]=9
            endMessage(update, context, user) 
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text = "Вкажіть Маршрут")
            onlineusers[user][1]+=1    
        


def error(update,context,user):
    update.message.reply_text("Виберіть машину!")
    context.bot.send_message(chat_id=update.effective_chat.id, text = "Вкажіть назву авто", reply_markup=InlineKeyboardMarkup(cars[0]))

def route(update, context, user):
    text = (update.message.text).replace(" ","").replace("-","").lower()  
    if text in routes:
        text = routes[text]
        onlineusers[user][2][2] = text
            
    update.message.reply_text("Заправка денна")
    onlineusers[user][1]+=1    

def changeRoute(update,message, user):
    text = (update.message.text).replace(" ","").replace("-","").lower()  
    if text in routes:
        text = routes[text]
        onlineusers[user][2][2] = text
            
    onlineusers[user][1]=9    
    endMessage(update, message, user)

    
    

def refill(update, context, user):
    onlineusers[user][2][3] = update.message.text
    if user in database: 
        datacards = database[user][4]
        buttons = []
        for numbers in datacards:
            buttons.append([KeyboardButton(numbers)])
        context.bot.send_message(chat_id=update.effective_chat.id, text="Номер паливної картки", reply_markup=ReplyKeyboardMarkup(buttons))
    else:
        update.message.reply_text("Номер паливної картки")
    onlineusers[user][1]+=1    

def changeRefill(update, context, user):
    onlineusers[user][2][3] = update.message.text
    onlineusers[user][1]=9    

    endMessage(update, context, user)

def fuelcard(update, context, user):
    onlineusers[user][2][4] = update.message.text
    context.bot.send_message(chat_id=update.effective_chat.id, text = "Вид палива", reply_markup=ReplyKeyboardMarkup([[KeyboardButton("ДП")],[KeyboardButton("ДП+")],[KeyboardButton("A95")],[KeyboardButton("A95+")]]))
    onlineusers[user][1]+=1    

def changeFuelcard(update, context, user):
    onlineusers[user][2][4] = update.message.text
    onlineusers[user][1]=9    

    endMessage(update, context, user)

def fueltype(update, context, user):
    text = update.message.text
    if text == "ДП" or text=="ДП+" or text == "A95" or text == "A95+":
        onlineusers[user][2][5]=text
        update.message.reply_text("Кінцевий пробіг")
        onlineusers[user][1]+=1    
        return
    context.bot.send_message(chat_id=update.effective_chat.id, text = "Виберіть вид палива із запропонованих", reply_markup=ReplyKeyboardMarkup([[KeyboardButton("ДП")],[KeyboardButton("ДП+")],[KeyboardButton("A95")],[KeyboardButton("A95+")]]))

def changeFueltype(update, context, user):
    text = update.message.text
    if text == "ДП" or text=="ДП+" or text == "A95" or text == "A95+":
        onlineusers[user][2][5]=text
        onlineusers[user][1]=9    
        endMessage(update, context, user)
        return
    context.bot.send_message(chat_id=update.effective_chat.id, text = "Виберіть вид палива із запропонованих", reply_markup=ReplyKeyboardMarkup([[KeyboardButton("ДП")],[KeyboardButton("ДП+")],[KeyboardButton("A95")],[KeyboardButton("A95+")]]))
    
    

def result(update, context, user):
    onlineusers[user][2][6]=update.message.text
    update.message.reply_text("Залишок")
    onlineusers[user][1]+=1    

def changeResult(update, context, user):
    onlineusers[user][2][6] = update.message.text
    onlineusers[user][1]=9    

    endMessage(update, context, user)

def remainder(update, context, user):
    onlineusers[user][2][7] = update.message.text
    update.message.reply_text("Кількість клієнтів")
    onlineusers[user][1]+=1    

def changRemainder(update, context, user):
    onlineusers[user][2][7] = update.message.text
    onlineusers[user][1]=9    

    endMessage(update, context, user)
    

def clientsamount(update, context, user):
    onlineusers[user][2][8] = update.message.text
    onlineusers[user][1]+=1
    
    endMessage(update, context, user)

def changeClientsAm(update, context, user):
    onlineusers[user][2][8] = update.message.text
    onlineusers[user][1]=9    

    endMessage(update, context, user)

def IneedChangeSomething(update, context, user):
    msg = update.message.text 
    if msg == "Все файно":
        updateFunction(user, update, context)
    else:
        if msg=="1":
            update.message.reply_text("Введіть своє прізвище та ім'я")
            onlineusers[user][1]=10
        elif msg=="2":
            onlineusers[user][1]=11
            context.bot.send_message(chat_id=update.effective_chat.id, text = "Вкажіть назву авто", reply_markup=InlineKeyboardMarkup(cars[0]))
        elif msg=="3":
            onlineusers[user][1]=12
            update.message.reply_text("Введіть маршрут")
        elif msg=="4":
            onlineusers[user][1]=13
            update.message.reply_text("Заправка денна")
        elif msg=="5":
            onlineusers[user][1]=14
            if user in database:
                datacards = database[user][4]
                buttons = []
                for numbers in datacards:
                    buttons.append([KeyboardButton(numbers)])
                context.bot.send_message(chat_id=update.effective_chat.id, text="Номер паливної картки", reply_markup=ReplyKeyboardMarkup(buttons))
            else:
                update.message.reply_text("Номер паливної картки")
        elif msg=="6":
            onlineusers[user][1]=15
            context.bot.send_message(chat_id=update.effective_chat.id, text = "Вид палива", reply_markup=ReplyKeyboardMarkup([[KeyboardButton("ДП")],[KeyboardButton("ДП+")],[KeyboardButton("A95")],[KeyboardButton("A95+")]]))
        elif msg=="7":
            onlineusers[user][1]=16
            update.message.reply_text("Кінцевий пробіг")
        elif msg=="8":
            onlineusers[user][1]=17
            update.message.reply_text("Залишок пального")
        elif msg=="9":
            onlineusers[user][1]=18
            update.message.reply_text("Кількість клієнтів")
            

def updateFunction(user, update, context):
    data = onlineusers[user][2]
    for i in range(9):
        sheet.update_cell(onlineusers[user][0], i+4, data[i])

    if user in database:
        datasheet.update_cell(database[user][2], 4, data[2])
        datasheet.update_cell(database[user][2], 5, data[4])

        print(database)
        print(data)
        
        routes = database[user][3]
        if not data[2] in routes:
            if len(routes)==5:
                routes.pop(0)
            routes.append(data[2])

        fuelcards = database[user][4]
        if not data[4] in fuelcards:
            if len(fuelcards)==4:
                fuelcards.pop(0)
            fuelcards.append(data[4])
    else:
        count = int(datasheet.cell(1,8).value)
        datasheet.update_cell(1,8, str(count+1))
        database[user] = [data[0], data[1], count, data[2], data[4]]

        datasheet.update_cell(count, 1, user)
        datasheet.update_cell(count, 2, data[0])
        datasheet.update_cell(count, 3, data[1])
        datasheet.update_cell(count, 4, data[2])
        datasheet.update_cell(count, 5, data[4])
    
    buttons = [[KeyboardButton(arrmsg)]]
    context.bot.send_message(chat_id=update.effective_chat.id, text = "Дякую, наступного разу натисніть кнопу: я приїхав", reply_markup=ReplyKeyboardMarkup(buttons))

func = [driver, error, route, refill, fuelcard, fueltype,result, remainder,  clientsamount, IneedChangeSomething, changeDriver, error, changeRoute, changeRefill, changeFuelcard, changeFueltype, changeResult, changRemainder, changeClientsAm]

print(len(func))

def start(update, context):
    buttons = [[KeyboardButton(arrmsg)]]
    context.bot.send_message(chat_id=update.effective_chat.id, text = "Бот для ведення контролю", reply_markup=ReplyKeyboardMarkup(buttons))


def mainfunc(update, context):
    user = update.effective_user.username

    if update.message.text == arrmsg:
        global inc
        inc += 1
        onlineusers[user] = [inc, 0, ["","","","","","","","",""]] 
        sheet.update_cell(onlineusers[user][0], 2, str(date.today()))
        sheet.update_cell(onlineusers[user][0], 3, str(datetime.now(pytz.timezone('Europe/Kiev')).strftime("%H:%M")))
        if user in database:
            onlineusers[user][2][0] = database[user][0]
            onlineusers[user][2][1] = database[user][1]
            onlineusers[user][1]= 2 
            buttons = []
            for routename in database[user][3]:
                buttons.append([KeyboardButton(routename)])
            
            context.bot.send_message(chat_id=update.effective_chat.id, text = "Вкажіть Маршрут", reply_markup = ReplyKeyboardMarkup(buttons))
        else:    
            update.message.reply_text("Вкажіть своє ім'я")

        datasheet.update_cell(1,7, str(inc))
        return
    func[onlineusers[user][1]](update,context,user)

    

updater = telegram.ext.Updater('5409836173:AAG1igVGCbsV1AhmjKFs_gQ8w8bLGhBIdsE', use_context = True)
#put your telegram bot token instead of 'TOKEN'
dp = updater.dispatcher

dp.add_handler(telegram.ext.CommandHandler("start", start))
dp.add_handler(telegram.ext.MessageHandler(telegram.ext.Filters.text,  mainfunc))
dp.add_handler(telegram.ext.CallbackQueryHandler(carChoosing))

updater.start_polling()
updater.idle()
