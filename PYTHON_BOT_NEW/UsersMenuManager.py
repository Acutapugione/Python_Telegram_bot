from Constants import *
from Connections import *
import ast

def show(elem=''):
    if isinstance(elem, (list, set, tuple)):
        for item in elem:
            print(type(item), '\t', item)
    elif isinstance(elem, (int, str, float)):
        print(type(elem), '\t', elem)
    elif isinstance(elem, dict):
        print(type(elem))
        for key, val in elem.items():
            print(key, ' : ', val)
    print('\n\n')
    
class Convertor:
    def strToDict( s =''):
        return ast.literal_eval(s)
    def dictToStr(d = ''):
        return str(d)
    def strArrToDictArr(arr=[]):
        tmp=[]
        for elem in arr:
            if isinstance(elem, (str, int, float)):
                tmp.append(Convertor.strToDict(elem))
            elif isinstance(elem, dict):
                tmp.append(elem)
        return tmp
    def dictArrToStrArr(arr=[]):
        tmp = []
        for elem in arr:
            tmp.append(Convertor.dictToStr(elem))
        return tmp
    
class User():
    def __init__(abc, user={}):
        abc.user = Convertor.dictToStr(user)
        abc.callStack = list()
        abc.measurements = list()
        abc.objParams = list()
        abc.objPhoto = list()
    def show(abc):
        show(abc.user)
    def getDictUser(abc):
        return Convertor.strToDict(abc.user)
    def getStrUser(abc):
        return Convertor.dictToStr(abc.user)
    
    #ФОТО ОБЪЕКТОВ
    def getObjPhoto(abc):
        return abc.objPhoto
    def findObjPhoto(abc, obj):
        tmp = list()
        for photo in abc.objPhoto:
            if obj[str(INDEX)] == photo[str(OBJECT_INDEX) if str(OBJECT_INDEX) in photo else str(INDEX)]:
                tmp.append(photo)
        return tmp
    def pushObjPhoto(abc, photo):
        for item in abc.objPhoto:
            if (item[str(INDEX)]==photo[str(INDEX)] and
               item[str(PHOTO)]==photo[str(PHOTO)]):
                item[str(DATE)]=photo[str(DATE)]
                return
        abc.objPhoto.append(photo)
    def popObjPhoto(abc):
        if len(abc.objPhoto)>0:
            abc.objPhoto.remove(abc.objPhoto[len(abc.objPhoto)-1])
    def clrObjPhoto(abc):
        while len(abc.objPhoto)>0:
            abc.popObjPhoto()
            
    #ПАРАМЕТРЫ ОБЪЕКТОВ
    def getObjPara(abc):
        return abc.objParams
    def pushObjPara(abc, elem):
        for item in abc.objParams:
            if (item[str(INDEX)]==elem[str(INDEX)] and
               item[str(OBJECT_PARAMS)]==elem[str(OBJECT_PARAMS)]):
                item[str(VALUE)]=elem[str(VALUE)]
                return
        abc.objParams.append(elem)
    def popObjPara(abc):
        if len(abc.objParams)>0:
            abc.objParams.remove(abc.objParams[len(abc.objParams)-1])
    def clrObjPara(abc):
        while len(abc.objParams)>0:
            abc.popObjPara()
    #ЗАМЕРЫ
    def getMeasu(abc):
        return abc.measurements
    def pushMeasu(abc, elem):
        for item in abc.measurements:
            if item[str(INDEX)]==elem[str(INDEX)]:
                item[str(VALUE)]=elem[str(VALUE)]
                return
        abc.measurements.append(elem)
    def popMeasu(abc):
        if len(abc.measurements)>0:
            abc.measurements.remove(abc.measurements[len(abc.measurements)-1])
    def clrMeasu(abc):
        while len(abc.measurements)>0:
            abc.popMeasu()
    #СТЭК ШАГОВ        
    def getS(abc):
        return abc.callStack
    def pushS(abc, elem):
        if not elem in abc.callStack:
            abc.callStack.append(elem)
    def popS(abc):
        if len(abc.callStack)>0:
            abc.callStack.remove(abc.callStack[len(abc.callStack)-1])
    def clrS(abc):
        while len(abc.callStack)>0:
            abc.popS()
class Menu():
    def __init__(abc, menu=MENU_ARCH):
        abc.menu = menu
        abc.level = 0
    def show(abc):
        show(abc.menu)
    def getDictMenu(abc):
        return Convertor.strArrToDictArr(abc.menu)
    def getStrMenu(abc):
        return Convertor.dictArrToStrArr(abc.menu)
    def getMenu(abc):
        return abc.menu
    def getTitle(abc):
        tmp = Convertor.strArrToDictArr(abc.menu)
        for elem in tmp:
            for key, val in elem.items():
                if str(TITLE) in key:
                    return val           
    def getIndex(abc):
        tmp = Convertor.strArrToDictArr(abc.menu)
        for elem in tmp:
            for key, val in elem.items():
                if str(INDEX) in key:
                    return val
    def getSubMenu(abc, index, arr=''):  
        if abc.level>5:
            abc.level=0
            return None
        abc.level+=1
        if index == str(STASH):
            return None
            #return {
            #    str(TITLE):str(STASH)
            #    }
        if not arr:
            for elem in abc.getDictMenu():
                
                if elem[str(INDEX)] == index or index in elem[str(INDEX)]:
                    return {
                        str(TITLE): elem[str(TITLE)],
                        str(SUB_MENU) : elem[str(SUB_MENU)]
                        }
                elif elem[str(SUB_MENU)]:
                    for item in elem[str(SUB_MENU)]:
                        
                        if item[str(INDEX)] == index or index in item[str(INDEX)]:
                            return {str(TITLE): item[str(TITLE)],
                                    str(SUB_MENU) : item[str(SUB_MENU)]}
                    return abc.getSubMenu( index, elem[str(SUB_MENU)])
            return abc.getSubMenu( index, elem[str(SUB_MENU)])
        else: 
            for elem in arr:
                if elem[str(INDEX)] == index or index in elem[str(INDEX)]:
                    
                    return {str(TITLE): elem[str(TITLE)],
                                    str(SUB_MENU) : elem[str(SUB_MENU)]}
                elif elem[str(SUB_MENU)]:
                    for item in elem[str(SUB_MENU)]:
                        if item[str(INDEX)].lower() == index.lower() or index.lower() in item[str(INDEX)].lower():
                            return {str(TITLE): item[str(TITLE)],
                                    str(SUB_MENU) : item[str(SUB_MENU)]}
                    return abc.getSubMenu( index, elem[str(SUB_MENU)])
            return abc.getSubMenu( index, elem[str(SUB_MENU)])

                
    
class MenuManager():
    def __init__(abc):
        abc.userMenu = []
        
    def find(abc, s):
        try:
            
            if isinstance(s, str):
                for dict_ in filter(lambda x: s in str(x['user'].getDictUser()['chat_id']) , abc.userMenu):
                    
                    return dict_
            elif isinstance(s, (int, float)):
                
                for dict_ in filter(lambda x: s == x['user'].getDictUser()['chat_id'] , abc.userMenu):
                    
                    return dict_
            else:
                for dict_ in filter(lambda x: x['menu'] == s or x['user']== s, abc.userMenu):
                    return dict_
        except Exception as e:
            print(e)
    def push(abc, user, menu=''):
        if not abc.find(user):
            if menu:
                abc.userMenu.append({'user':user, 'menu':menu})
            else:
                abc.userMenu.append({'user':user, 'menu':Menu()})
    def show(abc):
        for elem in abc.userMenu:
            show(elem)    
    def getDictMenu(abc, user):
        return abc.find(user)['menu'].getDictMenu()
    def getStrMenu(abc, user):
        return abc.find(user)['menu'].getStrMenu()
    def getUser(abc, user):
        if user:
            return abc.find(user)['user']
    def getMenu(abc, user, point=''):
        tmp = list()
        pointLen = None
        
        try:
            pointLen = len(point.split(';')) if len(point.split(';')) is not None else False
            if not point:
                tmp = abc.find(user)['menu']
                
            elif point.lower() == str(WEB_1C_WORK_ORDERS).lower():
                
                tmp = Web1C.getWorkOrders(user)
                
                for elem in tmp:
                    elem[str(TITLE)] = 'Наряд № '+ elem[str(INDEX)]
                    
                    elem[str(CALL_DATA)] = "{};{}".format(elem[str(INDEX)], elem[str(FROM_DB)])
            elif pointLen and str(WEB_1C_WORK_ORDERS) in point:
                
                tmp = Web1C.getObjects(user, point.split(';')[0])
                
                for elem in tmp:
                    
                    elem[str(CALL_DATA)] = "{};{};{}".format(
                        elem[str(INDEX)],
                        elem[str(FROM_DB)],
                        elem[str(ORDER_NUMBER)]
                        )
            elif pointLen and str(WEB_1C_OBJECTS) in point:
                tmp = Web1C.getParams({ str(INDEX) : point.split(';')[0]})
                if tmp is not None and len(tmp)>0:
                    for item in tmp:                        
                        if str(PARAM_CHOSE) in item.keys():
                            item[str(FROM_DB)] = str(WEB_1C_SELECT_PARAMS)
                            item[str(CALL_DATA)] = "{};{};{}".format(
                                item[str(INDEX)],
                                item[str(FROM_DB)],
                                point.split(';')[0]
                            )
                        else:
                            item[str(FROM_DB)] = str(WEB_1C_INPUT_PARAMS)
                            item[str(CALL_DATA)] = "{};{};{}".format(
                                item[str(INDEX)],
                                item[str(FROM_DB)],
                                point.split(';')[0]
                            )                
            elif pointLen and str(WEB_1C_SELECT_PARAMS) in point:
                
                
                params = Web1C.getParams({ str(INDEX) : point.split(';')[2]})
                if params is not None and len(params)>0:
                    for item in params:
                        if item[str(INDEX)] == point.split(';')[0]:
                            for elem in item[str(PARAM_CHOSE)]:
                                obj = dict()
                                obj[str(INDEX)] = item[str(INDEX)]
                                obj[str(TITLE)] = elem
                                obj[str(FROM_DB)] = str(PARAM_CHOSEN)
                                obj[str(CALL_DATA)] = "{};{};{};{}".format(
                                    point.split(';')[0],
                                    obj[str(FROM_DB)],
                                    point.split(';')[2],
                                    item[str(PARAM_CHOSE)].index(elem)
                                    )
                                tmp.append(obj)
                            
            elif pointLen and point.lower() == str(EZH_WORK_ORDERS).lower():
                try:
                    tmp = Requests().getWorkOrders(user)
                    for elem in tmp:
                        elem[str(CALL_DATA)] = "{};{}".format(elem[str(INDEX)], elem[str(FROM_DB)])
                except Exception as e:
                    print(e, " in MenuManager.getMenu(EZH_WORK_ORDERS)")

            elif pointLen and str(EZH_WORK_ORDERS) in point:
                
                tmp = Ehz.getObjectsFromOrder(point.split(';')[0])
                
                for elem in tmp:
                    elem[str(CALL_DATA)] = "{};{};{}".format(
                        elem[str(INDEX)],
                        elem[str(FROM_DB)],
                        elem[str(TYPE)].lower()
                        )
                
            elif pointLen and str(SUSTAIN) in point:
                tmp = Ehz.getSustainTypes()
                
                for elem in tmp:
                    elem[str(CALL_DATA)] = "{};{}".format(
                        elem[str(INDEX)],
                        elem[str(FROM_DB)]
                        )
            elif pointLen and str(EZH_OBJECTS) in point:
                obj = dict()
                obj[str(TYPE)] = point.split(';')[2]
                obj[str(INDEX)] = point.split(';')[0]

                is_photo = abc.isPhotoFilled(obj, user)
                is_coords = abc.isCoordsParamFilled(obj, user)

                if  is_photo and is_coords:
                    tmp = Ehz.getObjectNullParams(obj)
                    tmp.extend( Ehz.getObjectMeasurements(obj) )

                    tmp.append({ 
                            str(INDEX) : obj[str(INDEX)],
                            str(TYPE): obj[str(TYPE)],
                            str(PHOTO) : None,
                            str(OBJECT_PARAMS): str(PHOTO),
                            str(VALUE): None,
                            str(FROM_DB):str(EZH_OBJ_NULL_PARAMS),
                            str(OBJECT_INDEX): obj[str(INDEX)],
                           })
                    '''tmp.append({ 
                            str(INDEX) : obj[str(INDEX)],
                            str(TYPE): obj[str(TYPE)],
                            str(OBJECT_PARAMS): str(COORDINATES),
                            str(VALUE): None,
                            str(FROM_DB):str(EZH_OBJ_NULL_PARAMS),
                            str(OBJECT_INDEX): obj[str(INDEX)],
                           })   '''

                    for elem in tmp:
                        elem[str(CALL_DATA)] = "{};{};{};{};{}".format(
                            elem[str(INDEX)],
                            elem[str(VIEW)] if str(VIEW) in elem else elem[str(OBJECT_PARAMS)] if str(OBJECT_PARAMS) in elem else '',
                            elem[str(FROM_DB)],
                            elem[str(TYPE)].lower(),
                            elem[str(OBJECT_INDEX)] if str(OBJECT_INDEX) in elem else elem[str(VALUE)] if str(VALUE) in elem else ''
                            )
                else:
                    if not is_photo:
                        tmp.append({ 
                            str(INDEX) : obj[str(INDEX)],
                            str(TYPE): obj[str(TYPE)],
                            str(PHOTO) : None,
                            str(OBJECT_PARAMS): str(PHOTO),
                            str(VALUE): None,
                            str(FROM_DB):str(EZH_OBJ_NULL_PARAMS),
                            str(OBJECT_INDEX): obj[str(INDEX)],
                           })
                    if not is_coords:
                        tmp.append({ 
                            str(INDEX) : obj[str(INDEX)],
                            str(TYPE): obj[str(TYPE)],
                            str(OBJECT_PARAMS): str(COORDINATES),
                            str(VALUE): None,
                            str(FROM_DB):str(EZH_OBJ_NULL_PARAMS),
                            str(OBJECT_INDEX): obj[str(INDEX)],
                           })   
                #if str(PHOTO) not in obj:
                #    obj.update( { str(PHOTO) : None } )
                #    tmp.append(obj)
                #    for elem in tmp:
                #        if str(PHOTO) in elem:
                #            elem[str(OBJECT_PARAMS)] = str(PHOTO)
                #            elem[str(FROM_DB)]= str(EZH_OBJ_NULL_PARAMS)
                #            elem[str(VALUE)] = None
                    
                #            elem[str(CALL_DATA)] = "{};{};{};{};{}".format(
                #                elem[str(INDEX)],
                #                elem[str(OBJECT_PARAMS)] if str(OBJECT_PARAMS) in elem else elem[str(VIEW)],
                #                elem[str(FROM_DB)],
                #                elem[str(TYPE)].lower(),
                #                elem[str(VALUE)]
                #                )
                                
                try:
                    if str(IS_SKZ).lower() in point.lower():
                        tmpObj = {
                                str(INV_NUMBER): str(Ehz.getObjectInfo(obj)[str(INV_NUMBER)]),
                                str(OBJECT_PARAMS) : str(ELECTRICITY_METER_READING),
                                str(VALUE) : 0,
                                }
                        tmpObj.update(Electro.getInfo(tmpObj))
                        tmp.append(tmpObj)
                    
                except Exception as e:
                    print(e, point, ELECTRICITY_METER_READING)
                for elem in tmp:
                    
                    elem[str(CALL_DATA)] = "{};{};{};{};{}".format(
                        elem[str(INDEX)],
                        elem[str(VIEW)] if str(VIEW) in elem else elem[str(OBJECT_PARAMS)] if str(OBJECT_PARAMS) in elem else '',
                        elem[str(FROM_DB)] if str(FROM_DB) in elem else str(EZH_OBJ_NULL_PARAMS),
                        elem[str(TYPE)].lower(),
                        elem[str(OBJECT_INDEX)] if str(OBJECT_INDEX) in elem else obj[str(INDEX)]
                        )
            else:
                try:
                    tmp = abc.find(user)['menu'].getSubMenu(point)
                except:
                    tmp = list()
        except Exception as e:
            print(e, point, ' in MenuManager.getMenu()')
            print(sys.exc_info())
        finally:
            return tmp
    def isPhotoFilled(abc, obj, user):
        for elem in abc.getObjPhoto(user):
            print(elem[str(OBJECT_INDEX)])
        return len(
            list(
                filter(
                    lambda element: obj[str(INDEX)]== element[str(OBJECT_INDEX)] 
                    if str(OBJECT_INDEX) in element 
                    else element[str(INDEX)] == obj[str(INDEX)] ,
                    abc.getObjPhoto(user))
                )
            )>0
    def isCoordsParamFilled(abc, obj, user):
        return len(
            list(
                filter(
                    lambda element: str(COORDINATES) in element[str(OBJECT_PARAMS)] 
                    and obj[str(INDEX)]== element[str(OBJECT_INDEX)] 
                    if str(OBJECT_INDEX) in element 
                    else obj[str(INDEX)]== element[str(INDEX)], 
                    abc.getObjPara(user)
                    )
                )
            )>0
    #ШАГИ
    def pushS(abc, user, elem):
        abc.find(user)['user'].pushS(elem) if 'user' in abc.find(user) and abc.find(user) is not None else print(user)
        
    def popS(abc, user):
        abc.find(user)['user'].popS()
        
    def getS(abc, user):
        try:
            return abc.find(user)['user'].getS()
        except Exception as e:
            print(e)
            
    def clrS(abc, user):
        try:
            return abc.find(user)['user'].clrS()
        except Exception as e:
            print(e)
    #ЗАМЕРЫ
    def pushMeasu(abc, user, elem):
        abc.find(user)['user'].pushMeasu(elem)
        
    def popMeasu(abc, user):
        abc.find(user)['user'].popMeasu()
        
    def getMeasu(abc, user):
        try:
            return abc.find(user)['user'].getMeasu()
        except Exception as e:
            print(e)
            
    def clrMeasu(abc, user):
        try:
            return abc.find(user)['user'].clrMeasu()
        except Exception as e:
            print(e)
    
    #ПАРАМЕТРЫ ОБЪЕКТОВ
    def getObjPara(abc, user):
        try:
            return abc.find(user)['user'].getObjPara()
        except Exception as e:
            print(e)
            
    def pushObjPara(abc, user, elem):
        abc.find(user)['user'].pushObjPara(elem)
        #print(abc.find(user)['user'].getObjPara())
        
    def popObjPara(abc, user):
        abc.find(user)['user'].popObjPara()
        
    def clrObjPara(abc, user):
        try:
            return abc.find(user)['user'].clrObjPara()
        except Exception as e:
            print(e)
            
    #ФОТО ОБЪЕКТОВ
    def getObjPhoto(abc, user):
        try:
            return abc.find(user)['user'].getObjPhoto()
        except Exception as e:
            print(e)
    def findObjPhoto(abc, user, obj):
        return abc.find(user)['user'].findObjPhoto(obj)
    def pushObjPhoto(abc, user, photo):
        abc.find(user)['user'].pushObjPhoto(photo)

    def popObjPhoto(abc, user):
        abc.find(user)['user'].popObjPhoto()
        
    def clrObjPhoto(abc, user):
        try:
            return abc.find(user)['user'].clrObjPhoto()
        except Exception as e:
            print(e)   
print("MenuManager_v2 imported")

