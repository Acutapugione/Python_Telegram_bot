IS_TEST = True
#Библия для телебота
import telebot
from telebot import types
#from telebot import apihelper
#apihelper.proxy = {'http':'http://10.10.1.10:3128'}

#Библия для массивов и списков
from struct import *
from array import *

#Библия для работы с файлами
import os
cwd = os.getcwd()

#Библия для работы с Firebird
import firebirdsql as fdb
import datetime
import time
import pypyodbc

#Импортируем модуль работы с БД

if IS_TEST:
    from DataBase import ImportExport_v9_test as DB #тестовый бот
else:
    from DataBase import ImportExport_v9 as DB #original bot

if IS_TEST:
    token = "1367567298:AAHMFlPOzXcJh5L4vLH7_R2LsFWegWcqUcA" #тестовый бот
else:
    token = "1363230798:AAFLiTK4sLDtMAwuaSZb8K1dZKfGQP7b2Os" #original bot
bot = telebot.TeleBot(token)

float_in_text=0;
escape=0;

user_dict = {}
class User:
    def __init__(self, naryad):#ctor
        #print(self," ctor ")
        self.naryad = naryad
        keys = ['name_skz','skz_id','inv',
                'city','adres',
                'longitude','latitude',
                'info','sustain','vid_rabot','tz'
                'u','i',
                'p_bottom','p_top',
                'p_on','p_off',
                'tz_u','tz_i',
                'p1','p2',
                'pokazanie',
                'energy_active','energy_reactive','energy_generation',
                'fio',
                'name_tz','tz_id','categorie']        
        for key in keys:
            self.key = None
            
@bot.message_handler(commands=['start'])
def start_message(message): # 1 шаг выбор наряда
        chat_id = message.chat.id
        user_dict[chat_id] = User(message.text)
        #с 0 до 6 часов — ночь
        #с 6 до 12 часов — утро
        #с 12 до 18 часов — день
        #с 18 до 24 часов — вечер
        FIO = ''
        User.fio = ''
        chat_array = []
        chat_array = DB.DRW.check_id(message)
        if len(chat_array)>0:
            for element in chat_array:
                FIO = element.split(" ; ")[0].strip()   
        if len(FIO)>0:
            User.fio = str(FIO)
            start_with_login(message)
            return
        else:
            # удалить старую клавиатуру
            markup = types.ReplyKeyboardRemove(selective=False)
            keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True,
                                                 resize_keyboard=True)
            reg_button = types.KeyboardButton(text="Пройти аутентификацию",
                                              request_contact=True)
            keyboard.add(reg_button)
            response = bot.reply_to(message,
                                        day_time(message)+
                                        "для начала работы,\n"
                                        "пройдите аутентификацию", 
                                        reply_markup=keyboard)
        
def start_with_login(message):
        chat_id = message.chat.id
        user_dict[chat_id] = User(message.text)
        # удалить старую клавиатуру
        markup = types.ReplyKeyboardRemove(selective=False)
        keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True,
                                             resize_keyboard=True)
        #Обращение к БД и получение № наряда
        try:
            my_array = DB.Naryad.get_naryad_new(User.fio)
            count=0
            for element in my_array:
                # удалить старую клавиатуру
                markup = types.ReplyKeyboardRemove(selective=False)
                keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True,
                                                     resize_keyboard=True)
                itembtn = types.KeyboardButton(text = str(element))
                keyboard.add(itembtn)
                count+=1
            if count == 0:
                # удалить старую клавиатуру
                markup = types.ReplyKeyboardRemove(selective=False)
                keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True,
                                                     resize_keyboard=True)
                today = datetime.datetime.today()
                date = today.strftime("%H:%M:%d")
                msg = bot.reply_to(message, day_time(message)+
                                       'Ваших нарядов нет в списке.'
                                       '\nОбратитесь к своему мастеру.',
                                       reply_markup=keyboard )
                regular_in_main(message)
                return
            else:                    
                #Обращение к БД и получение № наряда
                try:
                    my_array = DB.Naryad.get_naryad_new(User.fio)
                    # удалить старую клавиатуру
                    markup = types.ReplyKeyboardRemove(selective=False)
                    keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True,
                                                         resize_keyboard=True)
                    for element in my_array:
                        itembtn = types.KeyboardButton(text = str(element))
                        keyboard.add(itembtn)
                    msg = bot.reply_to(message,
                                           day_time(message)+
                                           'Выберите наряд.',
                                           reply_markup=keyboard)
                    print(str(User.fio)+ ' начал работу с ботом')
                    bot.register_next_step_handler(msg, process_step_2)
                except Exception as e:
                    print(str(User.fio)+" call err:" +str(e) + " in start_with_login")
        except Exception as e:
            print(str(User.fio)+" call err:" +str(e)+ " in start_with_login")
            regular_in_main(message)
            return

@bot.message_handler(commands=['back']) 
def regular_in_main(message): # Регулярное выражение если
    #сохраняем введенные данные в класс
    chat_id = message.chat.id
    user_dict[chat_id] = User(message.text)

    markup = types.ReplyKeyboardRemove(selective=False)
    keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True,
                                         resize_keyboard=True)
    FIO = ''
    User.fio = ''
    chat_array = []
    chat_array = DB.DRW.check_id(message)
    if len(chat_array)>0:
        for element in chat_array:
            FIO = element.split(";")[0].strip()     
    if len(FIO)>0:
        User.fio = str(FIO)
        #Обращение к БД и получение № наряда
        my_array = DB.Naryad.get_naryad_new(User.fio)
        for element in my_array:
            itembtn = types.KeyboardButton(text = str(element))
            keyboard.add(itembtn)
        msg = bot.reply_to(message, 'Продолжайте, '
                                + str(User.fio)+
                                '.\nВыберите еще раз наряд.',
                               reply_markup=keyboard )
        print(str(User.fio)+
              ' вернулся в начало и начал работу с ботом')
        bot.register_next_step_handler(msg, process_step_2)
    else:
        markup = types.ReplyKeyboardRemove(selective=False)
        keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True,
                                             resize_keyboard=True)
        reg_button = types.KeyboardButton(text='Пройти аутентификацию',
                                              request_contact=True)
        keyboard.add(reg_button)
        response = bot.reply_to(message,
                                    day_time(message)+
                                    'для начала работы,\n'
                                    "пройдите аутентификацию",
                                    reply_markup=keyboard)
    return

@bot.message_handler(content_types=['contact'])
def contact_handler(message):
    #сохраняем введенные данные в класс
    chat_id = message.chat.id
    user_dict[chat_id] = User(message.text)
    # удалить старую клавиатуру
    markup = types.ReplyKeyboardRemove(selective=False)
    keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    if message.contact is not None: 
        my_array = DB.DRW.login(message)
        count_of_my_array = 0 
        if len(my_array)>0:
            for element in my_array:
                count_of_my_array+=1
                if count_of_my_array == 1:
                    FIO = element.split(";")[0].strip()
                    User.fio = str(FIO)
                    print(User.fio)
                    start_with_login(message)
                    return
        if count_of_my_array == 0:
            FIO = message.contact.first_name
            User.fio = str(FIO)
            bot.reply_to(message,"Извините, "
                                     +str(User.fio)+
                                     ".\nВам нельзя сюда, "
                                     "попробуйте еще раз "
                                     "или обратитесь к "
                                     "своему Мастеру")
            
# Default command handler. A lambda expression which always returns True is used for this purpose.
@bot.message_handler(func=lambda message: True, content_types=['location'])
def geo_get(message):
    chat_id = message.chat.id
    try:
        user = user_dict[chat_id]
    except Exception as errorMsg:
        user = 0
    # удалить старую клавиатуру
    markup = types.ReplyKeyboardRemove(selective=False)
    keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True,
                                         resize_keyboard=True)
    try:
        if message.location is None:
            process_step_2(message)
            return
        else:
            if user.categorie != 0 and message.location is not None:
                msg = bot.reply_to(message, "Долгота: "+str(message.location.longitude)+
                             ", широта: "+str(message.location.latitude))
                user.longitude = message.location.longitude
                user.latitude = message.location.latitude
            else:
                msg = bot.reply_to(message,
                                   "К сожалению что-то не получилось\n"
                                   "попробуйте еще раз!!!\n"
                                   "Для отмены нажмите /back",
                                   reply_markup=keyboard)
                process_step_2(message)
                return
    except Exception as e:
        msg = bot.reply_to(message,
                               "К сожалению что-то не получилось\n"
                               "попробуйте еще раз.\n"
                               "Для отмены нажмите /back",
                               reply_markup=keyboard)
        print(str(User.fio)+" call err:" +str(e)+ " in geo_get")
        process_step_2(message)
        return
    if user.tz is None:
        process_step_3(message)
        return
    if user.vid_rabot == "Діаграмма" and user.tz == 1:
        #Пошли по диаграмме
        step_enter_p_if_online(message)       
        return
    
    if user.vid_rabot == "Перевірка ІФЗ" and user.tz == 1:
        #Пошли по проверке эффективности
        step_enter_p_bottom_part(message)
        return
    
    if user.vid_rabot == "ТО ПМ" and user.tz == 1:
        #Пошли по техосмотру протекторов
        step_enter_protectors_U(message)
        return
    else:
        process_step_3(message)
        return
    return

    
    #Диаграмма
    #Вводим P при вкл
def step_enter_p_if_online(message):
    text = message.text          
    chat_id = message.chat.id
    try:
        user = user_dict[chat_id]
    except Exception as e: 
        user = 0
        print(str(User.fio)+" call err:" +str(e)+ " in step_enter_p_if_online")
        regular_in_main(message)
        return
    # удалить старую клавиатуру
    keyboard = types.ReplyKeyboardRemove()  
    msg = bot.reply_to(message, "Введите потенциал ИФС при включенной СКЗ",
                        reply_markup=keyboard)
    bot.register_next_step_handler(message,step_get_p_if_online)
    return
    
    #Записываем P при вкл
def step_get_p_if_online(message):
        text = message.text          
        chat_id = message.chat.id
        try:
            user = user_dict[chat_id]
        except Exception as e: 
            user = 0
            print(str(User.fio)+" call err:" +str(e)+ " in step_get_p_if_online")
            regular_in_main(message)
            return
        float_in_text = controll_vvoda_mess(message)
            
        if text is None or '/' in text or float_in_text is None:
            step_enter_p_if_online(message)
            return
        else:
            user.p_on = str(float_in_text)
            step_enter_p_if_offline(message)
        return
    
    #Вводим P при выкл
def step_enter_p_if_offline(message):
        text = message.text          
        chat_id = message.chat.id
        try:
            user = user_dict[chat_id]
        except Exception as e: 
            user = 0
            print(str(User.fio)+" call err:" +str(e)+ " in step_enter_p_if_offline")
            regular_in_main(message)
            return
        # удалить старую клавиатуру
        keyboard = types.ReplyKeyboardRemove()
        msg = bot.reply_to(message, "Введите потенциал ИФС при выключенной СКЗ",
                           reply_markup=keyboard)
        bot.register_next_step_handler(message,step_get_p_if_offline)
        return
    
    #Записываем P при выкл
def step_get_p_if_offline(message):
        text = message.text          
        chat_id = message.chat.id
        try:
            user = user_dict[chat_id]
        except Exception as e: 
            user = 0
            print(str(User.fio)+" call err:" +str(e)+ " in step_get_p_if_offline")
            
            regular_in_main(message)
            return
        float_in_text = controll_vvoda_mess(message)
        if text is None or '/' in text or float_in_text is None:
            step_enter_p_if_offline(message)
            return
        else:
            user.p_off = str(float_in_text)
            process_step_4_energy_type(message)
        return
    
    #Проверка ИФС
    #Вводим P нижней части
def step_enter_p_bottom_part(message):
        text = message.text          
        chat_id = message.chat.id
        try:
            user = user_dict[chat_id]
        except Exception as e: 
            user = 0
            print(str(User.fio)+" call err:" +str(e)+ " in step_enter_p_bottom_part")
            
            regular_in_main(message)
            return
        # удалить старую клавиатуру
        keyboard = types.ReplyKeyboardRemove()
        msg = bot.reply_to(message, "Введите потенциал на нижней части ИФС",
                           reply_markup=keyboard)
        bot.register_next_step_handler(message,step_get_p_bottom_part)
        return
    
    #Записываем P нижней части
def step_get_p_bottom_part(message):
        text = message.text          
        chat_id = message.chat.id
        try:
            user = user_dict[chat_id]
        except Exception as e: 
            user = 0
            print(str(User.fio)+" call err:" +str(e)+ " in step_get_p_bottom_part")
            
            regular_in_main(message)
            return
        float_in_text = controll_vvoda_mess(message)
            
        if text is None or '/' in text or float_in_text is None:
            step_enter_p_bottom_part(message)
            return
        else:
            user.p_bottom = str(float_in_text)
            step_enter_p_top_part(message)
        return

    #Вводим P верхней части
def step_enter_p_top_part(message):
        text = message.text          
        chat_id = message.chat.id
        try:
            user = user_dict[chat_id]
        except Exception as e: 
            user = 0
            print(str(User.fio)+" call err:" +str(e)+ " in step_enter_p_top_part")
            
            regular_in_main(message)
            return
        # удалить старую клавиатуру
        keyboard = types.ReplyKeyboardRemove()
        msg = bot.reply_to(message,
                           "Введите потенциал на верхней части ИФС",
                           reply_markup=keyboard)
        bot.register_next_step_handler(message,step_get_p_top_part)
        return

    #Записываем P верхней части
def step_get_p_top_part(message):
        text = message.text          
        chat_id = message.chat.id
        try:
            user = user_dict[chat_id]
        except Exception as e: 
            user = 0
            print(str(User.fio)+" call err:" +str(e)+ " in step_get_p_top_part")
            
            regular_in_main(message)
            return
        float_in_text = controll_vvoda_mess(message)
        if text is None:
            step_enter_p_top_part(message)
            return
        if '/' in text or float_in_text is None:
            step_enter_p_top_part(message)
            return
        else:
            user.p_top = str(float_in_text)
            process_step_4_energy_type(message)
        return

    #Пошли по техосмотру протекторов
    #Вводим U протектора
def step_enter_protectors_U(message):
        text = message.text          
        chat_id = message.chat.id
        try:
            user = user_dict[chat_id]
        except Exception as e: 
            user = 0
            print(str(User.fio)+" call err:" +str(e)+ " in step_enter_protectors_U")
            
            regular_in_main(message)
            return
        # удалить старую клавиатуру
        keyboard = types.ReplyKeyboardRemove()
        msg = bot.reply_to(message, "Введите напряжение протектора",
                           reply_markup=keyboard)
        bot.register_next_step_handler(message,step_get_protectors_U)
        return

    #Записываем U протектора
def step_get_protectors_U(message):
        text = message.text          
        chat_id = message.chat.id
        try:
            user = user_dict[chat_id]
        except Exception as e: 
            user = 0
            print(str(User.fio)+" call err:" +str(e)+ " in step_get_protectors_U")
            
            regular_in_main(message)
            return
        float_in_text = controll_vvoda_mess(message)       
        if '/' in text or float_in_text is None:
            step_enter_protectors_U(message)
            return
        else:
            user.tz_u = str(float_in_text)
            step_enter_protectors_I(message)
        return
    
    #Вводим I протектора
def step_enter_protectors_I(message):
        text = message.text          
        chat_id = message.chat.id
        try:
            user = user_dict[chat_id]
        except Exception as e: 
            user = 0
            print(str(User.fio)+" call err:" +str(e)+ " in step_enter_protectors_I")
            
            regular_in_main(message)
            return
        # удалить старую клавиатуру
        keyboard = types.ReplyKeyboardRemove()
        msg = bot.reply_to(message, "Введите силу тока протектора",
                           reply_markup=keyboard)
        bot.register_next_step_handler(message,step_get_protectors_I)
        return
    
    #Записываем I протектора
def step_get_protectors_I(message):
        text = message.text          
        chat_id = message.chat.id
        try:
            user = user_dict[chat_id]
        except Exception as e: 
            user = 0
            print(str(User.fio)+" call err:" +str(e)+ " in step_get_protectors_I")
            
            regular_in_main(message)
            return
        float_in_text = controll_vvoda_mess(message)  
        if '/' in text or float_in_text is None:
            step_enter_protectors_I(message)
            return
        else:
            user.tz_i = str(float_in_text)
            step_enter_p_bottom_part(message)
        return
    
def step_categorie(message): #Получение и присваивание категории ИФС
    text = message.text
    chat_id = message.chat.id
    second_word = 0
    try:
        user = user_dict[chat_id]
    except Exception as errorMsg:
        user = 0
    # удалить старую клавиатуру
    markup = types.ReplyKeyboardRemove(selective=False)
    keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True,
                                         resize_keyboard=True)
    if message is None or '/back' in text:
        regular_in_main(message)
        return
    else:
        try:
            second_word = text.split(";")[2].strip()
            if second_word!=0:
                user.categorie = second_word
                DB.Steps.step_update_categorie(message,user,bot)         
                try:
                    # удалить старую клавиатуру
                    markup = types.ReplyKeyboardRemove(selective=False)
                    keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
                    #Обращение к БД и получение СКЗ по выбранному наряду
                    my_array = DB.Naryad.get_skz(message,user)
                    for element in my_array:
                        itembtn = types.KeyboardButton(text = str(element))
                        keyboard.add(itembtn)
                    #Обращение к БД и получение TZ по выбранному наряду
                    my_array = DB.Naryad.get_tz(message,user)    
                    for element in my_array:
                        itembtn = types.KeyboardButton(text = str(element))
                        keyboard.add(itembtn)
                        
                    msg = bot.reply_to(message,
                                            'Выберите еще раз этот объект.\nДля перехода в начало нажмите - /back',
                                            reply_markup=keyboard )
                    bot.register_next_step_handler(message,geo_ask) #Даем пользователю на выбор
                except Exception as e:
                    print(str(User.fio)+" call err:" +str(e)+ " in step_categorie")
            
            else:
                regular_in_main(message)
                return
        except Exception as e:
                msg = bot.reply_to(message,
                                   "К сожалению что-то не получилось\n"
                                   "попробуйте еще раз.\n"
                                   "Для отмены нажмите /back",
                                   reply_markup=keyboard)
                print(str(User.fio)+" call err:" +str(e)+ " in step_categorie")
            
                regular_in_main(message)
                return
    return

    #Проверка ввода данных
def controll_vvoda_mess(message):
    text = message.text          
    chat_id = message.chat.id
    try:
        user = user_dict[chat_id]
    except Exception as e: 
        user = 0
        print(str(User.fio)+" call err:" +str(e)+ " in controll_vvoda_mess")
            
        regular_in_main(message)
        return
    # удалить старую клавиатуру
    keyboard = types.ReplyKeyboardRemove()
    if text != DB.DRW.controll_vvoda(message):
        print(text + " исправил на " + str(DB.DRW.controll_vvoda(message)))
        msg = bot.reply_to(message, "Вы имели ввиду - " + str(DB.DRW.controll_vvoda(message)) + " ?")
    text = DB.DRW.controll_vvoda(message)
    float_in_text=None
    try:
        float_in_text = float(text)
    except Exception as e:
        print(str(User.fio)+" call err:" +str(e)+ " in controll_vvoda_mess")
        
        return None
    return float_in_text

def day_time(message):
        today = datetime.datetime.today()
        date = int(today.strftime("%H"))
        if date>=0 and date<6:
            day_time = 'Доброй ночи, '+message.from_user.first_name+' ,\n'
        if date>=6 and date<12:
            day_time = 'Доброе утро, '+message.from_user.first_name+' ,\n'
        if date>=12 and date<18:
            day_time = 'Добрый день, '+message.from_user.first_name+' ,\n'
        if date>=18 and date<24:
            day_time = 'Добрый вечер, '+message.from_user.first_name+' ,\n'
        #print(day_time)
        return day_time
    
def process_step_2(message): # 2 шаг выбор скз
        text = message.text
        chat_id = message.chat.id
        try:
            user = user_dict[chat_id]
        except Exception as e: 
            user = 0
            print(str(chat_id)+" call err:" +str(e)+ " in process_step_2")
            regular_in_main(message)
            return
        int_in_text = None
        try:
            int_in_text = int(text.split(" ; ")[0].strip())
        except Exception as e:
            print(str(User.fio)+" call err:" +str(e)+ " in process_step_2")
        if int_in_text is None or '/' in text:
            regular_in_main(message)
            return
        else:
            user.naryad = int(int_in_text)
            try:
                user.vid_rabot = text.split(" ; ")[2].strip()
            except Exception as e:
                print(str(User.fio)+" call err:" +str(e)+ " in process_step_2")
                regular_in_main(message)
                return
            # удалить старую клавиатуру
            markup = types.ReplyKeyboardRemove(selective=False)
            keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            #Обращение к БД и получение СКЗ по выбранному наряду
            my_array = DB.Naryad.get_skz(message,user)
            for element in my_array:
                itembtn = types.KeyboardButton(text = str(element))
                keyboard.add(itembtn)
            my_array = DB.Naryad.get_tz(message,user)    
            for element in my_array:
                itembtn = types.KeyboardButton(text = str(element))
                keyboard.add(itembtn)
                
            msg = bot.reply_to(message,
                                    'Выберите объект.\nДля перехода в начало нажмите - /back',
                                    reply_markup=keyboard )
            bot.register_next_step_handler(message,geo_ask)

def geo_ask(message):#Обрабатываем выбор объекта
    text = message.text
    chat_id = message.chat.id
    try:
        user = user_dict[chat_id]
    except Exception as errorMsg:
        user = 0
    TZ = 0
    # удалить старую клавиатуру
    markup = types.ReplyKeyboardRemove(selective=False)
    keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    if text is None:
        regular_in_main(message)
        return
    if text is None:
        regular_in_main(message)
        return
    if '/' in text:
        regular_in_main(message)
        return
    else:
        try:
            second_word = int(float(text.split(" ; ")[2].strip())) 
            user.categorie = second_word
        except Exception as e:
            print(str(User.fio)+" call err:" +str(e)+ " in geo_ask")
            return
        try:
            # УДАЛИТЬ СТАРУЮ КЛАВИАТУРУ
            TZ=0
            markup = types.ReplyKeyboardRemove(selective=False)
            keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)

            #Если ТЗ   
            if user.categorie >= 140 and user.categorie <= 143:   
                TZ=1
                user.tz_id = text.split(" ; ")[1].strip()
                
            #Если СКЗ
            if user.categorie == 170 or user.categorie == 169: 
                TZ=0
                
            #Если не указана категория    
            if user.categorie == 0:
                TZ=1
                user.tz_id = text.split(" ; ")[1].strip()
                # удалить старую клавиатуру
                markup = types.ReplyKeyboardRemove(selective=False)
                keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
                itembtn1 = types.KeyboardButton(text = "ІФЗ високого тиску I категорії\n\n ; ; 140") #id140
                itembtn2 = types.KeyboardButton(text = "ІФЗ високого тиску II категорії\n\n ; ; 141") #id141
                itembtn3 = types.KeyboardButton(text = "ІФЗ середнього тиску\n\n ; ; 142") #id142
                itembtn4 = types.KeyboardButton(text = "ІФЗ низького тиску\n\n ; ; 143") #id143
                #itembtn5 = types.KeyboardButton(text = "СКЗ\n\n;170")#id170
                keyboard.add(itembtn1,itembtn2)
                keyboard.add(itembtn3,itembtn4)
                #keyboard.add(itembtn5)
                msg = bot.reply_to(message,
                                   "Категория этого объекта не указана.\n"
                                   "Выберите из списка правильную!\n"
                                   "Доступно только нажатие на кнопку!\n"    
                                   "Для перехода в начало нажмите - /back",
                                   reply_markup=keyboard)
                bot.register_next_step_handler(message,step_categorie)
                return
            
            #Мы работаем с Точками защиты?
            user.tz = int(TZ)
            
            #Если да то получаем инфо по точке
            if user.tz == 1:
                first_word = text.split(" ; ")[0].strip()
                second_word = text.split(" ; ")[1].strip()
                user.name_tz = first_word
                user.tz_id = second_word
                my_array = DB.Naryad.get_tz_info(message,user)
                print("WORK_TZ")
            #Иначе получаем инфо по СКЗ
            else:
                first_word = text.split(" ; ")[0].strip()
                second_word = text.split(" ; ")[1].strip()
                user.name_skz = first_word
                user.skz_id = second_word
                my_array = DB.Naryad.get_skz_info(message,user)
                print("WORK_SKZ")
                
            #Просим передать своё местоположение
            if user.categorie != 0:
                
                # удалить старую клавиатуру
                keyboard = types.ReplyKeyboardMarkup(row_width=1,
                                                     resize_keyboard=True)
                button_geo = types.KeyboardButton(text="Отправить своё местоположение",
                                                  request_location=True)
                keyboard.add(button_geo)
                msg = bot.reply_to(message,
                                    "Нажмите на кнопку и передайте мне свое местоположение\n"
                                    "Для перехода в начало нажмите - /back",
                                    reply_markup=keyboard)
                
        except Exception as e:
            msg = bot.reply_to(message,
                               "К сожалению что-то не получилось\n"
                               "попробуйте еще раз.\n"
                               "Для отмены нажмите /back",
                               reply_markup=keyboard)
            print(str(User.fio)+" call err:" +str(e)+ " in geo_ask")
            return
    return
    
def process_step_3(message): # 3 отправка показаний Напряжение
    text = message.text          
    chat_id = message.chat.id
    try:
        user = user_dict[chat_id]
    except Exception as e: 
        user = 0
        print(str(User.fio)+" call err:" +str(e)+ " in process_step_3")
        regular_in_main(message)
        return
    # удалить старую клавиатуру
    remove_keyboard = types.ReplyKeyboardRemove()           
    bot.reply_to(message,
                 "Укажите напряжение.\n"
                 "Для перехода в начало нажмите - /back",
                 reply_markup=remove_keyboard)
    bot.register_next_step_handler(message, process_step_4_I)
      
def process_step_4_U(message): # 4 Отправка показаний Напряжение
    text = message.text
    chat_id = message.chat.id
    try:
        user = user_dict[chat_id]
    except Exception as e:
        user = 0
        print(str(User.fio)+" call err:" +str(e)+ " in process_step_4_U")
        regular_in_main(message)
        return
    
    if message.location is None:
        regular_in_main(message)
        return
    else:
        user.longitude = message.location.longitude
        user.latitude = message.location.latitude
        # удалить старую клавиатуру
        remove_keyboard = types.ReplyKeyboardRemove()
        #Если выбрано СКЗ
        if int(user.tz) == 0 :
            bot.reply_to(message, "Укажите напряжение.\nДля перехода в начало нажмите - /back", reply_markup=remove_keyboard)
            bot.register_next_step_handler(message, process_step_4_I)
        else:
            msg = bot.reply_to(message,
                                   "Укажите потенциал нижней части.\n"
                                   "Для перехода в начало нажмите - /back",
                                   reply_markup=remove_keyboard)
            bot.register_next_step_handler(msg, process_step_4_P2)
        return
        
           
def process_step_4_I(message): #4 Отправка показаний Ток
    text = message.text
    chat_id = message.chat.id
    try:
        user = user_dict[chat_id]
    except Exception as e:
        user = 0
        print(str(User.fio)+" call err:" +str(e)+ " in process_step_4_I")
        regular_in_main(message)
        return
    float_in_text = controll_vvoda_mess(message)
    if text is None:
        regular_in_main(message)
        return
    if '/' in text or float_in_text is None:
        regular_in_main(message)
        return
    else:
        user.u = str(float_in_text)
        # удалить старую клавиатуру
        remove_keyboard = types.ReplyKeyboardRemove() 
        msg = bot.reply_to(message,
                               "Укажите силу тока.\n"
                               "Для перехода в начало нажмите - /back",
                               reply_markup=remove_keyboard)
        bot.register_next_step_handler(msg, process_step_4_P1)
   
def process_step_4_P1(message): #4 Отправка показаний P1
    text = message.text
    chat_id = message.chat.id
    try:
        user = user_dict[chat_id]
    except Exception as e:
        user = 0
        print(str(User.fio)+" call err:" +str(e)+ " in process_step_4_P1")
        regular_in_main(message)
        return
    float_in_text = controll_vvoda_mess(message)        
    if '/' in text or float_in_text is None:
        regular_in_main(message)
        return
    else:
        user.i = str(float_in_text)
        # удалить старую клавиатуру
        remove_keyboard = types.ReplyKeyboardRemove() 
        msg = bot.reply_to(message,
                               "Укажите потенциал при включенной станции.\n"
                               "Для перехода в начало нажмите - /back",
                               reply_markup=remove_keyboard)
        bot.register_next_step_handler(msg, process_step_4_P2)
    
       
def process_step_4_P2(message): #4 Отправка показаний P2
    text = message.text
    chat_id = message.chat.id
    try:
        user = user_dict[chat_id]
    except Exception as e:
        user = 0
        print(str(User.fio)+" call err:" +str(e)+ " in process_step_4_P2")
        regular_in_main(message)
        return
    float_in_text = controll_vvoda_mess(message)  
    if '/' in text or float_in_text is None:
        regular_in_main(message)
        return
    else:        
        user.p1 = str(float_in_text)
        # удалить старую клавиатуру
        remove_keyboard = types.ReplyKeyboardRemove()
        #Если выбрано СКЗ
        if int(user.tz) == 0 :
            msg = bot.reply_to(message,
                                    "Укажите потенциал при выключенной станции."
                                    "\nДля перехода в начало нажмите - /back",
                                    reply_markup=remove_keyboard)
            bot.register_next_step_handler(msg, process_step_4_energy_type)
        else:
            msg = bot.reply_to(message,
                                    "Укажите потенциал верхней части."
                                    "\nДля перехода в начало нажмите - /back",
                                    reply_markup=remove_keyboard)
            bot.register_next_step_handler(msg, process_step_4_energy_type)
            
def process_step_4_energy_type(message): # Получение типа потребления
    chat_id = message.chat.id
    try:
        user = user_dict[chat_id]
    except Exception as e:
        user = 0
        print(str(User.fio)+" call err:" +str(e)+ " in process_step_4_energy_type")
        regular_in_main(message)
        return
    if user.tz == 0 :
        text = message.text
        float_in_text = controll_vvoda_mess(message)  
        if '/' in text or float_in_text is None:
            regular_in_main(message)
            return
        else:
            user.p2 = str(float_in_text)
            #Если выбрано СКЗ
            # удалить старую клавиатуру
            markup = types.ReplyKeyboardRemove(selective=False)
            keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            itembtn1 = types.KeyboardButton(text = "Актив")#F399
            itembtn2 = types.KeyboardButton(text = "Реактив")#F400
            itembtn3 = types.KeyboardButton(text = "Генерация")#F401
            keyboard.add(itembtn1,itembtn2,itembtn3)
            msg = bot.reply_to(message, "Выберите тип потребления электросчётчика катодной станции."
                                    "\nДля перехода в начало нажмите - /back",
                                    reply_markup=keyboard)
            bot.register_next_step_handler(msg, process_step_4_pokaz)
    else:
        # удалить старую клавиатуру
        markup = types.ReplyKeyboardRemove(selective=False)
        keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        itembtn1 = types.KeyboardButton(text = "Работает") #id = 5
        itembtn2 = types.KeyboardButton(text = "Не работает")#id = 6
        itembtn3 = types.KeyboardButton(text = "Резерв")#id = 7
        itembtn4 = types.KeyboardButton(text = "Снято")#id = 8
        itembtn5 = types.KeyboardButton(text = "Отключено")#id = 9
        itembtn6 = types.KeyboardButton(text = "Отсутствует")#id = 10
        keyboard.add(itembtn1,itembtn2,itembtn3,itembtn4,itembtn5,itembtn6)
        msg = bot.reply_to(message, "Выберите состояние объекта.\nДля перехода в начало нажмите - /back", reply_markup=keyboard)
        bot.register_next_step_handler(msg, process_step_6)       
    return
            
def process_step_4_pokaz(message): # 4 Отправка показаний электросчётчика
    text = message.text;
    chat_id = message.chat.id;
    try:
        user = user_dict[chat_id]
    except Exception as e:
        user = 0
        print(str(User.fio)+" call err:" +str(e)+ " in process_step_4_pokaz")
        regular_in_main(message)
        return
    
    user.energy_active = "0"
    user.energy_reactive = "0"
    user.energy_generation = "0"
    if '/' in text:
        regular_in_main(message)
        return
    else:
        #'energy_active','energy_reactive','energy_generation',#
        if "Актив" in text:
            user.energy_active = "1"
        elif "Реактив" in text:
            user.energy_reactive = "1"
        elif "Генерация" in text:
            user.energy_generation = "1"
        else:
            #Повторяем процедуру заново
            # удалить старую клавиатуру
            markup = types.ReplyKeyboardRemove(selective=False)
            keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            itembtn1 = types.KeyboardButton(text = "Актив")#F399
            itembtn2 = types.KeyboardButton(text = "Реактив")#F400
            itembtn3 = types.KeyboardButton(text = "Генерация")#F401
            keyboard.add(itembtn1,itembtn2,itembtn3)
            msg = bot.reply_to(message, "Выберите тип потребления электросчётчика катодной станции."
                                   "\nДля перехода в начало нажмите - /back",
                                   reply_markup=keyboard)
            bot.register_next_step_handler(msg, process_step_4_pokaz)
            return
        # Вышли из цикла, идём дальше
        print("Актив = "+user.energy_active+" Реактив = "+user.energy_reactive+" Генерация = "+ user.energy_generation)
        # удалить старую клавиатуру
        remove_keyboard = types.ReplyKeyboardRemove() 
        msg = bot.reply_to(message, "Укажите показания электросчётчика катодной станции."
                               "\nДля перехода в начало нажмите - /back",
                               reply_markup=remove_keyboard)
        bot.register_next_step_handler(msg, process_step_5)
        
def process_step_5(message): # 5 отправка состояния СКЗ
    chat_id = message.chat.id;
    try:
        user = user_dict[chat_id]
    except Exception as e:
        user = 0
        print(str(User.fio)+" call err:" +str(e)+ " in process_step_5")
        regular_in_main(message)
        return
    if user.tz == 0:
        text = message.text; 
        float_in_text = controll_vvoda_mess(message)  
        if '/' in text or float_in_text is None:
            regular_in_main(message)
            return
        else: 
            user.pokazanie = str(float_in_text)
            # удалить старую клавиатуру
            markup = types.ReplyKeyboardRemove(selective=False)
            keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            itembtn1 = types.KeyboardButton(text = "Работает") #id = 5
            itembtn2 = types.KeyboardButton(text = "Не работает")#id = 6
            itembtn3 = types.KeyboardButton(text = "Резерв")#id = 7
            itembtn4 = types.KeyboardButton(text = "Снято")#id = 8
            itembtn5 = types.KeyboardButton(text = "Отключено")#id = 9
            itembtn6 = types.KeyboardButton(text = "Отсутствует")#id = 10
            keyboard.add(itembtn1,itembtn2,itembtn3,itembtn4,itembtn5,itembtn6)
            msg = bot.reply_to(message, "Выберите состояние СКЗ.\nДля перехода в начало нажмите - /back", reply_markup=keyboard)
            bot.register_next_step_handler(msg, process_step_6)
    else:
        # удалить старую клавиатуру
        markup = types.ReplyKeyboardRemove(selective=False)
        keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        itembtn1 = types.KeyboardButton(text = "Работает") #id = 5
        itembtn2 = types.KeyboardButton(text = "Не работает")#id = 6
        itembtn3 = types.KeyboardButton(text = "Резерв")#id = 7
        itembtn4 = types.KeyboardButton(text = "Снято")#id = 8
        itembtn5 = types.KeyboardButton(text = "Отключено")#id = 9
        itembtn6 = types.KeyboardButton(text = "Отсутствует")#id = 10
        keyboard.add(itembtn1,itembtn2,itembtn3,itembtn4,itembtn5,itembtn6)
        msg = bot.reply_to(message, "Выберите состояние объекта.\nДля перехода в начало нажмите - /back", reply_markup=keyboard)
        bot.register_next_step_handler(msg, process_step_6)
            
def process_step_6(message): # 6 отправка доп информации
    text = message.text;
    chat_id = message.chat.id;
    try:
        user = user_dict[chat_id]
    except Exception as e:
        user = 0
        print(str(User.fio)+" call err:" +str(e)+ " in process_step_6")
        regular_in_main(message)
        return    
    if '/' in text:
        regular_in_main(message)
        return
    else:
        if "Работает" in text:
            user.sustain = 5
        elif "Не работает" in text:
            user.sustain = 6
        elif "Резерв" in text:
            user.sustain = 7
        elif "Снято" in text:
            user.sustain = 8
        elif "Отключено"in text:
            user.sustain = 9
        elif "Отсутствует" in text:
            user.sustain = 10
        else:
            user.sustain = 0
            regular_in_main(message)
            return
            
        remove_keyboard = types.ReplyKeyboardRemove()
        #Если выбрано СКЗ
        if user.tz == 0 :
            msg = bot.reply_to(message, "Опишите выбор состояния СКЗ.\nДля перехода в начало нажмите - /back", reply_markup=remove_keyboard)
        else:
            msg = bot.reply_to(message, "Опишите выбор состояния объекта.\nДля перехода в начало нажмите - /back", reply_markup=remove_keyboard)
        bot.register_next_step_handler(msg, process_step_7)
        return

def process_step_7(message): # 7 отправка фото
    chat_id = message.chat.id;
    text = message.text;
    try:
        user = user_dict[chat_id]
    except Exception as e:
        user = 0
        print(str(User.fio)+" call err:" +str(e)+ " in process_step_7")
        regular_in_main(message)
        return
    if text is None:
        regular_in_main(message)
        return
    if '/' in text:
        regular_in_main(message)
        return
    else:
        #сохраняем введенные данные в класс
        user.info = text
        # удалить старую клавиатуру    
        remove_keyboard = types.ReplyKeyboardRemove()
        keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        msg = bot.reply_to(message, "Отправьте фото объекта.")
        bot.register_next_step_handler(msg, process_step_8)

            
def process_step_8(message): # 8 конец #cnxn.commit()
    chat_id = message.chat.id;
    text = message.text;
    try:
        user = user_dict[chat_id]
    except Exception as e:
        user = 0
        print(str(User.fio)+" call err:" +str(e)+ " in process_step_8")
        regular_in_main(message)
        return
 
    if text is not None:
        regular_in_main(message)
        return
    else:
        try:
            raw = message.photo[2].file_id
            name = raw+".jpg"
            file_info = bot.get_file(raw)
            downloaded_file = bot.download_file(file_info.file_path)
            with open(name,'wb') as new_file:
                new_file.write(downloaded_file)
                # ПОДКЛЮЧЕНИЕ К БД СЦ
                cnxn = pypyodbc.connect('DRIVER={SQL Server};SERVER=a380;DATABASE=scs;UID=sc;PWD=masterkey')
                cursor = cnxn.cursor()
                if user.tz == 0:
                    inv = user.inv
                else:
                    inv = 'ifs_'+user.tz_id
                today = datetime.datetime.today()
                date = today.strftime("%d.%m.%Y %H:%M:%d")
                #patch = str(cwd)+"\\"+ str(name)
                delpatch = str(cwd)+'\\'+ str(name) 
                # ВЫПОЛНЕНИЕ ЗАПРОСА                
                try:
                    fin=open(name, 'rb')
                    img = fin.read()
                    binary = pypyodbc.BINARY(img)
                    cursor.execute("INSERT INTO obj_img (invn, datae_objimg, img_det) VALUES ('"+str(inv)+"','"+str(date)+"',?)", (binary,) )                    
                    if not IS_TEST:
                        cnxn.commit()
                    cursor.close()
                    cnxn.close()                
                    fin.close()
                    if user.tz == 0:
                        bot.reply_to(message, "Получены данные: наряд: "+str(user.naryad)+
                                         ", СКЗ: "+user.name_skz+", долгота: "+str(user.longitude)+
                                         ", широта: "+str(user.latitude)+", доп. инфо: "+user.info+".")
                        print("Получены данные: наряд: "+str(user.naryad)+", СКЗ: "+user.name_skz+
                              ", долгота: "+str(user.longitude)+", широта: "+str(user.latitude)+
                              ", доп. инфо: "+user.info+".")
                    else:
                        bot.reply_to(message, "Получены данные: наряд: "+str(user.naryad)+
                                         ", ИФС: "+user.name_tz+", долгота: "+str(user.longitude)+
                                         ", широта: "+str(user.latitude)+", доп. инфо: "+user.info+".")
                        print("Получены данные: наряд: "+str(user.naryad)+", ИФС: "+user.name_tz+
                              ", долгота: "+str(user.longitude)+", широта: "+str(user.latitude)+
                              ", доп. инфо: "+user.info+".")
                except Exception as e:
                    bot.reply_to(message, "Фото не записано в базу! " + str(e))
                    print(str(User.fio)+" call err:" +str(e)+ " in process_step_8")
                    cnxn.close()
        except Exception as e:
                bot.reply_to(message, "Фото не записано в базу! " + str(e))
                print(str(User.fio)+" call err:" +str(e)+ " in process_step_8")
        # удалить старую клавиатуру
        try:
            os.remove(delpatch)
            #print("Фото успешно удалено из обменника " +str(delpatch))
        except Exception as e:
            print(str(User.fio)+" call err:" +str(e)+ " in process_step_8")
        remove_keyboard = types.ReplyKeyboardRemove()
        keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        if user.tz == 0:
            if user.categorie == 170:
                DB.Map.add(message,user,bot)
                DB.Naryad.add_to_ehz(message,user,bot)
                DB.Naryad.add_to_ehz_zamer(message,user,bot)
                DB.electro.add_pokaz(message,user,bot)
            else:
                DB.Map.add(message,user,bot)
                DB.Naryad.add_to_ehz(message,user,bot)
                DB.Naryad.add_to_ehz_zamer(message,user,bot)
        else:
            DB.Map.add(message,user,bot)                #Rdy
            DB.Naryad.add_to_ehz(message,user,bot)      #Rdy
            DB.Naryad.add_to_ehz_zamer(message,user,bot)#Rdy
        bot.reply_to(message, "Для продолжения нажмите - /start")

    
# Enable saving next step handlers to file "./.handlers-saves/step.save".
# Delay=2 means that after any change in next step handlers (e.g. calling register_next_step_handler())
# saving will hapen after delay 2 seconds.
bot.enable_save_next_step_handlers(delay=2)

# Load next_step_handlers from save file (default "./.handlers-saves/step.save")
# WARNING It will work only if enable_save_next_step_handlers was called!
bot.load_next_step_handlers()

def telegram_polling():
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(e)
        bot.stop_polling()
        time.sleep(10)
        telegram_polling()

telegram_polling()

