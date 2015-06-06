#!/usr/bin/env python
import Ice
from database import User

def connect(serverid=1):
    Ice.loadSlice('', ['-I', Ice.getSliceDir(), '/usr/share/slice/Murmur.ice'])
    prop = Ice.createProperties([])
    prop.setProperty('Ice.MessageSizeMax', '65535')
    prop.setProperty('Ice.ImplicitContext', 'Shared')
    prop_data = Ice.InitializationData()
    prop_data.properties = prop
    comm = Ice.initialize(prop_data)
    proxy = comm.stringToProxy("Meta:tcp -p 6502")
    import Murmur
    meta = Murmur.MetaPrx.checkedCast(proxy)
    return meta.getServer(serverid)

def get_users(server):
    users = server.getUsers()
    usernames = []
    for key in users.iterkeys():
        if users[key].userid > 0:
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

if __name__ == '__main__':
    update_users(connect())
