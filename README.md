# arm0.red bot

[![Version](https://img.shields.io/badge/version-0.7.5-red.svg)]() [![GitHub license](https://img.shields.io/github/license/trackmastersteve/bot.svg)](https://github.com/trackmastersteve/bot/tree/master/LICENSE) [![Python3](https://img.shields.io/badge/python-3.6-green.svg)]() [![GitHub issues](https://img.shields.io/github/issues/trackmastersteve/bot.svg)](https://github.com/trackmastersteve/bot/issues) [![GitHub stars](https://img.shields.io/github/stars/trackmastersteve/bot.svg)](https://github.com/trackmastersteve/bot/stargazers)  [![GitHub forks](https://img.shields.io/github/forks/trackmastersteve/bot.svg)](https://github.com/trackmastersteve/bot/network) 

Simple IRC bot/botnet PoC written in python 3. This bot is for educational purposes only!
Do **NOT** use this bot on a computer or network without written permission from the owner(s)!
This bot can connect to IRC over SSL and is compatible with Unrealircd's nospoof:PING.
Single python file for easy deployment. 

### Installation:

The following packages are required. You'll need to install the following using the
package manager:

```sudo apt install python3 python3-pip nmap```

Then you can install the following using pip3:

```pip3 install requirements.txt```

Then clone this project by running the following command:

```git clone https://github.com/trackmastersteve/bot.git```


### So far it responds to the following commands:

```.help``` (HELP menu)

```.uptime``` (shows bot uptime)

```.uname``` (get 1-line system info)

```.sysinfo``` (get formated system info)

```.osversion``` (get OS Version info)

```.linuxmemory``` (get memory stats from linux machine)

```.ip``` (get ip address of bot)

```.scan [ip] [comma,seperated,ports]``` (nmap port scanner)

```.msg [target] [message]``` (sends a msg to a user/channel)

```.ntc [target] [message]``` (sends a notice to a user/channel)

```Hi [botnick]``` (responds to any user saying hello to it)

```bye [botnick]``` (tells bot to quit)

```.join [channel]``` (tells bot to join channel)

```.part [channel]``` (tells bot to part channel)

```.pj [channel]``` (tells bot to part then join channel)

```.kick [channel] [nick] [reason]``` (tells bot to kick a user from a channel)

```.mode [target] [mode]``` (set mode on nick or channel)

```.nick [newnick]``` (sets a new botnick)

### TODO

- [ ] Send/Receive CTCP commands (so far it responds to **CTCP VERSION** only)

- [ ] Send/Receive DCC commands (CHAT and TRANSFER)

- [ ] Auto Vuln / Port Scan on join

- [ ] Accept uploads from admin

- [ ] Send downloads to admin 

- [ ] Execute file/code

- [ ] Self Replicating

- [ ] Proxy Scanner

- [ ] Self update

- [ ] Persistence

- [ ] Vuln Scan

- [ ] DoS/DDoS

- [ ] Open reverse shell/meterpreter (**my shell is already written. I just need to implement it!**)

- [x] Better handling of disconnects etc. - (**PING timeout is the only disconnect left to fix**) (in testing)

- [x] NickServ Identify (**a bug is preventing this**) (in testing)

- [x] Run in Background - (debugmode = False setting allows bot to run in the background)

- [x] Better error handling (still a few bugs to work out)

- [x] Better sigterm handling

- [x] Join and Part Channels

- [x] Connect over SSL 

- [x] Get ip address

- [x] Help Menu

