import config
from db import db
import time
from telegram import InlineKeyboardButton       # pip3 install python-telegram-bot
from telegram import InlineKeyboardMarkup       # pip3 install telegram
from telegram import CallbackQuery               
import telebot                                  # pip3 install telebot
from telebot import types                       # works only with python3.4 and lower
import logging

logging.basicConfig(level=logging.DEBUG)
logging.basicConfig(filename='onetoThirty.log', filemode='w', format='%(asctime)s - %(message)s')

bot_token = config.token
bot = telebot.TeleBot(token=bot_token)

@bot.message_handler(commands=['help'])
def startGame(message):
    chatId = message.chat.id
    bot.send_message(chatId, '''Hi I'm your OnetoThirty-Bot 🧙‍♂️''')
    time.sleep(1.5)
    bot.send_message(chatId, '''OnetoThirty is a game about challenging friends to do something.''')
    time.sleep(3)
    bot.send_message(chatId, '''And here's how it works:''')
    bot.send_message(chatId, '''The Challenger define first who he like to challenge and what to do.
The Challanged now define a range between two to thirty from which following both player secretly choose an number.
Finaly compare both choosen numbers. If the numbers match the Challenged has to do the stuff.
If the range is from one to two, the Challanger had to do the stuff if the numbers don't match!''')

    bot.send_message(chatId, '''*Note: The one who starts the game is set as the Challanger the one who define the range in the second phase is set as the Challanged. 
Only one game at a time is allowed. It is possible to restart or cancle a running game by enter the start command:  /1to30''')
    time.sleep(5)
    bot.send_message(chatId, '''To start a game enter: /1to30''')                           
    bot.send_message(chatId, '''Enjoy and have Fun🧙‍♂️''')

@bot.message_handler(commands=['1to30'])
def helpMessage(message):
    chatId = message.chat.id
    nameChallenger = message.from_user.first_name
    dbTable = db(chatId)
    logging.info(str(chatId) +' '+ nameChallenger +' starting a game')

    #Create table named chatId if not already exist
    if dbTable.checkTableExist() == False:
        dbTable.createTable()
         
    #Check if a Game ist still running. (If names are in db the game is still running)
    pendentGame = dbTable.checkPendentGame()
    print(pendentGame)
    
    #If a game is still running the user can choose between cancle the game and begin a new one or wait until it's done
    if pendentGame[0] != None or pendentGame[1] != None:
        bot.send_message(chatId, '''There's already a game running between '''+ str(pendentGame[0][0]) +' as challanger and '+ str(pendentGame[1][0]) +' as challanged:')
        cancleKeyboard = types.InlineKeyboardMarkup()
        cancleKeyboard.add(types.InlineKeyboardButton('Yes! 💣' , callback_data= 'loesche') , types.InlineKeyboardButton('No! 🎬' , callback_data= 'bhalte'))
        bot.send_message(chatId, 'Would you like to cancle the running game?', reply_markup=cancleKeyboard)
    else:  
        gameFirstStep(chatId, nameChallenger)

#Phase one of the game -> Challanged can define range trought buttons 
def gameFirstStep(chatId, nameChallenger):
    dbTable = db(chatId)
    dbTable.storeNameChallanger(nameChallenger)
    menuKeyboard = GenerateMenuKeyboard(30)
    bot.send_message(chatId, nameChallenger + ' challenges to a 1 to 30')
    bot.send_message(chatId, 'Challenged please define a range between 2-30', reply_markup=menuKeyboard)

#Generate the 30 Buttons for phase one 
def GenerateMenuKeyboard(numbersOfButtons):
    menuKeyboard = types.InlineKeyboardMarkup()
    menuKeyboard.add(types.InlineKeyboardButton('💪    2    💪' , callback_data= 2))
    i=4
    for i in range(3,numbersOfButtons,4):
        menuKeyboard.add(types.InlineKeyboardButton(i , callback_data= i), 
        types.InlineKeyboardButton(i + 1, callback_data= i + 1),
        types.InlineKeyboardButton(i + 2, callback_data= i + 2),
        types.InlineKeyboardButton(i + 3, callback_data= i + 3)) 
    return menuKeyboard

#Generate dynamic numbers of buttons for phase two (choose number) 
def GenerateGameKeyboard(numbersOfButtons):
    gameKeyboard = types.InlineKeyboardMarkup()
    for i in range(1, numbersOfButtons +1):
        gameKeyboard.add(types.InlineKeyboardButton(i , callback_data= i + 100))
    return gameKeyboard 

#Answer if the user want to keep the running game or cancle it
@bot.callback_query_handler(lambda query: query.data in ['loesche', 'bhalte'])
def handleExistingGame(query):
    chatId = query.message.chat.id
    messageId = query.message.message_id
    whoPressedTheButton = query.from_user.first_name

    #If the user decide to wait until the runnig game is done the bot just do nothing
    if query.data == 'bhalte':
        bot.send_message(chatId, 'Allright we let them finising their game')
        bot.delete_message(chatId, query.message.message_id) 

    #If te User decide to cancle the running game the bot truncate the db table
    else:
        logging.info(str(chatId) +' '+ whoPressedTheButton +' canceled pendent game') 
        dbTable = db(chatId)
        dbTable.cancleGame()
        deleteMessage(chatId, messageId) 
        nameChallenger = query.from_user.first_name
        gameFirstStep(chatId, nameChallenger)
         
def deleteMessage(chatId, messageId):
    bot.delete_message(chatId, messageId)
    bot.delete_message(chatId, messageId-1)

#Answer of phase one (define range)
@bot.callback_query_handler(lambda query: query.data in ['2','3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30'])
def defineRange(query):
    chatId = query.message.chat.id
    dbTable = db(chatId)
    messageId = query.message.message_id
    challanger = dbTable.getChallangerName()
    whoPressedTheButton = query.from_user.first_name
 
    if whoPressedTheButton == challanger[0]: #[0]!!!!!!!!!!!!!!!
        bot.send_message(chatId, whoPressedTheButton +''', you can't play with yourself 😒''')
    else:
        logging.info(str(chatId) +' '+ whoPressedTheButton +' accept the challange from '+ challanger[0])
        dbTable.storeNameChallanged(whoPressedTheButton)
        bot.delete_message(chatId, messageId)
        gameKeyboard = GenerateGameKeyboard(int(query.data))
        bot.send_message(chatId, whoPressedTheButton +' accept the challange by defining a range between 1 and '+ str(query.data))
        bot.send_message(chatId, challanger[0] +' and '+ whoPressedTheButton +', choose wisely:✨'   , reply_markup=gameKeyboard)
 
#Answer of phase two (choose number) and final compare of the choosen numbers. 
@bot.callback_query_handler(lambda query: query.data in ['101', '102', '103', '104', '105', '106', '107', '108', '109', '110', '111', '112', '113', '114', '115', '116', '117', '118', '119', '120', '121', '122', '123', '124', '125', '126', '127', '128', '129', '130'])
def chooseNumber(query):
    chatId = query.message.chat.id
    dbTable = db(chatId)
    whoPressedTheButton = query.from_user.first_name
    messageId = query.message.message_id
 
    nameChallanger = dbTable.getChallangerName()
    nameChallanged = dbTable.getChallangedName()
    numberChallanger = dbTable.getChallangerNumber()
    numberChallanged = dbTable.getChallangedNumber()
 
    if whoPressedTheButton == nameChallanger[0] and numberChallanger[0] == None:
        dbTable.storeNumberChallanger(int(query.data) -100)
        bot.send_message(chatId, whoPressedTheButton +' did choose')
    time.sleep(1)

    if whoPressedTheButton == nameChallanged[0] and numberChallanged[0] == None:
        dbTable.storeNumberChallanged(int(query.data) -100)
        bot.send_message(chatId, whoPressedTheButton +' did choose')
    time.sleep(1)

    if numberChallanger[0] != None and numberChallanged[0] != None:
        bot.send_message(chatId, 'The numbers are chosen! Lets come to the final and compare them in:')
        time.sleep(1)

        bot.send_message(chatId, 5)  
        time.sleep(1)
        bot.send_message(chatId, 4)
        time.sleep(1)
        bot.send_message(chatId, 3)
        time.sleep(1)
        bot.send_message(chatId, '😲')
        time.sleep(1)
        bot.send_message(chatId, '😱')
        time.sleep(1)
        bot.send_message(chatId, '😱')
        time.sleep(1)
 
        winKeyboard = types.InlineKeyboardMarkup()
         
        if numberChallanger[0] == numberChallanged[0]:
            winKeyboard.add(types.InlineKeyboardButton(nameChallanger[0] +'  ⭐ '+ str(numberChallanger[0]) +' ⭐', callback_data= 'qwert'), types.InlineKeyboardButton(nameChallanged[0] +' ⭐ '+ str(numberChallanged[0]) +' ⭐', callback_data= 'qwer'))
        else:
            winKeyboard.add(types.InlineKeyboardButton(nameChallanger[0] +'👉 '+ str(numberChallanger[0]), callback_data= 'qwert'), types.InlineKeyboardButton(nameChallanged[0] +'👉 '+ str(numberChallanged[0]), callback_data= 'qwer'))
         
        bot.send_message(chatId, ':', reply_markup=winKeyboard)

        logging.info(str(chatId) +' '+ nameChallanger[0] +' '+ nameChallanged[0] + ' finished the game') 
        dbTable.dropTable()

#Just delete the last messages of the game 
@bot.callback_query_handler(lambda query: query.data == 'qwert')
def deleteFinalMessages(query):
    chatId = query.message.chat.id
    messageId = query.message.message_id
    for i in range(12):
        bot.delete_message(chatId, messageId-i)
               
bot.polling(interval=1)