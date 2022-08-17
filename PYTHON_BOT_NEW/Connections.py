from Constants import *
from TRANSLAITS import *
##import json
##import firebirdsql as fdb
##import pypyodbc
##import datetime
import re
from DB_Worker import *
from Web1C import *
from Electro import *
from Ehz import *
from Scs import *
from Smap import *
from Debtors import *

re_pattern = r"""
[+-]?
(?:
    ([+-]\d+([.,]\d*)|
    ([+-]\d*([.,]\d+)|
    ([+-]\d+)))
)
"""
re_executor = re.compile(re_pattern, re.VERBOSE)

print("Connections.py imported")

def getDecimally(text):
    decimally = ''
    for elem in text:
        try:
            decimally = '{}{}'.format(decimally, int(elem))
        except:
            pass
    return int(decimally)

def controll_vvoda(message):
    
    text = message.text
    if text is None or '/' in text:
        return False
    else:
        first_res = ""
        first_reinc = text.replace(',','.')
        point = first_reinc.find('.')
        minus = first_reinc.find('-')
        if point != -1:
            second_reinc = first_reinc[point+1:int(len(text))]
            first_reinc = first_reinc[0:point+1]
            without_point = first_reinc[0:point]
            for i in without_point:
                if i.isnumeric() == True:
                    first_res += i
                    
            first_res += first_reinc[point]

            for i in second_reinc:
                if i.isnumeric() == True:
                    first_res += i
            try:
                text = float(first_res)
                if minus != -1:
                    text = text*(-1)
            except Exception:
                pass #print('U can\'t converts this '+str(text)+' to float')
                return False
        else:
            for i in first_reinc:
                if i.isnumeric() == True:
                    first_res += i
            try:
                text = int(first_res)
                if minus != -1:
                    text = text*(-1)
            except Exception:
                pass #print('U can\'t converts this '+str(text)+' to float')
                return False
        text = str(text)
    return text

def switch(match, dictionary, default=None):
    for key in dictionary.keys():
        if key == match:
            pass #print(match, ' : ', key)
            return dictionary.get(key)
    return default



class Localisator():
        def getLocal(abc, search):
                for key, val in TRANSLAITS.items():
                        if search == key:
                                return val
                        if search == val:
                                return key
                return search
        
        def getLocalList(abc, s_list):
                tmp = []
                for elem in s_list:
                    if isinstance(elem, dict):
                        tmp.append(abc.getLocalDict(elem))
                    else:
                        tmp.append( abc.getLocal(elem) )
                return tmp
            
        def getLocalDict(abc, s_dict):
            if isinstance(s_dict, dict):
                tmp = dict()
                for key, val in s_dict.items():
                    tmp[abc.getLocal(key)]=abc.getLocal(val)
                return tmp
            elif isinstance(s_dict, (list, tuple, set)):
                return abc.getLocalList(s_dict)
            else:
                return abc.getLocal(s_dict)

class Requests():
        def __init__(abc):
                abc.info=''
                
        def pushSMapInfo(abc, info):
            if isinstance(info, (list, tuple, set) ):
                for item in info:
                    abc.pushSMapInfo(item)
            elif isinstance(info, (dict) ):
                try:
                    res = Smap.insertLocation(info)
                    if res[str(SUSTAIN)]:
                        pass
                    else:
                        try:
                            res =  Smap.updateLocation(info)
                            if res[str(SUSTAIN)]:
                                pass
                        except Exception as e:
                            print(e)
                except Exception as e:
                    print(e)
            else:
                print(type(info), info)
                
        def getAvailability(abc, chat_id=''):#returns list of db what user_id can work
                availableList = []
                if Ehz.check_id(chat_id) is True:
                        availableList.append(str(IS_EZH))
                #print(availableList)
                if Electro.check_id(chat_id) is True:
                        availableList.append("Electro")
                #print(availableList)
                if Debtors().check_id(chat_id) is True:
                        availableList.append(str(IS_DEBTORS))
                #print(availableList)
                if Web1C.check_id(chat_id) is True:
                        availableList.append(str(IS_WEB_1C))
                #print(availableList)
                
                return availableList

        def getWorkOrders(abc, chat_id=''):
                workOrders = []
                dbList = abc.getAvailability(chat_id)
                if str(IS_EZH) in dbList:
                    if Ehz.getWorkOrders(chat_id) is not None:
                        workOrders.extend( Ehz.getWorkOrders(chat_id))
                #if str(IS_WEB_1C) in dbList:
                #    workOrders += Web1C.getWorkOrders(chat_id)
                #print(workOrders)
                return workOrders
        
        def getDistricts(abc, chat_id=''):
                districts = []
                dbList = abc.getAvailability(chat_id)
                if str(IS_DEBTORS) in dbList:
                    districts += Debtors().getDistricts()  
                return districts
        
        def getSettlements(abc, chat_id='', district=''):
                settlements = []
                dbList = abc.getAvailability(chat_id)
                if str(IS_DEBTORS) in dbList:
                    settlements += Debtors().getSettlements(district)  
                return settlements
        
        def getDebtors(abc, chat_id='', settlement='', ls=''):
                debtors = []
                dbList = abc.getAvailability(chat_id)
                if str(IS_DEBTORS) in dbList:
                    debtors += Debtors().getDebtors(settlement, ls)  
                return debtors
        
        def getDebtorInfo(abc, chat_id='', debtor=''):
                dbList = abc.getAvailability(chat_id)
                if str(IS_DEBTORS) in dbList:
                        return Debtors().getDebtorInfo(debtor)
                    
        def getObjects(abc, chat_id='', order_id=''):
                objects = []
                dbList = abc.getAvailability(chat_id)
                if str(IS_EZH) in dbList:
                    if Ehz.getObjects(chat_id, Ehz.getWorkOrders(chat_id, order_id)) is not None:
                        objects.extend(Ehz.getObjects(chat_id, Ehz.getWorkOrders(chat_id, order_id)))
                if str(IS_WEB_1C) in dbList:
                    pass #print(dbList)
                    objects.extend(Web1C.getObjects(chat_id, order_id))
                    
                return objects
                
                
        def check_id(abc, chat_id=''): #returns true if found
                if Ehz.check_id(chat_id) is True or Electro.check_id(chat_id) is True or Debtors.check_id(chat_id) is True:
                        return True
                return False
