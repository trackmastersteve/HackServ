# arm0.red bot

[![Version](https://img.shields.io/badge/version-0.6.9-red.svg)]() [![GitHub license](https://img.shields.io/github/license/trackmastersteve/bot.svg)](https://github.com/trackmastersteve/bot/tree/master/LICENSE) [![Python3](https://img.shields.io/badge/python-3.6-green.svg)]() [![GitHub issues](https://img.shields.io/github/issues/trackmastersteve/bot.svg)](https://github.com/trackmastersteve/bot/issues) [![GitHub stars](https://img.shields.io/github/stars/trackmastersteve/bot.svg)](https://github.com/trackmastersteve/bot/stargazers)  [![GitHub forks](https://img.shields.io/github/forks/trackmastersteve/bot.svg)](https://github.com/trackmastersteve/bot/network) 

Simple IRC bot/botnet PoC written in python 3. This bot is for educational purposes only!
Do **NOT** use this bot on a computer or network without written permission from the owner(s)!


This bot can connect to IRC over SSL and is compatible with Unrealircd's nospoof:PING.

### Installation:

The following packages are required. You'll need to install the following using the
package manager:

```sudo apt install python3 python3-pip nmap```

Then you can install the following using pip3:

```pip3 install requirements.txt```


### So far it responds to the following commands:

```.help``` (HELP menu)

```.uptime``` (shows bot uptime)

```.uname``` (get system info)

```.ip``` (get ip address of bot)

```.scan [ip] [comma,seperated,ports]``` (nmap port scanner)

```.msg [target] [message]``` (sends a msg to a user/channel)

```.notice [target] [message]``` (sends a notice to a user/channel) (**work in progress**)

```Hi [botnick]``` (responds to any user saying hello to it)

```bye [botnick]``` (tells bot to quit)

```.join [channel]``` (tells bot to join channel)

```.part [channel]``` (tells bot to part channel)

```.cycle [channel]``` (tells bot to part then join channel) (**work in progress**)

```.kick [channel] [nick] [reason]``` (tells bot to kick a user from a channel)

```.mode [target] [mode]``` (set mode on nick or channel)

```.nick [newnick]``` (sets a new botnick)

### TODO

- [ ] Send/Receive CTCP commands (so far it responds to **CTCP VERSION** only)

- [ ] Send/Receive DCC commands (CHAT and TRANSFER)

- [ ] Vuln Scan

- [ ] Auto Vuln / Port Scan on join

- [ ] Open reverse shell/meterpreter (**trying to figure out how to create secondary sockets for this**)

- [ ] Accept uploads from admin

- [ ] Send downloads to admin 

- [ ] Execute file/code

- [ ] Self update

- [x] Run in Background - (debugmode = False allows bot to run in the background)

- [ ] Persistence

- [ ] Better handling of disconnects etc. - (**a bug is preventing this**)

- [x] Better error handling

- [x] Better sigterm handling

- [ ] NickServ Identify (**a bug is preventing this**)

- [x] Connect over SSL 

- [x] Get ip address

- [x] Join and Part Channels

- [x] Help Menu

