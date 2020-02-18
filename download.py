# -*- coding: utf-8 -*-
"""
Created on Mon Mar 26 11:37:15 2018

@author: Sejal
"""
import os
import sqlite3
import csv
import matplotlib.pyplot as plt
import numpy as np
import sys
import pandas as pd
from Tkinter import *
import Tkinter as tk
from tabulate import tabulate
#from bson import json_util  

def parse(url):
	try:
		parsed_url_components = url.split('//')
		sublevel_split = parsed_url_components[1].split('/', 1)
		domain = sublevel_split[0].replace("www.", "")
		return domain
	except IndexError:
		count=0


data_path = os.path.expanduser('~')+"\AppData\Local\Google\Chrome\User Data\Default"
files = os.listdir(data_path)
history_db = os.path.join(data_path, 'history')
c = sqlite3.connect(history_db)
cursor = c.cursor()
select_statement="SELECT   datetime(start_time / 1000000 + (strftime('%s', '1601-01-01')), 'unixepoch','localtime') as start_t, site_url, current_path,target_path, received_bytes,total_bytes,interrupt_reason,datetime(downloads.end_time/1000000 + (strftime('%s', '1601-01-01')), 'unixepoch','localtime') as end_t,opened,referrer,last_modified,http_method,tab_url,tab_referrer_url FROM downloads  order  by downloads.start_time desc ;"
cursor.execute(select_statement)
results = cursor.fetchall() #tuple
select_statement="select start_time ,site_url,current_path FROM downloads"
cursor.execute(select_statement)
results1 = cursor.fetchall() #tuple
temp1=results1[0][0]
download_dict=[] #dict
timeline_analyser_down=[]
for start_t, site_url, current_path,target_path,received_bytes, total_bytes,interrupt_reason,end_t,opened,referrer,last_modified,http_method,tab_url,tab_referrer_url in results:
    site_url=parse(site_url)
    temp = [start_t, site_url, current_path,target_path,received_bytes, total_bytes,interrupt_reason,end_t,opened,referrer,last_modified,http_method,tab_url,tab_referrer_url]
    download_dict.append(temp)
    temp = [start_t, site_url, current_path, total_bytes]
    timeline_analyser_down.append(temp)

column=["start_t", "site_url"," current_path","target_path","received_bytes", "total_bytes","interrupt_reason","end_t","opened","referrer","last_modified","http_method","tab_url","tab_referrer_url"]

sites_url_download={}
reload(sys)
sys.setdefaultencoding('utf-8')
for site_url in results:
	site_url = parse(unicode(site_url))
	if site_url in sites_url_download:
		sites_url_download[site_url] += 1
	else:
		sites_url_download[site_url] = 1
# create data
#print sites_url_download        
x =sites_url_download.keys()
y=sites_url_download.values()             
# use the scatter function
'''
plt.figure()
plt.bar(range(len(y)),y, align='edge')
plt.xticks(rotation=45)
plt.xticks(range(len(x)),x)
#plt.show()
plt.savefig('download.png', bbox_inches='tight')
'''
#path="C:\Users\Sejal\Desktop\project\download.csv"

csv_file  = open('download.csv', "wb")
writer = csv.writer(csv_file, delimiter='	', lineterminator='\r\n')            
writer.writerow(column)
writer.writerows(download_dict)
csv_file.close()    

'''
class Windows(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.screen = Frame(self, width=200, bg='white', height=500, relief='sunken', borderwidth=2)
        self.screen.pack(expand=True, fill='y', side='left', anchor='nw')

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
        
        reader = csv.reader("download.csv")
        sys.stdout=self
        for row in reader:
        	print(" ".join(row))

if __name__ == "__main__":

    app = Windows()
    app.title("Internet Forensics")
    app.mainloop()


'''

series = pd.Series(y,x)
pie = series.plot(kind="pie", figsize=(6,6), legend = False, use_index=False, subplots=True)
fig = pie[0].get_figure()
plt.show()
fig.savefig('downloads.png',bbox_inches='tight')


