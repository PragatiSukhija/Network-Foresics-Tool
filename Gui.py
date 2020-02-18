# -*- coding: utf-8 -*-
"""
Created on Sat Mar 17 22:53:18 2018

@author: Goldy
"""
import Tkinter as tk   
from ScrolledText import ScrolledText 
from tkFileDialog import askopenfilename,asksaveasfilename 
import pymysql
import tkMessageBox
import pyshark
import tkFont as tkfont
from tabulate import tabulate
import os
from Tkinter import *
from PIL import ImageTk,Image  
import sys
import csv
#sys.path.append("C:\\Final Year Project\\Implementation")

def insert():
            global case_name
            case_name = entry.get()
            case_des = text.get("1.0","end-1c")
            
            #print(case_name)
            #print(case_des)
            conn=pymysql.connect(host="localhost",user="root",passwd="1234567890",db="poject")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO poject.case VALUES(default,%s,%s,now(),%s,%s,%s,%s,%s,%s)",(case_name,case_des,'','','','','',''))
            conn.commit()
            conn.close()
            popup_bonus()
            
            

def popup_bonus():
    win = tk.Toplevel()
    win.wm_title("Notification")
    win.wm_geometry("500x150+170+70")

    l = tk.Label(win, text="Case created successfully!",font=40)
    l.pack(side="top")
    b = tk.Button(win, text="Okay", command=win.destroy,font=40)
    b.pack(side="bottom")
    

class Windows(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, NewCase, PageTwo, WebPage, NetworkPage, EmailPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()
        
class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.grid()
        
        menubar = tk.Menu()
        #recentMenu = tk.Menu(filename,tearoff=0)
        filemenu = Menu(menubar, tearoff=0)
        recentMenu = tk.Menu(filemenu,tearoff=0)
        filemenu.add_cascade(label="Open Case",menu=recentMenu)

        filemenu.add_command(label="New Case", command=lambda: controller.show_frame("NewCase"))
        filemenu.add_command(label="Exit", command=self.quit)
        
    
        conn=pymysql.connect(host="localhost",user="root",passwd="1234567890",db="poject")
        cursor = conn.cursor()
        cursor.execute("SELECT case_name from poject.case")
        cases=cursor.fetchall()
        cursor.execute("SELECT count(*) from poject.case ")
        count=cursor.fetchone()[0]
        conn.commit()
        conn.close()
        
        for num in range(0,count):
            l=cases[num][0]
            recentMenu.add_command(label=l,command=lambda x=num:self.opencase(recentMenu,x))

        menubar.add_cascade(label="Case", menu=filemenu)
        
        
        helpmenu = Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Help Index", command=None)
        helpmenu.add_command(label="About...", command=None)
        menubar.add_cascade(label="Help", menu=helpmenu)
        
        
        aboutmenu = Menu(menubar,tearoff=0)
        aboutmenu.add_command(label="About",command=None)
        menubar.add_cascade(label="About", menu=aboutmenu)
    
        top = self.winfo_toplevel()
        top.configure(menu=menubar)
        
        self.label = tk.Label(self, text="Welcome..",bg='black',fg='white',font=100)
        self.label.pack(expand=True, fill='both')

    def opencase(self,menu,y):

        x= menu.entrycget(y,"label")
        sys.stdout = self
        self.screen = Frame(self, width=200, bg='white', height=500, relief='sunken', borderwidth=2)
        self.screen.pack(expand=True, fill='both', side='left', anchor='nw')
        self.xscrollbar = Scrollbar(self.screen, orient=HORIZONTAL)
        self.xscrollbar.pack(side=BOTTOM, fill=X)
        #Vertical (y) Scroll Bar
        self.yscrollbar = Scrollbar(self.screen)
        self.yscrollbar.pack(side=RIGHT, fill=Y)

        #Text Widget
        self.text = Text(self.screen, wrap=NONE,
                    xscrollcommand=self.xscrollbar.set,
                    yscrollcommand=self.yscrollbar.set)
        self.text['font'] = ('consolas', '12')
        self.text.grid(row=0,column=4)
        self.text.pack(expand=True, fill='both',side=RIGHT)
        #self.text.pack()

        #Configure the scrollbars
        self.xscrollbar.config(command=self.text.xview)
        self.yscrollbar.config(command=self.text.yview)

        conn=pymysql.connect(host="localhost",user="root",passwd="1234567890",db="poject")
        cursor = conn.cursor()
        cursor.execute("SELECT case_name,case_des,case_date,Filename,network_report,web_cookie_report,web_history_report,web_downloads_report,web_downloads_report from poject.case where case_name=%s",x)
        cases=cursor.fetchall()
        conn.commit()
        conn.close()
    
        print "\nCase Name:",cases[0][0]
        print "Case Description: ",cases[0][1]
        print "Case Registered on: ",cases[0][2]
        print "File Analyzed: ",cases[0][3]
        print "\n--------------------------Network Forensics Report Generated-------------------------------"
        print cases[0][4]
        print "\n--------------------------Web Forensics Report Generated-----------------------------------"
        print "\n-------------------------------------Cookie------------------------------------------------"
        print cases[0][5]
        print "\n--------------------------------------History-----------------------------------------------"
        print cases[0][6]
        
        print cases[0][7]
        
        print cases[0][8]  
        
    def write(self, txt):
        self.text.insert(INSERT, txt)


        
class NewCase(tk.Frame):
    
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="New Case",font=40)
        label.pack(side='left')
        
        sidebar = Frame(self, width=200, bg='white', height=500, relief='sunken', borderwidth=2)
        sidebar.pack(expand=True, fill='y', side='left', anchor='nw')
        
        label = tk.Label(sidebar, text="Case Name",font=40)
        label.pack(expand=True, fill='both')
        
        
        
        global entry
        entry= tk.Entry(sidebar)
        entry.pack(expand=True, fill='both')
        
        label = tk.Label(sidebar, text="Add Desciption",font=40)
        label.pack(expand=True, fill='both')
        
        global text
        text = ScrolledText(sidebar, undo=True,height=20)
        text['font'] = ('consolas', '12')
        text.pack(expand=True, fill='both')
        
        button = tk.Button(sidebar, text="Create",
                           command=lambda:insert(),font=40)
        button.pack(expand=True, fill='both')
        
        button = tk.Button(sidebar, text="Next>>",
                           command=lambda:controller.show_frame("PageTwo"),font=40)
    
        button.pack(side="right")


        
        
class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        #print case_name
        #data = cursor.fetchall()
            #id = cursor.execute("SELECT case_name from poject.case where case_name=self.case_name")
        label = tk.Label(self,text='')
        label.pack(side="top", fill="x", pady=10)
        
        
        sidebar = Frame(self, width=200, bg='white', height=500, relief='sunken', borderwidth=2)
        sidebar.pack(expand=True, fill='y', side='left', anchor='nw')
        
        screen = Frame(self, width=200, bg='white', height=500, relief='sunken', borderwidth=2)
        screen.pack(expand=True, fill='y', side='left', anchor='nw')
        
        label = tk.Label(sidebar,text='',width=20,bg="white")
        label.pack()
        
        button = tk.Button(sidebar, text="Web Forensics",
                           command=lambda: controller.show_frame("WebPage"),width=20)
        button.pack()
        
        label = tk.Label(sidebar,text='',width=20,bg="white")
        label.pack()
        
        button = tk.Button(sidebar, text="Network Forensics",
                           command=lambda: controller.show_frame("NetworkPage"),width=20)
        button.pack()
        
        label = tk.Label(sidebar,text='',width=20,bg="white")
        label.pack()
        button = tk.Button(sidebar, text="Email Forensics",
                           command=lambda: controller.show_frame("EmailPage"),width=20)
        button.pack()
        
        label = tk.Label(sidebar,text='',width=20,bg="white")
        label.pack()
        
        self.text = ScrolledText(screen, undo=True)
        self.text['font'] = ('consolas', '12')
        self.text.grid(row=0,column=4)
        self.text.pack(expand=True, fill='both',side=RIGHT)
    
        
class WebPage(tk.Frame):

   
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        global label1
        label1 = tk.Label(self,text="")
        label1.pack(side="top", fill="x", pady=10)
        
        sidebar = Frame(self, width=200, bg='white', height=500, relief='sunken', borderwidth=2)
        sidebar.pack(expand=True, fill='y', side='left', anchor='nw')
        
        self.screen = Frame(self, width=200, bg='white', height=500, relief='sunken', borderwidth=2)
        self.screen.pack(expand=True, fill='both', side='left', anchor='nw')
        
        self.xscrollbar = Scrollbar(self.screen, orient=HORIZONTAL)
        self.xscrollbar.pack(side=BOTTOM, fill=X)
        #Vertical (y) Scroll Bar
        self.yscrollbar = Scrollbar(self.screen)
        self.yscrollbar.pack(side=RIGHT, fill=Y)

        #Text Widget
        self.text = Text(self.screen, wrap=NONE,
                    xscrollcommand=self.xscrollbar.set,
                    yscrollcommand=self.yscrollbar.set)
        self.text['font'] = ('consolas', '12')
        self.text.grid(row=0,column=4)
        self.text.pack(expand=True, fill='both',side=RIGHT)
        #self.text.pack()

        #Configure the scrollbars
        self.xscrollbar.config(command=self.text.xview)
        self.yscrollbar.config(command=self.text.yview)
        #Run tkinter main lo
        
        label = tk.Label(sidebar,text='',width=20,bg="white")
        label.pack()
        button = tk.Button(sidebar, text="Cookie",command=lambda:self.cookie_script(),width=20)
        button.pack()

        label = tk.Label(sidebar,text='',width=20,bg="white")
        label.pack()
        live = tk.Button(sidebar, text="History",command=lambda:self.history_script(),width=20)
        live.pack()

        label = tk.Label(sidebar,text='',width=20,bg="white")
        label.pack()
        button = tk.Button(sidebar, text="Downloads",command=lambda:self.down_scripts(),width=20)
        button.pack()
        label = tk.Label(sidebar,text='',width=20,bg="white")
        label.pack()

        button = tk.Button(sidebar, text="TimeLine",command=lambda:self.timeline(),width=20)
        button.pack()
        label = tk.Label(sidebar,text='',width=20,bg="white")
        label.pack()
        
        button = tk.Button(sidebar, text="Clear Screen",command=lambda:self.clear(),width=20)
        button.pack()
        label = tk.Label(sidebar,text='',width=20,bg="white")
        label.pack()



        button = tk.Button(sidebar, text="Save Report",command=lambda:self.save_as(),width=20)
        button.pack()

        label = tk.Label(sidebar,text='',width=20,bg="white")
        label.pack()
        button = tk.Button(sidebar, text="Go Back <<",command=lambda:controller.show_frame("PageTwo"),width=20)
        button.pack()

    def cookie_script(self):
    
        sys.stdout = self
        import cookie1
        cookie1
        with open("cookies.csv") as file:
            reader = list(csv.reader(file))
            count=0
            r = 0
            print tabulate(reader,tablefmt="simple")
        self.que1("cookie")
            
    def history_script(self):
        
        sys.stdout = self
        import history
        history
        with open("history.csv") as file:
            reader = list(csv.reader(file))
            count=0
            r = 0
            print tabulate(reader,tablefmt="plain")
        self.que1("history")
          # PIL solution


    def down_scripts(self):
        
        sys.stdout = self

        import download
        download
        
        #with open("download.csv", "r") as f:
            #data = f.read().decode('latin-1')
            #data=list(data)
            #self.text.insert("1.0", data)
            #print tabulate(data,tablefmt="plain")
        '''
            reader=csv.reader(f)
            r = 0
            for col in reader:
                c = 0
                for row in col:
                    self.text.insert("1.0",row)
                    c += 1
                r += 1
            '''
            #self.text.insert("1.0", data)
        
        '''
        with open("download.csv", "r") as f:
            reader=csv.reader(f)
            list1=list(reader)
            list1=[x.encode('utf-8') for x in list1]
            print tabulate(reader,tablefmt="plain")
        self.que1("down")
        '''
        
    def save_as(self, whatever = None):
        #self.que()
        global filename
        self.filename = asksaveasfilename(defaultextension='.txt')
        f = open(self.filename, 'w')
        f.write(self.text.get('1.0', 'end'))
        f.close()
        tkMessageBox.showinfo('FYI', 'Log File Created')

    def timeline(self):
        

        import timeline_anlyser
        timeline_anlyser
        with open("timeline_analyser.csv") as f:
            red = list(csv.reader(f))
            count=0
            r = 0
            print tabulate(red,tablefmt="plain")
    
        sys.stdout = self

    def clear(self):
        self.text.delete("1.0","end-1c")

    def write(self, txt):
        self.text.insert(INSERT, txt)
        
    def que1(self,op):
        conn=pymysql.connect(host="localhost",user="root",passwd="1234567890",db="poject")
        cursor = conn.cursor()
        #file=self.filename
        rep=self.text.get('1.0', 'end')
        if op=="cookie":
            cursor.execute("SELECT @id := (SELECT caseid FROM poject.case ORDER BY caseid DESC LIMIT 1)")
            cursor.execute("UPDATE  poject.case set web_cookie_report=%s where caseid=@id", (rep))
            conn.commit()
            conn.close()
        if op=="history":
            cursor.execute("SELECT @id := (SELECT caseid FROM poject.case ORDER BY caseid DESC LIMIT 1)")
            cursor.execute("UPDATE  poject.case set web_history_report=%s where caseid=@id", (rep))
            conn.commit()
            conn.close()
        if op=="down":
            cursor.execute("SELECT @id := (SELECT caseid FROM poject.case ORDER BY caseid DESC LIMIT 1)")
            cursor.execute("UPDATE  poject.case set web_downloads_report=%s where caseid=@id", (rep))
            conn.commit()
            conn.close()
        return
        

class EmailPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        case_name = entry.get()
        label = tk.Label(self,text=case_name)
        label.pack(side="top", fill="x", pady=10)
    
        sidebar = Frame(self , width=200 , bg='white' , height=500, relief='sunken' , borderwidth=2)
        sidebar.pack(expand=True , fill='y' , side='left' , anchor='nw')
    
        screen = Frame(self, width=200, bg='white', height=500, relief='sunken', borderwidth=2)
        screen.pack(expand=True, fill='y', side='left', anchor='nw')
    
        self.text = ScrolledText(screen, undo=True)
        self.text['font'] = ('consolas', '12')
        self.text.grid(row=0,column=4)
        self.text.pack(expand=True, fill='both',side=RIGHT)
        
        label = tk.Label(sidebar,text='',width=20,bg="white")
        label.pack()
        button = tk.Button(sidebar, text="Start",command=lambda:self.run_script(),width=20)
        button.pack()

        label = tk.Label(sidebar,text='',width=20,bg="white")
        label.pack()
        button = tk.Button(sidebar, text="Go Back <<",command=lambda:controller.show_frame("PageTwo"),width=20)
        button.pack()


    def run_script(self):
        
        sys.stdout = self
        tkMessageBox.showinfo('FYI', 'Analyzing...Please Wait')
        import final_spam
        final_spam
        self.que()
    def write(self, txt):
        self.text.insert(INSERT, txt)

    def que(self):
        conn=pymysql.connect(host="localhost",user="root",passwd="1234567890",db="poject")
        cursor = conn.cursor()
        rep=self.text.get('1.0', 'end')
        cursor.execute("SELECT @id := (SELECT caseid FROM poject.case ORDER BY caseid DESC LIMIT 1)")
        cursor.execute("UPDATE  poject.case set email_report=%s where caseid=@id", (rep))
        conn.commit()
        conn.close()
        return

class NetworkPage(tk.Frame):
    
    filename = ''
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        global label1
        label1 = tk.Label(self,text="")
        label1.pack(side="top", fill="x", pady=10)
        
        sidebar = Frame(self, width=200, bg='white', height=500, relief='sunken', borderwidth=2)
        sidebar.pack(expand=True, fill='y', side='left', anchor='nw')
        
        screen = Frame(self, width=200, bg='white', height=500, relief='sunken', borderwidth=2)
        screen.pack(expand=True, fill='y', side='left', anchor='nw')
        '''
        self.text = ScrolledText(screen, undo=True)
        self.text['font'] = ('consolas', '12')
        self.text.grid(row=0,column=4)
        self.text.pack(expand=True, fill='both',side=RIGHT)
        '''

        #Horizontal (x) Scroll bar
        xscrollbar = Scrollbar(screen, orient=HORIZONTAL)
        xscrollbar.pack(side=BOTTOM, fill=X)
        #Vertical (y) Scroll Bar
        yscrollbar = Scrollbar(screen)
        yscrollbar.pack(side=RIGHT, fill=Y)

        #Text Widget
        self.text = Text(screen, wrap=NONE,
                    xscrollcommand=xscrollbar.set,
                    yscrollcommand=yscrollbar.set)
        self.text['font'] = ('consolas', '12')
        self.text.grid(row=0,column=4)
        self.text.pack(expand=True, fill='both',side=RIGHT)
        #self.text.pack()

        #Configure the scrollbars
        xscrollbar.config(command=self.text.xview)
        yscrollbar.config(command=self.text.yview)
        #Run tkinter main loop
        label = tk.Label(sidebar,text='',width=20,bg="white")
        label.pack()
        button = tk.Button(sidebar, text="Load Traffic",command=lambda:self.run_script(),width=20)
        button.pack()

        label = tk.Label(sidebar,text='',width=20,bg="white")
        label.pack()
        live = tk.Button(sidebar, text="Live Traffic",command=lambda:self.live_capture(),width=20)
        live.pack()

        label = tk.Label(sidebar,text='',width=20,bg="white")
        label.pack()
        button = tk.Button(sidebar, text="Clear Screen",command=lambda:self.clear(),width=20)
        button.pack()
        label = tk.Label(sidebar,text='',width=20,bg="white")
        label.pack()

        
        button = tk.Button(sidebar, text="Start Analysis",command=lambda:self.start_analysis(),width=20)
        button.pack()
        label = tk.Label(sidebar,text='',width=20,bg="white")
        label.pack()

        button = tk.Button(sidebar, text="Save Report",command=lambda:self.save_as(),width=20)
        button.pack()

        label = tk.Label(sidebar,text='',width=20,bg="white")
        label.pack()
        button = tk.Button(sidebar, text="Go Back <<",command=lambda:controller.show_frame("PageTwo"),width=20)
        button.pack()


    def que(self):
        conn=pymysql.connect(host="localhost",user="root",passwd="1234567890",db="poject")
        cursor = conn.cursor()
        file=self.filename
        rep=self.text.get('1.0', 'end')
        cursor.execute("SELECT @id := (SELECT caseid FROM poject.case ORDER BY caseid DESC LIMIT 1)")
        cursor.execute("UPDATE  poject.case set Filename=%s, network_report=%s where caseid=@id", (file,rep))
        conn.commit()
        conn.close()
        return

    def run_script(self):
        self.filename = askopenfilename()
        sys.stdout = self
        ## sys.stderr = self
        try:
            del(sys.modules[self.filename])
        except:
            pass
        import Pcap_Loader
        Pcap_Loader
        sys.stdout = sys.__stdout__		
        
    def write(self, txt):
        self.text.insert(INSERT, txt)


    def save_as(self, whatever = None):
        #self.que()
        global filename
        self.filename = asksaveasfilename(defaultextension='.txt')
        f = open(self.filename, 'w')
        f.write(self.text.get('1.0', 'end'))
        f.close()
        tkMessageBox.showinfo('FYI', 'Log File Created')


    def live_capture(self):
    	sys.stdout = self
        import Live_Traffic_Capturer
        Live_Traffic_Capturer
        #sys.stdout = sys.__stdout___
	
    def clear(self):
    	self.text.delete("1.0","end-1c")

    def start_analysis(self):
        
        sys.stdout = self
        tkMessageBox.showinfo('FYI', 'Analyzing...Please Wait')
        from Packet_Analyzer import analyzer
        analyzer(self.filename)
        self.que()
      


if __name__ == "__main__":

    app = Windows()
    app.title("Internet Forensics")
    app.mainloop()