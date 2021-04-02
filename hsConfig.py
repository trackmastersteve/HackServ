#!/usr/bin/env python3
#
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
