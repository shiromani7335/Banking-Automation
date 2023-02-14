#!/usr/bin/env python
# coding: utf-8

# In[46]:


from tkinter import *
from tkinter.ttk import Combobox
import time
from tkinter import messagebox
import sqlite3

con=sqlite3.connect(database="banking.sqlite")
cur=con.cursor()
try:
    table_1="create table account(acn_no integer primary key autoincrement,acn_name text,acn_pass text,acn_email text,acn_mob text,acn_bal float,acn_opendate text,acn_type text)"
    table_2="create table txn(txn_acn int,txn_date text,txn_amt float,txn_type text,txn_update_bal float)"
    cur.execute(table_1)
    cur.execute(table_2)
    con.commit()
    con.close()
    print("tables created")
except Exception as e:
    print("something went wrong",e)


win=Tk()
win.state('zoomed')
win.title("Banking")
win.resizable(width=False,height=False)

win_btn_clr="powder blue"

win.configure(bg=win_btn_clr)

lbl_title=Label(win,text="Banking Automation",font=('Arial',50,'bold','underline'),bg=win_btn_clr)
lbl_title.pack()

def home_screen():
    frm=Frame(win)
    frm.configure(bg='pink')
    frm.place(relx=0,rely=.15,relwidth=1,relheight=.85)

    def openacn_click():
        frm.destroy()
        openacn_screen()
    
    def fp_click():
        frm.destroy()
        forgot_screen()
        
    def login_click():
        global acn
        acn=e_acn.get()
        pwd=e_pass.get()
        
        con=sqlite3.connect(database="banking.sqlite")
        cur=con.cursor()
        cur.execute("select acn_name from account where acn_no=? and acn_pass=?",(acn,pwd))
        user_tup=cur.fetchone()
        if(user_tup==None):
            messagebox.showerror("Login","Invalid Acn/Pass")
        else:
            global uname
            uname=user_tup[0]
            frm.destroy()
            welcome_screen()
    lbl_acn=Label(frm,font=('Arial',20,'bold'),bg='pink',text="ACN")
    lbl_acn.place(relx=.3,rely=.1)

    e_acn=Entry(frm,font=('Arial',20,'bold'),bd=5)
    e_acn.place(relx=.45,rely=.1)
    e_acn.focus()
    
    lbl_pass=Label(frm,font=('Arial',20,'bold'),bg='pink',text="Pass")
    lbl_pass.place(relx=.3,rely=.2)

    e_pass=Entry(frm,font=('Arial',20,'bold'),bd=5,show="*")
    e_pass.place(relx=.45,rely=.2)
    
    lgn_btn=Button(frm,bg=win_btn_clr,font=('Arial',20,'bold'),bd=5,text="login",command=login_click)
    lgn_btn.place(relx=.4,rely=.35)
    
    reset_btn=Button(frm,bg=win_btn_clr,font=('Arial',20,'bold'),bd=5,text="reset")
    reset_btn.place(relx=.5,rely=.35)
    
    fp_btn=Button(frm,bg=win_btn_clr,font=('Arial',20,'bold'),width=14,bd=5,text="forgot password",command=fp_click)
    fp_btn.place(relx=.385,rely=.5)
    
    new_btn=Button(frm,bg=win_btn_clr,font=('Arial',20,'bold'),width=18,bd=5,text="open new account",command=openacn_click)
    new_btn.place(relx=.35,rely=.65)
    
def openacn_screen():
    frm=Frame(win)
    frm.configure(bg='pink')
    frm.place(relx=0,rely=.15,relwidth=1,relheight=.85)
    
    def back_click():
        frm.destroy()
        home_screen()
    
    def open_acn_db():
        name=e_name.get()
        pwd=e_pass.get()
        email=e_email.get()
        mob=e_mob.get()
        typ=cb_type.get()
        open_date=time.ctime()
        
        if(typ.lower()=="saving"):
            bal=1000
        elif(typ.lower()=="current"):
            bal=10000
        else:
            messagebox.showwarning("Account Type","Please select a type")
            return
        
        con=sqlite3.connect(database="banking.sqlite")
        cur=con.cursor()
        cur.execute("select max(acn_no) from account")
        acn=cur.fetchone()[0]
        if(acn==None):
            acn=100
        else:
            acn+=1
        con.close()
        
        con=sqlite3.connect(database="banking.sqlite")
        cur=con.cursor()
        cur.execute("insert into account values(?,?,?,?,?,?,?,?)",(acn,name,pwd,email,mob,bal,open_date,typ))
        con.commit()
        con.close()
        messagebox.showinfo("Open Account",f"Your Account is Opened with Account No:{acn}")
        return
    
    back_btn=Button(frm,bg=win_btn_clr,font=('Arial',20,'bold'),bd=5,text="back",command=back_click)
    back_btn.place(relx=0,rely=0)
    
    lbl_name=Label(frm,font=('Arial',20,'bold'),bg='pink',text="Name")
    lbl_name.place(relx=.3,rely=.1)

    e_name=Entry(frm,font=('Arial',20,'bold'),bd=5)
    e_name.place(relx=.45,rely=.1)
    e_name.focus()

    lbl_pass=Label(frm,font=('Arial',20,'bold'),bg='pink',text="Pass")
    lbl_pass.place(relx=.3,rely=.2)

    e_pass=Entry(frm,font=('Arial',20,'bold'),bd=5,show="*")
    e_pass.place(relx=.45,rely=.2)
    
    
    lbl_email=Label(frm,font=('Arial',20,'bold'),bg='pink',text="Email")
    lbl_email.place(relx=.3,rely=.3)

    e_email=Entry(frm,font=('Arial',20,'bold'),bd=5)
    e_email.place(relx=.45,rely=.3)
    
    lbl_mob=Label(frm,font=('Arial',20,'bold'),bg='pink',text="Mob")
    lbl_mob.place(relx=.3,rely=.4)

    e_mob=Entry(frm,font=('Arial',20,'bold'),bd=5)
    e_mob.place(relx=.45,rely=.4)
    
    lbl_type=Label(frm,font=('Arial',20,'bold'),bg='pink',text="Type")
    lbl_type.place(relx=.3,rely=.5)

    cb_type=Combobox(frm,font=('Arial',20,'bold'),values=['---select account---','Saving','Current'])
    cb_type.place(relx=.45,rely=.5)
    cb_type.current(0)
    
    open_btn=Button(frm,command=open_acn_db,bg=win_btn_clr,font=('Arial',20,'bold'),bd=5,text="open")
    open_btn.place(relx=.4,rely=.65)
    
    reset_btn=Button(frm,bg=win_btn_clr,font=('Arial',20,'bold'),bd=5,text="reset")
    reset_btn.place(relx=.5,rely=.65)

def forgot_screen():
    frm=Frame(win)
    frm.configure(bg='pink')
    frm.place(relx=0,rely=.15,relwidth=1,relheight=.85)
    
    def back_click():
        frm.destroy()
        home_screen()
    
    def getpass_db():
        acn=e_acn.get()
        email=e_email.get()
        mob=e_mob.get()
        con=sqlite3.connect(database="banking.sqlite")
        cur=con.cursor()
        cur.execute("select acn_pass from account where acn_no=? and acn_email=? and acn_mob=?",(acn,email,mob))
        tup=cur.fetchone()
        if(tup==None):
            messagebox.showerror("Forgot Password","Incorrect Details!")
        else:
            messagebox.showinfo("Forgot Password",f"Yout Pass:{tup[0]}")
        con.close()
        return
    
    
    def reset():
        e_acn.delete(0,"end")
        e_email.delete(0,"end")
        e_mob.delete(0,"end")
        e_acn.focus()
        
    back_btn=Button(frm,bg=win_btn_clr,font=('Arial',20,'bold'),bd=5,text="back",command=back_click)
    back_btn.place(relx=0,rely=0)
    
    lbl_acn=Label(frm,font=('Arial',20,'bold'),bg='pink',text="ACN")
    lbl_acn.place(relx=.3,rely=.1)

    e_acn=Entry(frm,font=('Arial',20,'bold'),bd=5)
    e_acn.place(relx=.45,rely=.1)
    e_acn.focus()

    lbl_email=Label(frm,font=('Arial',20,'bold'),bg='pink',text="Email")
    lbl_email.place(relx=.3,rely=.2)

    e_email=Entry(frm,font=('Arial',20,'bold'),bd=5)
    e_email.place(relx=.45,rely=.2)
    
    lbl_mob=Label(frm,font=('Arial',20,'bold'),bg='pink',text="Mob")
    lbl_mob.place(relx=.3,rely=.3)

    e_mob=Entry(frm,font=('Arial',20,'bold'),bd=5)
    e_mob.place(relx=.45,rely=.3)
    
    
    recover_btn=Button(frm,command=getpass_db,bg=win_btn_clr,font=('Arial',20,'bold'),bd=5,text="recover")
    recover_btn.place(relx=.4,rely=.55)
    
    reset_btn=Button(frm,command=reset,bg=win_btn_clr,font=('Arial',20,'bold'),bd=5,text="reset")
    reset_btn.place(relx=.55,rely=.55)

    
def welcome_screen():
    frm=Frame(win)
    frm.configure(bg='pink')
    frm.place(relx=0,rely=.15,relwidth=1,relheight=.85)
    
    def logout_click():
        frm.destroy()
        home_screen()
    
    def check_bal():
        ifrm=Frame(frm)
        ifrm.configure(bg='pink')
        ifrm.place(relx=.3,rely=.25,relwidth=.5,relheight=.5)
        lbl_msg.configure(text="This is Check Bal Page")
        
        con=sqlite3.connect(database="banking.sqlite")
        cur=con.cursor()
        cur.execute("select acn_bal,acn_opendate from account where acn_no=?",(acn,))
        bal,opendate=cur.fetchone()
        con.close()
        l1=Label(ifrm,text=f"Acn Balance:{bal}",fg='green',bg='pink',font=('',15,'bold'))
        l2=Label(ifrm,text=f"Open Date:{opendate}",fg='green',bg='pink',font=('',15,'bold'))
        l3=Label(ifrm,text=f"Acn:{acn}",fg='green',bg='pink',font=('',15,'bold'))
        l1.pack()
        l2.pack(pady=20)
        l3.pack()
    
    
    def deposit():
        ifrm=Frame(frm)
        ifrm.configure(bg='pink')
        ifrm.place(relx=.3,rely=.25,relwidth=.5,relheight=.5)
        lbl_msg.configure(text="This is Deposit Page")
        
        def dep_db():
            amt=float(e_amt.get())
            con=sqlite3.connect(database="banking.sqlite")
            cur=con.cursor()
            cur.execute("select acn_bal from account where acn_no=?",(acn,))
            bal=cur.fetchone()[0]
            con.close()
            
            con=sqlite3.connect(database="banking.sqlite")
            cur=con.cursor()
            cur.execute("update account set acn_bal=? where acn_no=?",(bal+amt,acn))
            con.commit()
            con.close()
            
            con=sqlite3.connect(database="banking.sqlite")
            cur=con.cursor()
            cur.execute("insert into txn values(?,?,?,?,?)",(acn,time.ctime(),amt,"Cr",bal+amt))
            con.commit()
            con.close()
            
            messagebox.showinfo("Deposit","Amount deposited")
            return
            
            
        lbl_amt=Label(ifrm,font=('Arial',20,'bold'),bg='pink',text="Amount",fg='green')
        lbl_amt.place(relx=0,rely=0)
        
        e_amt=Entry(ifrm,font=('Arial',20,'bold'),bd=5)
        e_amt.place(relx=.3,rely=0)
        
        dep_btn=Button(ifrm,command=dep_db,bg=win_btn_clr,font=('Arial',20,'bold'),bd=5,text="deposit")
        dep_btn.place(relx=.2,rely=.3)
    
    
    def withdraw():
        ifrm=Frame(frm)
        ifrm.configure(bg='pink')
        ifrm.place(relx=.3,rely=.25,relwidth=.5,relheight=.5)
        lbl_msg.configure(text="This is Withdraw Page")
        
        def withdraw_db():
            amt=float(e_amt.get())
            con=sqlite3.connect(database="banking.sqlite")
            cur=con.cursor()
            cur.execute("select acn_bal from account where acn_no=?",(acn,))
            bal=cur.fetchone()[0]
            con.close()
           
            if(bal>=amt):
        
                con=sqlite3.connect(database="banking.sqlite")
                cur=con.cursor()
                cur.execute("update account set acn_bal=? where acn_no=?",(bal-amt,acn))
                con.commit()
                con.close()

                con=sqlite3.connect(database="banking.sqlite")
                cur=con.cursor()
                cur.execute("insert into txn values(?,?,?,?,?)",(acn,time.ctime(),amt,"Dr",bal-amt))
                con.commit()
                con.close()

                messagebox.showinfo("Withdraw","Amount withdrawn")
                return
            else:
                messagebox.showwarning("Withdraw","Insufficient Bal")
            
        lbl_amt=Label(ifrm,font=('Arial',20,'bold'),bg='pink',text="Amount",fg='green')
        lbl_amt.place(relx=0,rely=0)
        
        e_amt=Entry(ifrm,font=('Arial',20,'bold'),bd=5)
        e_amt.place(relx=.3,rely=0)
        
        with_btn=Button(ifrm,command=withdraw_db,bg=win_btn_clr,font=('Arial',20,'bold'),bd=5,text="withdraw")
        with_btn.place(relx=.2,rely=.3)
    
    
    def update():
        ifrm=Frame(frm)
        ifrm.configure(bg='pink')
        ifrm.place(relx=.2,rely=.25,relwidth=.7,relheight=.5)
        lbl_msg.configure(text="This is Update Page")
        
        def update_db():
            name=e_name.get()
            pwd=e_pass.get()
            email=e_email.get()
            mob=e_mob.get()
        
            con=sqlite3.connect(database="banking.sqlite")
            cur=con.cursor()
            cur.execute("update account set acn_name=?,acn_email=?,acn_mob=?,acn_pass=? where acn_no=?",(name,email,mob,pwd,acn))
            con.commit()
            con.close()
            messagebox.showinfo("Update","Details Updated")
            return
        
        con=sqlite3.connect(database="banking.sqlite")
        cur=con.cursor()
        cur.execute("select acn_pass,acn_email,acn_mob from account where acn_no=?",(acn,))
        acn_pass,acn_email,acn_mob=cur.fetchone()
        con.close()
        
        lbl_name=Label(ifrm,font=('Arial',20,'bold'),bg='pink',text="Name")
        lbl_name.place(relx=.3,rely=.1)

        e_name=Entry(ifrm,font=('Arial',20,'bold'),bd=5)
        e_name.place(relx=.45,rely=.1)
        e_name.insert(0,uname)
        e_name.focus()

        lbl_pass=Label(ifrm,font=('Arial',20,'bold'),bg='pink',text="Pass")
        lbl_pass.place(relx=.3,rely=.25)

        e_pass=Entry(ifrm,font=('Arial',20,'bold'),bd=5)
        e_pass.place(relx=.45,rely=.25)
        e_pass.insert(0,acn_pass)
        
        lbl_email=Label(ifrm,font=('Arial',20,'bold'),bg='pink',text="Email")
        lbl_email.place(relx=.3,rely=.4)

        e_email=Entry(ifrm,font=('Arial',20,'bold'),bd=5)
        e_email.place(relx=.45,rely=.4)
        e_email.insert(0,acn_email)
        
        lbl_mob=Label(ifrm,font=('Arial',20,'bold'),bg='pink',text="Mob")
        lbl_mob.place(relx=.3,rely=.55)

        e_mob=Entry(ifrm,font=('Arial',20,'bold'),bd=5)
        e_mob.place(relx=.45,rely=.55)
        e_mob.insert(0,acn_mob)
        
        update_btn=Button(ifrm,command=update_db,bg=win_btn_clr,font=('Arial',15,'bold'),bd=5,text="update")
        update_btn.place(relx=.4,rely=.7)
        
        
    
    logout_btn=Button(frm,bg=win_btn_clr,font=('Arial',20,'bold'),bd=5,text="logout",command=logout_click)
    logout_btn.place(relx=.9,rely=0)
    
    lbl_wel=Label(frm,font=('Arial',20,'bold'),bg='pink',text=f"Welcome:{uname}",fg='green')
    lbl_wel.place(relx=0,rely=0)
    
    lbl_msg=Label(frm,font=('Arial',25,'bold'),bg='pink',fg='blue',text="This is Home Page")
    lbl_msg.place(relx=.4,rely=.05)
    
    bal_btn=Button(frm,command=check_bal,font=('Arial',20,'bold'),bd=5,width=12,text="check balance",bg=win_btn_clr)
    bal_btn.place(relx=0,rely=.2)
    
    deposit_btn=Button(frm,command=deposit,font=('Arial',20,'bold'),width=12,bd=5,text="deposit",bg=win_btn_clr)
    deposit_btn.place(relx=0,rely=.35)
    
    withdraw_btn=Button(frm,command=withdraw,font=('Arial',20,'bold'),width=12,bd=5,text="withdraw",bg=win_btn_clr)
    withdraw_btn.place(relx=0,rely=.5)   
    
    update_btn=Button(frm,command=update,font=('Arial',20,'bold'),width=12,bd=5,text="update",bg=win_btn_clr)
    update_btn.place(relx=0,rely=.65)
    
    
home_screen()
win.mainloop()

