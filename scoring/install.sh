#!/bin/bash
mkdir /usr/bin/scorebot
cp scorebot /etc/init.d/
update-rc.d scorebot defaults
apt update 
apt install  python-pip
pip install cython==0.25
cython scorebot.py --embed
gcc  -I/usr/include/python2.7/ scorebot.c -lpython2.7 -o /usr/bin/scorebot/scorebot



	
