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

NOTICE = 'THIS BOT IS FOR EDUCATION PURPOSES ONLY! DO NOT USE IT FOR MALICIOUS INTENT!'
author = 'Stephen Harris (trackmastersteve@gmail.com)'
version = '0.1.0'
last_modification = '2018.08.14'

import socket
import datetime
import platform
import nmap

########################
##### Bot Settings #####
server = "chat.freenode.net" # Server
port = 6667 # Port
channel = "#channel" # Channel
botnick = "botnick" # Your bots IRC nick
botident = "password" # Bots NickServ password
adminname = "master" # Your IRC nick
exitcode = "bye " + botnick
##### Bot Settings #####
########################

ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ircsock.connect((server, port)) # Here we connect to the server.
ircsock.send(bytes("USER "+ botnick +" "+ botnick +" "+ botnick +" "+ botnick + " " + botnick + "\n", "UTF-8")) # We are basically filling out a form with this line and saying to set all the fields to the bot nickname.
ircsock.send(bytes("NICK "+ botnick +"\n", "UTF-8")) # Assign the nick to the bot.

def joinchan(chan): # Join channel(s).
    ircsock.send(bytes("JOIN "+ chan +"\n", "UTF-8"))
    ircmsg = ""
    while ircmsg.find("End of /NAMES list.") == -1:
        ircmsg = ircsock.recv(2048).decode("UTF-8")
        ircmsg = ircmsg.strip('\n\r')
        print(ircmsg)

def ping(): # Respond to server Pings.
    ircsock.send(bytes("PONG :pingis\n", "UTF-8"))

def sendmsg(msg, target=channel): # Sends messages to the target.
    ircsock.send(bytes("PRIVMSG "+ target +" :"+ msg +"\n", "UTF-8"))

def memory(): # Used for .uptime command
    starttime = datetime.datetime.utcnow()
    return starttime

def uptime(): # Used for .uptime command
    delta = datetime.timedelta(seconds=round((datetime.datetime.utcnow() - memory()).total_seconds()))
    return delta

def uname(): # Used for .uname command
    sysinfo = platform.uname()
    return sysinfo

def nmapScan(tgtHost, tgtPort):
    nmScan = nmap.PortScanner()
    nmScan.scan(tgtHost, tgtPort)
    state = nmScan[tgtHost]['tcp'][int(tgtPort)]['state']
    sendmsg((" [*] " + tgtHost + " tcp/" +tgtPort + "" + state), adminname)

def main():
    joinchan(channel)
    while 1:
        ircmsg = ircsock.recv(2048).decode("UTF-8")
        ircmsg = ircmsg.strip('\n\r')
        print(ircmsg)

        # Messages come in from IRC in the format of: ":[Nick]!~[hostname]@[IPAddress]PRIVMSG[channel]:[message]"
        if ircmsg.find("PRIVMSG") != -1:
            name = ircmsg.split('!',1)[0][1:]
            message = ircmsg.split('PRIVMSG',1)[1].split(':',1)[1]

            if len(name) < 17:
                # Respond to anyone telling bot 'Hi'.
                if message.find('Hi ' + botnick) != -1:
                    sendmsg("Hello " + name + "!")

                # Respond to .tell [target] [message] command from anyone.
                if message[:5].find('.tell') != -1:
                    target = message.split(' ', 1)[1]
                    if target.find(' ') != -1:
                        message = target.split(' ', 1)[1]
                        target = target.split(' ')[0]
                    else:
                        target = name
                        message = "Could not parse. The message should be in format of '.tell [target] [message]' to work properly."
                    sendmsg(message, target)

                # Respond to .uptime command from admin.
                if name.lower() == adminname.lower() and message.find('.uptime') != -1:
                    sendmsg("My current uptime:", name)
                    sendmsg(format(uptime()), name)
                    
                # Respond to .uname command from admin.
                if name.lower() == adminname.lower() and message.find('.uname') != -1:
                    sendmsg("System Info:", name)
                    sendmsg(format(uname()), name)

                # Respond to .scan [target] command from admin.
                if name.lower() == adminname.lower() and message[:5].find('.scan') != -1:
                    target = message.split(' ', 1)[1]
                    if target.find(' ') != -1:
                        message = ".scan currently in testing..."
                        port = target.split(' ', 1)[1]
                        target = target.split(' ')[0]
                        nmapScan(target, port)
                    else:
                        message = "Could not parse. The command should be in the format of '.scan [target] [port]' to work properly."
                    sendmsg(message, adminname)

                # Respond to 'exitcode' from admin.
                if name.lower() == adminname.lower() and message.rstrip() == exitcode:
                    sendmsg("oh... okay. :'(")
                    ircsock.send(bytes("QUIT \n", "UTF-8"))
                    return

        else:
            if ircmsg.find("PING :") != -1:
                ping()

main()



