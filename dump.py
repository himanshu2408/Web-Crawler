import sqlite3
import json
import codecs

conn = sqlite3.connect('jobs2.sqlite')
cur = conn.cursor()

cur.execute('SELECT * FROM Job')
fhand = codecs.open('job.js','w', "utf-8")
fhand.write("{ \"myData\": [\n")
count = 0
for row in cur:
	title=row[1]
	org=row[2]
	location=row[3]
	exp=row[4]
	posted=row[5]
	link=row[6]
	description=row[7]
	description=description[:160]
	try :
		count = count + 1
		if count > 1 : fhand.write(",\n")
		output = "{\"title\":\""+title+"\",\"org\":\""+org+"\",\"location\":\""+location+"\",\"exp\":\""+exp+"\",\"posted\":\""+posted+"\",\"link\":\""+link+"\",\"description\":\""+description+"\"}"
		fhand.write(output)
	except:
		continue
fhand.write("\n]}\n")
cur.close()
fhand.close()
print ("\nHurray!!! Please check job.js and open jobs.html")