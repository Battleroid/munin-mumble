#!/usr/bin/env python
import Ice, os
from database import User

def connect():
    # setup
    iceslice = os.environ.get('iceslice', '/usr/share/slice/Murmur.ice')
    iceincpath = os.environ.get('iceincpath', '/usr/share/Ice/slice')
    port = int(os.environ.get('murmurport', '6502'))
    secret = os.environ.get('mumursecret', '')
    messagemax = os.environ.get('murmurmessagemax', '65535')
    # open
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
        return server
    except Murmur.InvalidSecretException:
        print 'Incorrect secret!'
        ice.shutdown()
        return None

def get_users(server):
    users = server.getUsers()
    usernames = []
    for key in users.iterkeys():
        usernames.append(users[key].name)
    return usernames

def update_users(server):
    current_users = get_users(server)
    query = User.select()
    for user in current_users:
        if query.where(User.username == user).exists():
            u = query.where(User.username == user).get()
            u.points += 1
            u.save()
        else:
            User.create(username=user)
