import json

from zeep import Client, helpers

from Connections import *
from Constants import *


class Web1C:
    def get_number(phone_number): 
        '''Процедура получения и очистки номера телефона, Возврат готового номера телефона'''
        phone_brutal = phone_number
        phone_number= ''
        #phone_brutal = phone_number
        #phone_number=''
        for i in phone_brutal:        #Перебираем каждый символ
            if i.isnumeric() == True: #Выбираем только числа
                phone_number += i
        #print(phone_number)
        #Заполняем согласно маски ввода
        phone_brutal3 = phone_number[len(phone_number) - 2:len(phone_number)]
        phone_brutal2 = phone_number[len(phone_number) - 4:len(phone_number) - 2]
        phone_brutal1 = phone_number[len(phone_number) - 7:len(phone_number) - 4]
        phone_number = phone_brutal1 + '-' + phone_brutal2 + '-' + phone_brutal3
            
        #print(phone_number)
        
        return phone_number 
        
    def getClient():
        web1C = connections['1C']
        client = Client(web1C['1COrdersServ'])
        return client
        
    def getParamsClient():
        web1C = connections['1C']
        client = Client(web1C['1CObjectsServ'])
        return client
        
    def check_id(chat_id):
        return len(Web1C.getObjects(chat_id)) is not 0

    def getWorkOrders(phone):
        client = Web1C.getClient()
        req_data = dict({ 'НомерТелефона': str(phone) })
        res_obj = client.service.Get(**req_data)
        objects = list()
        if isinstance(res_obj, (tuple, list, set)):
            for order in res_obj:
                if 'Nomer' in order:
                    objects.append({
                            str(INDEX): order['Nomer'],
                            str(FROM_DB): str(WEB_1C_WORK_ORDERS),
                            })

        objects = list({v[str(INDEX)]:v for v in objects}.values())
        return objects
        
    def getObjects(phone, num=''):
        client = Web1C.getClient()
        req_data = dict({ 'НомерТелефона': str(phone) })
        res_obj = client.service.Get(**req_data)
        #print(type(res_obj))
        objects = list()
        if isinstance(res_obj, (tuple, list, set)):
            for order in res_obj:
                if num is not '':
                    if (order['Nomer'] == num) if 'NaryadSostavs' in order and 'Nomer' in order else False:
                        for item in order['NaryadSostavs']:
                            tmp = dict({
                                        str(INDEX): item.InvNomer,
                                        str(FROM_DB): str(WEB_1C_OBJECTS),
                                        str(ORDER_NUMBER) : order['Nomer'],
                                        str(TITLE): item.Name,
                                        str(TYPE): item.Categoriya,
                                        str(COMMENTS): None
                                        },)
                            objects.append(tmp)
                else:
                    for item in order['NaryadSostavs']:
                        tmp = dict({
                                        str(INDEX): item.InvNomer,
                                        str(FROM_DB): str(WEB_1C_OBJECTS),
                                        str(ORDER_NUMBER) : order['Nomer'],
                                        str(TITLE): item.Name,
                                        str(TYPE): item.Categoriya,
                                        str(COMMENTS): None
                                        },)
                        objects.append(tmp)
        #objects = list({v[str(INDEX)]:v for v in objects}.values())
        return objects

    def getParams(obj):
        client = Web1C.getParamsClient()
        req_data = dict({ 'ИнвНомер' : str(obj[str(INDEX)]) })
        res_obj = client.service.Get(**req_data)
        input_dict = helpers.serialize_object(res_obj)
        output_dict = json.loads(json.dumps(input_dict))
        obj[str(OBJECT_PARAMS)] = list()
            
        for item in output_dict:
            #print(item)
            if (item[str(VALUE)] if str(VALUE) in item else None) is not None :
                obj[str(OBJECT_PARAMS)].append({
                        str(TITLE) : item['Name'],
                        str(INDEX): item['Id'],
                        str(PARAM_CHOSE): item[str(VALUE)].split(';')[:-1] if (len(item[str(VALUE)].split(';')[:-1]) > 0) else None ,
                        str(VALUE): None
                        })
            else:
                obj[str(OBJECT_PARAMS)].append({
                        str(TITLE): item['Name'],
                        str(INDEX): item['Id'],
                        str(VALUE): None
                        })
            
        return obj[str(OBJECT_PARAMS)]
        
    def updateData(objects):
        try:
            client = Web1C.getClient()
            input_data = post = ''
            #print(objects)
            if objects:
                tmp = list()
                for item in objects:
                    curr_elem = next((elem for elem in tmp if elem[str(OBJECT_INDEX)] == item[str(OBJECT_INDEX)]), False)
                    if curr_elem:
                        #curr_elem[str(OBJECT_PARAMS)].append({ str(VALUE):
                        #item[str(VALUE)], str(INDEX): item[str(INDEX)] })
                        curr_elem[str(OBJECT_PARAMS)].append({ str(str(VALUE)): item[str(str(VALUE))], str(INDEX): item[str(INDEX)] })
                    else:
                        #print(type(item), item)
                        tmp.append({
                                    str(ORDER_NUMBER): item[str(ORDER_NUMBER)],
                                    str(OBJECT_INDEX): item[str(OBJECT_INDEX)],
                                    str(OBJECT_PARAMS): [{
                                            str(VALUE): item[str(VALUE)] if str(VALUE) in item else '0' ,
                                            #str(VALUE): item[str(VALUE)]
                                            #if str(VALUE) in item else '0'
                                            #,
                                            str(INDEX): item[str(INDEX)] if str(INDEX) in item else '0',
                                            }] 
                                    })
                for elem in tmp:
                    if str(OBJECT_PARAMS) in elem:
                        input_data = {
                            'НомерНаряда':  str(elem[str(ORDER_NUMBER)]),
                            'ИнвНомер': str(elem[str(OBJECT_INDEX)]),
                            'Комментарий': str(datetime.datetime.now().strftime("%m.%d.%Y. %H:%M:%S")),
                            'Параметры' : str(elem[str(OBJECT_PARAMS)]),
                            }
                            
                        post = client.service.Post(**input_data)

                return {str(SUSTAIN): True, 'Data': input_data , 'Message': post}
        except Exception as e:
            return {str(SUSTAIN): False, 'Data': input_data , 'Message': post, 'exception': e }
