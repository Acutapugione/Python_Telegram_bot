from Constants import *
from Connections import *
import firebirdsql as fdb
import datetime
class Ehz():
        def getCon():
                ehz = connections['EHZ']
                return fdb.connect(
                    host=ehz['host'],
                    database=ehz['database'],
                    port = ehz['port'],
                    user=ehz['user'],
                    password=ehz['password'],
                    charset=ehz['charset']
                    )
        
        def check_id(chat_id=''):
            if chat_id:
                tables = [
                    {
                        'table' : 'T23',
                        'as'    : 'Workers',
                        },
                    ]
                fields = [
                    'id as '+str(INDEX),
                    'F1828 as chat_id',
                    'F104 as FIO',
                    'F1102 as Status',
                    'F1803 as Ph_number',
                    ]
                
                where = 'F1102 = 1 and F1828 = \'{}\''.format(chat_id)
                
                tmp = DB_Worker.selectRecords(
                    con=Ehz.getCon(),
                    fields=fields,
                    tables=tables,
                    where=where
                )
                for elem in tmp:
                    return True
            return False
     
        def getWorkOrders(chat_id='', order_id=''):
            tables = [
            {
                'table' : 'T162',
                'as'    : 'WorkersInNaryad',
                },
            {
                'table' : 'T23',
                'as'    : 'Workers',
                'join'  : 'LEFT JOIN',
                'on'    : 'Workers.Id = WorkersInNaryad.F854',
                },
            {
                'table' : 'T151',
                'as'    : 'WorkOrders',
                'join'  : 'LEFT JOIN',
                'on'    : 'WorkersInNaryad.pId = WorkOrders.id',
                },
            {
                'table' : 'T244',
                'as'    : 'WorkTypes',
                'join'  : 'LEFT JOIN',
                'on'    : 'WorkOrders.F1834 = WorkTypes.id',
                },
            ]
            fields = [
                'WorkOrders.id as '+str(INDEX),
                'WorkOrders.F839 as '+str(TITLE),
                'WorkTypes.F1305 as '+str(TYPE),                
                ]
            where =(
                "Workers.F1102 = 1 and " +
                "WorkOrders.F1073 = 0 and " +
                "Workers.F1828 = {} and " +
                "WorkOrders.F840 <= '{}' "
                ).format(chat_id, datetime.date.today())
            if order_id:
                where = "{} and WorkOrders.id = {}".format(where, order_id)
            group_by = [ str(INDEX), str(TITLE), str(TYPE) ]
            return DB_Worker.selectRecords(
                con=Ehz.getCon(),
                fields=fields,
                group_by=group_by,
                tables=tables,
                where=where,
                from_db=str(EZH_WORK_ORDERS)
                )
        
        def getObjects(chat_id='', orders=''):  
            
            fieldsSKZ = [
                'Object.id        as '+str(INDEX),
                'Object.F632      as '+str(TITLE),
                'Object.F1781     as '+str(LONGITUDE),
                'Object.F1782     as '+str(LATITUDE),
                'Object.F691      as '+str(INV_NUMBER),
                'Object.F1780     as '+str(COMMENTS),
                'Statuses.F838    as '+str(SUSTAIN),
                'Categories.F1838 as '+str(CATEGORIE),
                ]
            fieldsIFZ = [
                'Object.id        as '+str(INDEX),
                'Object.F1042     as '+str(TITLE),
                'Object.F1836     as '+str(LONGITUDE),
                'Object.F1837     as '+str(LATITUDE),
                'Object.F1769     as '+str(COMMENTS),
                'Types.F601       as '+str(TYPE),
                'Statuses.F838    as '+str(SUSTAIN),
                'Categories.F1838 as '+str(CATEGORIE),
                ]
            
            tablesIFZ = [
                {
                    'table' : 'T151',
                    'as'    : 'Naryad',
                    },
                {
                    'table' : 'T161',
                    'as'    : 'Vipusk',
                    'join'  : 'LEFT JOIN',
                    'on'    : 'Vipusk.pId = Naryad.id',
                    },
                {
                    'table' : 'T135',
                    'as'    : 'Object',
                    'join'  : 'LEFT JOIN',
                    'on'    : 'Vipusk.F1043 = Object.id',
                    },
                {
                    'table' : 'T110',
                    'as'    : 'Types',
                    'join'  : 'LEFT JOIN',
                    'on'    : 'Object.F739 = Types.id',
                    },
                {
                    'table' : 'T357',
                    'as'    : 'Categories',
                    'join'  : 'LEFT JOIN',
                    'on'    : 'Object.F1864 = Categories.F1839',
                    },
                {
                    'table' : 'T157',
                    'as'    : 'Statuses',
                    'join'  : 'LEFT JOIN',
                    'on'    : 'Object.F1785 = Statuses.id',
                    },
                ]
            tablesSKZ = [
                {
                    'table' : 'T151',
                    'as'    : 'Naryad',
                    },
                {
                    'table' : 'T161',
                    'as'    : 'Vipusk',
                    'join'  : 'LEFT JOIN',
                    'on'    : 'Vipusk.pId = Naryad.id',
                    },
                {
                    'table' : 'T115',
                    'as'    : 'Object',
                    'join'  : 'LEFT JOIN',
                    'on'    : 'Vipusk.F884 = Object.id',
                    },
                {
                    'table' : 'T357',
                    'as'    : 'Categories',
                    'join'  : 'LEFT JOIN',
                    'on'    : 'Object.F1864 = Categories.F1839',
                    },
                {
                    'table' : 'T157',
                    'as'    : 'Statuses',
                    'join'  : 'LEFT JOIN',
                    'on'    : 'Object.F1785 = Statuses.id',
                    },
                ]

            if orders=='':
                orders = Ehz.getWorkOrders(chat_id)
            ordersList = set()
            
            sqlwhere = "Naryad.F839 = "
            objectsList = list()
            if orders is not None:
                
                for order in orders:
                    if isinstance(order, (dict)):
                        sqlwhere = "Naryad.id = "
                        for key, value in order.items():
                            if key == str(INDEX):
                                ordersList.add(value)
                    else:
                        ordersList.add( order.split(';')[0].strip())
            for order in ordersList:
                where = '{} {}'.format(sqlwhere, order)

                objectsList.extend( DB_Worker.selectRecords(
                    con=Ehz.getCon(),
                    fields=fieldsSKZ,
                    tables=tablesSKZ,
                    where=where,
                    obj_class = 'SKZ',
                    from_db = str(IS_EZH)
                ))
                
                objectsList.extend(DB_Worker.selectRecords(
                    con=Ehz.getCon(),
                    fields=fieldsIFZ,
                    tables=tablesIFZ,
                    where='{} {}'.format( where, "and Object.F1042<>''"),
                    obj_class = 'TZ',
                    from_db = str(EZH_OBJECTS)
                ))
            return objectsList
        
        def getSustainTypes():
            tables = [
                {
                    'table' : 'T157',
                    'as'    : 'Statuses',
                    }
                ]
            fields = [
                'id as {}'.format(str(INDEX)),
                'F838 as {}'.format(str(TITLE)),
                ]
            return DB_Worker.selectRecords(
                    con=Ehz.getCon(),
                    fields=fields,
                    tables=tables,
                    from_db = str(EZH_SUSTAIN_TYPES)
                    )

        def getObjectInfo(myObject):
            if myObject:
                if myObject[str(TYPE)].lower() == str(IS_SKZ).lower():
                    tables = [
                        {
                            'table' : 'T115',
                            'as'    : 'SKZ_objects',
                            },
                        ] 
                    fields = [
                        'id AS '+str(INDEX),
                        'F632 AS '+ str(TITLE),
                        'F1781 AS '+ str(LONGITUDE),
                        'F1782 AS '+ str(LATITUDE),
                        'F691 AS '+ str(INV_NUMBER),
                        'F1785 AS '+ str(SUSTAIN),
                        ]
                    where = 'id = {}'.format(myObject[str(INDEX)])
                elif myObject[str(TYPE)].lower() == IS_IFZ.lower():
                    tables = [
                        {
                            'table' : 'T135',
                            'as'    : 'IFZ_objects',
                            },
                        ] 
                    fields = [
                        'id AS '+str(INDEX),
                        'F1042 AS '+ str(TITLE),
                        'F1836 AS '+ str(LONGITUDE),
                        'F1837 AS '+ str(LATITUDE),
                        'F1846 AS '+ str(SUSTAIN),
                        ]
                    where = 'id = {}'.format(myObject[str(INDEX)])
                    
            if tables and fields and where:
                return DB_Worker.selectRecords(
                    con=Ehz.getCon(),
                    fields=fields,
                    tables=tables,
                    where=where,
                    from_db=str(EZH_OBJ_INFO)
                )[0]
            
        def getObjectNullParams(myObject):
            if myObject:
                if myObject[str(TYPE)].lower() == str(IS_SKZ).lower():
                    tables = [
                        {
                            'table' : 'T115',
                            'as'    : 'SKZ_objects',
                            }
                        ]
                    fields = [
                        'id AS '+str(INDEX),
                        'F632 AS '+str(TITLE),
                        'F1781 AS '+str(LONGITUDE),
                        'F1782 AS '+str(LATITUDE),
                        'F691 AS '+str(INV_NUMBER),
                        'F1785 AS '+str(SUSTAIN),
                        ]
                elif myObject[str(TYPE)].lower() == IS_IFZ.lower():
                    tables = [
                        {
                            'table' : 'T135',
                            'as'    : 'IFZ_objects',
                            }
                        ]
                    fields = [
                        'id AS '+str(INDEX),
                        'F1042 AS '+str(TITLE),
                        'F1836 AS '+str(LONGITUDE),
                        'F1837 AS '+str(LATITUDE),
                        'F1846 AS '+str(SUSTAIN),
                        ]
                where = 'id = {}'.format(myObject[str(INDEX)])
                nullParams = list()
                tmp = DB_Worker.selectRecords(
                    con=Ehz.getCon(),
                    fields=fields,
                    tables=tables,
                    where=where,
                    from_db=str(EZH_OBJ_NULL_PARAMS)
                )
               
                
                for elem in tmp:
                    for key, val in elem.items():
                        if not bool(val) or val is None:
                            inform = dict()
                            inform.update(myObject)
                            if (str(LONGITUDE) in key.lower())or(str(LATITUDE) in key.lower()):
                                inform[str(OBJECT_PARAMS)] = str(COORDINATES)
                            else:
                                inform[str(OBJECT_PARAMS)] = key.lower()
                            inform[str(VALUE)] = None
                            inform[str(FROM_DB)] = str(EZH_OBJ_NULL_PARAMS)                            
                            if inform not in nullParams:
                                nullParams.append(inform)
                        elif (str(LONGITUDE) in key.lower())or(str(LATITUDE) in key.lower()):
                            inform = dict()
                            inform.update(myObject)
                            if (str(LONGITUDE) in key.lower())or(str(LATITUDE) in key.lower()):
                                inform[str(OBJECT_PARAMS)] = str(COORDINATES)
                            else:
                                inform[str(OBJECT_PARAMS)] = key.lower()
                            inform[str(VALUE)] = None
                            inform[str(FROM_DB)] = str(EZH_OBJ_NULL_PARAMS)                            
                            if inform not in nullParams:
                                nullParams.append(inform)
                
                return nullParams if len( nullParams )>0 else list()
                
        def getObjectMeasurements(myObject):
            sqlText = ''
            sqlWhere = ''
            measurements = list()
            try:
                con = Ehz.getCon()
                cur = con.cursor()
                if myObject:
                    sqlWhere = "WHERE details.F3786 = 0 "#zamers.id = {} ".format(zamer_index)
                else:
                    return
                if myObject:
                    
                    if IS_SKZ.lower() in myObject[str(TYPE)]:
                        sqlWhere += "AND details.F3783 = {} ".format(myObject[str(INDEX)])
                    elif IS_IFZ.lower() in myObject[str(TYPE)]:  
                        sqlWhere += "AND details.F3784 = {} ".format(myObject[str(INDEX)])
                    
                    sqlText = (
                        "SELECT "+
                        "details.id as "+str(INDEX)+", "+
                        "details.F3786 as "+str(VALUE).lower()+", "+
                        "details.F3785 as param_id, "+
                        "details.F3788 as "+str(TITLE)+", "+

                        "params.f3744 as param_name, "+
                        "params.f3748 as "+str(VIEW)+", "+
                        
                        "zamers.id as zamer_index "+

                        "FROM t736 AS zamers "+
                        "LEFT JOIN t737 AS details "+
                        "ON zamers.id = details.pid "+
                        "LEFT JOIN t732 AS params "+
                        "ON details.F3785 = params.id "+    
                        str(sqlWhere) + 
                        "GROUP BY "+str(INDEX)+", zamer_index, param_id, "+str(TITLE)+", param_name, "+str(VIEW)+", "+str(VALUE).lower()+" ")
                    if TEST_MODE:
                            pass #print('\n', sqlText,'\n')
                    cur.execute(sqlText)
                    
                    for row in cur.itermap():
                        measurement = dict()
                        for col in row:
                            measurement[col.lower()] = row[col]
                        measurement[str(FROM_DB)] = str(EZH_MEASUREMENTS)
                        measurement[str(TYPE)] = myObject[str(TYPE)]
                        measurement[str(OBJECT_INDEX)] = myObject[str(INDEX)]
                        measurements.append(measurement)                    
            except Exception as e:
                    if TEST_MODE:
                        print(e)
                        print(measurements)
            finally:
                cur.close()
                con.close()
                return measurements if measurements else list()
                
        def getObjectsFromOrder(order=''):
            sqlText = ''
            try:
                con = Ehz.getCon()
                cur = con.cursor()
                sqlWhere = ''
                if order:
                    sqlWhere = "WHERE zamers.f3789 = {} and details.F3786 = 0 ".format(order)
                else:
                    sqlWhere = "WHERE details.F3786 = 0 "
                sqlText = (
                        "SELECT "+
                        "details.F3783 as skz_id, "+
                        "details.F3784 as ifz_id, "+
                        "details.F3788 as "+str(TITLE)+" "+
                        "FROM t736 AS zamers "+
                        "LEFT JOIN t737 AS details "+
                        "ON zamers.id = details.pid "+
                        "LEFT JOIN t732 AS params "+
                        "ON details.F3785 = params.id "+
                        str(sqlWhere) +
                        "GROUP BY skz_id, ifz_id, "+str(TITLE)+" ")
                pass #print(sqlText)
                cur.execute(sqlText)
                list_obj = list()
                for row in cur.itermap():
                    obj = dict()
                    for col in row:
                        
                        if 'skz_id'.upper() in col and row[col] is not None:
                                obj[str(INDEX)]= row[col]
                                obj[str(TYPE)]=str(IS_SKZ)

                        elif 'ifz_id'.upper() in col and row[col] is not None:
                                obj[str(INDEX)]=row[col]
                                obj[str(TYPE)]=str(IS_IFZ)    
                        else:
                                obj[col.lower()] = row[col]
                    obj[str(FROM_DB)] = str(EZH_OBJECTS)
                    list_obj.append(obj)
                return list_obj
            finally:
                cur.close()
                con.close()
                if TEST_MODE:
                    pass #print('\n'+sqlText+'\n')
                    
        def updateObjectsParams(myObjects=None):
            if myObjects:
                for elem in myObjects:
                    Ehz.updateObjectNullParams(elem)
                    
        def updateObjectNullParams(myObject=None):
            table =  where = None
            params = dict()
            if myObject[str(TYPE)].lower() == str(IS_SKZ).lower():
                table = 'T115'
            else:
                table = 'T135'
            if myObject:
                if myObject[str(TYPE)].lower() == str(IS_SKZ).lower():
                    if switch(myObject[str(OBJECT_PARAMS)], geoAsk):
                        if isinstance(myObject[str(VALUE)], dict):
                            params['F1781']= myObject[str(VALUE)][str(LONGITUDE)]
                            params['F1782']= myObject[str(VALUE)][str(LATITUDE)]

                        elif isinstance(myObject[str(VALUE)], (set, list, tuple)):
                            params['F1781']= myObject[str(VALUE)][0]
                            params['F1782']= myObject[str(VALUE)][1]

                    if switch(myObject[str(OBJECT_PARAMS)], { str(EZH_SUSTAIN_TYPES) : True} ):
                            params['F1785']= myObject[str(VALUE)]
                            
                    if switch(myObject[str(OBJECT_PARAMS)], inputAsk):
                        
                        
                        if str(INV_NUMBER) in myObject[str(OBJECT_PARAMS)]:
                            params['F691']= myObject[str(VALUE)]
                elif myObject[str(TYPE)].lower() == str(IS_IFZ).lower():
                    if switch(myObject[str(OBJECT_PARAMS)], geoAsk):
                        if isinstance(myObject[str(VALUE)], dict):
                            params['F1836']= myObject[str(VALUE)][str(LONGITUDE)]
                            params['F1837']= myObject[str(VALUE)][str(LATITUDE)]
                        elif isinstance(myObject[str(VALUE)], (set, list, tuple)):
                            params['F1836']= myObject[str(VALUE)][0]
                            params['F1837']= myObject[str(VALUE)][1]
                            
                    if switch(myObject[str(OBJECT_PARAMS)], { str(EZH_SUSTAIN_TYPES) : True} ):
                        params['F1846']= myObject[str(VALUE)]

                where = 'id = {}'.format(myObject[str(INDEX)])
                if table and params and where:
                    DB_Worker.updateRecord(con=Ehz.getCon(), table=table, params=params, where=where)
                    
        def updateMeasurementDoc(measurements=None):
            if measurements:
                for elem in measurements:
                    table = params = where = None
                    table = 'T737'
                    params = {
                        'F3786' : elem[str(VALUE)],
                        'F3787' : '\'знято показ: {} = {}\''.format(elem[str(VIEW)], elem[str(VALUE)]), 
                        }
                    where = 'id = {}'.format(elem[str(INDEX)])
                    if table and params and where:
                        DB_Worker.updateRecord(con=Ehz.getCon(), table=table, params=params, where=where)
                    table = params = where = None
                    table = 'T736'
                    params = {
                        'F3768' : '\'{}\''.format(datetime.date.today())
                        }
                    where = 'id = (SELECT pid FROM t737 WHERE id = {})'.format(elem[str(INDEX)])
                    if table and params and where:
                        DB_Worker.updateRecord(con=Ehz.getCon(), table=table, params=params, where=where)
