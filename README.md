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


### Installation
Run the install.sh file after completeting the scoring booleans. The file will compile scoring.py and create an init job.
