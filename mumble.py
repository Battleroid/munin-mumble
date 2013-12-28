#!/usr/bin/env python
import os

def connect():
	# setup
	iceslice = os.environ.get('iceslice', '/usr/share/slice/Murmur.ice')
	iceincpath = os.environ.get('iceincpath', '/usr/share/Ice/slice')
	port = int(os.environ.get('port', '6502'))
	secret = os.environ.get('secret', '')
	messagemax = os.environ.get('messagemax', '65535')
	# open
	import Ice, sys
	Ice.loadSlice('--all -I%s %s' % (iceincpath, iceslice))
	props = Ice.createProperties([])
	props.setProperty('Ice.MessageSizeMax', str(messagemax))
	props.setProperty('Ice.ImplicitContext', 'Shared')
	id = Ice.InitializationData()
	id.properties = props
	ice = Ice.initialize(id)
	ice.getImplicitContext().put('secret', secret)
	# init
	import Murmur
	meta = Murmur.MetaPrx.checkedCast(ice.stringToProxy('Meta:tcp -h 127.0.0.1 -p %s' % (port)))
	try:
		server = meta.getServer(1)
	except Murmur.InvalidSecretException:
		print 'Incorrect secret!'
		ice.shutdown()
		sys.exit(1)
	return server
