from Constants import *
from Connections import *

class DB_Worker():
    def selectRecords(con=None, tables=list(), fields=list(), where=str(""), group_by=list(), from_db=''):
        try:
            objects = list()
            cur = con.cursor()
            sqlText = "\nSELECT"
            cntr = 0
            for elem in fields:
                if cntr>0:
                    sqlText = "{}, {}".format(sqlText, elem)
                else:
                    sqlText = "{} {}".format(sqlText, elem)
                cntr+=1
            
            cntr = 0
            
            for elem in tables:
                if cntr>0:
                    sqlText = "{}{} {} AS {}\nON {}\n\n".format(sqlText, elem['join'], elem['table'], elem['as'], elem['on'])
                else:
                    sqlText = "{}\n\nFROM {} AS {}\n".format(sqlText, elem['table'], elem['as'])
                cntr+=1
            if where:
                sqlText = "{}WHERE {}\n".format(sqlText, where)
            cntr = 0
            
            if len(group_by)==0 and len(tables)>=1:
                group_by = fields
            
            for elem in group_by:
                try:
                    if not (elem.split('(')[0].upper() in sqlStatement )or(
                        elem.split(' ')[0].upper() in sqlStatement )or(isinstance(elem, (int, float))):
                        if cntr>0:
                            sqlText = "{}, {}".format(sqlText, elem.split(' ')[2])
                        else:
                            sqlText = "{}GROUP BY {}".format(sqlText, elem.split(' ')[2])
                        cntr+=1
                except:
                    if not (elem.split('(')[0].upper() in sqlStatement )or(
                        elem.split(' ')[0].upper() in sqlStatement ):
                        if cntr>0:
                            sqlText = "{}, {}".format(sqlText, elem.split(' ')[0])
                        else:
                            sqlText = "{}GROUP BY {}".format(sqlText, elem.split(' ')[0])
                        cntr+=1
            #print(sqlText)  
            cur.execute(sqlText)
              
            
            my_map = None
            

            try:
                my_map = cur.itermap()
                
            except:
                my_map = [dict(zip([column[0] for column in cur.description], row)) for row in cur.fetchall()]
                
              
            for row in my_map:
                obj={}
                for elem in row:
                    try:
                        if not bool(row[elem]):
                            obj[elem.lower()] = None
                        else:
                            obj[elem.lower()] = row[elem]
                    except Exception as e:
                        pass #print(e)
                
                if from_db:
                    obj[str(FROM_DB)] = from_db
                #print(obj)
                objects.append(obj)
                #print('~', obj)
            
            return objects
        except Exception as e:
            return {str(SUSTAIN): False, 'SQL': sqlText , 'exception': e }
        finally:
            cur.close()
            con.close()
            
    def insertRecord(con=None, table='', fields=[], values=[]):
        try:
            cur = con.cursor()
            sqlText = "\nINSERT INTO {}".format(table)
            cntr = 0
            for item in fields:
                if cntr==0:
                    sqlText = "{} ({}".format(sqlText, item)
                elif cntr == len(fields)-1:
                    sqlText = "{}, {})\n VALUES\n".format(sqlText, item)
                    
                else:
                    sqlText = "{}, {}".format(sqlText, item)
                cntr+=1
            cntr = 0
            for val in values:
                if cntr==0:
                    sqlText = "{} ({}".format(sqlText, val)
                elif cntr == len(fields)-1 :
                    sqlText = "{}, {})\n".format(sqlText, val)
                else:
                    sqlText = "{}, {}".format(sqlText, val)
                cntr+=1
            #print(sqlText)
            cur.execute(sqlText)
            if not TEST_MODE:
                con.commit()
            return {str(SUSTAIN): True, 'SQL': sqlText }
        except Exception as e:
            #print(sqlText)
            #pass #print(e, ' in insertRecord()')

            return {str(SUSTAIN): False, 'SQL': sqlText , 'exception': e }
        finally:
            cur.close()
            con.close()
            
    def updateRecord(con=None, table='', params=dict(), where=''):
        try:
            cur = con.cursor()
            sqlText = "UPDATE {}".format(table)
            
            cntr = 0
            for key, val in params.items():
                if cntr>0:
                    sqlText = "{}, {} = {}\n".format(sqlText, key, val)
                else:
                    sqlText = "{} SET {} = {}\n".format(sqlText, key, val)
                cntr+=1
            sqlText = "{}\n WHERE {}\n".format(sqlText, where)
            
            cur.execute(sqlText)
            if not TEST_MODE:
                con.commit()
            return {str(SUSTAIN): True, 'SQL': sqlText }
        except Exception as e:
            #print(sqlText)
            #pass #print(e, ' in updateRecord()')
            return {str(SUSTAIN): False, 'SQL': sqlText , 'exception': e }
        finally:
            cur.close()
            con.close()
            #return sqlText
