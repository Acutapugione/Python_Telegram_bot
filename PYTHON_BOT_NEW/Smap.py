from Constants import *
from Connections import *
import pypyodbc
import datetime
class Smap:
        def getCon():
                smap = connections['Map']
                return pypyodbc.connect(
                    driver=smap['driver'],
                    server=smap['server'],
                    database=smap['database'],
                    uid=smap['uid'],
                    pwd=smap['pwd']
                   )
            
        def insertLocation(obj):#Поправить инвномер по типам объектов и категория
            if isinstance( obj, (tuple, list, set) ):
                for item in obj:
                    Smap.insertLocation(item)
            else:
                fields = values = list()
                try:
                    fields = [
                        'invn',#
                        'categorie',#
                        'kod',
                        'name',
                        'adres',
                        'notes',
                        'loc_long',
                        'loc_lat',
                        'remark',
                        'datae_obj',
                        'status'
                        ]
                    values = [
                        obj[str(INV_NUMBER)],#
                        obj[str(CATEGORIE)],#
                        obj['orgid'],
                        "\'{}\'".format( obj[str(TITLE)]),
                        "\'{}\'".format( obj[str(LOCATION)]),
                        "\'{}\'".format( obj[str(COMMENTS)]),
                        obj[str(COORDINATES)][str(LONGITUDE)],
                        obj[str(COORDINATES)][str(LATITUDE)],
                        "\'\'" ,
                        "'"+datetime.date.today().strftime("%d.%m.%Y %H:%M:%d") +"'" ,
                        obj[str(SUSTAIN)],
                        ]
                except Exception as e:
                    print( e )
                finally:
                    return DB_Worker.insertRecord(
                        Smap.getCon(),
                        'obj',
                        fields,
                        values
                        )

        def updateLocation(obj):#Поправить InsertLocation
            if isinstance( obj, (tuple, list, set) ):
                for item in obj:
                    Smap.updateLocation(item)
            else:
                table = 'obj'
                where = params = ''
                try:
                    params = {
                        #'invn': "\'{}\'".format(obj[str(INV_NUMBER)]),
                        #'categorie' : obj[str(CATEGORIE)],
                        #'kod' : obj['orgid'],
                        #'name': "\'{}\'".format(  obj[str(TITLE)]),
                        #'name': "\'{}\'".format(  obj[str(TITLE)]),
                        #'adres': "\'{}\'".format( obj[str(LOCATION)]),
                        #'notes': "\'{}\'".format( obj[str(COMMENTS)]),
                        'loc_long':obj[str(COORDINATES)][str(LONGITUDE)],
                        'loc_lat':obj[str(COORDINATES)][str(LATITUDE)],
                        #'remark': "\'\'" ,
                        'datae_obj': "'"+datetime.date.today().strftime("%d.%m.%Y %H:%M:%d") +"'",
                        #'status' : obj[str(SUSTAIN)],
                        }
                    where = 'invn = \'{}\''.format(obj[str(INV_NUMBER)])#
                except Exception as e:
                    print( e )
                finally:
                    
                    return DB_Worker.updateRecord(con=Smap.getCon(), table=table, params=params, where=where )
