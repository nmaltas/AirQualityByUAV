# Script for fetching the data from the UAV payload



#!/usr/bin/env python

# Copyright (C) 2003-2007  Robey Pointer <robeypointer@gmail.com>
#
# This file is part of paramiko.
#
# Paramiko is free software; you can redistribute it and/or modify it under the
# terms of the GNU Lesser General Public License as published by the Free
# Software Foundation; either version 2.1 of the License, or (at your option)
# any later version.
#
# Paramiko is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Paramiko; if not, write to the Free Software Foundation, Inc.,
# 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA.

# based on code provided by raymond mosteller (thanks!)
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.ticker as plticker
import numpy as np 
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter, AutoMinorLocator)
import linecache
import time
import base64
import getpass
import os
import socket
import sys
import traceback

import paramiko
from paramiko.py3compat import input


# setup logging
paramiko.util.log_to_file("demo_sftp.log")
bufsize = 2**20

# Paramiko client configuration
UseGSSAPI = False  # enable GSS-API / SSPI authentication
DoGSSAPIKeyExchange = False
Port = 22

# get hostname
username = ""
if len(sys.argv) > 1:
    hostname = sys.argv[1]
    if hostname.find("@") >= 0:
        username, hostname = hostname.split("@")
else:
    hostname = '192.168.1.101' #input("Hostname: ")
if len(hostname) == 0:
    print("*** Hostname required.")
    sys.exit(1)

if hostname.find(":") >= 0:
    hostname, portstr = hostname.split(":")
    Port = int(portstr)


# get username
if username == "":
    default_username = getpass.getuser()
    username = 'pi' #input("Username [%s]: " % default_username)
    if len(username) == 0:
        username = default_username
if not UseGSSAPI:
    password = 'knopflab' #getpass.getpass("Password for %s@%s: " % (username, hostname))
else:
    password = None


# get host key, if we know one
hostkeytype = None
hostkey = None
try:
    host_keys = paramiko.util.load_host_keys(
        os.path.expanduser("~/.ssh/known_hosts")
    )
except IOError:
    try:
        # try ~/ssh/ too, because windows can't have a folder named ~/.ssh/
        host_keys = paramiko.util.load_host_keys(
            os.path.expanduser("~/ssh/known_hosts")
        )
    except IOError:
        print("*** Unable to open host keys file")
        host_keys = {}

if hostname in host_keys:
    hostkeytype = host_keys[hostname].keys()[0]
    hostkey = host_keys[hostname][hostkeytype]
    print("Using host key of type %s" % hostkeytype)


# now, connect and use paramiko Transport to negotiate SSH2 across the connection
try:
    t = paramiko.Transport((hostname, Port))
    t.connect(
        hostkey,
        username,
        password,
        gss_host=socket.getfqdn(hostname),
        gss_auth=UseGSSAPI,
        gss_kex=DoGSSAPIKeyExchange)

    sftp = paramiko.SFTPClient.from_transport(t)

    # dirlist on remote host
    #dirlist = sftp.listdir(".")
   # print("Dirlist: %s" % dirlist)
    print ("Obtaining file.")
    # BETTER: use the get() and put() methods
    #sftp.put("HelloWorld.txt", "Shared/Remote_HelloWorld.txt")
    #sftp.get("demo_sftp_folder/README", "README_demo_sftp")
    
    
    while True:
        print('Obtaining data.')
        
        Data = sftp.open("Shared/StreamData.txt" , bufsize=bufsize)
        DataOut = open('Data.txt', 'a')
        for line in Data:
            pass
        last = line
        
        DataOut.write(line)
        
        DataOut.close()
        Data.close()

    
        
        time.sleep(3)

    t.close()

except Exception as e:
    print("*** Caught exception: %s: %s" % (e.__class__, e))
    traceback.print_exc()
    try:
        t.close()
    except:
        pass
    sys.exit(1)