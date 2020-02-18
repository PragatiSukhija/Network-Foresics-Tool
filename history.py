import os
import sqlite3
import operator
from collections import OrderedDict
import matplotlib.pyplot as plt
import csv
import pandas as pd
import datetime
import time
def parse(url):
	try:
		parsed_url_components = url.split('//')
		sublevel_split = parsed_url_components[1].split('/', 1)
		domain = sublevel_split[0].replace("www.", "")
		return domain
	except IndexError:
		print "URL format error!"

def analyze(results):

	prompt = raw_input("[.] Type <c> to print or <p> to plot\n[>] ")

	if prompt == "c":
		for site, count in sites_count_sorted.items():
			print site, count
	elif prompt == "p":
		plt.bar(range(len(results)), results.values(), align='edge')
		plt.xticks(rotation=30)
		plt.xticks(range(len(results)), results.keys())
		plt.show()
	else:
		print "[.] Uh?"
		quit()

def convert_date_to_timestamp(p):
    year=""
    month=""
    day=""
    hr=""
    min1=""
    sec1=""
    counter=0
    for i in p:
        if i!='-' and i!=' ' and i!=':':
           if counter==0:
               year+=i
           if counter==1:
               month+=i
           if counter==2:
               day+=i
           if counter==3:
               hr+=i
           if counter==4:
              min1+=i
           if counter==5:
              sec1+=i
        else:
            counter+=1
    year=int(year)
    month=int(month)
    day=int(day)
    hr=int(hr)
    min1=int(min1)
    sec1=int(sec1)
    #print year,month,day,hr,min1,sec1        
    date = datetime.datetime(year, month, day,hr,min1,sec1,0)
    #date = int(time.mktime(yesterday_beginning.timetuple()))
    return date          




#path to user's history database (Chrome)
data_path = os.path.expanduser('~')+"\AppData\Local\Google\Chrome\User Data\Default"
files = os.listdir(data_path)
history_db = os.path.join(data_path, 'history')

#querying the db
c = sqlite3.connect(history_db)
cursor = c.cursor()

select_statement = "SELECT urls.url, urls.visit_count,datetime(last_visit_time / 1000000 + (strftime('%s', '1601-01-01')), 'unixepoch','localtime') as last_v_t FROM urls, visits WHERE urls.id = visits.url;"
cursor.execute(select_statement)
results = cursor.fetchall() #tuple
#print results
select_statement = "PRAGMA table_info(urls);"
cursor.execute(select_statement)
results1 = cursor.fetchall() #tupleyp
sites_count = {} #dict makes iterations easier :D


for url, count,last_v_time in results:
    l_ts=convert_date_to_timestamp(list(last_v_time))
    url = parse(url)
    if url in sites_count:
        sites_count[url][0]+=1
        if convert_date_to_timestamp(list(sites_count[url][1])) < l_ts:
            sites_count[url][1]=last_v_time 
    else:
        temp=[]
        temp.append(1)
        temp.append(last_v_time)
        sites_count[url]=temp
sites_count_sorted = OrderedDict(sorted(sites_count.items(),key=operator.itemgetter(1), reverse=True))
#print sites_count_sorted
dictlist=[]
yesterday = datetime.datetime.now() - datetime.timedelta(weeks = 4)
yesterday_beginning = unicode(datetime.datetime(yesterday.year, yesterday.month, yesterday.day,0,0,0,0))

for key, value in sites_count_sorted.iteritems():
  
    c=value[0]
    f=value[1]
    temp = [key,c,f]
    dictlist.append(temp)
path="C:\Users\Sejal\Desktop\project\history.csv"
csv_file  = open('history.csv', "wb")
writer = csv.writer(csv_file, delimiter=',', lineterminator='\r\n')            
writer.writerows(dictlist)
csv_file.close()

##count = [elem[0] for elem in sites_count_sorted.values()]
#count = [elem[1] for elem in dictlist]
#keys= [elem[0] for elem in dictlist]
'''
plt.figure()
plt.bar(range(len(sites_count_sorted)),count, align='edge')
plt.xticks(rotation=45)
plt.xticks(range(len(sites_count_sorted)), sites_count_sorted.keys())
plt.savefig('history.png', bbox_inches='tight')
'''
#
#series = pd.Series(count,keys, name='series')
##series.plot.pie(figsize=(6, 6))
#pie = series.plot(kind="pie", figsize=(6,6), legend = False, use_index=False, subplots=True,explode=list()
#fig = pie[0].get_figure()
#fig.savefig("myplot.pdf",bbox_inches='tight',dpi=100)



