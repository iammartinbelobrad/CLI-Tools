#!/usr/bin/python

import sys, os, getpass, _mysql

print """
##############################################
#   Vytvoreni hostingu s FTP a MYSQL uctem   #
##############################################

"""

# PATHS --------------------------------------------------------------------------

HOSTING_HOME   = "/var/www/external"
UID            = 33
GID            = 33
CHMOD          = 0775

MYSQL_HOST     = "localhost"
MYSQL_USERNAME = "root"
MYSQL_PASSWORD = ""
MYSQL_DB       = "proftpd"

# connect to mysql --------------------------------------------------------------

db = _mysql.connect(MYSQL_HOST, MYSQL_USERNAME, MYSQL_PASSWORD, MYSQL_DB);

# ask user first ---------------------------------------------------------------

DOMAIN     = raw_input('Zadejte nazev domeny (bez www): ')
CREATE_FTP = raw_input('Chcete vytvorit FTP ucet? (y,n): ');

if (CREATE_FTP.lower() == 'y'):
    FTP_USERNAME = raw_input("Zadejte nazev FTP uctu: ");
    
    while True:
        FTP_PASSWORD       = getpass.getpass("Zadejte heslo k FTP uctu: ");
        FTP_PASSWORD_RETRY = getpass.getpass("Zadejte heslo k FTP uctu pro kontrolu: ");

	if (FTP_PASSWORD != FTP_PASSWORD_RETRY):
	    print "CHYBA: Heslo nesouhlasi, zkuste to prosim znovu"
	    print ""
	else:
	    break

CREATE_MYSQL = raw_input('Chcete vytvorit MySQL databazi? (y,n): ');

if (CREATE_MYSQL.lower() == 'y'):
    MYSQL_NEWDB       = raw_input('Zadejte nazev databaze a uzivatele: ');
    
    while True:
        MYSQL_NEWPASSWORD       = getpass.getpass('Zadejte heslo k databazi: ');
        MYSQL_NEWPASSWORD_RETRY = getpass.getpass('Zadejte heslo k databazi znovu: ');
        
        if (MYSQL_NEWPASSWORD != MYSQL_NEWPASSWORD_RETRY):
    	    print "CHYBA: Heslo hesouhlasi, zkuste to prosim znovu"
    	    print ""
    	else:
    	    break

# create domain folder ---------------------------------------------------------

DOMAIN_PARTS = DOMAIN.split('.')
DOMAIN_PARTS.reverse()

DOMAIN_PATH = HOSTING_HOME;
for domain_part in DOMAIN_PARTS:
    DOMAIN_PATH += '/'+ domain_part
    # create folder
    try :
        os.mkdir(DOMAIN_PATH)
        os.chown(DOMAIN_PATH, UID, GID)
	os.chmod(DOMAIN_PATH, CHMOD)
    except OSError:
        pass

# create www and nonwww folder
WWW_DOMAIN_PATH = DOMAIN_PATH+ '/www'
NONWWW_DOMAIN_PATH = DOMAIN_PATH+ '/_'

os.mkdir(WWW_DOMAIN_PATH)
os.chown(WWW_DOMAIN_PATH, UID, GID)
os.chmod(WWW_DOMAIN_PATH, CHMOD)

os.symlink(WWW_DOMAIN_PATH, NONWWW_DOMAIN_PATH)
os.chown(NONWWW_DOMAIN_PATH, UID, GID)
os.chmod(NONWWW_DOMAIN_PATH, CHMOD)

# create FTP account ----------------------------------------------------------------

if (CREATE_FTP.lower() == 'y'):
    db.query("INSERT INTO ftp(id,allowed,login,pass,dir,last_access) VALUES(null,'y','"+ FTP_USERNAME+ "', '"+ FTP_PASSWORD+ "', '"+ WWW_DOMAIN_PATH+ "',null)");

# create MySQL database -------------------------------------------------------------

if (CREATE_MYSQL.lower() == 'y'):
    db.query("CREATE DATABASE "+ MYSQL_NEWDB);
    db.query("GRANT ALL PRIVILEGES ON "+ MYSQL_NEWDB+ ".* TO '"+ MYSQL_NEWDB+ "'@'localhost' IDENTIFIED BY '"+ MYSQL_NEWPASSWORD+ "'");

# results ---------------------------------------------------------------------------

print 'OK'

print "Domena: "+ DOMAIN
print "Cesta k hostingu: "+ DOMAIN_PATH

if (CREATE_FTP.lower() == 'y'):
    print ""
    print "FTP"
    print "Server: onyx.slam.cz"
    print "Uzivatel: "+ FTP_USERNAME
    print "Heslo: "+ FTP_PASSWORD
    
if (CREATE_MYSQL.lower() == 'y'):
    print ""
    print "MySQL"
    print "PhpMyAdmin: http://phpmyadmin.slam.cz"
    print "Server: localhost"
    print "Uzivatel: "+ MYSQL_NEWDB
    print "Heslo: "+ MYSQL_NEWPASSWORD
    print "Databaze: "+ MYSQL_NEWDB

