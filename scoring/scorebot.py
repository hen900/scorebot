# coding: utf=8
from __future__ import division
import os
import sys
import time


class Vuln:

    def __init__(self, desc, val, boolean):
        self.desc = desc
        self.boolean = boolean
        self.val = val
    #returns the point value of a vuln
    def getValue(self):
        return self.val
    #returns the description of a vuln
    def getDescription(self):
        return self.desc
    #returns True if a vuln if fixed, false if it is not
    def isFixed(self):
        if os.system(self.boolean) == 0:
            return True
        else:
            return False


class Service:

    def __init__(self, name, port):
        self.port = port
        self.name = name
    #retusns the port a service runs on 
    def getPort(self):
        return self.port

    def getName(self):
        return self.name
    #checks if a service is up by checking if its port is open
    def isDown(self):
        if os.system('netstat -tulpn| grep \"\:' + str(self.port) + '\"')  == 0:
            return False
        return True


class User:

    def __init__(self, name):
        self.name = name

    def getName(self):
        return self.name
    #checks if users have proper functionality
    def works(self):
        if os.system(' [ -e /home/' + self.name + '/ ]') \
            + os.system(' [ "$(grep ' + self.name + ' /etc/passwd)" ]') \
            == 0:
            return True

        return False


def update():
    percent = str(round(points / totalPoints * 100, 1)) + '%'
    #autogenerates a score report with baked in html
    with open('/home/'+mainUser+'/Desktop/Score_Report.html', 'w') as f:
        f.write('<!DOCTYPE html> <html> <head> <meta name="viewport" content="width=device-width, initial-scale=1"> <style> * { box-sizing: border-box; } .column { float: left; padding: 10px; height: 1500px; } .left, .right { width: 25%; } .middle { width: 50%; } .row:after { content: ""; display: table; clear: both; }</style> </head> <body><div class="row"> <div class="column left" style="background-color:#0d60bf;"></div> <div class="row"> <div class="column middle" style="background-color:#fff;"><h1 style="text-align: center;"><span style="font-family: arial, helvetica, sans-serif;">Score Report</span></h1><h2 style="text-align: center;"><br /><span style="font-family: arial, helvetica, sans-serif;">'
                 + percent + ' completed</span></h2><p> </p>')
        f.write('<p><span style="font-family: arial, helvetica, sans-serif;"><strong>'
                 + str(penalties)
                + ' Points in Scoring Penalties</strong></span></p> <font color="red">'
                )
        for i in services:
            if i.isDown():
                f.write('<p><span style="font-size: 10pt;  font-family: arial, helvetica, sans-serif;">'
                         + i.getName()
                        + ' not functional &ndash 5 points</span></p>')
        for i in users:
            if not i.works():
                f.write('<p><span style="font-size: 10pt;  font-family: arial, helvetica, sans-serif;"> User '
                         + i.getName()
                        + ' not functional &ndash 5 points</span></p>')
        f.write('</font><p><span style="font-family: arial, helvetica, sans-serif;"><strong>'
                 + str(numFixedVulns) + ' out of ' + str(numVulns)
                + '  Vulnerabilities Fixed</strong></span></p>\n')
        for i in allVulns:
            if i.isFixed():
                f.write('<p><span style="font-size: 10pt; font-family: arial, helvetica, sans-serif;">'
                         + i.getDescription() + ' &ndash '
                        + str(i.getValue()) + ' points</span></p>')
        f.write('</div> <div class="row"> <div class="column right" style="background-color:#0d60bf;"></div> </body>'
                )
        f.write('<meta http-equiv="refresh" content="20">')
        f.write('<footer><h6>Henry Mackay</h6></footer>')


mainUser = 'analyst'
users = [User('analyst'), User('cyber')]
services = [Service('sshd', 22), Service('mysqld', 3306)]
allVulns = [
    Vuln('Forensics Question correct', 1, '[ "$(grep answer /home/'+ mainUser + '/Desktop/Forensics_1.txt)" ]'),
    Vuln('Removed unauthorized user ', 1,'! [ "$(grep user  /etc/passwd)" ]'),
    Vuln('Removed unauthorized admin ', 1,'! [ "$(grep sudo /etc/group | grep user)" ]'),
    Vuln('Secure Permissions set for shadow file', 5,'[ "$(stat -c "%a %n" /etc/shadow | grep 640)" ]'),
    Vuln('Secure hashing algorithm is used', 1,'[ "$(grep ENCRYPT_METHOD\ SHA512 /etc/login.defs)" ]'),
    Vuln('Failed logins are logged', 1,'[ "$(grep FAILLOG_ENAB /etc/login.defs | grep yes)" ]'),
    Vuln('Login retries set', 1,'[ "$(grep LOGIN_RETRIES /etc/login.defs | grep 3)" ]'),
    Vuln('Guest account is disabled', 1,'[ "$(grep guest /etc/lightdm/lightdm.conf | grep false)" ] '),
    Vuln('Firewall protection enabled', 1,'[ "$(ufw status | grep enable)" ] '),
    Vuln('Root login disabled', 1,'[ "$(grep PermitRootLogin /etc/ssh/sshd_config | grep No)" ]'),
    Vuln('Stricter memory defaults enabled', 1,'[ "$(grep shm /etc/fstab)" ]'),
    Vuln('Password required for sudo', 1,'! [ "$(grep NOPASSWD /etc/sudoers)" ]'),
    Vuln('Password policy enforced', 1,' [ "$( grep -E \'remember|minlen|ucredit|dcredit|ocredit|cracklib\' /etc/pam.d/common-password)" ] '),
    Vuln('Firefox blocks dangerous websites', 1,'[ "$(grep -r "safebrowsing.malware.enabled" /home/'+ mainUser + '/.mozilla/ | wc -l )" == "1" ] '),
    Vuln('Security updates automatically installed', 1,' [ "$(grep -r Unattended\-Upgrade\ \"1\" /etc/apt)" ] '),
    Vuln('Media files removed', 1, ' ! [ "$(find /home/ | grep mp3)" ]'),
    Vuln('Hacking tool removed', 1, ' [ "$(dpkg --list | grep nikto)" ]'),
    Vuln('Netcat listener disabled', 1,' ! [ "$(netstat -tulpn | grep  nc )" ] '),
    Vuln('Unauthorized website disabled', 1,'[ "$(netstat -tulpn | grep 8080)" ]'),
    Vuln('Dangerous banner removed ', 1,'! [ "$(grep poop /etc/issue.net)" ] '),
    Vuln('ASLR randomization enabled ', 1,' [ "$(grep kernel.randomize_va_space /etc/sysctl.conf | grep 2 )" ] '),
    Vuln('Martian packets are logged ', 1,' [ "$(grep net.ipv4.conf.all.log_martians /etc/sysctl.conf | grep 1)" ] '),
    Vuln('SYN cookies are enabled', 1,' [ "$(grep net.ipv4.tcp_syncookie /etc/sysctl.conf | grep 1)" ] '),
    Vuln('IPv6 is disabled', 1,'[ "$(grep net.ipv6.conf.all.disable_ipv6 /etc/sysctl.conf | grep 1)" ]'),
    Vuln('Spoofing protection enabled', 1,'[ "$(grep net.ipv4.conf.all.rp_filter /etc/sysctl.conf | grep 1 )" ]'),
    Vuln('Insecure password for root changed', 1,'[ "$(grep root /etc/shadow | grep 8yg)" ]'),
    Vuln('Bash updated', 1, '! [ "$(bash --version | grep 4.3)" ]'),
    Vuln('Firefox updated', 1, '! [ "$(sudo -u ' + mainUser+ ' firefox -v | grep 3)" ]'),
    ]


numVulns = len(allVulns)

while True:
    totalPoints = 0
    points = 0
    numFixedVulns = 0
    penalties = 0
    for i in services:
        if i.isDown():
            penalties = penalties + 5

    for i in users:
        if not i.works():
            penalties = penalties + 5
    for i in allVulns:
        totalPoints = totalPoints + i.getValue()
        if i.isFixed():
            numFixedVulns = numFixedVulns + 1
            points = points + i.getValue()

    points = points - penalties

    update()
    #delay between each scoring loop
    time.sleep(60)

			
