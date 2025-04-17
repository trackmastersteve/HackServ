# HackServ IRC Bot

[![Version](https://img.shields.io/badge/version-1.3.3-red.svg)]() [![GitHub license](https://img.shields.io/github/license/trackmastersteve/HackServ.svg)](https://github.com/trackmastersteve/HackServ/tree/master/LICENSE) [![Python3](https://img.shields.io/badge/python-3.12-green.svg)]() [![GitHub issues](https://img.shields.io/github/issues/trackmastersteve/HackServ.svg)](https://github.com/trackmastersteve/HackServ/issues) [![GitHub stars](https://img.shields.io/github/stars/trackmastersteve/HackServ.svg)](https://github.com/trackmastersteve/HackServ/stargazers)  [![GitHub forks](https://img.shields.io/github/forks/trackmastersteve/HackServ.svg)](https://github.com/trackmastersteve/HackServ/network) 

Advanced IRC bot/botnet PoC written in python 3. This bot is for educational purposes only!
Do **NOT** use this bot on a computer or network without written permission from the owner(s)!
This bot can connect to IRC over SSL and is compatible with Unrealircd's nospoof:PING.
Seperate config file for easy upgrades.

### Installation:

The following packages are required. You'll need to install the following using the
package manager:

```sudo apt install python3 nmap python3-nmap metasploit-framework python3-pymetasploit3```

Then clone this project by running the following command:

```git clone https://github.com/trackmastersteve/HackServ.git```

If you have sudo privleges, you can make the bot persist:

```sudo useradd hackserv```

Edit: ```hackserv.service``` with correct location of script i.e. ```/usr/local/bin/.hackserv.py```

```sudo cp hackserv.py /usr/local/bin/.hackserv.py```

```sudo cp hsConfig.py /usr/local/bin/hsConfig.py``` (Don't forget to edit this file afterwards)

```sudo cp hackserv.service /etc/systemd/system/hackserv.service```

```sudo systemctl enable --now hackserv.service```

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

```.cno [shell command]``` (run shell command without output)

```.chmd [file] [permissions]``` (change permissions of a file)

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

```.ls [dir]``` (lists files in a directory)

```.dl [url] [file]``` (downloads [url] and saves as [file])

```.run [execute type] [executable file]``` (execute a file)

```.upgrade [link] [file]``` (upgrades the hackserv.py file)

```.mining [start/stop]``` (**coming soon!**)

```.persistence``` (**testing**)

### TODO

- [x] Move configuration to external file to make updates more seamless

- [x] Send/Receive CTCP commands (so far it responds to **CTCP VERSION** only)

- [x] Persistence (**.service file was created to run this as a systemd service**)

- [ ] Convert the port scanner from nmap to sockets (to remove the nmap dependency) (TO Do List)

- [ ] Send/Receive DCC commands (CHAT and TRANSFER) (To DO List)

- [x] Accept uploads from admin (File Server)

- [ ] Auto Vuln/Port/Proxy Scan on join (Need ability to get IP from server) (To Do List)

- [ ] Key Logger (To Do List)

- [ ] Self Replicating (**testing, not working yet**)

- [ ] Proxy Scanner (To Do List)

- [ ] Vuln Scanner (To Do List)

- [ ] Crypto Miner (To Do List)

- [ ] Self proxy (To Do List)

- [ ] DoS/DDoS (To Do List)

- [x] Open reverse shell/meterpreter

- [x] Run in Background - ('debugmode = False' setting allows bot to run in the background)

- [x] Better error handling (still a few bugs to work out)

- [x] Send downloads to admin (File Server)

- [x] Better handling of disconnects etc.

- [x] Run single shell commands

- [x] Better sigterm handling

- [x] Join and Part Channels

- [x] Execute files/code

- [x] NickServ Identify

- [x] SASL Auth Support

- [x] Connect over SSL 

- [x] Get ip address

- [x] File Server

- [x] Self update

- [x] Help Menu

