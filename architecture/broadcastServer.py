import networking

s = networking.BroadcastServer(port = 1567, host = 'localhost')
s.listenAndConnect()
