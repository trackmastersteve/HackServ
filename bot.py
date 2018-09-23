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
software = 'arm0red bot'
version = '0.7.4'
last_modification = '2018.09.23'

import ssl
import sys
import nmap
import time
import sched
import random
import socket
import ipgetter
import datetime
import platform

starttime = datetime.datetime.utcnow() # Start time is used to calculate uptime.
ip = ipgetter.myip() # Get public IP address. (used to set botnick-to-ip as well as the '.ip' command.)

#################################################
##### Bot Settings ##############################
debugmode = True # If True, all print msgs will be active. (use False if you want to run in the background)
server = "irc.freenode.net" # Server to connect to.
usessl = True # Connect using SSL. (True or False)
port = 6697 # Port to connect to.
useservpass = False # Use a password to connect to IRC Server. (True or False)
serverpass = "password" # Password for IRC Server. (UnrealIRCD uses this as default NickServ ident method)
channel = "#arm0red" # Channel to join on connect.
#botnick = "botnick" # Your bots IRC nick.
#botnick = "ip" + ip.replace(".", "_") # Set bots nick to IP address, but in proper IRC nick compatible format.
botnick = "abot" + str(random.randint(10000,99999)) # Set bots IRC Nick to abot + 5 random numbers.
nspass = "password" # Bots NickServ password.
nickserv = "NickServ" # Nickname service name. (sometimes it's differnet on some networks.)
adminname = "arm0red" # Bot Master's IRC nick.
exitcode = "bye" # Command 'exitcode + botnick' is used to kill the bot.
##### Bot Settings ##############################
#################################################

st = sched.scheduler(time.time, time.sleep) # Time Scheduler.
ctime = time.time() # Current time.
lastping = time.time() # Time at last PING.
threshold = 200 # Ping timeout before reconnect.
connected = False # Variable to say if bot is connected or not.
ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Set ircsock variable.
if usessl: # If SSL is True, connect using SSL.
    ircsock = ssl.wrap_socket(ircsock)

def curtime(sc):
    global ctime
    ctime = time.time() # Set current time as variable.
    return ctime
    st.enter(10, 1, curtime, (sc,)) # Restart this scheduler.
    
def connect():
    global connected
    while not connected:
        try: # Try and connect to the IRC server.
            if debugmode: # If debugmode is True, msgs will print to screen.
                print("Connecting to " + str(server) + ":" + str(port))
            ircsock.connect((server, port)) # Here we connect to the server.
            if useservpass: # If useservpass is True, send serverpass to server to connect.
                ircsock.send(bytes("PASS "+ serverpass +"\n", "UTF-8")) # Send the server password to connect to password protected IRC server.
            ircsock.send(bytes("USER "+ botnick +" "+ botnick +" "+ botnick +" "+ botnick + " " + botnick + "\n", "UTF-8")) # We are basically filling out a form with this line and saying to set all the fields to the bot nickname.
            ircsock.send(bytes("NICK "+ botnick +"\n", "UTF-8")) # Assign the nick to the bot.
            connected = True
            main()
        except: # If you can't connect, wait 10 seconds and try again.
            if debugmode: # If debugmode is True, msgs will print to screen.
                print("Failed to connect to " + str(server) + ":" + str(port) + ". Retrying in 10 seconds...")
            time.sleep(10)
            reconnect()

def reconnect():
    global connected
    global ircsock
    while not connected:
        ircsock.close() # Close previous socket.
        ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Set ircsock variable.
        if usessl: # If SSL is True, connect using SSL.
            ircsock = ssl.wrap_socket(ircsock) 
        try:
            if debugmode: # If debugmode is True, msgs will print to screen.
                print("Reconnecting to " + str(server) + ":" + str(port))
            ircsock.connect((server, port)) # Here we connect to the server.
            if useservpass: # If useservpass is True, send serverpass to server to connect.
                ircsock.send(bytes("PASS "+ serverpass +"\n", "UTF-8")) # Send the server password to connect to password protected IRC server.
            ircsock.send(bytes("USER "+ botnick +" "+ botnick +" "+ botnick +" "+ botnick + " " + botnick + "\n", "UTF-8")) # We are basically filling out a form with this line and saying to set all the fields to the bot nickname.
            ircsock.send(bytes("NICK "+ botnick +"\n", "UTF-8")) # Assign the nick to the bot.
            connected = True
            main()
        except: # If you can't connect, wait 10 seconds and try again.
            if debugmode: # If debugmode is True, msgs will print to screen.
                print("Failed to reconnect to " + str(server) + ":" + str(port) + ". Retrying in 10 seconds...")
            time.sleep(10)
            reconnect()
            
def joinchan(chan): # Join channel(s).
    ircsock.send(bytes("JOIN "+ chan +"\n", "UTF-8"))
    ircmsg = ""
    while ircmsg.find("End of /NAMES list.") == -1:
        ircmsg = ircsock.recv(2048).decode("UTF-8")
        ircmsg = ircmsg.strip('\n\r')
        if debugmode: # If debugmode is True, msgs will print to screen.
            print(ircmsg) # Print messages to the screen. (won't allow bot to run in the background.)
        #sendmsg(ircmsg, adminname) # Sends messages to the channel/admin. (Will run in background. But spams admin)

def partchan(chan): # Part channel(s).
    ircsock.send(bytes("PART "+ chan +"\n", "UTF-8"))
        
def pjchan(chan): # Part then Join channel(s) 
    ircsock.send(bytes("PART "+ chan +"\n", "UTF-8"))
    ircsock.send(bytes("JOIN "+ chan +"\n", "UTF-8"))
    ircmsg = ""
    while ircmsg.find("End of /NAMES list.") == -1:
        ircmsg = ircsock.recv(2048).decode("UTF-8")
        ircmsg = ircmsg.strip('\n\r')
        if debumode: # If debugmode is True, msgs will print to screen.
            print(ircmsg) # Print messages to the screen. (won't allow bot to run in the background.)
        #sendmsg(ircmsg, adminname) # Sends messages to the channel/admin. (Will run in background. But spams admin)
        
def ping(): # Respond to server Pings.
    ircsock.send(bytes("PONG :pingis\n", "UTF-8"))
    
def newnick(newnick): # Change botnick.
    ircsock.send(bytes("NICK "+ newnick +"\n", "UTF-8"))

def sendversion(nick, ver): # Respond to VERSION request.
    ver = software + ' ' + version + ' ' + github
    ircsock.send(bytes("PRIVMSG "+ nick +" :VERSION: " + ver +"\n", "UTF-8"))
    
def sendmsg(msg, target=channel): # Sends messages to the target.
    ircsock.send(bytes("PRIVMSG "+ target +" :"+ msg +"\n", "UTF-8"))

def sendntc(ntc, target=channel): # Sends a NOTICE to the target.
    ircsock.send(bytes("NOTICE "+ target +" :"+ ntc +"\n", "UTF-8"))
    
def kick(msg, usr, chan): # Kick a user from the channel.
    ircsock.send(bytes("KICK "+ chan + " " + usr + " :"+ msg +"\n", "UTF-8"))
    
def uptime(): # Used to get current uptime for .uptime command
    delta = datetime.timedelta(seconds=round((datetime.datetime.utcnow() - starttime).total_seconds()))
    return delta

def uname(): # Used to get system info for .uname command
    sysinfo = platform.uname()
    return sysinfo

def linuxMemory():
    sendmsg("Memory Info: ", adminname)
    with open("/proc/meminfo", "r") as f:
        lines = f.readlines()

    sendmsg("     " + lines[0].strip(), adminname)
    sendmsg("     " + lines[1].strip(), adminname)

def nmapScan(tgtHost, tgtPort): # Use nmap to scan ports on an ip address with .scan command
    nmScan = nmap.PortScanner()
    nmScan.scan(tgtHost, tgtPort)
    state = nmScan[tgtHost]['tcp'][int(tgtPort)]['state']
    if state == 'open':
        st = '[*]'
    else:
        st = '[ ]'
    sendmsg((st + " " + tgtHost + " tcp/" +tgtPort + " -" + state), adminname)

def setmode(flag, target=channel): # Sets given mode to nick or channel.
    ircsock.send(bytes("MODE "+ target +" "+ flag +"\n", "UTF-8"))

def main():
    global connected
    global botnick
    global ip
    global lastping
    while connected:
        ircmsg = ircsock.recv(2048).decode("UTF-8")
        ircmsg = ircmsg.strip('\n\r')
        if debugmode: # If debugmode is True, msgs will print to screen.
            print(ircmsg) # Print messages to the screen. (won't allow bot to run in the background.)
            #sendmsg(ircmsg, adminname) # Sends messages to the channel/admin. (Will run in background. But spams admin.)
        
        # Wait 30 seconds and try to reconnect if 'too many connections from this IP'
        if ircmsg.find('Too many connections from your IP') != -1:
            if debugmode: # If debugmode is True, msgs will print to screen.
                print("Too many connections from this IP! Reconnecting in 30 seconds...")
            connected = False
            time.sleep(30)
            reconnect()
        
        # Change nickname if current nickname is already in use.
        if ircmsg.find('Nickname is already in use') != -1:
            botnick = "abot" + str(random.randint(10000,99999))
            ircsock.send(bytes("NICK "+ botnick +"\n", "UTF-8"))
        
        # Join 'channel' and msg 'admin' after you are fully connected to server.
        if ircmsg.find('NOTICE') != -1:
            name = ircmsg.split('!',1)[0][1:]
            message = ircmsg.split('NOTICE',1)[1].split(':',1)[1]
            if message.find('*** You are connected') != -1:
                joinchan(channel)
                #sendmsg(format(ip) + " Online!", adminname)
                
            # Respond to NickServ ident request.
            if name.lower() == nickserv.lower() and message.find('This nickname is registered') != -1:
                sendmsg("IDENTIFY %s" % nspass, nickserv)
                sendmsg("IDENTIFIED: %s" % nspass, adminname)
                
        # Respond to CTCP VERSION
        if ircmsg.find('VERSION') != -1:
            name = ircmsg.split('!',1)[0][1:]
            vers = version
            sendversion(name, vers)
            
        # Messages come in from IRC in the format of: ":[Nick]!~[hostname]@[IPAddress]PRIVMSG[channel]:[message]"
        if ircmsg.find('PRIVMSG') != -1:
            name = ircmsg.split('!',1)[0][1:]
            message = ircmsg.split('PRIVMSG',1)[1].split(':',1)[1]

            # IRC Nicks are normally less than 17 characters long.
            if len(name) < 17:
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

                # Respond to '.ntc [target] [message]' command from admin.
                if name.lower() == adminname.lower() and message[:5].find('.ntc') != -1:
                    target = message.split(' ', 1)[1]
                    if target.find(' ') != -1:
                        message = target.split(' ', 1)[1]
                        target = target.split(' ')[0]
                    else:
                        target = name
                        message = "Could not parse. The message should be in the format of '.notice [target] [message]' to work properly."
                    sendntc(message, target)
                
                # Respond to '.kick [channel] [nick] [reason]' command from admin.
                if name.lower() == adminname.lower() and message[:5].find('.kick') != -1:
                    target = message.split(' ', 1)[1]
                    if target.find(' ') != -1:
                        reason = target.split(' ', 2)[2]
                        nick = target.split(' ')[1]
                        chnl = target.split(' ')[0]
                        message = nick + " was kicked from " + chnl + " Reason:" + reason
                        kick(reason, nick, chnl)
                    else:
                        message = "Could not parse. The message should be in the format of '.kick [#channel] [nick] [reason]' to work properly."
                    sendmsg(message, name)
                
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
                
                # Respond to the '.nick [newnick]' command from admin.
                if name.lower() == adminname.lower() and message[:5].find('.nick') != -1:
                    if message.split(' ', 1)[1] != -1:
                        botnick = message.split(' ', 1)[1]
                        message = "Ok, Changing my nick to: " + botnick
                        newnick(botnick)
                    else:
                        message = "Could not parse. Please make sure the command is in the format of '.nick [newnick]' to work properly."
                    sendmsg(message, name)
                
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
                if name.lower() == adminname.lower() and message[:5].find('.pj') != -1:
                    if message.split(' ', 1)[1].startswith('#'):
                        target = message.split(' ', 1)[1]
                        message = "Ok, cycling " + target + " now!"
                        pjchan(target)
                    else:
                        message = "Could not parse. Please make sure the channel is in the format of '#channel'."
                    sendmsg(message, name)
                
                # Respond to the '.help' command.
                if message.find('.help') != -1:
                    message = "End of Help."
                    if name.lower() == adminname.lower():
                        helpmsg = """
                                  '.help' shows this message.,
                                  '.uptime' (shows bot uptime),
                                  '.uname' (get 1-line system info),
                                  '.sysinfo' (get formated system info),
                                  '.osversion' (get OS version info),
                                  '.linuxmemory' (get memory stats from linux machine),
                                  '.ip' (get ip address of bot),
                                  '.scan [ip] [comma seperated ports]' (nmap port scanner),
                                  '.msg [target] [message]' (sends a msg to a user/channel),
                                  '.ntc [target] [message]' (sends a notice to a user/channel),
                                  '.join [channel]' (tells bot to join channel),
                                  '.part [channel]' (tells bot to part channel),
                                  '.pj [channel]' (tells bot to part then join channel),
                                  '.kick [channel] [nick] [reason]' (tells bot to kick a user from a channel),
                                  '.mode [target] [mode]' (set mode on nick or channel),
                                  '.nick [newnick]' (sets a new botnick),
                                  'Hi [botnick]' (responds to any user saying hello to it),
                                  'bye [botnick]' (tells bot to quit)
                                  """
                    else:
                        helpmsg = """
                                  '.help' shows this message.,
                                  'Hi [botnick]' responds to any user saying hello to it.
                                  """
                    helpmsg = [m.strip() for m in str(helpmsg).split(',')]
                    for line in helpmsg:
                        sendmsg(line, name)
                    sendmsg(message, name)
                
                # Respond to '.ip' command from admin.
                if name.lower() == adminname.lower() and message.find('.ip') != -1:
                    ip = ipgetter.myip()
                    sendmsg("My public ip address is: " + format(ip), name)
                
                # Respond to '.uptime' command from admin.
                if name.lower() == adminname.lower() and message.find('.uptime') != -1:
                    sendmsg("My current uptime: " + format(uptime()), name)
                    
                # Respond to '.uname' command from admin.
                if name.lower() == adminname.lower() and message.find('.uname') != -1:
                    sendmsg("System Info: " + format(uname()), adminname)
                    
                # Respond to '.sysinfo' command from admin.
                if name.lower() == adminname.lower() and message.find('.sysinfo') != -1:
                    # System
                    sendmsg("System: " + format(platform.system()), adminname)
                    # Node
                    sendmsg("Node: " + format(platform.node()), adminname)
                    # Release
                    sendmsg("Release: " + format(platform.release()), adminname)
                    # Version
                    sendmsg("Version :" + format(platform.version()), adminname)
                    # Architecture
                    sendmsg("Architecture: " + format(platform.architecture()[0]), adminname)
                    # Machine
                    sendmsg("Machine: " + format(platform.machine()), adminname)
                    
                # Respond to '.osversion' command from admin.
                if name.lower() == adminname.lower() and message.find('.osversion') != -1:
                    sendmsg("OS Version: " + format(platform.version()), adminname)
                    
                # Respond to '.linuxmemory' command from admin.
                if name.lower() == adminname.lower() and message.find('.linuxmemory') != -1:
                    linuxMemory()
                                
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
                        message = "Could not parse. The command should be in the format of '.scan [targetIP] [comma,seperated,ports]' to work properly."
                    sendmsg(message, adminname)

                # Respond to 'exitcode' from admin.
                if name.lower() == adminname.lower() and message.rstrip() == exitcode + " " + botnick:
                    sendmsg("Okay, Bye!")
                    ircsock.send(bytes("QUIT Killed by " + adminname + "\n", "UTF-8"))
                    sys.exit()

        else:
            if ircmsg.find("PING") != -1: # Reply to PINGs.
                nospoof = ircmsg.split(' ', 1)[1] # Unrealircd 'nospoof' compatibility.
                ircsock.send(bytes("PONG " + nospoof +"\n", "UTF-8"))
                lastping = time.time() # Set time of last PING.
                
            if (ctime - lastping) >= threshold: # If last PING was longer than set threshold, try and reconnect.
                if debugmode: # If debugmode is True, msgs will print to screen.
                    print('PING time exceeded threshold')
                connected = False
                reconnect()
                
            if not ircmsg: # If no response from server, try and reconnect.
                if debugmode: # If debugmode is True, msgs will print to screen.
                    print('Disconnected from server')
                connected = False
                reconnect()
                
try: # Here is where we actually start the Bot.
    connect() # Connect to server.
    st.enter(10, 1, curtime, (st,)) # Set time scheduler.
    st.run() # Start time scheduler.
except KeyboardInterrupt: # Kill Bot from CLI using CTRL+C
    ircsock.send(bytes("QUIT Killed Bot using [ctrl + c] \n", "UTF-8"))
    if debugmode: # If debugmode is True, msgs will print to screen.
        print('... Killed Bot using [ctrl + c], Shutting down!')
    sys.exit()
    
