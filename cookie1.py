# -*- coding: utf-8 -*-
"""
Created on Mon Mar 19 22:30:08 2018

@author: Sejal
"""

import os
import sqlite3
import csv


# Function to get rid of padding
def clean(x): 
    return x[:-x[-1]].decode('utf8')

def decrypt(x):
    # replace with your encrypted_value from sqlite3
    encrypted_value = x

# Trim off the 'v10' that Chrome/ium prepends
    encrypted_value = encrypted_value[3:]

# Default values used by both Chrome and Chromium in OSX and Linux
    salt = b'saltysalt'
    iv = b' ' * 16
    length = 16
    iterations = 1003
    my_pass = "ilovebits"
    key = PBKDF2(my_pass, salt, length, iterations)
    cipher = AES.new(key, AES.MODE_CBC, IV=iv)
    decrypted = cipher.decrypt(encrypted_value)
    return clean(decrypted)




data_path = os.path.expanduser('~')+"\AppData\Local\Google\Chrome\User Data\Default"
files = os.listdir(data_path)
path="C:\Users\Sejal\Desktop\project\cookies.csv"
cookies_db = os.path.join(data_path, 'Cookies')
csv_file  = open('cookies.csv', "wb")
writer = csv.writer(csv_file, delimiter=',', lineterminator='\r\n')            
def csv_write_column(column,path):
    writer.writerow(column)
    
#querying the db
c = sqlite3.connect(cookies_db)
cursor = c.cursor()
select_statement = "PRAGMA table_info(cookies)"
cursor.execute(select_statement)
results1 = cursor.fetchall() #tuple
results1=["creation_utc","host_key","name","path","expires_utc","is_secure","is_httponly","last_access_utc","has_expires","is_persistent","priority"]
csv_write_column(results1,path)


select_statement="select datetime(creation_utc / 1000000 + (strftime('%s', '1601-01-01')), 'unixepoch','localtime'),host_key,name,path,datetime(expires_utc/ 1000000 + (strftime('%s', '1601-01-01')), 'unixepoch','localtime'),is_secure,is_httponly,datetime(last_access_utc / 1000000 + (strftime('%s', '1601-01-01')), 'unixepoch','localtime'),has_expires,is_persistent,priority  from cookies order by last_access_utc  ;"
cursor.execute(select_statement)
results1 = cursor.fetchall() #list
cookie_dict=[] #dict
timeline_analyser_cookie=[]
for creation_utc,host_key,name,path,expires_utc,is_secure,is_httponly,last_access_utc,has_expires,is_persistent,priority in results1:
    if is_secure==0:
       is_secure=""
   # creation_utc=datetime(creation_utc / 1000000 + (strftime('%s', '1601-01-01'))
    temp = [creation_utc,host_key,name,path,expires_utc,is_secure,is_httponly,last_access_utc,has_expires,is_persistent,priority]
    cookie_dict.append(temp)
    temp=[creation_utc,host_key,name,path]
    timeline_analyser_cookie.append(temp)
    

writer.writerows(cookie_dict)

csv_file.close()


