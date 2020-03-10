# scorebot.py
scorebot.py runs booleans provided by the user every minute to create an html score report. Scores are based on solving vulnerabilites and service uptime.
### Creating Services and Users
The mainUser variable is set to whichever user is the primary login in a given scenario. The score report will be created in the mainUser's home directory. Other authorized users should be added to the users array as User objects. The scorebot will check for user functionality and deduct points for deleting authorized users. The following user array defines two users: the mainUser and "cyber"
```
mainUser = 'analyst'
users = [User(mainUser), User('cyber')]
```
Services are defined in the services array and should be created with a process name and port as arguments. The scorebot will check that authorized services are listening on the correct port. SSHD and mysql are defined in the follwoing services array.

```
services = [Service('sshd', 22), Service('mysqld', 3306)]
```
### Creating Vulnerabilities
Vulnerabilites are based on booleans to be run on the host system. ll Vuln objects should be created in the allVulns array. A vulnerability has the following fields. 
```
Vuln('Text_to_be_displayed when_vulnerability_is_fixed',point_value, 'scoring_boolean')
```
Scoring booleans are placed in between brackets and run in the command line. Some examples of scoring booleans:
```
 Vuln('Secure Permissions set for shadow file', 5,'[ "$(stat -c "%a %n" /etc/shadow | grep 640)" ]'),
 Vuln('Secure hashing algorithm is used', 1,'[ "$(grep ENCRYPT_METHOD\ SHA512 /etc/login.defs)" ]'),
 Vuln('Failed logins are logged', 1,'[ "$(grep FAILLOG_ENAB /etc/login.defs | grep yes)" ]')
```
### Installation
Run the install.sh file after completeting the scoring booleans. The file will compile scoring.py and create an init job.
