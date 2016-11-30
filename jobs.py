import urllib
import urllib.request
from bs4 import BeautifulSoup
import os
import sqlite3

conn = sqlite3.connect('jobs2.sqlite')
cur = conn.cursor()

cur.executescript('''
DROP TABLE IF EXISTS Job;

CREATE TABLE Job (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    Name    TEXT,
    Org     TEXT,
    Location TEXT,
    Experience Text,
    Posted	TEXT,
    Link TEXT,
    Description TEXT

);

''')
numb=input("Please enter no of jobs you want to checkout: ")
i=1
k=1
file=open(os.path.expanduser("jobslisting.txt"),"wb")
while (1):
	flag=1
	url="http://jobsearch.monsterindia.com/jobresults/it-jobs.html?n="+str(k)
	page=urllib.request.urlopen(url)
	soup=BeautifulSoup(page, "html.parser")
	print ("crawling: ", url)
	for s in soup.find_all('div',{"class":"tpjob_d"}):
		title=s.find('span',{"itemprop":"title"})
		org=s.find('span',{"itemprop":"hiringOrganization"})
		location=s.find('span',{"itemprop":"jobLocation"})
		posted=s.find('div',{"class":"date"})
		exp=s.find('span',{"itemprop":"experienceRequirements"})
		link=s.find('a',{"class":"tpjob_lnk"}).get('href')
		description=s.find('div',{"class":"tpjob_desc"})
		if (description == None):
			continue
		if("\"" in description.text or "	" in description.text or "\\" in description.text):
			continue
		if("\"" in title.text or "	" in title.text or "\\" in title.text):
			continue
		if("\"" in org.text or "	" in org.text or "\\" in org.text):
			continue
		if(exp!=None):
			experience=str(exp.text)
		else:
			experience=""
		if(posted!=None):
			posted=str(posted.text)
		else:
			posted=""
		file.write(bytes(str(i)+": "+title.text + "\n", encoding="ascii", errors='ignore'))
		file.write(bytes(org.text + "\n", encoding="ascii", errors='ignore'))
		file.write(bytes(location.text+" " + experience +"\n", encoding="ascii", errors='ignore'))
		file.write(bytes(posted + "\n", encoding="ascii", errors='ignore'))
		file.write(bytes("\n\n\n\n\n", encoding="ascii", errors='ignore'))
		"""if(experience!=None):
			print (experience.text)
		print (title.text, "\n")
		print (org.text, "\n")
		print (location.text+ "\n")
		print (posted.text, "\n")
		print ("\n\n\n\n\n")"""
		if title is None or org is None or location is None or description is None:
			continue
		cur.execute('''INSERT OR IGNORE INTO Job (Name, Org, Location, Experience, Posted, Link, Description) VALUES ( ?, ?, ?, ?, ?, ?, ? )''', ( title.text, org.text, location.text, experience, posted, link, description.text ) )
		i=i+1
		if(i>int(numb)):
			flag=0;
			break
	conn.commit()
	k=k+1
	if(flag==0):
		break

print("\n\n Run dump.py to proceed further")

	