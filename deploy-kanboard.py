#!/usr/bin/env python3


import subprocess as sp

from seccomp import * 


def setup_seccomp():

    # create a filter object with a default KILL action
    f = SyscallFilter(defaction=KILL)

    '''Arguments:
        defaction - the default filter action'''

    # add syscall filter rules to allow certain syscalls
    f.add_rule(ALLOW, "wait4")
    f.add_rule(ALLOW, "clone")
    f.add_rule(ALLOW, "read")
    f.add_rule(ALLOW, "stat")
    f.add_rule(ALLOW, "close")
    f.add_rule(ALLOW, "pipe2")
    f.add_rule(ALLOW, "getdents64")
    f.add_rule(ALLOW, "openat")
    f.add_rule(ALLOW, "fstat")
    f.add_rule(ALLOW, "write")
    f.add_rule(ALLOW, "lseek")
    f.add_rule(ALLOW, "rt_sigaction")
    f.add_rule(ALLOW, "ioctl")
    f.add_rule(ALLOW, "brk")
    f.add_rule(ALLOW, "mmap")
    f.add_rule(ALLOW, "gettid")
    f.add_rule(ALLOW, "dup")
    f.add_rule(ALLOW, "fcntl")
    f.add_rule(ALLOW, "sysinfo")
    f.add_rule(ALLOW, "sigaltstack")
    f.add_rule(ALLOW, "lstat")
    f.add_rule(ALLOW, "geteuid")
    f.add_rule(ALLOW, "getcwd")
    f.add_rule(ALLOW, "readlink")
    f.add_rule(ALLOW, "getuid")
    f.add_rule(ALLOW, "getgid")
    f.add_rule(ALLOW, "getegid")
    f.add_rule(ALLOW, "mprotect")
    f.add_rule(ALLOW, "munmap")
    f.add_rule(ALLOW, "rt_sigprocmask")
    f.add_rule(ALLOW, "pread64")
    f.add_rule(ALLOW, "access")
    f.add_rule(ALLOW, "execve")
    f.add_rule(ALLOW, "arch_prctl")
    f.add_rule(ALLOW, "futex")
    f.add_rule(ALLOW, "set_tid_address")
    f.add_rule(ALLOW, "set_robust_list")
    f.add_rule(ALLOW, "prlimit64")
    f.add_rule(ALLOW, "getrandom")
    

    # load the filter into the kernel
    f.load()
    print(f'Seccomp enabled...')

setup_seccomp()

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
