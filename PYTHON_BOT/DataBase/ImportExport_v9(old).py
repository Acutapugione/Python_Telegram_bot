#Библия для телебота
import telebot
# Импортируем типы из модуля, чтобы создавать кнопки
from telebot import types

#Библия для массивов и списков
from struct import *
from array import *
import firebirdsql as fdb
import datetime
import pypyodbc

wrong_arr = [ '[', ']', '{', '}', '/', 
              ':', ';', '*', '+', '#',
              '!', '@', '$', '%', '^',
              '&', '  ','\\']

class Steps:
    def step_update_categorie(message,user,bot): #commit()
        con = fdb.connect(host='192.168.1.248',database='v:\Oper\Ehz.fdb', port = '3075', user='sysdba', password='masterkey', charset='UTF8')
        cur = con.cursor()
        tz_id = user.tz_id
        categorie = user.categorie
        try:# Object.F1840 as categorie
            cur.execute("Select id as kod,"
                        " F1839 as categorie"
                        " From T357 as cat"
                        " Where F1839="+str(categorie))
            for row in cur.itermap():
                kod = str(row['kod'])
            cur.execute("Update T135 Set F1835 = "+str(kod)+
                        ", F1840 = "+str(categorie)+
                        " Where T135.id = '"+str(tz_id)+"'")
                                            
            con.commit()
            cur.close()
        except Exception as errorMsg:
            print(errorMsg + " in upgrade_categorie")
        con.close()
        return
    
class Map:
    def add(message,user,bot): #commit()
            try:
                orgid = user.city
            except Exception as errorMsg:
                orgid = 0     
            cnxn = pypyodbc.connect('DRIVER={SQL Server};SERVER=192.168.1.5;DATABASE=smap;UID=sc;PWD=masterkey')
            cursor = cnxn.cursor()
            if user.tz == 0:
                inv = user.inv
                name = user.name_skz
            else:
                inv = 'ifs_'+user.tz_id
                name = user.name_tz
            adres = user.adres
            categorie = user.categorie
            if categorie == 169:
                inv = 'pm_'+user.skz_id
            dopinfo = user.info
            today = datetime.datetime.today()
            date = today.strftime("%d.%m.%Y %H:%M:%d") 
            latitude = user.latitude
            longitude = user.longitude
            sustain = user.sustain   

            try:
                cursor.execute(" UPDATE obj SET invn = '"+str(inv)+"'" +
                           ", categorie = "+str(categorie)+", kod = "+str(orgid)+", name = '"+str(name)+"'"+
                           ", adres = '"+str(adres)+"', notes = '"+str(dopinfo)+"'"+
                           ", loc_long = "+str(longitude)+", loc_lat = "+str(latitude)+", remark = ''"+
                           ", datae_obj = '"+str(date)+"'"+
                           ", status = "+str(sustain)+""+ 
                           " WHERE invn = '"+str(inv)+"'"+
                           " IF @@ROWCOUNT = 0"+
                           " INSERT INTO obj(invn, categorie, kod, name, adres, notes, loc_long, loc_lat, remark, datae_obj, status)"+ 
                           " VALUES('"+str(inv)+"',"+str(categorie)+","+str(orgid)+",'"+str(name)+"','"+str(adres)+"','"+str(dopinfo)+"',"+str(longitude)+","+str(latitude)+",'','"+str(date)+"',"+str(sustain)+")")
                cnxn.commit()
                cursor.close()
                bot.reply_to(message, "Данные записаны в карту")
            except Exception as errorMsg:
                bot.reply_to(message, "Данные не записаны в карту!" + str(errorMsg))
                print(str(errorMsg) + " in Map::Add")
            cnxn.close()

    def add_photo(message,user,bot): #con.commit()
        chat_id = message.chat.id;
        text = message.text;
        
        if text is None:
            try:
                user = user_dict[chat_id]
            except Exception as errorMsg:
                user = 0
            try:
                raw = message.photo[2].file_id
                name = raw+".jpg"
                file_info = bot.get_file(raw)
                downloaded_file = bot.download_file(file_info.file_path)
                with open(name,'wb') as new_file:
                    new_file.write(downloaded_file)
                    # ПОДКЛЮЧЕНИЕ К БД СЦ
                    cnxn = pypyodbc.connect('DRIVER={SQL Server};SERVER=192.168.1.5;DATABASE=scs;UID=sc;PWD=masterkey')
                    cursor = cnxn.cursor()
                    categorie = user.categorie
                    if categorie == 169:
                        inv = 'pm_'+user.skz_id
                    else:
                        inv = user.inv
                    today = datetime.datetime.today()
                    date = today.strftime("%d.%m.%Y %H:%M:%d")
                    #patch = str(cwd)+"\\"+ str(name)
                    delpatch = str(cwd)+'\\'+ str(name) 
                    # ВЫПОЛНЕНИЕ ЗАПРОСА                
                    try:
                        fin=open(name, 'rb')
                        img = fin.read()
                        binary = pypyodbc.BINARY(img)
                        cursor.execute("INSERT INTO obj_img (invn, datae_objimg, img_det) VALUES ('"+str(inv)+"','"+str(date)+"',?)", (binary,) )                    
                        cnxn.commit()
                        cursor.close()
                        cnxn.close()                
                        fin.close()    
                        bot.reply_to(message, "Получены данные: наряд: "+str(user.naryad)+
                                         ", объект: "+user.name_skz+", долгота: "+str(user.longitude)+
                                         ", широта: "+str(user.latitude)+", доп. инфо: "+user.info+".")
                        print("Получены данные: наряд: "+str(user.naryad)+", объект: "+user.name_skz+
                              ", долгота: "+str(user.longitude)+", широта: "+str(user.latitude)+
                              ", доп. инфо: "+user.info+".") 
                    except Exception as errorMsg:
                        bot.reply_to(message, "Фото не записано в базу! " + str(errorMsg))
                        print(str(errorMsg)+  " in Map::add_photo")
                        cursor.close()
                        cnxn.close()
                        fin.close()
            except Exception as errorMsg:
                    bot.reply_to(message, "Фото не записано в базу! " + str(errorMsg))                
                    print(str(errorMsg)+" in Map::add_photo")
            # удалить старую клавиатуру
            try:
                os.remove(delpatch)
                print("Фото успешно удалено из обменника " +str(delpatch))
            except Exception as errorMsg:
                print(str(errorMsg)+" in Map::add_photo")
                #print(str(errorMsg)+ " Путь :"+ str(delpatch))
            remove_keyboard = types.ReplyKeyboardRemove()
            keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        
class Naryad:
    def add_to_ehz_zamer(message,user,bot):  #con.commit()
        con = fdb.connect(host='192.168.1.248',database='v:\Oper\Ehz.fdb', port = '3075', user='sysdba', password='masterkey', charset='UTF8')
        cur = con.cursor()
        if user.tz == 0:
            try:
                categorie = user.categorie
                if categorie == 169:
                    inv = 'pm_'+user.skz_id
                else:
                    inv = user.inv
                skz_id = user.skz_id
                text = user.u
                U = text
                text = user.i
                I = text
                text = user.p1
                P1 = text
                text = user.p2
                P2 = text
                naryad = int(user.naryad)
            except Exception as e:
                print(str(e))
                return
            try:
                cur.execute("Update t232 Set F1208 = "+str(skz_id)+ 
                        ", F1209 = '"+str(U)+"'"+  
                        ", F1210 = '"+str(I)+"'"+  
                        ", F1206 = '"+str(P1)+"'"+ 
                        ", F1207 = '"+str(P2)+"'"+
                        " Where F1208 = "+str(skz_id)+
                        " AND id = (select z.id"+
                                    " from T232 as z"+
                                    " left join T118 as t"+
                                    " On z.pid=t.id"+
                                    " left join T151 as tn"+
                                    " On tn.id = t.f1123"+ 
                                    " Where tn.f839 = '"+str(naryad)+"' AND z.F1208 = '"+str(skz_id)+"')")   
                con.commit()
                print(str("U = "+str(U)+", I = "+ str(I) +", P1 = "+ str(P1) +", P2 = "+str(P2)+""))
                bot.reply_to(message, "Данные по замерам записаны в базу ЭХЗ!")
            except Exception as errorMsg:
                bot.reply_to(message, "Данные по замерам не записаны в базу ЭХЗ! " + str(errorMsg))
                print(str(errorMsg)+" in Naryad::add_to_ehz_zamer")
                return
            cur.close()
            con.close()
        #Если ИФСы 
        else:
            try: 
                tz_id = user.tz_id
                try: 
                    p_on = user.p_on
                    p_off = user.p_off
                except:
                    p_on = 0
                    p_off = 0
                try:
                    p_top = user.p_top
                    p_bottom = user.p_bottom
                except:
                    p_top = 0
                    p_bottom = 0
                try:
                    tz_u = user.tz_u
                    tz_i = user.tz_i
                except:
                    tz_u = 0
                    tz_i = 0
                info = user.info
                naryad = int(user.naryad)
            except Exception as e:
                print(str(e))
                return
            try:
                #[Деталі зняття заміру ТЗ]
                    #[Точка захисту] as F1240
                    #[Pвкл] as F1825
                    #[Pвыкл] as F1824
                    #[Pверх] as F1843
                    #[Pниз] as F1842
                    #[Напруга, В] as F1845
                    #[Сила току, А] as F1844
                    #[Додатково] as F1841

                #[Зняття заміру СКЗ та ТЗ
                    #[Наряд] as F1123
                    #[Дата заміру] as F624
                    #[Деталі зняття заміру ТЗ] as T235
                    #[Зняття заміру СКЗ та ТЗ] as T118 
                cur.execute("Update T235 Set "+
                            "F1825 = '"+str(p_on)+"', "+
                            "F1824 = '"+str(p_off)+"', "+
                            "F1843 = '"+str(p_top)+"', "+
                            "F1842 = '"+str(p_bottom)+"', "+
                            "F1845 = '"+str(tz_u)+"', "+
                            "F1844 = '"+str(tz_i)+"', "+
                            "F1841 = '"+str(info)+"' "+
                            "Where F1240 = "+str(tz_id)+" "+
                            "And id = ("+
                            "Select TZ_Zamer.id "+
                            "From T235 as TZ_Zamer "+
                            "Left join T118 as Zamer "+
                            "On TZ_Zamer.pId = Zamer.Id "+
                            "Left join T151 as Naryad "+
                            "On Naryad.id = Zamer.F1123 "+
                            "Where Naryad.F839 = '"+str(naryad)+"' "+
                            "And TZ_Zamer.F1240 = '"+str(tz_id)+"')")
                con.commit()
                print(str("U = "+str(tz_u)+", I = "+ str(tz_i) +
                          ", Pвкл = "+ str(p_on) +", Pвыкл = "+str(p_off)+
                          ", Pверх = "+str(p_top)+", Pниз = "+str(p_bottom)+""))
                bot.reply_to(message, "Данные по замерам записаны в базу ЭХЗ!")
            except Exception as errorMsg:
                bot.reply_to(message, "Данные по замерам не записаны в базу ЭХЗ! " + str(errorMsg))
                print(str(errorMsg)+" in Naryad::add_to_ehz_zamer #Если ИФС")
                return
            cur.close()
            con.close()

    def add_to_ehz(message,user,bot):#con.commit()
            con = fdb.connect(host='192.168.1.248',database='v:\Oper\Ehz.fdb', port = '3075', user='sysdba', password='masterkey', charset='UTF8')
            cur = con.cursor()
            try:
                if user.tz == 0:
                    
                    inv = user.inv 
                    sustain = user.sustain
                    dopinfo = user.info
                    latitude = user.latitude
                    longitude = user.longitude
                    skz_id = user.skz_id
                    categorie = user.categorie
                    if categorie == 170:
                        cur.execute("Update T115 Set F1785 = "+str(sustain)+
                                        ", F1113 = '"+str(dopinfo)+
                                        "', F1781 = '"+str(longitude)+
                                        "', F1782 = '"+str(latitude)+
                                        "' Where F691 = '"+str(inv)+"'")
                    else:
                        cur.execute("Update T115 Set F1785 = "+str(sustain)+
                                        ", F1113 = '"+str(dopinfo)+
                                        "', F1781 = '"+str(longitude)+
                                        "', F1782 = '"+str(latitude)+
                                        "' Where id = '"+str(skz_id)+"'")
                else:
                    tz_id = user.tz_id 
                    sustain = user.sustain
                    dopinfo = user.info
                    latitude = user.latitude
                    longitude = user.longitude
                    
                    cur.execute("Update T135 Set F1846 = "+str(sustain)+
                                ", F1769 = '"+str(dopinfo)+
                                "', F1836 = '"+str(longitude)+
                                "', F1837 = '"+str(latitude)+
                                "' Where id = '"+str(tz_id)+"'")
                con.commit()
                cur.close()
                bot.reply_to(message, "Данные по объекту обновлены!")
            except Exception as errorMsg:
                print(str(errorMsg) + " in Naryad::add_to_ehz")
                bot.reply_to(message, "Данные по объекту не были обновлены!" + str(errorMsg))
            con.close()

    #Получаем данные по точке защиты    
    def get_tz_info(message,user):
        con = fdb.connect(host='192.168.1.248',database='v:\Oper\Ehz.fdb', port = '3075', user='sysdba', password='masterkey', charset='UTF8')
        cur = con.cursor()
        my_array = []
        TZ_id = user.tz_id 
        if TZ_id is not None:
            cur.execute('select t.F748, dil.F1783 as Orgid, ' +
                  'np.F318 as Nas_Punkt, ' +
                  'vul.f599 as Vul, ' +
                  't.F741 as Dom, ' +
                  't.F772 as Id_tz ' +
                  'from T135 as t ' +
                  'left join T52 as dil ' +
                  'on t.F748 = dil.id ' +
                  'left join T53 as np ' +
                  'on t.F749 = np.id ' +
                  'left join T109 as vul ' +
                  'on t.F740 = vul.id '+
                  'where t.id = '+str(TZ_id)+'');
            for row in cur.itermap():
                user.city = str(row['OrgId'])
                user.tz_id = str(row['Id_tz'])
                user.adres = DRW.check_addres(row)
                my_array.append(str(user.city)+" ; "+str(user.tz_id)+" ; "+str(user.adres))
            cur.close()
            con.close()
        return my_array
                        
    def get_skz_info(message,user):
            con = fdb.connect(host='192.168.1.248',database='v:\Oper\Ehz.fdb', port = '3075', user='sysdba', password='masterkey', charset='UTF8')
            cur = con.cursor()
            my_array = []
            SKZ_id = user.skz_id
            if SKZ_id is not None:
                cur.execute("select t.F614, dil.F1783 as Orgid,"+
                  " np.F318 as Nas_Punkt,"+
                  " vul.f599 as Vul,"+
                  " t.F643 as Dom,"+
                  " t.F691 as Inv"+
                  " from T115 as t"+
                  " left join T52 as dil"+
                  " on t.F614 = dil.id"+
                  " left join T53 as np"+
                  " on t.F615 = np.id"+
                  " left join T109 as vul"+
                  " on t.F616 = vul.id"+
                  " where t.id = '"+str(SKZ_id)+"'")
                for row in cur.itermap():
                     user.city = str(row['OrgId'])
                     user.inv = str(row['Inv'])
                     user.adres = DRW.check_addres(row)
                     my_array.append(str(user.city)+" ; "+str(user.inv)+" ; "+str(user.adres))
                cur.close()
                con.close()
            return my_array
    
    def get_naryad_new(FIO):
        con = fdb.connect(host='192.168.1.248',database='v:\Oper\Ehz.fdb', port = '3075', user='sysdba', password='masterkey', charset='UTF8')
        now = datetime.date.today() 
        cur = con.cursor()  
        cur.execute("select"+
        " Naryad.F1834 as Naryad_VidRabot,"+ ##12.01
        " Naryad.F839 as Naryad_Nom,"+                
        " Naryad.id as Naryad_Key," +                 
        " Isponliteli.F854 as Isponitel_Key," +        
        " Sotrudniki.id as Key_V_Sprav," +             
        " Sotrudniki.F104 as FIO," +
        " VidiRabot.F1305 as VidRabot" + ##12.01
        " from T151 as Naryad" +                       
        " Left join T162 as Isponliteli" +             
        " On Isponliteli.Pid = Naryad.id" +                 
        " Left join T23 as Sotrudniki" +              
        " On Isponliteli.F854 = Sotrudniki.id" +       
        " Left join T161 as Vipusk"+                       
        " On Vipusk.pId = Naryad.id" +                
        " Left join T115 as Object"+                    
        " On Vipusk.F884 = OBJECT.id" +
        " Left join T244 as VidiRabot"+    ##12.01               
        " On Naryad.F1834 = VidiRabot.id" + ##12.01
        " where (Naryad.F1073 = 0) and (Naryad.F840 <= '"+str(now)+"')"+
        " group by Naryad_Nom,Naryad_Key,Isponitel_Key,Key_V_Sprav,FIO,VidRabot,Naryad_VidRabot"+ ##12.01
        " Order by Isponitel_Key ASC")
        my_array = []
        for row in cur.itermap():
            if str(row['FIO']) != "None":
                if str(FIO) == str(row['FIO']):
                    my_array.append(str(row['Naryad_Nom'])+" ; "+str(row['FIO'])+" ; "+str(row['VidRabot'])) #+Naryad_VidRabot##12.01
        cur.close()
        con.close()
        return my_array
            
    def get_naryad():
        con = fdb.connect(host='192.168.1.248',database='v:\Oper\Ehz.fdb', port = '3075', user='sysdba', password='masterkey', charset='UTF8')
        now = datetime.date.today() 
        cur = con.cursor()  
        cur.execute("select"+
        " Naryad.F1834 as Naryad_VidRabot,"+ ##12.01
        " Naryad.F839 as Naryad_Nom,"+                
        " Naryad.id as Naryad_Key," +                 
        " Isponliteli.F854 as Isponitel_Key," +        
        " Sotrudniki.id as Key_V_Sprav," +             
        " Sotrudniki.F104 as FIO" +
        " VidiRabot.F1305 as VidRabot" + ##12.01
        " from T151 as Naryad" +                       
        " Left join T162 as Isponliteli" +             
        " On Isponliteli.Pid = Naryad.id" +                 
        " Left join T23 as Sotrudniki" +              
        " On Isponliteli.F854 = Sotrudniki.id" +       
        " Left join T161 as Vipusk"+                       
        " On Vipusk.pId = Naryad.id" +                
        " Left join T115 as Object"+                    
        " On Vipusk.F884 = OBJECT.id" +
        " Left join T244 as VidiRabot"+    ##12.01               
        " On Naryad.F1834 = VidiRabot.id" + ##12.01
                    
        " where (Naryad.F1073 = 0) and (Naryad.F840 <= '"+str(now)+"')"+
        " group by Naryad_Nom,Naryad_Key,Isponitel_Key,Key_V_Sprav,FIO,VidRabot,Naryad_VidRabot"+
        " Order by Isponitel_Key ASC")
        my_array = []
        for row in cur.itermap():
            if str(row['FIO']) != "None":
                my_array.append(str(row['Naryad_Nom'])+" ; "+str(row['FIO']))
        cur.close()
        con.close()
        return my_array

    def get_tz(message,user):
        con = fdb.connect(host='192.168.1.248',database='v:\Oper\Ehz.fdb', port = '3075', user='sysdba', password='masterkey', charset='UTF8')
        cur = con.cursor()
        Naryad_Nom = int(user.naryad)
        cur.execute("select "+
          "Types.F601 as type_name, "+
          "Object.F739 as type_id, "+
          "Object.F1840 as categorie, "+
          "Object.F1042 as TZ_Name, "+
          "Vipusk.F1043 as TZ_id, "+
          "Naryad.id as Naryad_Key "+
          "from T151 as Naryad "+
          "Left join T161 as Vipusk "+
          "On Vipusk.pId = Naryad.id "+
          "Left join T135 as Object "+
          "On Vipusk.F1043 = OBJECT.id "+
          "Left join T110 as Types "+    
          "On Object.F739=Types.id "+      
          "where Naryad.F839 = '"+str(Naryad_Nom)+"' and Object.F1042<>'' "+
          " group by type_name,type_id,categorie,TZ_id,TZ_Name,Naryad_Key"+
          " Order by TZ_id ASC")
        
        my_array = []
        for row in cur.itermap():
            try:
                if row['TZ_name'] is not None:
                    TZ_name = DRW.clear_name(row['TZ_name'].title())
                    name_for_user = str(row['type_name'])+" "+str(TZ_name)
                    if row['categorie'] is None:
                        my_array.append(name_for_user+" ; "+str(row['TZ_id'])+" ; "+str(row['categorie']))
                    else:
                        my_array.append(name_for_user+" ; "+str(row['TZ_id'])+" ; "+str(int(row['categorie'])))
            except Exception as e:
                print(e)
        cur.close()
        con.close()
        return my_array
  
    def get_skz(message,user):
            con = fdb.connect(host='192.168.1.248',database='v:\Oper\Ehz.fdb', port = '3075', user='sysdba', password='masterkey', charset='UTF8')
            cur = con.cursor()
            Naryad_Nom = int(user.naryad)
            cur.execute("select Object.F632 as SKZ_Name,"+
                        " Object.F1864 as categorie,"+  
                        " Vipusk.F884 as SKZ_id,"+                    
                        " Naryad.id as Naryad_Key " +                             
                        " from T151 as Naryad" +                     
                        " Left join T161 as Vipusk"+                    
                        " On Vipusk.pId = Naryad.id" +                
                        " Left join T115 as Object"+                 
                        " On Vipusk.F884 = OBJECT.id" +               
                        " where Naryad.F839 = '"+str(Naryad_Nom)+"'"+
                        " group by SKZ_id,SKZ_Name,Naryad_Key,categorie"+
                        " Order by SKZ_id ASC")
            my_array = []
            for row in cur.itermap():
                try:
                    if row['SKZ_Name'] is not None:
                        SKZ_Name = DRW.clear_name(row['SKZ_Name'])
                        my_array.append(str(SKZ_Name)+" ; "+str(row['SKZ_id'])+" ; "+str(row['categorie']))
                except Exception as e:
                    print(e)
            cur.close()
            con.close()
            return my_array


class electro:


    def add_pokaz(message,user,bot):#con.commit()
        try:
            Max_count = 0
            coefficient = 0
            type_potreb_name = ''
            now_potreb = 0
            active = user.energy_active
            reactive = user.energy_reactive
            generation = user.energy_generation
            inv = user.inv
            pokazanie = user.pokazanie
            now = datetime.date.today()
            con = fdb.connect(dsn='DbOper.gaz/3075:v:\Oper\Operativka_expl.fdb',
                              user='sysdba',
                              password='masterkey',
                              charset='UTF8')
            cur = con.cursor()
            #Есть ли такие записи вообще?
            try:
                
                      
                cur.execute("select t_counter.F354 as nas_punkt,"+
                        " t_counter.F377 as potreb_punkt,"+
                        " t_counter.id as counter,"+
                        " t_counter.F346 as dogovor,"+
                        " t_pokaz.F379 as coefficient,"+
                        " max(t_pokaz.F362) as lastpokaz,"+
                        " t_pokaz.F402 as type_potreb"+
                        " from t54 as t_counter"+
                        " left join T58 as t_potreb"+
                        " on t_counter.F377 = t_potreb.id"+
                        " left join T80 as t_pokaz"+
                        " on t_counter.id = t_pokaz.F361"+
                          
                        " where t_potreb.F322 = '"+str(inv)+ 
                        "' and t_pokaz.F360 <= '"+str(now)+
                        "' and t_pokaz.F399 = '"+str(active)+
                        "' and t_pokaz.F400 = '"+str(reactive)+
                        "' and t_pokaz.F401 = '"+str(generation)+

                        "' Group by t_counter.F354,"+
                        " t_counter.F377,"+
                        " t_counter.id,"+
                        " t_pokaz.F379,"+
                        " t_counter.F346,"+
                        " t_pokaz.F402")
                for row in cur.itermap():
                    '''IIF([Показания с поверки]<>1, (([Снятые показания]-[Предыдущие показания])*[Расчётный коэффициент])+[Потери], 0)  '''
                    Max_count += 1
                    type_potreb_name = str(row['type_potreb'])
                    coefficient = str(row['coefficient'])
                    lastpokaz = str(row['lastpokaz'])
                    try:
                        now_potreb = (float(pokazanie)-float(lastpokaz))*float(coefficient)
                    except Exception as e:
                        print(e)
                    counter = str(row['counter'])
                    nas_punkt = str(row['nas_punkt'])
                    potreb_punkt = str(row['potreb_punkt'])
                    dogovor = str(row['dogovor'])
                    
                print("Таких записей : "+str(Max_count))
            except Exception as e:
                print(str(e)+" в есть ли такие вообще")
            if Max_count > 0:
                #Есть ли такие записи за сегодня?
                try:
                    cur.execute("select t_counter.F354 as nas_punkt,"+
                        " t_counter.F377 as potreb_punkt,"+
                        " t_counter.id as counter,"+
                        " t_counter.F346 as dogovor"+
                        " from t54 as t_counter"+
                        " left join T58 as t_potreb"+
                        " on t_counter.F377 = t_potreb.id"+
                        " left join T80 as t_pokaz"+
                        " on t_counter.id = t_pokaz.F361"+
                        " where t_potreb.F322 = '"+str(inv)+ 
                        "' and t_pokaz.F360 = '"+str(now)+
                        "' and t_pokaz.F399 = '"+str(active)+
                        "' and t_pokaz.F400 = '"+str(reactive)+
                        "' and t_pokaz.F401 = '"+str(generation)+"'")
                    number_of_rows = 0
                    for row in cur.itermap():
                        if int(row['count'])>0:
                            number_of_rows += 1
                    print("Таких записей : "+str(number_of_rows)+" за сегодня")
                except Exception as e:
                    print(str(e)+" в есть ли такие сегодня")
                #Если есть
                if number_of_rows > 0:
                    cur.execute("Update T80 Set F362 = '"+str(pokazanie)+"'"+
                                ", F399 = '"+str(active)+"'"+
                                ", F400 = '"+str(reactive)+"'"+
                                ", F401 = '"+str(generation)+"'"+
                                ", F438 = '0'"+#Потери
                                ", F379 = '"+str(coefficient)+"'"+#Коэффициент
                                ", F369 = '"+str(lastpokaz)+"'"+#Предыдущие показания
                                ", F445 = '1'"+#TelegramBot
                                ", F402 = '"+str(type_potreb_name)+"'"+#Тип потребления
                                ", F439 = '0'"+#Показания с поверки
                                ", F386 = '"+str(now_potreb)+"'"+#Текущее потребление
                                " Where id = "+
                                    "(select first 1 T80.id"+              
                                    " from t54"+
                                    " left join T58"+
                                    " on t54.F377 = T58.id"+
                                    " left join T80"+
                                    " on t54.id = T80.F361 "+
                                    "where T58.F322 = '"+str(inv)+
                                    "' and T80.F360 = '"+str(now)+
                                    "' and T80.F399 = '"+str(active)+
                                    "' and T80.F400 = '"+str(reactive)+
                                    "' and T80.F401 = '"+str(generation)+
                                    "' and T54.id   = '"+str(counter)+
                                    "' and T54.F354 = '"+str(nas_punkt)+
                                    "' and T54.F377 = '"+str(potreb_punkt)+
                                    "' and T54.F363 = '"+str(dogovor)+"')")
                    print("В уже созданую запись '"+str(inv)+"' внесены показания '"+str(pokazanie)+"' и модернизировалась сама запись")
                    '''
                    select
                    [Потери]/*F438*/,
                    max([Расчётный коэффициент]) as coefficient/*F379*/,
                    max([Предыдущие показания]) as lastpokaz/*F369*/,
                    [TelegramBot]/*F445*/,
                    [Тип потребления]/*F402*/,
                    [Показания с поверки]/*F439*/,
                    [Key_id]/*F441*/
                    from [Снятия показаний]/*T80*/
                    group by
                    [Потери]/*F438*/,
                    [TelegramBot]/*F445*/,
                    [Тип потребления]/*F402*/,
                    [Показания с поверки]/*F439*/,
                    [Key_id]/*F441*/
                    
                    '''
                #Если нет
                else:
                    cur.execute("SELECT (MAX(ID)+1) as max_id FROM T80")
                    max_id = 0
                    for row in cur.itermap():
                        max_id = row['max_id']
                    if max_id > 0 :
                        cur.execute("INSERT INTO T80(ID, F362, F361, F364, F375, F360, F363, F399, F400, F401, F438, F379, "+
                                    "F369, F445, F402, F439, F441, F386)"+
                        " VALUES('"+str(max_id)+"','"+str(pokazanie)+
                                    "','"+str(counter)+"','"+str(nas_punkt)+
                                    "','"+str(potreb_punkt)+"','"+str(now)+
                                    "','"+str(dogovor)+"','"+str(active)+
                                    "','"+str(reactive)+"','"+str(generation)+
                                    "','0' ,'"+str(coefficient)+"','"+str(lastpokaz)+
                                    "', '1','"+str(type_potreb_name)+
                                    "', '0', '"+str(max_id)+
                                    "', '"+str(now_potreb)+"')")
                        print("В базу Электросчётчики создано запись и занесены показания '"+str(pokazanie)+"'")
                con.commit()
                cur.close()
                bot.reply_to(message, "Данные записаны в базу Электросчётчики!")
                print("Обновилась запись '"+str(inv)+"' и внесены показания '"+str(pokazanie)+"'")
        except Exception as errorMsg:
            bot.reply_to(message, "Данные не записаны в базу Электросчётчики! " + str(errorMsg))
            print(" "+str(errorMsg))
        con.close()
        return
                
class DRW:
    def clear_name(name):
        if name is not None:
            for i in wrong_arr:
                name = name.replace(i,' ')

        return name

    def check_addres(row):

        Dom = Vul = Nas_Punkt = ""
        if row['Dom'] is not None:
            Dom = str(", "+row['Dom']);
        if row['Vul'] is not None:
            Vul = str(", "+row['Vul']);
        if row['Nas_Punkt'] is not None:
            Nas_Punkt = str(row['Nas_Punkt']);

        adres = str(Nas_Punkt+Vul+Dom);
        for i in wrong_arr:
            adres = adres.replace(i,' ')

        return adres
    
    def check_id(message):
        chat_id = message.chat.id
        chat_id_in_bd = ''
        con = fdb.connect(host='192.168.1.248',database='v:\Oper\Ehz.fdb', port = '3075', user='sysdba', password='masterkey', charset='UTF8')
        cur = con.cursor()
        cur.execute("select id, F1828 as chat_id, F104 as FIO, F1102 as Status, F1803 as Ph_number"+ 
                        " from T23"+
                        " where F1102 = 1 and F1828 = '"+str(chat_id)+"'")
        my_array = []
        for row in cur.itermap():
            my_array.append(str(row['FIO'])+" ; "+str(row['Ph_number']+" ; "+str(row['Status'])+" ; "+str(row['chat_id'])+" ; "+str(row['id'])))
            chat_id_in_bd = str(row['chat_id'])
            print(my_array)
        cur.close()
        con.close()
        if my_array=='':
            return ''
        else:
            return my_array
            
    def login(message):#con.commit()
        
        phone = ''
        if message.contact is not None:
            chat_id = message.chat.id
            phone_brutal = message.contact.phone_number
            for i in phone_brutal:  #Форматируем вх. номер телефона
                    if i.isnumeric() == True:
                        phone += i

            #Соединение с БД ЭХЗ для поиска по номеру телефона        
            #con = fdb.connect(dsn='DbOper.gaz/3075:v:\Oper\Ehz.fdb', user='sysdba', password='masterkey', charset='UTF8')
            con = fdb.connect(host='192.168.1.248',database='v:\Oper\Ehz.fdb', port = '3075', user='sysdba', password='masterkey', charset='UTF8')

            #Объявление курсора для запроса
            cur = con.cursor()
            #Присваиваем курсору запрос к таблице Сотрудники
            cur.execute("select id, F1828 as chat_id, F104 as FIO, F1102 as Status, F1803 as Ph_number"+ 
                        " from T23"+
                        " where F1102 = 1 and F1803<>''")
            phones_array = [] #Объявляем массив номеров 
            #Перебор строк запроса
            for row in cur.itermap(): 
                #Очистили главную переменную
                phone_from_bd=''
                #Записали в переменные значения
                phone_brutal = str(row['Ph_number'])
                name = str(row['FIO'])
                id_key = str(row['id'])
                chat_id_key = str(row['chat_id'])
                #Перебор каждого символа в переменной
                for i in phone_brutal:
                    #Условие очистки от ненужных символов
                    if i.isnumeric() == True:
                        #Заполняем главную переменную
                        phone_from_bd += i
                #Заполняем массив номеров
                phones_array.append(name+";"+phone_from_bd+";"+id_key+";"+chat_id_key) #Очистили и получили FIO и цифры телефона
            #Закрываем курсор запроса
            cur.close()
            my_array=[]    
            #Перебираем каждый элемент массива номеров
            for element in phones_array:
                #Поиск нужного значения
                phone_from_bd = element.split(";")[1].strip()
                if str(phone) == str(phone_from_bd):
                    #Записываем в переменные нужные значения из строки массива
                    name = element.split(";")[0].strip()
                    id_key = element.split(";")[2].strip()
                    chat_id_key = element.split(";")[3].strip()
                    #Заполняем массив для возврата в main
                    my_array.append(element)
                    #Если в БД ключ чата не заполнен или устарел
                    if str(chat_id_key) != str(chat_id):
                        #Обновляем поле ключ чата в БД
                        cur.execute("Update T23 Set F1828 = '"+str(chat_id)+"' "+
                        " Where id = '"+str(id_key)+"' ")
                        #Подтверждаем обновление по строке подключения
                        con.commit()
                        #Закрываем курсор обновы
                        cur.close()
            #Закрываем строку подключения    
            con.close()
            #Возвращаем массив в main
            return my_array   
  

  
    def controll_vvoda(message):
        text = message.text
        #print(text)
        if text is None or '/' in text:
            pass;
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
                    print('U can\'t converts this '+str(text)+' to float')
                    pass;
            else:
                for i in first_reinc:
                    if i.isnumeric() == True:
                        first_res += i
                try:
                    text = int(first_res)
                    if minus != -1:
                        text = text*(-1)
                except Exception:
                    print('U can\'t converts this '+str(text)+' to float')
                    pass;
            text = str(text)
        return text
