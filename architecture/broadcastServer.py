import networking

s = networking.BroadcastServer(port = 1567, host = '10.41.24.42')
s.listenAndConnect()
