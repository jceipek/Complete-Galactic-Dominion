import networking

s = networking.BroadcastServer(port = 1567, host = '10.41.25.14')
s.listenAndConnect()
