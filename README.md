# arm0.red bot

[![Version](https://img.shields.io/badge/version-0.9.5-red.svg)]() [![GitHub license](https://img.shields.io/github/license/trackmastersteve/bot.svg)](https://github.com/trackmastersteve/bot/tree/master/LICENSE) [![Python3](https://img.shields.io/badge/python-3.6-green.svg)]() [![GitHub issues](https://img.shields.io/github/issues/trackmastersteve/bot.svg)](https://github.com/trackmastersteve/bot/issues) [![GitHub stars](https://img.shields.io/github/stars/trackmastersteve/bot.svg)](https://github.com/trackmastersteve/bot/stargazers)  [![GitHub forks](https://img.shields.io/github/forks/trackmastersteve/bot.svg)](https://github.com/trackmastersteve/bot/network) 

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

```.username``` (shows username of machine bot is running on)

```.uptime``` (shows bot uptime)

```.uname``` (get 1-line system info)

```.sysinfo``` (get formated system info)

```.osversion``` (get OS Version info)

```.memory``` (get memory stats from linux machine)

```.ip``` (get ip address of bot)

```.macaddress``` (get mac address info)

```.rsh [target] [port]``` (reverse shell to target)

```.cmd [shell command]``` (run shell command on host)

```.fsdl``` (run file server to download files from)

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

```.raw [command]``` (sends a raw command to the server)

```.dl [url] [file]``` (downloads [url] and saves as [file])

```.run [file]``` (execute a file)

```.upgrade``` (upgrades the bot.py file)

### TODO

- [ ] Send/Receive CTCP commands (so far it responds to **CTCP VERSION** only)

- [ ] Send/Receive DCC commands (CHAT and TRANSFER)

- [ ] Auto Vuln/Port/Proxy Scan on join

- [ ] Accept uploads from admin (File Server)

- [ ] Send downloads to admin (File Server) (**testing**)

- [x] Execute file/code

- [ ] Self Replicating

- [ ] Proxy Scanner

- [x] Self update (**testing**)

- [ ] Persistence

- [ ] File Server (**testing**)

- [ ] Key Logger

- [ ] Vuln Scan

- [ ] DoS/DDoS

- [x] Open reverse shell/meterpreter

- [x] Run in Background - ('debugmode = False' setting allows bot to run in the background)

- [x] Better error handling (still a few bugs to work out)

- [x] Better handling of disconnects etc.

- [x] Run single shell commands

- [x] Better sigterm handling

- [x] Join and Part Channels

- [x] NickServ Identify

- [x] SASL Auth Support

- [x] Connect over SSL 

- [x] Get ip address

- [x] Help Menu

