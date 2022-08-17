from Constants import *
from Connections import *
import pypyodbc
import datetime
#База данных фото объектов  
class Scs:
        def getCon():
            scs = connections['Scs']
            return pypyodbc.connect(
                    driver=scs['driver'],
                    server=scs['server'],
                    database=scs['database'],
                    uid=scs['uid'],
                    pwd=scs['pwd']
                   )

        def pushPhoto(photo):#Проработать инв номер по типам объектов
            if isinstance( photo, (list, tuple, set) ):
                for item in photo:
                    Scs.pushPhoto(item)
            else:
                try:
                    con=Scs.getCon()
                    binary = pypyodbc.BINARY( photo[str(PHOTO)] )
                    
                    cursor = con.cursor()
                    cursor.execute("INSERT INTO obj_img (invn, datae_objimg, img_det)"+
                           "VALUES ('"+photo[str(INDEX)]+"','"+photo[str(DATE)]+"',?)", (binary,) )                  
                    #con.commit()
                    pass #print(photo[str(INDEX)], ' inserted' )
                except Exception as e:
                    pass #print(e, 'pushPhoto()')
                    
                finally:
                    cursor.close()
                    con.close()
                
        def testReq():
            tables = [
                {
                    'table' : 'obj_img',
                    'as'    : 'ph_t',
                    }
                ]
            fields = [
                'invn',
                'datae_objimg',
                #'img_det',
                ]
            return DB_Worker.selectRecords(
                con=Scs.getCon(),
                tables=tables,
                fields=fields,
                group_by=['invn', 'datae_objimg']
                )[0]
