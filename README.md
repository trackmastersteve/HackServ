# arm0.red bot

[![Version](https://img.shields.io/badge/version-0.4.9-red.svg)]() [![GitHub license](https://img.shields.io/github/license/trackmastersteve/bot.svg)](https://github.com/trackmastersteve/bot/tree/master/LICENSE) [![Python3](https://img.shields.io/badge/python-3.6-green.svg)]() [![GitHub issues](https://img.shields.io/github/issues/trackmastersteve/bot.svg)](https://github.com/trackmastersteve/bot/issues) [![GitHub stars](https://img.shields.io/github/stars/trackmastersteve/bot.svg)](https://github.com/trackmastersteve/bot/stargazers)  [![GitHub forks](https://img.shields.io/github/forks/trackmastersteve/bot.svg)](https://github.com/trackmastersteve/bot/network) 

Simple IRC bot PoC written in python. This bot is for educational purposes only!
Do **NOT** use this bot on a computer or network without written permission from the owner(s)!


This bot can connect to IRC over SSL and is compatible with Unrealircd's nospoof:PING.

### Installation:

The following packages are required. You'll need to install the following using the
package manager:

```sudo apt install python3 python3-pip nmap```

Then you can install the following using pip3:

```pip3 install requirements.txt```


### So far it responds to the following commands:

```.help``` (HELP menu) (***work in progress**)

```.uptime``` (shows bot uptime)

```.uname``` (get system info)

```.ip``` (get ip address of bot)

```.scan [ip] [comma,seperated,ports]``` (nmap port scanner)

```.msg [target] [message]``` (sends a msg to a user/channel)

```.notice [target] [message]``` (sends a notice to a user/channel) (**work in progress**)

```Hello [botnick]``` (responds to any user saying hello to it)

```bye [botnick]``` (tells bot to quit)

```.join [channel]``` (tells bot to join channel)

```.part [channel]``` (tells bot to part channel)

```.cycle [channel]``` (tells bot to part then join channel) (**work in progress**)

```.kick [channel] [nick] [reason]``` (tells bot to kick a user from a channel)

```.mode [target] [mode]``` (set mode on nick or channel)

```.nick [newnick]``` (sets a new botnick) (**work in progress**)

### TODO

- [ ] Help Menu

- [ ] send/receive CTCP commands

- [ ] send/receive DCC commands (CHAT and TRANSFER)

- [ ] Vuln Scan

- [ ] Auto Vuln / Port Scan on join

- [ ] open reverse shell/meterpreter

- [ ] Accept uploads from admin

- [ ] Send downloads to admin 

- [ ] Execute file/code

- [ ] Self update

- [x] Run in Background - (almost done)

- [ ] Persistence

- [ ] Better handling of disconnects etc.

- [x] Better error handling (:No such nick/channel)

- [x] Better sigterm handling

- [ ] NickServ Identify

- [x] connect over SSL 

- [x] get ip address

- [x] join and part channels

