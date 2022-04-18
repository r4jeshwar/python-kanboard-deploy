#!/usr/bin/env python3


import subprocess as sp
import random
import bcrypt
import string

def system_update():

   sp.call(["sudo", "apt-get","update"])
   sp.call(["sudo", "apt", "upgrade", "-y"])

def install_apache_php():

    sp.call(["sudo", "apt", "install", "-y", "apache2", "libapache2-mod-php", "php-cli", "php-mbstring", "php-sqlite3", "php-opcache", "php-json", "php-mysql", "php-pgsql", "php-ldap", "php-gd", "php-xml"])
    sp.call(["sudo", "systemctl", "enable", "--now", "apache2.service"])


def install_maraidb():

    sp.call(["sudo", "apt", "install", "-y", "mariadb-server", "mariadb-client"])
    sp.call(["sudo", "systemctl", "enable", "--now", "mariadb.service"])
    sp.call(["sudo", "mysql_secure_installation"])

def install_kb():
    result_str = ''.join(random.choice(string.ascii_letters) for i in range(8))
    print (result_str)
    passwd = result_str
    salt = bcrypt.hashpw(passwd.encode('utf8'), bcrypt.gensalt())
    hashed = bcrypt.checkpw(passwd.encode('utf8'), salt)
    print(salt)
    password = str(salt)
    print(password)
    sp.call(["sudo", "sed", "-i", "s/'\$2y\$10\$GzDCeQl\/GdH\.pCZfz4fWdO3qmayutRCmxEIY9U9t1k9q9F89VNDCm'/"+password+"/g", "/var/www/html/kanboard/app/Schema/Sql/mysql.sql"])

    version = input("Enter the version: ")
    print(version)
    kbversion = "kanboard-"+version+"/data"
    filename = "v"+version+".tar.gz"
    url = "https://github.com/kanboard/kanboard/archive/"+filename
    print(url)
    sp.call(["wget", url ])
    sp.call(["tar", "xzvf", filename, "-C", "/var/www/html/"])
    sp.call(["sudo", "mv", "/var/www/html/kanboard-"+version, "/var/www/html/kanboard"])
    sp.call(["chown", "-R", "www-data:www-data", "/var/www/html/kanboard/data"])
    sp.call(["rm", filename])

    sp.call(["mysql", "-u", "root" , "-p", "-e", "CREATE DATABASE kanboard"])
    sp.call(["mysql", "-u", "root", "-p", "-e", "CREATE USER 'kanboarduser'@'localhost' IDENTIFIED BY 'rajeshwar';"])
    sp.call(["mysql", "-u", "root", "-p", "-e", "GRANT ALL PRIVILEGES ON kanboard.* TO 'kanboarduser'@'localhost' IDENTIFIED BY 'rajeshwar' WITH GRANT OPTION;"])
    sp.call(["mysql", "-u", "root", "-p", "-e", "FLUSH PRIVILEGES;"])
    sp.call(["sudo", "sed", "-i", "s/DB_DRIVER', 'sqlite'/DB_DRIVER', 'mysql'/g", "/var/www/html/kanboard/config.default.php"])
    sp.call(["sudo", "sed", "-i", "s/DB_USERNAME', 'root'/DB_USERNAME', 'kanboarduser'/g", "/var/www/html/kanboard/config.default.php"])
    sp.call(["sudo", "sed", "-i", "s/DB_PASSWORD', ''/DB_PASSWORD', 'rajeshwar'/g", "/var/www/html/kanboard/config.default.php"])
    
def restart_apache():
    
    sp.call(["sudo", "touch", "/etc/php/7.4/mods-available/php.ini"])
    f=open('/etc/php/7.4/mods-available/php.ini', "w")
    sp.call(["echo", "extension=php.so"],stdout=f)
    sp.call(["sudo", "systemctl", "restart", "apache2.service"])
    sp.call(["sudo", "systemctl", "restart", "mysqld.service"])

if __name__ == '__main__':
    system_update()
    install_apache_php()
    install_maraidb()
    install_kb()
    restart_apache()

