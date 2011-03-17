import networking, time

a=networking.PrintServer()
a.listenAndConnect()
time.sleep(1)
b=networking.MessengerClient('hello')
c=networking.MessengerClient('hello')
del b
del a
