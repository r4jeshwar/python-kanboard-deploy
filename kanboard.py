#!/usr/bin/env python3


import subprocess as sp

def system_update():

 try:
   sp.call(["sudo", "apt-get","update"])
   sp.call(["sudo", "apt", "upgrade", "-y"])
 except exception:
   print (a)

def apache_php():

   # sp.call(["sudo", "apache2", "mariadb-server", "php", "libapache2-mod-php", "php-common", "php-curl", "php-intl", "php-mbstring", "php-xmlrpc", "php-mysql", "php-gd", "php-pgsql", "php-xml", "php-cli", "php-zip"])   
    sp.call(["sudo", "apt", "install", "-y", "apache2", "libapache2-mod-php", "php-cli", "php-mbstring", "php-sqlite3", "php-opcache", "php-json", "php-mysql", "php-pgsql", "php-ldap", "php-gd", "php-xml"])
    sp.call(["sudo", "systemctl", "enable", "--now", "apache2.service"])


def install_maraidb():

    sp.call(["sudo", "apt", "install", "-y", "mariadb-server", "mariadb-client"])
    sp.call(["sudo", "systemctl", "enable", "--now", "mariadb.service"])
    sp.call(["sudo", "mysql_secure_installation"])

def install_kb():

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
    sp.call(["sudo", "cd", "/etc/php/7.4/mods-available"])
    sp.call(["sudo", "touch", "php.ini"])
    sp.call(["sudo", "echo", "extension=php.so", ">", "php.ini"])
    sp.call(["sudo", "cd"])
    sp.call(["sudo", "systemctl", "restart", "apache2.service"])

if __name__ == '__main__':
    system_update()
    apache_php()
    install_maraidb()
    install_kb()

