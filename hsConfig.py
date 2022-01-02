#!/usr/bin/env python3
#
# HackServ IRC Bot - Config File
# hsConfig.py
#
# Copyright (c) 2018-2022 Stephen Harris <trackmastersteve@gmail.com>
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
#
config_version = 1.2
import random
from requests import get
ip = get('https://api.ipify.org').text
#################################################
############# Booleans ##########################
debugmode = False # If True, all print msgs will be active. (use False if you want to run in the background)
onJoin = False # If True, the bots onJoin actions will be enabled.
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
