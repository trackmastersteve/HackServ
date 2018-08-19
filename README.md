# bot
Simple IRC bot written in python. This bot is for educational purposes only!
Do NOT use this bot on a computer or network without written permission from the owner!


This bot can connect over SSL and is compatible with Unrealircd's nospoof:PING.

# So far it responds to the following commands:

```.uptime``` (shows bot uptime)

```.uname``` (get system info)

```.ip``` (get ip address of bot)

```.scan [ip] [port]``` (nmap port scanner)

```.tell [target] [message]``` (sends a msg to a user/channel)

```Hello [botnick]``` (responds to user saying hello to it)

```bye [botnick]``` (tells bot to quit)

```.join [channel]``` (tells bot to join channel)

```.part [channel]``` (tells bot to part channel)



# TODO

Help Menu

send/receive CTCP commands

send/receive DCC commands

Vuln Scan

Auto Vuln / Port Scan on join

open reverse shell/meterpreter

Accept uploads from admin

Send downloads to admin

Run file/code

Self update

Run in Background

Persistence

Better sigterm handling

~~NickServ Identify~~

~~connect over SSL~~ 

~~get ip address~~ 

~~join and part channels~~

