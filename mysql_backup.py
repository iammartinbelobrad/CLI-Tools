#!/usr/bin/python

import sys, os, MySQLdb as mysql, datetime

# DATABASE SETTINGS --------------------------------------------------------------

HOST     = ""

USERNAME = ""

PASSWORD = ""

# --------------------------------------------------------------------------------

# PATH TO BACKUP FOLDER ----------------------------------------------------------

BACKUP_PATH = ""

# --------------------------------------------------------------------------------

db = mysql.connect(host=HOST, user=USERNAME, passwd=PASSWORD, db="mysql")

databases = db.cursor()
databases.execute("SHOW DATABASES")
databasesRowset = databases.fetchall()

date = datetime.date.today()

for row in databasesRowset:
    if row[0] != 'mysql' and row[0] != 'information_schema':
        filename = row[0]+'_'+str(date)
        sql_filename = filename+'.sql';
        tar_filename = filename+'.sql.gz';
        
        if os.path.isdir(BACKUP_PATH+'/'+row[0]) == False:
            os.popen('mkdir '+BACKUP_PATH+'/'+row[0])

        os.popen('mysqldump --opt -Q --user='+USERNAME+' --password='+PASSWORD+' --single-transaction '+row[0]+' | gzip -9 > '+BACKUP_PATH+'/'+row[0]+'/'+tar_filename)

# remove old backups then month
os.popen('find '+BACKUP_PATH+'/* -mtime +30 -exec rm {} \;')