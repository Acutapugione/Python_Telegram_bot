from Constants import *
from Connections import *
import firebirdsql as fdb
import datetime

class Debtors():
        def __init__(abc, chat_id=''):
                abc.info = ''
                abc.checked = abc.check_id(chat_id)
                
        def getCon(abc):
                debtors = connections['Debtors']
                return fdb.connect(
                    host=debtors['host'],
                    database=debtors['database'],
                    port = debtors['port'],
                    user=debtors['user'],
                    password=debtors['password'],
                    charset=debtors['charset']
                    )

        def check_id(abc, chat_id=''):
                con = abc.getCon()
                cur = con.cursor()
                sqlString ="select F104 as FIO, F1276 as chat_id, F1277 as status, F729 as Ph_number from T23 where F1277 = 1 and F1276 = '" +str(chat_id)+"'"
                cur.execute(sqlString)
                for elem in cur:
                        cur.close()
                        con.close()
                        return True
                cur.close()
                con.close()
                return False
        
        def getDebtorInfo(abc, debtor=''):
                con = abc.getCon()
                cur = con.cursor()
                info = []
                sqlWhere = "where Porush.F102 = \'{}\'".format(str(debtor))

                sqlText = ("select "+
                           "Vidi_Porush.F107 as vid_porushennya, "+
                           "Porush.F101 as Protocol_Date, "+
                           "Porush.F237 as Protocol_Num, "+
                           "Porush.F1264 as Nachisleno, "+
                           "Porush.F141 as Oplatcheno, "+
                           "Porush.F142 as Ostatok, "+

                           "Porush.F257 as filing_lawsuit_date, "+ #[Дата подання позову]
                           "Porush.F259 as receipt_decision_date, "+ #[Дата отримання рішення суду],
                           "Porush.F260 as message_send_date, "+ #[Дата надіслання повідомлення],
                           "Porush.F261 as Appeal_proceedings, "+ #[Апеляційне провадження],
                           "Porush.F262 as Cassation_proceedings, "+ #[Касаційне провадження],
                           "Porush.F263 as referral_RWDWS_date, "+ #[Дата направлення до РВ ДВС],
                           "Porush.F264 as return_RWDWS_date, "+ #[Дата повернення з РВ ДВС],
                           "Porush.F266 as enforcement_court_decision_date, "+ #[Дата примусового виконання рішення суду],
                           "Porush.F280 as Case_number, "+ #[Номер справи],
                           "Porush.F487 as Resolution_number, "+ #[№ постанови],
                           "Porush.F488 as ruling_date, "+#[Дата постанови],
                           "Porush.F489 as Administrative_Commission, "+ #[Адмінкомісія],
                           "Porush.F634 as Incoming_claim_number, "+ #[Номер вхідного позову],
                           "Porush.F635 as Incoming_lawsuit_date, "+ #[Дата вхідного позову],
                           "Porush.F636 as Securing_claim, "+ #[Забезпечення позову],
                           "Porush.F637 as is_decision, "+ #[Рішення прийнято],
                           "Porush.F272 as agreement_date, "+ #[Дата домовленості],
                           "Porush.F274 as term_end, "+ #[Кінець строку],
                           "Porush.F273 as term_begin, "+ #[Початок строку],
                           "Porush.F240 as issuance_Deadline, "+ #[Термін видачі],
                           "Porush.F243 as Execution_date, "+ #[Дата виконання],
                           "Porush.F244 as Invoice_date, "+ #[Дата рахунку],
                           "Porush.F361 as approval_date " #[Дата затвердження]
                           
                           "from T21 as Porush "+
                           "left join T24 as Vidi_Porush "+
                           "on Vidi_Porush.id = Porush.F103 "+

                           str(sqlWhere)+" ")
                           
                cur.execute(sqlText)
                if cur :
                        info.append(    {
                                Localisator().getLocal(str(FROM_DB)) :
                                Localisator().getLocal(str(IS_DEBTORS)) + '\n'
                                }       )
                for row in cur.itermap():
                        obj={}
                        for elem in row:
                                if row[elem] is not None:
                                        obj[Localisator().getLocal(elem).lower()] = Localisator().getLocal(str(row[elem])) 
                        info.append(obj)
                cur.close()
                con.close()
                return info
        
        def getDebtors(abc, settlement='', ls=''):
                con = abc.getCon()
                cur = con.cursor()
                sqlWhere = ''

                if ls and settlement:
                        sqlWhere = "where porteb.F320 = \'{}\' and porteb.F21 = \'{}\' ".format(str(settlement), str(ls))
                elif settlement:
                        sqlWhere = "where porteb.F320 = \'{}\' ".format(str(settlement))
                elif ls:
                        sqlWhere = "where porteb.F21 = \'{}\' ".format(str(ls))
                debtors = []
                if TEST_MODE:
                            pass #print(sqlWhere)
                sqlText = ("select "+
                           "porteb.id   as "+str(INDEX)+", "+
                           "porteb.F20  as "+str(TITLE)+", "+
                           "porteb.F22  as "+str(LOCATION)+", "+
                           "porteb.f623 as "+str(PHONE)+", "+
                           "local.F318  as "+str(SETTLEMENT)+" "+

                           "from t2 as porteb "+
                           "left join t53 as local "+
                           "on porteb.f320 = local.id "+

                           str(sqlWhere)+

                           "group by "+
                                   str(INDEX)+","+
                                   str(TITLE)+","+
                                   str(LOCATION)+","+
                                   str(PHONE)+","+
                                   str(SETTLEMENT)+" "
                           
                           "Order by "+str(INDEX)+" ASC")
                if TEST_MODE:
                            pass #print(sqlText)
                cur.execute(sqlText)
                for row in cur.itermap():
                        obj={}
                        for elem in row:
                                obj[elem.lower()] = row[elem]
                        obj[str(FROM_DB)] = str(IS_DEBTORS)
                        debtors.append(obj)
                cur.close()
                con.close()
                return debtors
        
        def getSettlements(abc, district=''):
                con = abc.getCon()
                cur = con.cursor()
                sqlWhere = ''
                if district:
                        sqlWhere = "where dist.id = \'{}\' ".format(str(district))
                settlements = [] 
                 
                sqlText = ("select "+
                           "local.id   as "+str(INDEX)+", "+
                           "local.F318 as "+str(TITLE)+", "+
                           "dist.f317 as distName "+

                           "from t53 as local "+
                           "left join t52 as dist "+
                           "on local.F319 = dist.id "+
                           str(sqlWhere)+
                           
                           "group by "+
                                   str(INDEX)+","+
                                   "distName,"+
                                   str(TITLE)+" "+
                           "Order by "+str(INDEX)+" ASC"
                           )
                
                cur.execute(sqlText)
                for row in cur.itermap():
                        obj={}
                        for elem in row:
                                obj[elem.lower()] = row[elem]
                        obj[str(TYPE)]=str(IS_DISTRICT)
                        obj[str(FROM_DB)] = str(IS_DEBTORS)
                        settlements.append(obj)
                cur.close()
                con.close()
                return settlements
        
        def getDistricts(abc):
                con = abc.getCon()
                cur = con.cursor()
                districts = []
                sqlText = ("select "+
                           "id as "+str(INDEX)+", "+
                           "F317 as "+str(TITLE)+" "+
                           "from t52")
                cur.execute(sqlText)
                for row in cur.itermap():
                        obj={}
                        for elem in row:
                                obj[elem.lower()] = row[elem]
                        obj[str(TYPE)]=str(IS_DISTRICT)
                        obj[str(FROM_DB)] = str(IS_DEBTORS)
                        districts.append(obj)
                cur.close()
                con.close()
                return districts
