import config
from db import db
import time
from telegram import InlineKeyboardButton       # pip3 install python-telegram-bot
from telegram import InlineKeyboardMarkup       # pip3 install telegram
from telegram import CallbackQuery               
import telebot                                  # pip3 install telebot
from telebot import types                       # works only with python3.4 and lower
import logging

logging.basicConfig(filename='theOdds_bot.log', filemode='w', format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.DEBUG)

bot_token = config.token
bot = telebot.TeleBot(token=bot_token)

@bot.message_handler(commands=['help'])
def startGame(message):
    chatId = message.chat.id
    bot.send_message(chatId, '''Hi I'm your What-are-the-odds_bot 🧙‍♂️''')
    time.sleep(3)
    bot.send_message(chatId, '''What Are the Odds, or Odds Are, is a simple game where you dare another player to do a ridiculous task.

And here's how it works:
One player asks another how likely they are to complete a dare, and then the second player picks a number between 2 and 30 as a limit for a number range.
Both players then choose a number within the range. If you choose the same number, the person who was dared must follow through with it!
If the range is from 1 to 2, the Challenger had to do the task if the numbers don't match!

*Note: The one who starts the game is set as the Challenger the one who define the range in the second phase is set as the Challenged. 
Only one game at a time is allowed. It is possible to restart or cancle a running game by enter the start command:  
/1to30''')

    time.sleep(5)
    bot.send_message(chatId, '''To start a game enter: 
/1to30
Enjoy and have Fun🧙‍♂️''')                           

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
        cancleKeyboard = types.InlineKeyboardMarkup()
        cancleKeyboard.add(types.InlineKeyboardButton('Yes! 💣' , callback_data= 'loesche') , types.InlineKeyboardButton('No! 🎬' , callback_data= 'bhalte'))
        bot.send_message(chatId, '''There's already a game running between '''+ str(pendentGame[0][0]) +' as challenger and '+ str(pendentGame[1][0]) +''' as challenged.
Would you like to cancle the running game?''', reply_markup=cancleKeyboard)
    else:  
        gameFirstStep(chatId, nameChallenger)

#Phase one of the game -> Challenged can define range trought buttons 
def gameFirstStep(chatId, nameChallenger):
    dbTable = db(chatId)
    dbTable.storeNameChallenger(nameChallenger)
    menuKeyboard = types.InlineKeyboardMarkup()
    menuKeyboard.add(types.InlineKeyboardButton('💪    2    💪' , callback_data= 2))
    
    sentMessage = bot.send_message(chatId, nameChallenger + ''' challenges to a 1 to 30
Challenged please define a range between 2-30''', reply_markup= menuKeyboard)
    
#Made to build up the button slowly but dont look good as expected -> Changed to build instantly
    for i in range(3, 30, 4):
        menuKeyboardUltra = GenerateMenuKeyboard(menuKeyboard, i)
    bot.edit_message_text(chat_id=chatId, message_id=sentMessage.message_id, text= nameChallenger + ''' challenges to a 1 to 30
Challenged please define a range between 2-30''', reply_markup=menuKeyboardUltra)
        #time.sleep(1)

#Generate the 30 Buttons for phase one 
def GenerateMenuKeyboard(menuKeyboard, i):
    menuKeyboard.add(types.InlineKeyboardButton(i , callback_data= i), 
    types.InlineKeyboardButton(i + 1, callback_data= i + 1),
    types.InlineKeyboardButton(i + 2, callback_data= i + 2),
    types.InlineKeyboardButton(i + 3, callback_data= i + 3)) 
    return menuKeyboard

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
        bot.delete_message(chatId, messageId)
        nameChallenger = query.from_user.first_name
        gameFirstStep(chatId, nameChallenger)

#Answer of phase one (define range)
@bot.callback_query_handler(lambda query: query.data in ['2','3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30'])
def defineRange(query):
    chatId = query.message.chat.id
    dbTable = db(chatId)
    messageId = query.message.message_id
    challenger = dbTable.getChallengerName()
    whoPressedTheButton = query.from_user.first_name
 
    if whoPressedTheButton == challenger: #[0]!!!!!!!!!!!!!!!
        bot.send_message(chatId, whoPressedTheButton +''', you can't play with yourself 😒''')
    else:
        logging.info(str(chatId) +' '+ whoPressedTheButton +' accept the challenge from '+ challenger[0])
        dbTable.storeNameChallenged(whoPressedTheButton)

#Generate dynamic numbers of buttons for phase two (choose number) 
        gameKeyboard = types.InlineKeyboardMarkup()
        for i in range(1, int(query.data) +1):
            gameKeyboard.add(types.InlineKeyboardButton(i , callback_data= i + 100))
            #time.sleep(0.5)  <- Button slowly buid, but dosent look good as expected
        bot.edit_message_text(chat_id=chatId,  message_id=messageId, text= whoPressedTheButton +' accept the challenge by defining a range between 1 and '+ str(query.data) +'''
''' +challenger[0] +' and '+ whoPressedTheButton +', choose your numbers wisely:✨'   , reply_markup=gameKeyboard)
 
#Answer of phase two (choose number) and final compare of the choosen numbers. 
@bot.callback_query_handler(lambda query: query.data in ['101', '102', '103', '104', '105', '106', '107', '108', '109', '110', '111', '112', '113', '114', '115', '116', '117', '118', '119', '120', '121', '122', '123', '124', '125', '126', '127', '128', '129', '130'])
def chooseNumber(query):
    chatId = query.message.chat.id
    dbTable = db(chatId)
    whoPressedTheButton = query.from_user.first_name
    messageId = query.message.message_id
 
    nameChallenger = dbTable.getChallengerName()
    nameChallenged = dbTable.getChallengedName()
    numberChallenger = dbTable.getChallengerNumber()
    numberChallenged = dbTable.getChallengedNumber()
 
    if whoPressedTheButton == nameChallenger[0] and numberChallenger[0] == None:
        dbTable.storeNumberChallenger(int(query.data) -100)
        challengerChoosed = bot.send_message(chatId, whoPressedTheButton +' did choose')
    time.sleep(1.5)

    if whoPressedTheButton == nameChallenged[0] and numberChallenged[0] == None:
        dbTable.storeNumberChallenged(int(query.data) -100)
        challengedChoosed = bot.send_message(chatId, whoPressedTheButton +' did choose')
    time.sleep(1.5)
    
    numberChallenger = dbTable.getChallengerNumber()
    numberChallenged = dbTable.getChallengedNumber()
    if numberChallenger[0] != None and numberChallenged[0] != None:
        
        bot.delete_message(chat_id=chatId, message_id=challengerChoosed.message_id)
        bot.delete_message(chat_id=chatId, message_id=challengedChoosed.message_id)

        bot.edit_message_text(chat_id=chatId, message_id=messageId, text = 'The numbers are chosen! Lets come to the final and compare them in:')
        time.sleep(2.5)
        sentMessage = bot.send_message(chatId, '5') 
        time.sleep(1)
        bot.edit_message_text(chat_id=chatId, message_id=sentMessage.message_id, text = '4')
        time.sleep(1)
        bot.edit_message_text(chat_id=chatId, message_id=sentMessage.message_id, text = '3')
        time.sleep(1)
        bot.edit_message_text(chat_id=chatId, message_id=sentMessage.message_id, text = '😲')
        time.sleep(1)
        bot.edit_message_text(chat_id=chatId, message_id=sentMessage.message_id, text = '😱')
        time.sleep(1)
        bot.edit_message_text(chat_id=chatId, message_id=sentMessage.message_id, text = '😱😱')
        time.sleep(1.5)
        bot.edit_message_text(chat_id=chatId, message_id=sentMessage.message_id, text = '''It's coming soon☝️''')
        time.sleep(1.5)
 
        winKeyboard = types.InlineKeyboardMarkup()
        if numberChallenger[0] == numberChallenged[0]:
            winKeyboard.add(types.InlineKeyboardButton(nameChallenger[0] +'  ⭐ '+ str(numberChallenger[0]) +' ⭐', callback_data= 'qwert'), types.InlineKeyboardButton(nameChallenged[0] +' ⭐ '+ str(numberChallenged[0]) +' ⭐', callback_data= 'qwert'))
        else:
            winKeyboard.add(types.InlineKeyboardButton(nameChallenger[0] +'👉 '+ str(numberChallenger[0]), callback_data= 'qwert'), types.InlineKeyboardButton(nameChallenged[0] +'👉 '+ str(numberChallenged[0]), callback_data= 'qwert'))
         
        bot.delete_message(chat_id=chatId, message_id=messageId)                                    
        bot.edit_message_text(chat_id=chatId, message_id=sentMessage.message_id, text = '🧐', reply_markup=winKeyboard)

        logging.info(str(chatId) +' '+ nameChallenger[0] +' '+ nameChallenged[0] + ' finished the game') 
        dbTable.dropTable()


#Just delete the last messages of the game 
@bot.callback_query_handler(lambda query: query.data == 'qwert')
def deleteFinalMessages(query):
    chatId = query.message.chat.id
    messageId = query.message.message_id
    bot.delete_message(chat_id=chatId, message_id=messageId)
               
#while True:
 #   try:
bot.polling(interval=1)
   # except Exception:
    #    time.sleep(15)