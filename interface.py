from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import sqlite3 as sl


class Form:
    def __init__(self, name_form, geom):
        self.root=Tk()
        self.root.title(name_form)
        self.root.geometry(geom)                 
        
class Entry_1:
    def __init__(self, form, label, data, packside):
        self.lab_1=Label(form, text=label)
        self.ent_1=Entry(form)
        self.lab_1.pack(side=packside)
        self.ent_1.pack(side=packside)
        self.ent_1.insert(0,data)
    def get_1(self):
        return self.ent_1.get()
    def set_1(self,d):
        self.ent_1.delete(0,END)
        self.ent_1.insert(0,d)


class Button_1:
    def __init__(self, form, txt, com, packside):
        self.but_1=Button(form, text=txt)
        self.but_1.config(command=com)
        self.but_1.pack(side=packside)
        
        
class Box_1:
    def __init__(self, form, h, w, data):
        self.bx_1=Listbox(form, selectmode=SINGLE, height=h, width=w) 
        self.bx_1.pack(side=LEFT)
        self.scrl=Scrollbar(form, command=self.bx_1.yview)
        self.scrl.pack(side=LEFT, fill=Y)
        self.bx_1.config(yscrollcommand=self.scrl.set) 
        self.Refresh(data)     
    def Return_index(self):
        cursel=self.bx_1.curselection()
        return cursel[0]
    def Refresh(self, data):
        self.bx_1.delete(0,END)
        i=0 
        for str in data:
            self.bx_1.insert(i,str)
            i+=1 
        
       
class Combobox_1:
    def __init__(self, form, label, data, packside):
        self.lab_1=Label(form, text=label)
        self.lab_1.pack(side=packside)
        self.cmbx_1=ttk.Combobox(form, values=data, state="readonly")
        self.cmbx_1.pack(side=packside)
    def get_1(self):
        return self.cmbx_1.get()
    def set_1(self, data):
        self.cmbx_1.set(data)
     
     
class scene_client:
    def __init__(self):
        con = sl.connect('Logs.db')
        cursor=con.cursor()
        cursor.execute("""SELECT name FROM CLIENTS""")
        clients_list=cursor.fetchall()
        cursor.execute("""SELECT * FROM CLIENTS WHERE id_client=1""")
        answear=cursor.fetchall()
        id_client=answear[0][0]
        name_client=answear[0][1]
        gmt_client=answear[0][2]
        type_client=answear[0][3]
        self.form_client=Form("Клиенты","400x360")
        self.f_left=Frame(self.form_client.root)
        self.f_left.pack(side=LEFT)
        self.f_right=Frame(self.form_client.root)
        self.f_right.pack(side=LEFT)
        self.f_left_bot=Frame(self.f_left)
        self.f_left_bot.pack(side=BOTTOM)
        self.Box_1_client_list=Box_1(self.f_left,"20","40",clients_list)
        self.Button_1_show=Button_1(self.f_left_bot,"Выбрать",lambda:self.Select_client(clients_list),LEFT)
        self.Button_1_add=Button_1(self.f_left_bot,"Добавить",lambda:self.Add_client_f(),LEFT)
        self.Button_1_change=Button_1(self.f_left_bot,"Изменить",lambda:self.Update_client_f(),LEFT)
        self.Button_1_delete=Button_1(self.f_left_bot,"Удалить",lambda:self.Delete_client_f(self.Entry_1_id_client.get_1()),LEFT)
        self.Entry_1_id_client=Entry_1(self.f_right,"ID клиента",id_client,TOP)
        self.Entry_1_name=Entry_1(self.f_right,"Имя клиента",name_client,TOP)
        self.Entry_1_gmt=Entry_1(self.f_right,"Часовой пояс",gmt_client,TOP)
        self.Entry_1_type=Entry_1(self.f_right,"Тип обслуживания",type_client,TOP)
        self.Button_1_device=Button_1(self.f_right,"Устройства",lambda:self.Show_device(self.Entry_1_id_client.get_1()),TOP)
        self.form_client.root.mainloop()
    
    def Select_client(self,clients_list):
        index=clients_list[self.Box_1_client_list.Return_index()][0]
        con = sl.connect('Logs.db')
        cursor=con.cursor()
        cursor.execute("""SELECT * FROM CLIENTS WHERE name='"""+str(index)+"""'""")
        answear=cursor.fetchall()
        self.Entry_1_id_client.set_1(answear[0][0])
        self.Entry_1_name.set_1(answear[0][1])
        self.Entry_1_gmt.set_1(answear[0][2])
        self.Entry_1_type.set_1(answear[0][3])
        
    def Add_client_f(self):
        self.form_add_client=Form("Добавить клиента","200x300")
        type_client=["customer","service","opi"]
        self.Entry_1_add_name=Entry_1(self.form_add_client.root,"Имя клиента","",TOP)
        self.Entry_1_add_gmt=Entry_1(self.form_add_client.root,"Часовой пояс","",TOP)
        self.Cmbx_1_add_type=Combobox_1(self.form_add_client.root,"Тип обслуживания",type_client,TOP)
        self.Button_1_save_client=Button_1(self.form_add_client.root,"Добавить",lambda:self.Add_client_DB(),TOP)
    
    def Add_client_DB(self):
        name=str(self.Entry_1_add_name.get_1())
        gmt=str(self.Entry_1_add_gmt.get_1())
        type_client=str(self.Cmbx_1_add_type.get_1())
        con = sl.connect('Logs.db')  
        cursor=con.cursor()
        cursor.execute("""INSERT INTO CLIENTS (name,gmt,type) VALUES ('"""+name+"""','"""+gmt+"""','"""+type_client+"""')""")
        con.commit()
        self.Refresh_client_list()
        self.form_add_client.root.destroy()
        
    def Refresh_client_list(self):
        con = sl.connect('Logs.db')
        cursor=con.cursor()
        cursor.execute("""SELECT name FROM CLIENTS""")
        clients_list=cursor.fetchall()
        self.Box_1_client_list.Refresh(clients_list)
        
    def Update_client_f(self):
        self.form_upd_client=Form("Изменить клиента","200x300")
        type_client=["customer","service","opi"]
        id_client=str(self.Entry_1_id_client.get_1())
        self.Entry_1_upd_name=Entry_1(self.form_upd_client.root,"Имя клиента",self.Entry_1_name.get_1(),TOP)
        self.Entry_1_upd_gmt=Entry_1(self.form_upd_client.root,"Часовой пояс",self.Entry_1_gmt.get_1(),TOP)
        self.Cmbx_1_upd_type=Combobox_1(self.form_upd_client.root,"Тип обслуживания",type_client,TOP)
        self.Cmbx_1_upd_type.set_1(self.Entry_1_type.get_1())
        self.Button_1_upd_client=Button_1(self.form_upd_client.root,"Сохранить",lambda:self.Upd_client_BD(id_client),TOP)
     
    def Upd_client_BD(self,id_client):
        name=str(self.Entry_1_upd_name.get_1())
        gmt=str(self.Entry_1_upd_gmt.get_1())
        type_client=str(self.Cmbx_1_upd_type.get_1())
        con = sl.connect('Logs.db')  
        cursor=con.cursor()
        cursor.execute("""UPDATE CLIENTS SET name='"""+name+"""',gmt='"""+gmt+"""',type='"""+type_client+"""' WHERE id_client="""+id_client)
        con.commit()
        self.Refresh_client_list()
        self.form_upd_client.root.destroy()    
        
    def Delete_client_f(self,id_client):
        con = sl.connect('Logs.db')
        cursor=con.cursor()
        cursor.execute("""SELECT name FROM DEVICES WHERE id_client="""+str(id_client))
        device_list=cursor.fetchall()
        self.form_delete_client=Form("Удаление клиента","400x50")
        if device_list!=[]:
            self.lab_del=Label(self.form_delete_client.root, text="УДАЛЕНИЕ НЕВОЗМОЖНО! ЕСТЬ ПРИВЯЗАННЫЕ УСТРОЙСТВА!")
            self.lab_del.pack(side=TOP)
            self.Button_1_del_client=Button_1(self.form_delete_client.root,"ОК",lambda:self.form_delete_client.root.destroy(),TOP)
        else:
            self.lab_del=Label(self.form_delete_client.root, text="ВЫ ТОЧНО ХОТИТЕ УДАЛИТЬ КЛИЕНТА?")
            self.lab_del.pack(side=TOP)
            self.f=Frame(self.form_delete_client.root)
            self.f.pack(side=TOP, padx=150)
            self.Button_1_del_client=Button_1(self.f,"Да",lambda:self.Delete_client_BD(id_client),LEFT)
            self.Button_1_cnl_client=Button_1(self.f,"Нет",lambda:self.form_delete_client.root.destroy() ,RIGHT)
        
    def Delete_client_BD(self,id_client):
        con = sl.connect('Logs.db')
        cursor=con.cursor()
        cursor.execute("""DELETE FROM CLIENTS WHERE id_client="""+str(id_client))
        con.commit()
        self.Refresh_client_list()
        self.form_delete_client.root.destroy()  
            
    def Show_device(self,id_client):
        scene_device(id_client,self.Entry_1_name.get_1())

        
class scene_device:
    def __init__(self, id_cur_client, name_client):
        con = sl.connect('Logs.db')
        cursor=con.cursor()
        cursor.execute("""SELECT name FROM DEVICES WHERE id_client="""+id_cur_client)
        self.device_list=cursor.fetchall()
        if self.device_list!=[]:
            cursor.execute("""SELECT * FROM DEVICES WHERE name='"""+str(self.device_list[0][0])+"""'""")
            answear=cursor.fetchall()
            id_device=answear[0][0]
            id_client=answear[0][1]
            name_device=answear[0][2]
            user_name=answear[0][3]
            version=answear[0][4]
        else:
            id_device=""
            id_client=""
            name_device=""
            user_name=""
            version=""
        self.form_device=Form("Устройства "+name_client,"400x360")
        self.f_left=Frame(self.form_device.root)
        self.f_left.pack(side=LEFT)
        self.f_right=Frame(self.form_device.root)
        self.f_right.pack(side=LEFT)
        self.f_left_bot=Frame(self.f_left)
        self.f_left_bot.pack(side=BOTTOM)
        self.Box_1_device_list=Box_1(self.f_left,"20","40",self.device_list)
        self.Button_1_show=Button_1(self.f_left_bot,"Выбрать",lambda:self.Select_device(self.device_list),LEFT)
        self.Button_1_add=Button_1(self.f_left_bot,"Добавить",lambda:self.Add_device_f(id_cur_client),LEFT)
        self.Button_1_change=Button_1(self.f_left_bot,"Изменить",lambda:self.Update_device_f(id_cur_client),LEFT)
        self.Button_1_delete=Button_1(self.f_left_bot,"Удалить",lambda:self.Delete_device_f(self.Entry_1_id_device.get_1(),id_cur_client),LEFT)
        self.Entry_1_id_device=Entry_1(self.f_right,"ID устройства",id_device,TOP)
        self.Entry_1_id_client=Entry_1(self.f_right,"ID клиента",id_client,TOP)
        self.Entry_1_name_device=Entry_1(self.f_right,"Номер устройства",name_device,TOP)
        self.Entry_1_user_name=Entry_1(self.f_right,"Имя устройства",user_name,TOP)
        self.Entry_1_version=Entry_1(self.f_right,"Версия",version,TOP)
        self.Button_1_device=Button_1(self.f_right,"Просмотр архива",lambda:self.Show_log(self.Entry_1_id_device.get_1()),TOP)
        self.form_device.root.mainloop()
        
    def Select_device(self,device_list):
        index=device_list[self.Box_1_device_list.Return_index()][0]
        con = sl.connect('Logs.db')
        cursor=con.cursor()
        cursor.execute("""SELECT * FROM DEVICES WHERE name='"""+str(index)+"""'""")
        answear=cursor.fetchall()
        self.Entry_1_id_device.set_1(answear[0][0])
        self.Entry_1_id_client.set_1(answear[0][1])
        self.Entry_1_name_device.set_1(answear[0][2])
        self.Entry_1_user_name.set_1(answear[0][3])
        self.Entry_1_version.set_1(answear[0][4])
        
    def Add_device_f(self, id_client):
        self.form_add_device=Form("Добавить устройство","200x300")
        self.Entry_1_add_name_device=Entry_1(self.form_add_device.root,"Номер устройства","",TOP)
        self.Entry_1_add_user_name=Entry_1(self.form_add_device.root,"Имя устройства","",TOP)
        self.Entry_1_add_version=Entry_1(self.form_add_device.root,"Версия","",TOP)
        self.Button_1_save_device=Button_1(self.form_add_device.root,"Добавить",lambda:self.Add_device_DB(id_client),TOP)
      
    def Add_device_DB(self, id_client):
        name_device=str(self.Entry_1_add_name_device.get_1())
        user_name=str(self.Entry_1_add_user_name.get_1())
        version=str(self.Entry_1_add_version.get_1())
        con = sl.connect('Logs.db')  
        cursor=con.cursor()
        cursor.execute("""INSERT INTO DEVICES (id_client,name,username,version) VALUES ('"""+str(id_client)+"""',"""+name_device+""",'"""+user_name+"""','"""+version+"""')""")
        con.commit()
        self.Refresh_device_list(id_client)
        self.form_add_device.root.destroy()  
        
    def Refresh_device_list(self, id_client):
        con = sl.connect('Logs.db')
        cursor=con.cursor()
        cursor.execute("""SELECT name FROM DEVICES WHERE id_client="""+str(id_client))
        self.device_list=cursor.fetchall()
        self.Box_1_device_list.Refresh(self.device_list)
        
    def Update_device_f(self, id_client):
        self.form_upd_device=Form("Изменить устройство","200x300")
        id_device=str(self.Entry_1_id_device.get_1())
        self.Entry_1_upd_id_client=Entry_1(self.form_upd_device.root,"ID клиента",self.Entry_1_id_client.get_1(),TOP)
        self.Entry_1_upd_name_device=Entry_1(self.form_upd_device.root,"Номер устройства",self.Entry_1_name_device.get_1(),TOP)
        self.Entry_1_upd_user_name=Entry_1(self.form_upd_device.root,"Имя устройства",self.Entry_1_user_name.get_1(),TOP)
        self.Entry_1_upd_version=Entry_1(self.form_upd_device.root,"Версия",self.Entry_1_version.get_1(),TOP)
        self.Button_1_upd_client=Button_1(self.form_upd_device.root,"Сохранить",lambda:self.Upd_device_DB(id_device,id_client),TOP)
        
    def Upd_device_DB(self, id_device, id_client):
        name_device=str(self.Entry_1_upd_name_device.get_1())
        user_name=str(self.Entry_1_upd_user_name.get_1())
        version=str(self.Entry_1_upd_version.get_1())
        con = sl.connect('Logs.db')  
        cursor=con.cursor()
        cursor.execute("""UPDATE DEVICES SET id_client='"""+str(id_client)+"""',name='"""+name_device+"""',username='"""+user_name+"""',version='"""+version+"""' WHERE id_device="""+str(id_device))
        con.commit()
        self.Refresh_device_list(id_client)
        self.form_upd_device.root.destroy() 
        
    def Delete_device_f(self,id_device,id_client):
        self.form_delete_device=Form("Удаление устройства","400x50")
        self.lab_del=Label(self.form_delete_device.root, text="ВЫ ТОЧНО ХОТИТЕ УДАЛИТЬ УСТРОЙСТВО?")
        self.lab_del.pack(side=TOP)
        self.f=Frame(self.form_delete_device.root)
        self.f.pack(side=TOP, padx=150)
        self.Button_1_del_client=Button_1(self.f,"Да",lambda:self.Delete_device_DB(id_device,id_client),LEFT)
        self.Button_1_cnl_client=Button_1(self.f,"Нет",lambda:self.form_delete_device.root.destroy() ,RIGHT)
        
    def Delete_device_DB(self,id_device,id_client):
        con = sl.connect('Logs.db')
        cursor=con.cursor()
        cursor.execute("""DELETE FROM DEVICES WHERE id_device="""+str(id_device))
        con.commit()
        self.Refresh_device_list(id_client)
        self.form_delete_device.root.destroy()
        
    def Show_log(self,id_device):
        scene_log(id_device)



class scene_log:
    def __init__(self,id_device):
        con = sl.connect('Logs.db')
        cursor=con.cursor()
        cursor.execute("""SELECT DISTINCT date FROM LOG WHERE id_device="""+id_device)
        self.date_list=cursor.fetchall()
        cursor.execute("""SELECT username FROM DEVICES WHERE id_device="""+id_device)
        answear=cursor.fetchall()
        self.form_log=Form("Архив "+answear[0][0],"1100x360")
        self.f_left=Frame(self.form_log.root)
        self.f_left.pack(side=LEFT)
        self.f_right=Frame(self.form_log.root)
        self.f_right.pack(side=LEFT)
        self.f_left_bot=Frame(self.f_left)
        self.f_left_bot.pack(side=BOTTOM)
        self.Box_1_log_list=Box_1(self.f_left,"20","40",self.date_list)
        self.Button_1_choose_file=Button_1(self.f_left_bot,"Выбрать дату",lambda:self.Select_date(self.date_list,id_device),LEFT)
        self.Button_1_add_log=Button_1(self.f_left_bot,"Добавить данные",lambda:self.Add_log(id_device),LEFT)
        headings=("Дата","Время","Глубина","Мощность")
        self.data_table=ttk.Treeview(self.f_right, show="headings", selectmode="extended", height="300")
        self.data_table["columns"]=headings
        self.data_table["displaycolumns"]=headings
        for head in headings:
            self.data_table.heading(head, text=head, anchor=CENTER)
            self.data_table.column(head, anchor=CENTER)
        if self.date_list!=[]:
            cursor.execute("""SELECT date,time,depth,power FROM LOG WHERE id_device="""+id_device+""" AND date='"""+str(self.date_list[0][0])+"""'""")
            data=(row for row in cursor.fetchall())
            for row in data:
                self.data_table.insert('',END,values=tuple(row))
        scrolltable=Scrollbar(self.f_right,command=self.data_table.yview)
        self.data_table.configure(yscrollcommand=scrolltable.set)
        scrolltable.pack(side=RIGHT, fill=Y)
        self.data_table.pack(expand=YES,fill=BOTH)  
     
    def Select_date(self,date_list,id_device):
        self.data_table.delete(*self.data_table.get_children())
        index=date_list[self.Box_1_log_list.Return_index()][0]
        con = sl.connect('Logs.db')
        cursor=con.cursor()
        cursor.execute("""SELECT date,time,depth,power FROM LOG WHERE id_device="""+id_device+""" AND date='"""+str(index)+"""'""")
        data=(row for row in cursor.fetchall())
        for row in data:
            self.data_table.insert('',END,values=tuple(row))   
    
    def Refresh_date(self,id_device):
        con = sl.connect('Logs.db')
        cursor=con.cursor()
        cursor.execute("""SELECT DISTINCT date FROM LOG WHERE id_device="""+id_device)
        self.date_list=cursor.fetchall()
        self.Box_1_log_list.Refresh(self.date_list)
        
    def Add_log(self,id_device):
        filepath = filedialog.askopenfilename()
        if filepath != "":
            self.Import_log(id_device,filepath)
            
    def Import_log(self,id_device,filepath):
        arcfile=open(filepath,'r')
        con = sl.connect('Logs.db')
        cursor=con.cursor()
        for line in arcfile:
            data=line.split(sep=";")
            data[2]=data[2].replace("\n","")
            datetime=data[0].split()
            cursor.execute("""INSERT INTO LOG (id_device,date,time,depth,power) VALUES ('"""+str(id_device)+"""','"""+datetime[0]+"""','"""+datetime[1]+"""','"""+data[1]+"""','"""+data[2]+"""')""")
        con.commit()
        arcfile.close()
        self.Refresh_date(id_device)
        
        
        
        
        
scene_1=scene_client()