#Библия для телебота
import telebot
from telebot import types
#token = "1367567298:AAHMFlPOzXcJh5L4vLH7_R2LsFWegWcqUcA" #тестовый бот
#from DataBase import ImportExport_v9_test as DB #тестовый бот

class Bot():  
    def __init__(abc, _telebot = "", _token = ""):
        abc.bot =  _telebot.TeleBot(_token)
        abc.users = []
        abc.userStep={}
    #getters
    def getBot(abc):
        if abc.bot is not None:
            return abc.bot
        return False
    def getUsers(abc):
        return abc.users
    def getUserStep(abc, uid):
        if uid in abc.userStep:
            return abc.userStep[uid]
        else:
            abc.users.append(uid)
            abc.userStep[uid] = 0
            #print("New user detected, who hasn't used \"/start\" yet")
        return 0
    #setters
    def setBot(_telebot="", _token=""):
        abc.bot =  _telebot.TeleBot(_token)
    def setUsers(abc, users=[]):
        for user in users:
            abc.users.append(user)
        return True
    def setUserStep(abc, user, step=0):
        abc.userStep[user] = step
    def appendUser(abc, user):
        abc.users.append(user)
    #
    def findUser(abc, chatId):
        for user in abc.users:
            if user["chatId"] == chatId:
                return user
        return False
    def showInfo(abc):
        for user in abc.users:
            print(user.getAllParams())
        print(abc.bot)
        
class Logger():
    def logTelebot(abc):
        logger = telebot.logger
        formatter = telebot.logging.Formatter('[%(asctime)s] %(thread)d {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
                                                      '%m-%d %H:%M:%S')
        ch = telebot.logging.StreamHandler(telebot.sys.stdout)
        logger.addHandler(ch)
        logger.setLevel(telebot.logging.INFO)  # or use logging.INFO
        ch.setFormatter(formatter)
                
    def logMessage(messages):
        for message in messages:
            if message.content_type == 'text':
                print(str(message.chat.first_name) + " [" + str(message.chat.id) + "]: " + message.text)

