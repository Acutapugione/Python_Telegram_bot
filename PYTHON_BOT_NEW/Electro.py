from Constants import *
from Connections import *
import firebirdsql as fdb
import datetime

class Electro:
        def getCon():
                electro = connections['Electro']
                return fdb.connect(
                    host=electro['host'],
                    database=electro['database'],
                    port = electro['port'],
                    #dsn=electro['dsn'],
                    user=electro['user'],
                    password=electro['password'],
                    charset=electro['charset']
                    )
        def check_id(chat_id=''):
                con = Electro.getCon()
                cur = con.cursor()
                sqlString ="select F416 as FIO, F453 as chat_id, F454 as status, F455 as Ph_number from T87 where F454 = 1 and F453 = '" +str(chat_id)+"'"
                cur.execute(sqlString)
                for elem in cur:
                        cur.close()
                        con.close()
                        return True
                cur.close()
                con.close()
                return False
            
        def getInfo(myObject):
            tables = [
                {
                    'table' : 'T80',
                    'as'    : 't_pokaz',
                    },
                {
                    'table' : 'T58',
                    'as'    : 't_punkt',
                    'join'  : 'LEFT JOIN',
                    'on'    : 't_pokaz.F375 = t_punkt.id',
                    }
                ]
            fields = [
                'first 1 t_pokaz.id AS '+str(INDEX),
                "\'{}\'".format(str(ELECTRICITY_METER_READING))+ " AS "+str(TITLE),
                "\'{}\'".format(str(IS_ELECTRO).lower()) + " AS "+str(TYPE),
                't_pokaz.F361 AS counter',
                't_pokaz.F363 AS dogovor',
                't_pokaz.F375 AS p_punkt',
                't_pokaz.F364 AS n_punkt',
                't_punkt.F322 AS inv_num',
                't_pokaz.F399 AS is_active',
                't_pokaz.F400 AS is_reactive',
                't_pokaz.F401 AS is_generation',
                '(select first 1 (story.F462) from T89 as story where story.F434 = t_pokaz.F361 order by story.F429 desc) AS lastKoef',
                ]
            where = 't_punkt.F322 = \'{}\''.format(myObject[str(INV_NUMBER)])
            tmp = DB_Worker.selectRecords(
                    con=Electro.getCon(),
                    tables=tables,
                    fields=fields,
                    where=where,
                    group_by=[
                        str(INDEX),
                        str(TITLE),
                        str(TYPE),
                        'counter',
                        'dogovor',
                        'p_punkt',
                        'n_punkt',
                        'inv_num',
                        'is_active',
                        'is_reactive',
                        'is_generation'
                        ],  
                    from_db=str(ELECTRO_DB)
                    )
            
            if tmp and len(tmp)>0:
                myObject.update(tmp[0])
               
            return myObject
        
        def getMeasurements(myObject=None):
            if myObject[str(INDEX)]:
                tables = [
                    {
                        'table' : 'T80',
                        'as'    : 't_pokaz',                   
                        }
                    ]
                fields = [
                    
                    't_pokaz.F402 AS type_potreb',
                    't_pokaz.F379 AS coefficient',
                    'MAX(t_pokaz.F360) AS created_at',
                    't_pokaz.F399 AS is_active',
                    't_pokaz.F400 AS is_reactive',
                    't_pokaz.F401 AS is_generation',
                    'MAX(t_pokaz.F362) AS lastPokaz',
                    ]
                where = 't_pokaz.F361 = {}'.format(myObject[str(INDEX)])
                
                return DB_Worker.selectRecords(
                    con=Electro.getCon(),
                    tables=tables,
                    fields=fields,
                    where=where
                    )
        
        def getCounter(myObject=None):
            if myObject[str(INV_NUMBER)]:
                tables = [
                    {
                        'table' : 't54',
                        'as'    : 't_counter',
                        },
                     {
                        'table' : 'T58',
                        'as'    : 't_potreb',
                        'join'  : 'LEFT JOIN',
                        'on'    : 't_counter.F377 = t_potreb.id',
                        },
                    ]
                
                fields = [
                    't_counter.id as {}'.format(str(INDEX)),
                    ]
                where = 't_potreb.F322 = \'{}\''.format(myObject[str(INV_NUMBER)])
                return DB_Worker.selectRecords(
                    con=Electro.getCon(),
                    tables=tables,
                    fields=fields,
                    where=where
                    )[0]

        def pullMeasurement(meas=None):
            if meas and str(VALUE) in meas: 
                fields = [
                    'id',
                    'F361',# AS counter',
                    'F363',# AS dogovor',
                    'F375',# AS p_punkt',
                    'F364',# AS n_punkt',
                    'F379',# AS lastKoef',
                    'F360',# AS createdAt',
                    
                    ('F399' or ('','F399')['t_active' in meas]+('', ',F400')['t_reactive' in meas]+('', ',F401')['t_generative' in meas]),
                    'F402',# AS type_potreb_text              
                    'F445',# AS t_bot',
                    'F362',# AS measure_val',
                    'F438',# AS wasted
                    ]
                values = [
                    '(select MAX(id)+1 from T80)',
                    meas['counter'],
                    meas['dogovor'],
                    meas['p_punkt'],
                    meas['n_punkt'],
                    meas['lastkoef'],
                    "'"+datetime.date.today().strftime("%d.%m.%Y")+"'",
                    
                    ('1' or ('','1')['t_active' in meas]+('', ',1')['t_reactive' in meas]+('', ',1')['t_generative' in meas]),
                    "'{}'".format('А' or ('','А')['t_active' in meas] or ('', 'Р')['t_reactive' in meas] or ('', 'Г')['t_generative' in meas]),#IIF([Актив]=1,'А', IIF([Реактив]=1,'Р' , IIF([Генерация]=1, 'Г', '')))
                    
                    1,
                    "'{}'".format( meas[str(VALUE)]),
                    0
                    ]
                return DB_Worker.insertRecord(
                    Electro.getCon(),
                    'T80',
                    fields,
                    values
                    )
