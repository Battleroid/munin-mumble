#!/usr/bin/env python
# -*- coding: utf-8
#
# munin-murmur.py - "murmur stats (User/Bans/Uptime/Channels)" script for munin.
# Copyright (c) 2012, Natenom / natenom@natenom.name

#Path to Murmur.ice
iceslice='/usr/share/Ice/slice/Murmur.ice'

#Includepath for Ice, this is default for Debian
iceincludepath="/usr/share/Ice/slice"

#Murmur-Port (not needed to work, only for display purposes)
serverport=64738

#Port where ice listen
iceport=6502

#Ice Password to get read access.
#If there is no such var in your murmur.ini, this can have any value.
#You can also use the icesecretwrite of your server.
icesecretread="secureme"

#MessageSizeMax; increase this value, if you get a MemoryLimitException.
# Also check this value in murmur.ini of your Mumble-Server.
# This value is being interpreted in kibiBytes.
messagesizemax="65535"

import Ice, sys
Ice.loadSlice("--all -I%s %s" % (iceincludepath, iceslice))

props = Ice.createProperties([])
props.setProperty("Ice.MessageSizeMax", str(messagesizemax))
props.setProperty("Ice.ImplicitContext", "Shared")
id = Ice.InitializationData()
id.properties = props

ice = Ice.initialize(id)
ice.getImplicitContext().put("secret", icesecretread)

import Murmur

if (sys.argv[1:]):
  if (sys.argv[1] == "config"):
    print 'graph_title Murmur (Port %s)' % (serverport)
    print 'graph_vlabel Count'
    print 'users.label Users (All)'
    print 'usersnotauth.label Users (Not authenticated)'
    print 'uptime.label Uptime in days'
    print 'chancount.label Channelcount/10'
    print 'bancount.label Bans on server'
    sys.exit(0)


meta = Murmur.MetaPrx.checkedCast(ice.stringToProxy("Meta:tcp -h 127.0.0.1 -p %s" % (iceport)))
try:
    server=meta.getServer(1)
except Murmur.InvalidSecretException: 
    print 'Given icesecreatread password is wrong.'
    ice.shutdown()
    sys.exit(1)

#count users
usersnotauth=0
users=server.getUsers()
for key in users.keys():
  if (users[key].userid == -1):
    usersnotauth+=1

print "users.value %i" % (len(users))
print "uptime.value %.2f" % (float(meta.getUptime())/60/60/24)
print "chancount.value %.1f" % (len(server.getChannels())/10)
print "bancount.value %i" % (len(server.getBans()))
print "usersnotauth.value %i" % (usersnotauth)
  
ice.shutdown()