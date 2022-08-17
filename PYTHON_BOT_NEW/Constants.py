connections = {
    "1C"  :   {
        "1COrdersServ" : "http://192.168.1.7/WS/ws/Naryadi?wsdl",
        "1CObjectsServ": "http://192.168.1.7/WS/ws/Parametrs?wsdl",
        },
    "EHZ" :   {
        "host" : '192.168.1.248',
        "database": 'v:\Oper\Ehz.fdb',
        "port" : '3075',
        "user" : 'sysdba',
        "password": 'masterkey',
        "charset": 'UTF8',
        },
    "Scs": {
        "driver" : "{SQL Server}",
        "server" : "192.168.1.5",
        "database" : "scs",
        "uid" : "sc",
        "pwd" : "masterkey",
        "charset": 'UTF8',
        },
    "Map": {
        "driver" : "{SQL Server}",
        "server" : "192.168.1.5",
        "database" : "smap",
        "uid" : "sc",
        "pwd" : "masterkey",
        "charset": 'UTF8',
        },
    "Electro": {
        "host" : '192.168.1.248',
        "database": 'v:\Oper\Operativka_expl.fdb',
        "port":'3075',
        "user": 'sysdba',
        "password": 'masterkey',
        "charset": 'UTF8',
        },
    "Debtors" : {
        "host" : '192.168.1.248',
        "database": 'v:\Oper\Debtors.fdb',
        "port":'3075',
        "user": 'sysdba',
        "password": 'masterkey',
        "charset": 'UTF8',
        },
    }
TEST_MODE = False
ICONS = {
    'x':'\u274C',
    'arrow_heading_up'  :'\U0001F51D',
    'arrow_left'        :'\U0001F519',
    'refresh'           :'\U0001F504',
    'accept'            :'\U0001F4E5',
    'commit'            :'\U0001F44C',
    'stash'             :'\U0001F4C2',
    }

#constants
BACK_TITLE = 'Повернутись до попереднього меню?'
BACK = 'back'
BEGIN_TITLE = 'Повернутись на початок?'
BEGIN = 'start'

STASH_TITLE = ICONS['stash']#'Підтвердити відправлення?'
STASH = 'look_at_stash'

COMMIT_TITLE = ICONS['commit']#'Підтвердити відправлення?' accept
COMMIT = 'commit'

MAIN = 'main'
DB_CHOSE = 'bdChoose'
PARAM_CHOSE = 'selectParam'
PARAM_CHOSEN = 'paramSelected'
ORDER_TYPES = 'workTypes'
OBJECTS = 'objects'
OBJECT_PARAMS = 'params'
WORK_ORDERS = 'naryads'
ORDERS = 'orders'
SUB_MENU = 'points'
KEYBOARD = 'keyboard'
TITLE = 'name'
INDEX = 'id'
OBJECT_INDEX = 'obj_id'
LEVEL = 'level'
IS_VALUE = 'isValue'
IS_PARAM = 'isParam'
END = 'end'
DATE = 'dateTime'
VALUE = 'my_value' #'Value'#
VIEW = 'my_view'

#for objects
CATEGORIE= 'categorie'
TYPE = 'type_name'
CITY = 'city'
LOCATION = 'adres'
SETTLEMENT = 'settlement'
PHONE = 'phone'
LONGITUDE = 'longitude'
LATITUDE = 'latitude'
COORDINATES = 'coords'
INV_NUMBER = 'inv_numb'
ORDER_NUMBER = 'orderNumber'
SUSTAIN = 'status'
SUSTAIN_TITTLE = 'Стан об\'єкту'
COMMENTS = 'comments'
OBJECT_CLASS = 'OBJ_CLASS'
GRM_CLASS = 'GRMModule.Object'
ORDER_MENU = 'orders'
ORDER_CLASS = 'WorkOrderModule.WorkOrder'
CARD_LIST = 'cards'
FROM_DB = 'fromWhatDB'
PHOTO = 'photo'
ELECTRICITY_METER_READING = 'electro_met'
#for menus
CALL_DATA = 'callbackData'

IS_EZH = 'is_Ehz'
EZH_WORK_ORDERS = 'is_Ehz_Orders'
EZH_OBJECTS = 'is_Ehz_Objects'
EZH_OBJ_INFO = 'is_Ehz_Object_Info'
EZH_OBJ_NULL_PARAMS = 'is_Ehz_Object_Null_Parameters'
EZH_OBJ_PHOTO = 'is_Ehz_Object_Photo'
EZH_MEASUREMENTS = 'is_Ehz_Measurements'
EZH_SUSTAIN_TYPES= 'is_Ehz_Sustainee_Types'

ELECTRO_DB = 'Electricity_met'

IS_WEB_1C = 'is_Web_1c'
WEB_1C_WORK_ORDERS = 'is_Web_1c_Orders'
WEB_1C_OBJECTS = 'is_Web_1c_Objects'
WEB_1C_INPUT_PARAMS = 'Web_1c_Inputs' 
WEB_1C_SELECT_PARAMS = 'Web_1c_Selects'#Selective

IS_WEBS = 'is_Webs'
WEBS_WORK_ORDERS = 'is_Webs_Orders'
WEBS_OBJECTS= 'is_Webs_Objects'

IS_GRP_SHRP='is_GRP_SHRP'
GRP_SHRP_WORK_ORDERS='is_GRP_SHRP_Orders'
GRP_SHRP_OBJECTS='is_GRP_SHRP_Objects'

IS_DEBTORS='is_Debtors'
IS_DISTRICT='is_District'

DISTRICTS = 'districts'
#DISTRICT_CLASS = 'DebtorsModule.DistrictObj'
DISTRICT_CLASS = 'DebtorsModule_v2.DistrictObj'
SETTLEMENTS = 'settlements'
#SETTLEMENT_CLASS = 'DebtorsModule.SettlementObj'
SETTLEMENT_CLASS = 'DebtorsModule_v2.SettlementObj'
DEBTORS = 'debtors'
#DEBTOR_CLASS = 'DebtorsModule.DebtorsObj'
DEBTOR_CLASS = 'DebtorsModule_v2.DebtorsObj'

IS_SKZ = 'is_Skz'
IS_IFZ = 'is_Ifz'
IS_PM = 'is_PM'
IS_ELECTRO = 'is_electro_met'
photoAsk = {
    str(PHOTO): True,
    }
inputAsk = {
    str(EZH_MEASUREMENTS) : True,
    str(EZH_OBJ_NULL_PARAMS):True,
    str(WEB_1C_INPUT_PARAMS): True,
    #str(WEB_1C_SELECT_PARAMS):True,
    str(INV_NUMBER):True,
    str(COMMENTS): True,
    str(ELECTRICITY_METER_READING): True,
}
geoAsk = {
    str(LONGITUDE) : True,
    str(LATITUDE) : True,
    str(COORDINATES) : True,
}
inputStr = {
    str(COMMENTS): True,
    str(WEB_1C_INPUT_PARAMS):True,
    #str(WEB_1C_SELECT_PARAMS): True,
    str(ELECTRICITY_METER_READING): True,
    }
sqlStatement = {
    'SELECT': True,
    'FROM': True,
    'JOIN': True,
    'GROUP BY': True,
    'SORT': True,
    'MAX': True,
    'COUNT': True,
    'AVG': True,
    'MIN': True,
    'SUM': True,
    'UNIQUE': True,
    'FIRST': True,
    
    }
MENU_ARCH = [
    {
        str(TITLE) : "Головне меню",
        str(INDEX) : str(MAIN),
        str(SUB_MENU) : [{

            str(TITLE) : "Вибір напряму робіт",
            str(INDEX) : str(ORDER_TYPES),
            str(SUB_MENU) : [{

                str(TITLE) : "Електрохімічний захист",
                str(INDEX) : str(IS_EZH),
                str(SUB_MENU) : [{

                    str(TITLE) : "Вибір наряду",
                    str(INDEX) : str(EZH_WORK_ORDERS),
                    str(SUB_MENU) : [{

                        str(TITLE) : "Вибір об\'єкту",
                        str(INDEX) : str(EZH_OBJECTS),
                        str(SUB_MENU) : [{

                            str(TITLE) : "Вибір параметру",
                            str(INDEX): str(OBJECT_PARAMS),
                            str(SUB_MENU) : [],

                            }]
                        }]
                    }]
                },
            {
               
                str(TITLE) : "Експлуатація",
                str(INDEX) : str(IS_WEB_1C),
                str(SUB_MENU) : [{

                    str(TITLE) : "Вибір наряду",
                    str(INDEX) : str(WEB_1C_WORK_ORDERS),
                    str(SUB_MENU) : [{

                        str(TITLE) : "Вибір об\'єкту",
                        str(INDEX) : str(WEB_1C_OBJECTS),
                        str(SUB_MENU) : [{

                            str(TITLE) : "Вибір параметру",
                            str(INDEX): str(OBJECT_PARAMS),
                            str(SUB_MENU) : [],

                            }]
                        }]
                    }]
                },
                             ]
            }]
        }]

print("Constants.py imported")
'''{
    str(TITLE) : "Порушення",
    str(INDEX) : str(IS_DEBTORS),
    str(SUB_MENU) : [{

        str(TITLE) : "Вибір дільниці",
        str(INDEX) : str(DISTRICTS),
        str(SUB_MENU) : [{

            str(TITLE) : "Вибір населенного пункту",
            str(INDEX) : str(SETTLEMENTS),
            str(SUB_MENU) : [],
            }]
        }]
    },                
{
    str(TITLE) : "Газові мережі",
    str(INDEX) : str(IS_WEBS),
    str(SUB_MENU) : [{

        str(TITLE) : "Вибір наряду",
        str(INDEX) : str(WEBS_WORK_ORDERS),
        str(SUB_MENU) : [{

            str(TITLE) : "Вибір об\'єкту",
            str(INDEX) : str(WEBS_OBJECTS),
            str(SUB_MENU) : [{

                str(TITLE) : "Вибір параметру",
                str(INDEX): str(OBJECT_PARAMS),
                str(SUB_MENU) : []
                }]
            }]
        }]
    },
{
    str(TITLE) : "ГРП(ШРП)",
    str(INDEX) : str(IS_GRP_SHRP),
    str(SUB_MENU) : [{

        str(TITLE) : "Вибір наряду",
        str(INDEX) : str(GRP_SHRP_WORK_ORDERS),
        str(SUB_MENU) : [{

            str(TITLE) : "Вибір об\'єкту",
            str(INDEX) : str(GRP_SHRP_OBJECTS),
            str(SUB_MENU) : [{

                str(TITLE) : "Вибір параметру",
                str(INDEX): str(OBJECT_PARAMS),
                str(SUB_MENU) : []
                }]
            }]
        }]                                 
    },'''
            
                    
