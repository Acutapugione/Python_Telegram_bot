import sys
# Библия для телебота
import telebot
from telebot import types
import time
from ast import literal_eval
from Constants import *
from Connections import *
from UsersMenuManager import *

from Bot import Bot
from Bot import Logger
#import ImportExport_test as DB

#Библия для работы с файлами
import os
cwd = os.getcwd()
import textwrap
def short(val):
    return str(textwrap.shorten(val, 40, placeholder=" ..."))
#token = "1367567298:AAHMFlPOzXcJh5L4vLH7_R2LsFWegWcqUcA"  # тестовый бот
token = "5125086405:AAGjsxeyP58kLRPqDTxNPPxRSun_H_HLF9A"
del_list = list()
  
class BotManager(Bot):

    
    def __init__( abc, _telebot=telebot,
                  _token=token, _menu_manager=MenuManager()
                  ):  
        super().__init__(_telebot=telebot, _token=token)
        abc.menuManager = _menu_manager
        abc.keyboard =''
        
    def test_send_message_with_markdown(    self    ):
        tb = telebot.TeleBot(   TOKEN   )
        markdown = """
        *bold text*
        _italic text_
        [text](URL)
        """
        ret_msg = tb.send_message(
            CHAT_ID,
            markdown,
            parse_mode="Markdown"
            )
        assert ret_msg.message_id
    
    def makeCommitText(abc, call):
        try:
            commitText = local = ''
            
            tmp = abc.menuManager.getMeasu(call.message.chat.id)
            if tmp:
                commitText = 'Ваші заміри:'
                for elem in tmp:
                    
                    if local == elem[str(OBJECT_INDEX)]:
                        commitText = '{}\n{}: {}'.format(
                            commitText,
                            
                            Localisator().getLocalDict(elem[str(VIEW)]),
                            Localisator().getLocalDict(elem[str(VALUE)])
                            )
                    else:    
                        commitText = '{}\n{}:\n{}: {}'.format(
                            commitText,
                            Localisator().getLocalDict(elem[str(TITLE)] if str(TITLE) in elem else elem[str(OBJECT_PARAMS)] if str(OBJECT_PARAMS) in elem else ''),###REVIEW
                            Localisator().getLocalDict(elem[str(VIEW)]),
                            Localisator().getLocalDict(elem[str(VALUE)])
                            )
                    local = elem[str(OBJECT_INDEX)]
                else:
                    commitText = '{}\n'.format(commitText)
            tmp = abc.menuManager.getObjPara(call.message.chat.id)
            
            if tmp:
                commitText = '{}\nВаші заповнені параметри:'.format(commitText)
                for elem in tmp:
                    
                    if str(local) == str(elem[str(OBJECT_INDEX)] if str(OBJECT_INDEX) in elem else elem[str(INDEX)]):
                        
                        commitText = '{}\n{}: {}'.format(
                        commitText,
                        #Localisator().getLocalDict(elem[str(TITLE)]),
                        Localisator().getLocalDict(elem[str(VIEW)] if str(VIEW) in elem else elem[str(OBJECT_PARAMS)] if str(OBJECT_PARAMS) in elem else ''),
                        Localisator().getLocalDict(elem[str(VALUE)])
                        )
                    else:    
                        commitText = '{}\n{}:\n{}: {}'.format(
                        commitText,
                        Localisator().getLocalDict(elem[str(TITLE)] if str(TITLE) in elem else elem[str(OBJECT_PARAMS)] if str(OBJECT_PARAMS) in elem else '' ),
                        Localisator().getLocalDict(elem[str(VIEW)]  if str(VIEW) in elem else elem[str(OBJECT_PARAMS)] if str(OBJECT_PARAMS) in elem else ''),
                        Localisator().getLocalDict(elem[str(VALUE)])
                        )
                    local = str(elem[str(OBJECT_INDEX)] if str(OBJECT_INDEX) in elem else elem[str(INDEX)])
                else:
                    commitText = '{}\n'.format(commitText)
            tmp = list()
            tmp.extend( abc.menuManager.getObjPhoto(call.message.chat.id) )
            if tmp:
                commitText = '{}\nВаші відправлені фото: {}'.format(commitText, len(tmp))
            #print("{} in MakeCommitText()".format(compmitText))    
            return commitText
        except Exception as e:
            #print(e, "in makeCommitText()")
            raise e 
    
    def getGeoKb(abc, tittle='Отправить своё местоположение'):
        kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        kb.add(
            types.KeyboardButton(
                text=str(tittle),
                request_location=True
                ))
        ''',
        types.KeyboardButton(
            text=str(BACK_TITLE),
            #request_location=True
            )
        )'''
        return kb
    
    def editMessageTextForGeo(abc, call, keyboard):
        abc.bot.edit_message_text(
            chat_id         =   call.message.chat.id,
            message_id      =   call.message.message_id,
            
            text            =   'Контекстне меню',
            reply_markup    =   abc.getSimpleKb(call),
            )
        '''abc.bot.reply_to(
                    call.message,
                    text            =   'Натисніть, для відправлення {}'.format(Localisator().getLocal(str(call.data.split(';')[1]))),
                    reply_markup    =   keyboard
                    )'''
        
        abc.bot.send_message(
            chat_id         =   call.message.chat.id,
            text            =   'Натисніть, для відправлення {}'.format(Localisator().getLocal(str(call.data.split(';')[1]))),
            reply_markup    =   keyboard
            )
        global del_list
        del_list.append(call.message.message_id+1)
        
    def getSimpleKb(abc, call):
        kb = types.InlineKeyboardMarkup()
        if len(abc.menuManager.getS(call.message.chat.id))>1:
            kb.add(types.InlineKeyboardButton(text = str(BACK_TITLE), callback_data = str(BACK)), types.InlineKeyboardButton(text = str(BEGIN_TITLE), callback_data = str(MAIN)))
        else:
            kb.add(types.InlineKeyboardButton(text = str(BACK_TITLE), callback_data = str(BACK)))
        return kb

    def editMessageTextForPhoto(abc, call, keyboard):
        text = Localisator().getLocal(call.data.split(';')[0])
        abc.bot.edit_message_text(
            chat_id         =   call.message.chat.id,
            message_id      =   call.message.message_id,
            
            text            =   'Відправте фото для {}'.format(text),
            reply_markup    =   keyboard,
            )
        
    def editMessageTextForInput(abc, call, keyboard):
        text = Localisator().getLocal(call.data.split(';')[1])
        if WEB_1C_OBJECTS in call.data.split(';')[1]:
            text = Localisator().getLocal(COMMENTS)
        abc.bot.edit_message_text(
            chat_id         =   call.message.chat.id,
            message_id      =   call.message.message_id,
            
            text            =   'Введіть значення для {}'.format(text),
            reply_markup    =   keyboard,
            )
        
    def pullParam(abc, call):
        try:
            objParam = dict()
            
            if call.data.split(';')[1] == str(PARAM_CHOSEN):
                objParam[str(VALUE)] = call.data.split(';')[3]
                objParam[str(INDEX)] = call.data.split(';')[0]
                objParam[str(OBJECT_INDEX)] = call.data.split(';')[2]
                
                params = Web1C.getParams({ str(INDEX) : objParam[str(OBJECT_INDEX)]})
                if params is not None and len(params)>0:
                    for item in params:
                        if str(item[str(INDEX)]) == str(objParam[str(INDEX)]):
                            for elem in item[str(PARAM_CHOSE)]:
                                if str(item[str(PARAM_CHOSE)].index(elem)) == str(objParam[str(VALUE)]):
                                    objParam[str(VALUE)] = elem
                                    objParam[str(VIEW)] = item[str(TITLE)]
                                    objParam[str(OBJECT_PARAMS)]=  item[str(PARAM_CHOSE)].index(elem)
                                    #objParam[str(INDEX)] =
                                    
                objects = Web1C.getObjects(call.message.chat.id)
                for obj in objects:
                    if obj[str(INDEX)] == objParam[str(OBJECT_INDEX)]:
                        objParam[str(TITLE)] = obj[str(TITLE)]
                        objParam[str(ORDER_NUMBER)] = obj[str(ORDER_NUMBER)]
                        
            else:
                objParam[str(VALUE)] = call.data.split(';')[0]
                objParam[str(INDEX)] = abc.menuManager.getS(call.message.chat.id)[-2].split(';')[0]
                objParam[str(OBJECT_PARAMS)] =  call.data.split(';')[1]
                objParam[str(TYPE)] = abc.menuManager.getS(call.message.chat.id)[-2].split(';')[3]
                
                objParam[str(TITLE)] = Ehz.getObjectInfo(objParam)

            abc.menuManager.pushObjPara(call.message.chat.id, objParam)
            
            abc.menuManager.popS(call.message.chat.id)
            abc.menuManager.popS(call.message.chat.id)
            
            pass #print(objParam)
        except Exception as e:
            pass #print(e)
        finally:
            abc.clrInput(call.message)
            
    def clearMessage(abc, message):
        try:
            kb = abc.getKeyboard(message.chat.id)
            if kb:
                abc.bot.reply_to(
                    message,
                    text            =   kb[str(TITLE)],
                    reply_markup    =   kb[str(KEYBOARD)]
                    )
                numb = -2
                try:
                    while abc.bot.delete_message(
                            message.chat.id,
                            message.message_id - numb
                            ) is True:
                        
                        numb-=1
                except:
                    pass #print('Message not found')
                numb = 0
                try:
                    while abc.bot.delete_message(
                            message.chat.id,
                            message.message_id - numb
                            ) is True:
                        numb+=1
                except:
                    pass #print('Message not found')
        except Exception as e:
            pass #print(e)
        finally:
            pass#abc.clearDelList(message)
            
    def clearCommit(abc, message):
        try:
            kb = ''
            pass #print(abc.menuManager.getS(message.chat.id))
            if len(abc.menuManager.getS(message.chat.id))>1:
                abc.menuManager.popS(message.chat.id)
                abc.menuManager.popS(message.chat.id)
                kb = abc.getKeyboard(message.chat.id, abc.menuManager.getS(message.chat.id)[-1])
            else:
                kb = abc.getKeyboard(message.chat.id)
            if kb:
                abc.bot.reply_to(
                    message,
                    text            =   kb[str(TITLE)],
                    reply_markup    =   kb[str(KEYBOARD)]
                    )
                numb = -2
                try:
                    while abc.bot.delete_message(
                            message.chat.id,
                            message.message_id - numb
                            ) is True:
                        
                        numb-=1
                except:
                    pass #print('Message not found')
                numb = 0
                try:
                    while abc.bot.delete_message(
                            message.chat.id,
                            message.message_id - numb
                            ) is True:
                        
                        numb+=1
                except:
                    pass #print('Message not found')
                
        except Exception as e:
            pass#abc.clearDelList(message)
        finally:
            pass#abc.clearDelList(message)
    
    def clrInput(abc, message, action_name = 'typing'):
        try:
            kb = ''
            pass #print(abc.menuManager.getS(message.chat.id))
            if len(abc.menuManager.getS(message.chat.id))>1:
                kb = abc.getKeyboard(message.chat.id, abc.menuManager.getS(message.chat.id)[-1])
            else:
                kb = abc.getKeyboard(message.chat.id)
            if kb:
                try:
                    if action_name is not None:
                        abc.bot.send_chat_action(message.chat.id, action_name )
                    abc.bot.reply_to(
                        message,
                        text            =   kb[str(TITLE)],
                        reply_markup    =   kb[str(KEYBOARD)]
                        )
                except Exception as e:
                    print("ERROR", e)
                numb = -2
                    
                try:
                    while abc.bot.delete_message(
                            message.chat.id,
                            message.message_id - numb
                            ) is True:
                        
                        numb-=1
                except:
                    pass #print('Message not found')
                numb = 0
                try:
                    while abc.bot.delete_message(
                            message.chat.id,
                            message.message_id - numb
                            ) is True:
                        
                        numb+=1
                except:
                    pass #print('Message not found')
        except Exception as e:
            pass#abc.clearDelList(message)
        finally:
            pass#abc.clearDelList(message)
        
    def getKeyboard(abc, user, call_data=''):
        try:
            
            abc.keyboard = types.InlineKeyboardMarkup()
            header =''
            if len(abc.menuManager.getS(user))>0:
                abc.keyboard.add(
                    types.InlineKeyboardButton(
                        text = '{}'.format(ICONS['arrow_heading_up']), #str(BEGIN_TITLE)
                        callback_data = str(BEGIN)
                        ),
                    types.InlineKeyboardButton(
                        text = '{}'.format(ICONS['arrow_left']),
                        callback_data = str(BACK)
                        )
                    )
            is_pokaz = False
            if not call_data:
                menu = abc.menuManager.getMenu(user)
                header = menu.getTitle()
                abc.keyboard.add(types.InlineKeyboardButton(text = short(menu.getTitle()), callback_data = menu.getIndex()))
                
                return {str(TITLE) : str(header), str(KEYBOARD): abc.keyboard}
            else:
                
                menu = abc.menuManager.getMenu(user, call_data)
                
                if menu:
                    
                    if str(SUB_MENU) in menu:
                        for elem in menu[str(SUB_MENU)]:
                            call_data = '' 
                            try:
                                call_data = elem[str(CALL_DATA)]
                            except:
                                call_data = elem[str(INDEX)]
                            finally:
                                
                                abc.keyboard.add(types.InlineKeyboardButton(text = short(elem[str(TITLE)]), callback_data = call_data))#
                                header = menu[str(TITLE)]
                    else:
                        for elem in menu:
                            
                            if isinstance(elem, dict):
                                is_pokaz = False
                                if  str(EZH_MEASUREMENTS) in elem[str(FROM_DB)] or str(ELECTRO_DB) in elem[str(FROM_DB)]:
                                    is_pokaz = True
                                    header = 'Виберіть один із замірів'
                                elif switch( elem[str(FROM_DB)], { str(EZH_WORK_ORDERS) : True, str(WEB_1C_WORK_ORDERS): True }):
                                    header = 'Виберіть один із нарядів'
                                    abc.keyboard.add(
                                        types.InlineKeyboardButton(
                                            text = short(Localisator().getLocal(elem[str(TITLE)])),
                                            callback_data = elem[str(CALL_DATA)]
                                            )
                                        )
                                elif str(EZH_OBJ_NULL_PARAMS) in elem[str(FROM_DB)]:
                                    header = 'Виберіть один із параметрів'
                                    abc.keyboard.add(
                                        types.InlineKeyboardButton(
                                            text = short(Localisator().getLocal(elem[str(OBJECT_PARAMS)])),
                                            callback_data = elem[str(CALL_DATA)]
                                            )
                                        )
                                elif switch( elem[str(FROM_DB)], { str(WEB_1C_SELECT_PARAMS) : True, str(WEB_1C_INPUT_PARAMS): True }):
                                #elif  elem[str(FROM_DB)] in ( str(WEB_1C_SELECT_PARAMS) ):
                                    header = 'Виберіть один із параметрів'
                                    abc.keyboard.add(
                                        types.InlineKeyboardButton(
                                            text = short(Localisator().getLocal(elem[str(TITLE)] if str(TITLE) in elem else elem[str(CALL_DATA)].split(';')[0])),
                                            callback_data = elem[str(CALL_DATA)]))
                                    
                                elif  elem[str(FROM_DB)] in ( str(EZH_OBJECTS), str(WEB_1C_OBJECTS)):
                                    header = 'Виберіть один із об\'єктів'
                                   
                                    abc.keyboard.add(
                                        types.InlineKeyboardButton(
                                            text = short(Localisator().getLocal(elem[str(TITLE)])),
                                            callback_data = elem[str(CALL_DATA)]))
                                else:
                                    header = 'Виберіть один із варіантів'
                                    
                                    call_data = '' 
                                    try:
                                        call_data = str(elem[str(CALL_DATA)])
                                    except:
                                        call_data = elem[str(INDEX)]    
                                    abc.keyboard.add(types.InlineKeyboardButton(text = short(Localisator().getLocal(str(elem[str(TITLE)]))), callback_data = call_data))
                                if is_pokaz:
                                    abc.keyboard.add(types.InlineKeyboardButton(text = short(Localisator().getLocal(elem[str(CALL_DATA)].split(';')[1])), callback_data = elem[str(CALL_DATA)]))
                                
                                
                        #if switch( elem[str(FROM_DB)], { str(EZH_OBJECTS) : True, str(WEB_1C_OBJECTS): True }):
                        #if ( str(EZH_OBJECTS) in elem[str(FROM_DB)] and
                        if ( switch( elem[str(FROM_DB)], { str(EZH_OBJECTS) : True, str(WEB_1C_OBJECTS): True }) and
                             ( abc.menuManager.getMeasu(user)
                               or abc.menuManager.getObjPara(user)
                               or abc.menuManager.getObjPhoto(user)
                               )
                             ):
                            abc.keyboard.add(types.InlineKeyboardButton(text = short(STASH_TITLE), callback_data = str(STASH)))
                elif str(EZH_MEASUREMENTS) in call_data:
                    header = 'Введіть показ заміру'
            if str(STASH) in call_data and (abc.menuManager.getMeasu(user) or abc.menuManager.getObjPara(user) or abc.menuManager.getObjPhoto(user)):
                abc.keyboard.add(types.InlineKeyboardButton(text = short(COMMIT_TITLE), callback_data = str(COMMIT)))
        except Exception as e:
            #print(e, ' in getKeyboard', call_data)
            #print(sys.exc_info())
            raise e
        #    
        finally:
            
            
            if not header:
                header = 'За цим запитом нічого не знайдено, спробуйте ще раз'
            
            return {str(TITLE) : str(header), str(KEYBOARD): abc.keyboard}
            
    def main(abc):
        try:
            
            @abc.bot.message_handler(commands=[str(BEGIN)])  # комманда Старт
            def startDialog(message):
                abc.menuManager.push(User({'chat_id': message.chat.id}))
                abc.menuManager.pushS(message.chat.id, str(ORDER_TYPES))
                abc.clearMessage(message)

            @abc.bot.message_handler(func=lambda message: True, content_types=['photo']) # получили фото
            def photoMessageHandi(message):
                try: 
                    abc.menuManager.push(User({'chat_id': message.chat.id}))                
                    if len(abc.menuManager.getS(message.chat.id))>1:
                        
                        lastStep = abc.menuManager.getS(message.chat.id)[-1]
                        if switch(lastStep.split(';')[1], photoAsk):
                            abc.menuManager.popS(message.chat.id)

                            paraObj = dict()
                            raw = message.photo[2].file_id
                            name = raw+".jpg"
                            file_info = abc.bot.get_file(raw)
                            downloaded_file = abc.bot.download_file(file_info.file_path)

                            with open( name, 'wb' ) as new_file:
                                new_file.write( downloaded_file )
                                delpatch = str(cwd)+ '\\' + str(name)

                                with open( name, 'rb' ) as file_bin:
                                    img = file_bin.read()
                                    #binary_img = pypyodbc.BINARY( img )
                                    paraObj[str(PHOTO)] = img #binary_img
                                

                            try:
                                os.remove( delpatch )
                                pass #print("Фото успешно удалено из обменника " +str(delpatch))
                            except Exception as e:
                                pass #print("Не удалось удалить фото: " +e)
                            paraObj[str(INDEX)] = len(abc.menuManager.getObjPhoto(message.chat.id))
                            paraObj[str(OBJECT_INDEX)] = lastStep.split(';')[0]
                            today = datetime.datetime.today()
                            date = today.strftime("%d.%m.%Y %H:%M:%d")
                            paraObj[str(DATE)] = date
                            

                            abc.menuManager.pushObjPhoto(message.chat.id, paraObj)
                            
                            #print(paraObj)
                except Exception as e:
                    pass #print(e, 'photoMessageHandi')
                    
                finally:
                    #markup = types.ReplyKeyboardRemove(selective=False)
                    
                    abc.clrInput(message, 'upload_photo')
                    
            @abc.bot.message_handler(func=lambda message: True, content_types=['location']) # получили локацию
            def geoMessageHandi(message):
                
                try: 
                    abc.menuManager.push(User({'chat_id': message.chat.id}))                
                    if len(abc.menuManager.getS(message.chat.id))>1:
                        
                        lastStep = abc.menuManager.getS(message.chat.id)[-1]
                        if switch(lastStep.split(';')[1], geoAsk):
                            abc.menuManager.popS(message.chat.id)
                            paraObj = dict()
                            paraObj[str(VALUE)] = {
                                str(LATITUDE):message.location.latitude,
                                str(LONGITUDE):message.location.latitude
                                }
                            paraObj[str(INDEX)] = lastStep.split(';')[0]
                            paraObj[str(OBJECT_PARAMS)] = lastStep.split(';')[1]
                            paraObj[str(TYPE)] = lastStep.split(';')[3]
                            #print(paraObj[str(TYPE)])
                            abc.menuManager.pushObjPara(message.chat.id, paraObj)
                            
                            pass #print(paraObj)
                except Exception as e:
                    pass#abc.clearDelList(message)
                    pass #print(e, 'geoMessageHandi')
                    
                finally:
                    markup = types.ReplyKeyboardRemove(selective=False)
                    
                    abc.clrInput(message, 'find_location')
                    pass#abc.clearDelList(message)
                
            @abc.bot.message_handler( content_types=["text"] )  # Любое сообщение
            def messageHandi(message):
                
                try:
                    abc.menuManager.push(User({'chat_id': message.chat.id}))
                    if len(abc.menuManager.getS(message.chat.id))>1:
                        lastStep = abc.menuManager.getS(message.chat.id)[-1]
                        
                        if str(WEB_1C_INPUT_PARAMS) in lastStep.split(';'):
                            objParam = dict()
                            objParam[str(INDEX)] = lastStep.split(';')[0]
                            objParam[str(OBJECT_INDEX)] = lastStep.split(';')[2]

                            params = Web1C.getParams({ str(INDEX) : objParam[str(OBJECT_INDEX)]})
                            if params is not None and len(params)>0:
                                for item in params:
                                    if str(item[str(INDEX)]) == str(objParam[str(INDEX)]):
                                        objParam[str(VIEW)] = item[str(TITLE)]
                            
                            objects = Web1C.getObjects(message.chat.id)
                            #print(objects)
                            for obj in objects:
                                #print(obj[str(INDEX)] , objParam[str(OBJECT_INDEX)])
                                if obj[str(INDEX)] == objParam[str(OBJECT_INDEX)]:
                                    objParam[str(TITLE)] = obj[str(TITLE)]
                                    objParam[str(ORDER_NUMBER)] = obj[str(ORDER_NUMBER)]
                            
                            if controll_vvoda(message):
                                objParam[str(VALUE)] = controll_vvoda(message)
                            else:
                                objParam[str(VALUE)] = message.text
                            '''                           
                            params = Web1C.getParams({ str(INDEX) : objParam[str(OBJECT_INDEX)]})
                            if params is not None and len(params)>0:
                                for item in params:
                                    if str(item[str(INDEX)]) == str(objParam[str(INDEX)]):
                                        for elem in item[str(PARAM_CHOSE)]:
                                            if str(item[str(PARAM_CHOSE)].index(elem)) == str(objParam[str(VALUE)]):
                                                objParam[str(VALUE)] = elem
                                                objParam[str(VIEW)] = item[str(TITLE)]
                                                objParam[str(OBJECT_PARAMS)]=  item[str(PARAM_CHOSE)].index(elem)
                                                #objParam[str(INDEX)] =
                                                
                            objects = Web1C.getObjects(call.message.chat.id)
                            for obj in objects:
                                if obj[str(INDEX)] == objParam[str(OBJECT_INDEX)]:
                                    objParam[str(TITLE)] = obj[str(TITLE)]
                                    objParam[str(ORDER_NUMBER)] = obj[str(ORDER_NUMBER)]
                            '''
                            #Web1C.updateData([objParam])
                            abc.menuManager.pushObjPara(message.chat.id, objParam)
                            abc.menuManager.popS(message.chat.id)
                            abc.clrInput(message)
                            #print(objParam)
                        elif str(EZH_MEASUREMENTS) in lastStep.split(';'):
                            if switch(lastStep.split(';')[1], inputStr) or controll_vvoda(message):
                                zamerObj = dict()
                                if controll_vvoda(message):
                                    zamerObj[str(VALUE)] = controll_vvoda(message)
                                else:
                                    zamerObj[str(VALUE)] = message.text
                                zamerObj[str(VIEW)] = lastStep.split(';')[1]
                                zamerObj[str(INDEX)] = lastStep.split(';')[0]
                                zamerObj[str(TYPE)] = lastStep.split(';')[3]
                                zamerObj[str(OBJECT_INDEX)]= lastStep.split(';')[4]
                                abc.menuManager.pushMeasu(message.chat.id, zamerObj)
                                
                                abc.menuManager.popS(message.chat.id)
                                abc.clrInput(message)
                                pass #print(zamerObj)
                        elif str(EZH_OBJ_NULL_PARAMS) in lastStep.split(';'):
                            if switch(lastStep.split(';')[1], inputStr) or controll_vvoda(message):

                                objParam = dict()
                                if controll_vvoda(message):
                                    objParam[str(VALUE)] = controll_vvoda(message)
                                else:
                                    objParam[str(VALUE)] = message.text
                                objParam[str(INDEX)] = lastStep.split(';')[0]
                                objParam[str(OBJECT_PARAMS)] = lastStep.split(';')[1]
                                objParam[str(TYPE)] = lastStep.split(';')[3]
                                

                                abc.menuManager.pushObjPara(message.chat.id, objParam)
                                
                                abc.menuManager.popS(message.chat.id)
                                abc.clrInput(message)
                                pass #print(objParam)
                        elif str(ELECTRICITY_METER_READING) in lastStep.split(';'):
                            if switch(lastStep.split(';')[1], inputStr) or controll_vvoda(message):
                                zamerObj = dict()
                                if controll_vvoda(message):
                                    zamerObj[str(VALUE)] = controll_vvoda(message)
                                else:
                                    zamerObj[str(VALUE)] = message.text
                                zamerObj[str(VIEW)] = lastStep.split(';')[1]
                                zamerObj[str(INDEX)] = lastStep.split(';')[0]
                                zamerObj[str(TYPE)] = lastStep.split(';')[3]
                                zamerObj[str(OBJECT_INDEX)]= lastStep.split(';')[4]
                                ObjInfo = Ehz.getObjectInfo(
                                    {
                                        str(INDEX): zamerObj[str(OBJECT_INDEX)],
                                        str(TYPE): str(IS_SKZ),
                                        }
                                    )
                                zamerObj[str(INV_NUMBER)] = ObjInfo[str(INV_NUMBER)] if INV_NUMBER in ObjInfo else ''
                                
                                abc.menuManager.pushMeasu(message.chat.id, zamerObj)
                                
                                abc.menuManager.popS(message.chat.id)
                                abc.clrInput(message)
                                pass #print(zamerObj)
                        else:
                            abc.clearMessage(message)
                    else:
                        abc.clearMessage(message)
                except Exception as e:
                    #print(e, message.text)
                    abc.clearMessage(message)
                finally:
                    pass#abc.clearDelList(message)
                    
            @abc.bot.callback_query_handler(
                func=lambda call: call.data not in (str(BACK) , str(BEGIN))
            )  # Нажатие любой кнопки, кроме назад и начало
            def callback_inline(call):
                pass #print('callback_inline', call.data)
                abc.menuManager.push(User({'chat_id': call.message.chat.id}))
                abc.menuManager.pushS(call.message.chat.id, call.data)
                
                if len(call.data.split(';'))>1:
                    if switch(call.data.split(';')[1], inputAsk) :
                        
                        abc.editMessageTextForInput(call, abc.getSimpleKb(call))
                    elif switch(call.data.split(';')[1], geoAsk) :
                        abc.editMessageTextForGeo(call, abc.getGeoKb())
                    elif switch(call.data.split(';')[1], { str(EZH_SUSTAIN_TYPES) : True} ):
                        abc.pullParam(call)
                    elif switch(call.data.split(';')[1], { str(PARAM_CHOSEN) : True } ):
                        abc.pullParam(call)
                    elif switch(call.data.split(';')[1], photoAsk):
                        abc.editMessageTextForPhoto(call, abc.getSimpleKb(call))
                        #pass
                        #ОБРАБОТАТЬ ЗАПОЛНЕНИЕ ПАРАМЕТРА
                    else:
                        kb = abc.getKeyboard(call.message.chat.id, call.data)
                        if kb:
                            try:
                                if call.message.text == kb[str(TITLE)]:
                                    kb[str(TITLE)] = '{} повторення'.format(kb[str(TITLE)])
                                pass #print(kb[str(KEYBOARD)])
                                abc.bot.edit_message_text(
                                    chat_id         =   call.message.chat.id,
                                    message_id      =   call.message.message_id,
                                    #parse_mode      =   "Markdown",
                                    text            =   kb[str(TITLE)],
                                    reply_markup    =   kb[str(KEYBOARD)]
                                    )
                            except Exception as e:
                                print("ERROR", e)
                elif str(STASH) in call.data:
                    mess_text = abc.makeCommitText(call)
                    
                    kb = abc.getKeyboard(call.message.chat.id, call.data)
                    if len(abc.menuManager.getS(call.message.chat.id))>1:
                        kb = abc.getKeyboard(call.message.chat.id, abc.menuManager.getS(call.message.chat.id)[-1])
                    else:
                        kb = abc.getKeyboard(call.message.chat.id)
                    
                    if mess_text:
                        abc.bot.reply_to(
                            call.message,
                            text            =   mess_text,
                            reply_markup    =   kb[str(KEYBOARD)]
                            )
                        abc.bot.delete_message(
                            call.message.chat.id,
                            call.message.message_id
                            )
                    elif len( abc.menuManager.getMeasu(call.message.chat.id) )==0 and len( abc.menuManager.getObjPara(call.message.chat.id) )==0 and len( abc.menuManager.getObjPhoto(call.message.chat.id) )==0:
                        abc.bot.reply_to(
                            call.message,
                            #parse_mode      =   "Markdown",
                            text            =   "Жодних данних не введено",
                            reply_markup    =   kb[str(KEYBOARD)]
                            )
                        abc.bot.delete_message(
                            call.message.chat.id,
                            call.message.message_id
                            )
                    else:
                        abc.bot.reply_to(
                            call.message,
                            #parse_mode      =   "Markdown",
                            text            =   "Немає можливості....",
                            reply_markup    =   kb[str(KEYBOARD)]
                            )
                        abc.bot.delete_message(
                            call.message.chat.id,
                            call.message.message_id
                            )
                elif str(COMMIT) in call.data:  
                    try:
                        ##pass #print('In COMMIT')
                        try:
                            if len(abc.menuManager.getMeasu(call.message.chat.id)) > 0:
                                measurements = abc.menuManager.getMeasu( call.message.chat.id )
                                
                                for measu in measurements:
                                    if str(IS_ELECTRO) in measu[str(TYPE)]:
                                        tmp = {
                                            str(INV_NUMBER): measu[str(INV_NUMBER) if INV_NUMBER in measu else ''],
                                            str(VALUE): measu[str(VALUE)],
                                            }
                                        tmp.update( Electro.getInfo(tmp) )
                                        print( Electro.pullMeasurement(tmp) )
                                       
                                print(  Ehz.updateMeasurementDoc( measurements ) )
                            if len(abc.menuManager.getObjPara(call.message.chat.id)) > 0:
                                print( Ehz.updateObjectsParams(abc.menuManager.getObjPara(call.message.chat.id)))
                        except:
                            print("EHZ WASNT UPDATE")

                        try:
                            if len( abc.menuManager.getObjPhoto(call.message.chat.id) ) > 0:
                                print( Scs.pushPhoto(abc.menuManager.getObjPhoto(call.message.chat.id)))
                        except:
                            print("PHOTO WASNT UPLOAD")

                        try:
                            if len(abc.menuManager.getObjPara(call.message.chat.id)) > 0:
                                print( Web1C.updateData(abc.menuManager.getObjPara(call.message.chat.id)))
                        except Exception as e:
                            print ("Web1C WASNT UPLOAD", e)
                        try:
                            if len(abc.menuManager.getObjPara(call.message.chat.id)) > 0:
                                print( Requests().pushSMapInfo( abc.menuManager.getObjPara(call.message.chat.id) ))
                        except:
                            print ("SMapInfo WASNT UPLOAD")
                    
                    finally:
                        abc.menuManager.clrMeasu(call.message.chat.id)
                        abc.menuManager.clrObjPara(call.message.chat.id)
                        abc.menuManager.clrObjPhoto(call.message.chat.id)
                        abc.clearCommit(call.message)
                    
                else:   
                    kb = abc.getKeyboard(call.message.chat.id, call.data)
                    
                    if kb:
                        try:
                            if call.message.text == kb[str(TITLE)]:
                                kb[str(TITLE)] = '{} повторення'.format(kb[str(TITLE)])
                            abc.bot.edit_message_text(
                                chat_id         =   call.message.chat.id,
                                message_id      =   call.message.message_id,
                                parse_mode      =   "Markdown",
                                text            =   kb[str(TITLE)],
                                reply_markup    =   kb[str(KEYBOARD)]
                                )
                        except Exception as e:
                                print("ERROR", e)

            @abc.bot.callback_query_handler(
                func=lambda call: call.data == str(BACK) or Localisator().getLocal(str(BACK)) in call.message.text
            )  # Была нажата кнопка Назад
            def callback_inline(call):
                pass#abc.clearDelList(call.message)
                abc.menuManager.push(User({'chat_id': call.message.chat.id}))
                if len(abc.menuManager.getS(call.message.chat.id))>1:
                    abc.menuManager.popS(call.message.chat.id)
                    call.data = abc.menuManager.getS(call.message.chat.id)[-1]
                
                    if str(EZH_MEASUREMENTS) in call.data:
                        try:
                            if call.message.text == 'Введіть значення для {}'.format(call.data.split(';')[1]):
                                return
                            abc.bot.edit_message_text(
                                chat_id         =   call.message.chat.id,
                                message_id      =   call.message.message_id,
                                parse_mode      =   "Markdown",
                                text            =   'Введіть значення для {}'.format(call.data.split(';')[1]),
                                reply_markup    =   types.InlineKeyboardMarkup()
                                )
                        except Exception as e:
                                print("ERROR", e)
                    else:      
                        kb = abc.getKeyboard(call.message.chat.id, call.data)
                        if kb:
                            try:
                                if call.message.text == kb[str(TITLE)]:
                                    kb[str(TITLE)] = '{} повторення'.format(kb[str(TITLE)])
                                abc.bot.edit_message_text(
                                        chat_id         =   call.message.chat.id,
                                        message_id      =   call.message.message_id,
                                        parse_mode      =   "Markdown",
                                        text            =   kb[str(TITLE)],
                                        reply_markup    =   kb[str(KEYBOARD)]
                                        )
                            except Exception as e:
                                print("ERROR", e)

            @abc.bot.callback_query_handler(
                func=lambda call: call.data == str(BEGIN)
            )  # Была нажата кнопка НАЧАЛО
            def callback_inline(call):
                pass#abc.clearDelList(call.message)
                abc.menuManager.push(User({'chat_id': call.message.chat.id}))
                abc.menuManager.clrS(call.message.chat.id)
                kb = abc.getKeyboard(call.message.chat.id)
                #print(call.message.chat.id)
                if kb:
                    try:
                        if call.message.text == kb[str(TITLE)]:
                            kb[str(TITLE)] = '{} повторення'.format(kb[str(TITLE)])
                        abc.bot.edit_message_text(
                            chat_id         =   call.message.chat.id,
                            message_id      =   call.message.message_id,
                            #parse_mode      =   "Markdown",
                            text            =   kb[str(TITLE)],
                            reply_markup    =   kb[str(KEYBOARD)]
                            )
                    except Exception as e:
                        print("ERROR", e)
            @abc.bot.callback_query_handler(
                func=lambda call: call.data == "eof" or call.data == str(END)
            )  # В случае отсутсвия нужного шага или его обработчика
            def callback_inline(call):
                pass
            try:
                abc.bot.polling()
            except Exception as e:
                print(e)
        except Exception as e:
            print("{}".format(e))
try:
    botManager = BotManager()
    botManager.main()
except Exception as e:
    print(e)
