#!/usr/bin/python3
#
# ircbot.py
#
# Copyright (c) 2018 Stephen Harris <trackmastersteve@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

legal_notice = 'THIS BOT IS FOR EDUCATION PURPOSES ONLY! DO NOT USE IT FOR MALICIOUS INTENT!'
author = 'Stephen Harris (trackmastersteve@gmail.com)'
github = 'https://github.com/trackmastersteve/bot.git'
version = '0.3.9'
last_modification = '2018.08.25'

import ssl
import sys
import nmap
import socket
import ipgetter
import datetime
import platform

ip = ipgetter.myip() # Get public IP address
########################
##### Bot Settings #####
server = "chat.freenode.net" # Server
port = 6697 # Port (If you want to use standard 6667, comment out the appropriate line down below to turn off SSL.)
channel = "#channel" # Channel
#botnick = "botnick" # Your bots IRC nick (If you want to set this manually, comment out the line below to disable ip-to-nick.)
botnick = "ip" + ip.replace(".", "_") # Change bots nick to IP address, but in proper IRC nick format.
botident = "password" # Bots NickServ password
adminname = "master" # Your IRC nick
exitcode = "bye " + botnick # Command used to kill the bot.
##### Bot Settings #####
########################

starttime = datetime.datetime.utcnow() # Start time is used to calculate uptime.
ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ircsock = ssl.wrap_socket(ircsock) # Comment this line out if you don't want to use SSL.
ircsock.connect((server, port)) # Here we connect to the server.
ircsock.send(bytes("USER "+ botnick +" "+ botnick +" "+ botnick +" "+ botnick + " " + botnick + "\n", "UTF-8")) # We are basically filling out a form with this line and saying to set all the fields to the bot nickname.
ircsock.send(bytes("NICK "+ botnick +"\n", "UTF-8")) # Assign the nick to the bot.

def joinchan(chan): # Join channel(s).
    ircsock.send(bytes("JOIN "+ chan +"\n", "UTF-8"))
    ircmsg = ""
    while ircmsg.find("End of /NAMES list.") == -1:
        ircmsg = ircsock.recv(2048).decode("UTF-8")
        ircmsg = ircmsg.strip('\n\r')
        print(ircmsg) # Print messages to the screen. (won't allow bot to run in the background.)
        #sendmsg(ircmsg, adminname) # Sends messages to the channel/admin. (Will run in background. But spams admin)

def partchan(chan): # Part channel(s).
    ircsock.send(bytes("PART "+ chan +"\n", "UTF-8"))
        
def cycle(chan): # Part then Join channel(s) 
    ircsock.send(bytes("PART "+ chan +"\n", "UTF-8"))
    ircsock.send(bytes("JOIN "+ chan +"\n", "UTF-8"))
    ircmsg = ""
    while ircmsg.find("End of /NAMES list.") == -1:
        ircmsg = ircsock.recv(2048).decode("UTF-8")
        ircmsg = ircmsg.strip('\n\r')
        print(ircmsg) # Print messages to the screen. (won't allow bot to run in the background.)
        #sendmsg(ircmsg, adminname) # Sends messages to the channel/admin. (Will run in background. But spams admin)
        
def ping(): # Respond to server Pings.
    ircsock.send(bytes("PONG :pingis\n", "UTF-8"))

def sendversion(nick, ver): # Respond to VERSION request.
    ircsock.send(bytes("PRIVMSG "+ nick +" :VERSION: arm0red bot "+ ver +"\n", "UTF-8"))
    
def sendmsg(msg, target=channel): # Sends messages to the target.
    ircsock.send(bytes("PRIVMSG "+ target +" :"+ msg +"\n", "UTF-8"))

def sendnotice(notice, target=channel): # Sends a NOTICE to the target.
    ircsock.send(bytes("NOTICE "+ target +" :"+ notice +"\n", "UTF-8"))
    
def uptime(): # Used for .uptime command
    delta = datetime.timedelta(seconds=round((datetime.datetime.utcnow() - starttime).total_seconds()))
    return delta

def uname(): # Used for .uname command
    sysinfo = platform.uname()
    return sysinfo

def nmapScan(tgtHost, tgtPort): # Used for .scan command
    nmScan = nmap.PortScanner()
    nmScan.scan(tgtHost, tgtPort)
    state = nmScan[tgtHost]['tcp'][int(tgtPort)]['state']
    sendmsg((" [*] " + tgtHost + " tcp/" +tgtPort + "" + state), adminname)

def setmode(flag, target=channel): # Sets given mode to nick or channel.
    ircsock.send(bytes("MODE "+ target +" "+ flag +"\n", "UTF-8"))
    
def main():
    while 1:
        ircmsg = ircsock.recv(2048).decode("UTF-8")
        ircmsg = ircmsg.strip('\n\r')
        print(ircmsg) # Print messages to the screen. (won't allow bot to run in the background.)
        #sendmsg(ircmsg, adminname) # Sends messages to the channel/admin. (Will run in background. But spams admin.)
        
        # Join 'channel' and msg 'admin' after you are fully connected to server.
        if ircmsg.find('NOTICE') != -1:
            message = ircmsg.split('NOTICE',1)[1].split(':',1)[1]
            if message.find('*** You are connected') != -1:
                joinchan(channel)
                sendmsg(format(ip) + " Online!", adminname)
                
        # Respond to CTCP VERSION
        if ircmsg.find('VERSION') != -1:
            name = ircmsg.split('!',1)[0][1:]
            vers = version
            sendversion(name, vers)
            
        # Messages come in from IRC in the format of: ":[Nick]!~[hostname]@[IPAddress]PRIVMSG[channel]:[message]"
        if ircmsg.find('PRIVMSG') != -1:
            name = ircmsg.split('!',1)[0][1:]
            message = ircmsg.split('PRIVMSG',1)[1].split(':',1)[1]

            if len(name) < 17:
                # Respond to NickServ ident request.
                if name.lower() == 'nickserv' and message.find('This nickname is registered') != -1:
                    ircsock.send("nickserv identify " + botident + "\r\n")
                    
                # Respond to anyone saying 'Hi [botnick]'.
                if message.find('Hi ' + botnick) != -1:
                    sendmsg("Hello " + name + "!")

                # Respond to '.msg [target] [message]' command from admin.
                if name.lower() == adminname.lower() and message[:5].find('.msg') != -1:
                    target = message.split(' ', 1)[1]
                    if target.find(' ') != -1:
                        message = target.split(' ', 1)[1]
                        target = target.split(' ')[0]
                    else:
                        target = name
                        message = "Could not parse. The message should be in format of '.msg [target] [message]' to work properly."
                    sendmsg(message, target)

                # Respond to '.notice [target] [message]' command from admin.
                if name.lower() == adminname.lower() and message[:5].find('.notice') != -1:
                    target = message.split(' ', 1)[1]
                    if target.find(' ') != -1:
                        message = target.split(' ', 1)[1]
                        target = target.split(' ')[0]
                    else:
                        target = name
                        message = "Could not parse. The message should be in the format of '.notice [target] [message]' to work properly."
                    sendnotice(message, target)
                
                # Respond to the '.mode [target] [mode]' command from admin.
                if name.lower() == adminname.lower() and message[:5].find('.mode') != -1:
                    target = message.split(' ', 1)[1]
                    if target.find(' ') != -1:
                        mode = target.split(' ', 1)[1]
                        target = target.split(' ')[0]
                        message = "The mode " + mode + " was set on " + target + "!"
                    else:
                        message = "Could not parse. The message should be in the format of '.mode [target] [mode]' to work properly."
                    setmode(mode, target)
                    sendmsg(message, adminname)
                
                # Respond to the '.join [channel]' command from admin.
                if name.lower() == adminname.lower() and message[:5].find('.join') != -1:
                    if message.split(' ', 1)[1].startswith('#'):
                        target = message.split(' ', 1)[1]
                        message = "Ok, I will join the channel: " + target
                        joinchan(target)
                    else:
                        message = "Could not parse. Please make sure the channel is in the format of '#channel'."
                    sendmsg(message, name)
                
                # Respond to the '.part [channel]' command from admin.
                if name.lower() == adminname.lower() and message[:5].find('.part') != -1:
                    if message.split(' ', 1)[1].startswith('#'):
                        target = message.split(' ', 1)[1]
                        message = "Ok, I will part the channel: " + target
                        partchan(target)
                    else:
                        message = "Could not parse. Please make sure the channel is in the format of '#channel'."
                    sendmsg(message, name)

                # Respond to the '.cycle [channel]' command from admin.
                if name.lower() == adminname.lower() and message[:5].find('.cycle') != -1:
                    if message.split(' ', 1)[1].startswith('#'):
                        target = message.split(' ', 1)[1]
                        message = "Ok, cycling " + target + " now!"
                        cycle(target)
                    else:
                        message = "Could not parse. Please make sure the channel is in the format of '#channel'."
                    sendmsg(message, name)
                
                # Respond to '.ip' command from admin.
                if name.lower() == adminname.lower() and message.find('.ip') != -1:
                    sendmsg("My public ip address is:", name)
                    sendmsg(format(ip), name)
                
                # Respond to '.uptime' command from admin.
                if name.lower() == adminname.lower() and message.find('.uptime') != -1:
                    sendmsg("My current uptime:", name)
                    sendmsg(format(uptime()), name)
                    
                # Respond to '.uname' command from admin.
                if name.lower() == adminname.lower() and message.find('.uname') != -1:
                    sendmsg("System Info:", name)
                    sendmsg(format(uname()), name)

                # Respond to '.scan [target] [port(s)]' command from admin.
                if name.lower() == adminname.lower() and message[:5].find('.scan') != -1:
                    target = message.split(' ', 1)[1]
                    if target.find(' ') != -1:
                        message = "nmap scan has completed!"
                        ports = target.split(' ', 1)[1]
                        target = target.split(' ')[0]
                        ports = [s.strip() for s in str(ports).split(',')] 
                        for port in ports: # loops through comma seperated list of ports.
                            nmapScan(target, port)
                    else:
                        message = "Could not parse. The command should be in the format of '.scan [target] [port]' to work properly."
                    sendmsg(message, adminname)

                # Respond to 'exitcode' from admin.
                if name.lower() == adminname.lower() and message.rstrip() == exitcode:
                    sendmsg("Okay, Bye!")
                    ircsock.send(bytes("QUIT \n", "UTF-8"))
                    return

        else:
            if ircmsg.find("PING") != -1:
                nospoof = ircmsg.split(' ', 1)[1] # Unrealircd 'nospoof' compatibility.
                ircsock.send(bytes("PONG " + nospoof +"\n", "UTF-8"))

main()



