WHAT IS IT?
===========

Complete Galactic Dominion (CGD) is a a cross-platform, networked real time strategy game (RTS) with a macro focus. 
It features planets with wrapping terrain (go off one edge and pop up on the other side), unlimited unit colors,
and a radial menu for interaction.

It was intended to include management of cross-planet supply chains.

The graphics are isometric 2d with pre-rendered 3d objects used as sprites.

CGD is written for Python 2.6-2.7 and uses the Pygame module.

![](https://github.com/jceipek/Complete-Galactic-Dominion/blob/master/ActionScreenshot.png?raw=true "CGD in Action")


CAN I PLAY IT YET?
=================
Kind of. Networking is finicky and the code is somewhat unweildy, but CGD currently has one unit type (a ship) that can fly around and 
attack enemies at range as well as collect gold ore (a resource) and construct buildings. There is also one building (a Town Center)
that can create new units. 


STATUS
======
Currently on hold. CGD was created as part of a Software Design class in python which is now over, so we don't have as much time to
work on it as we would like. Furthermore, some of the fundamental components of the architecture (such as the game loop and 
networking) were not implemented in a robust, scalable fashion, and would need to be modified before CGD could grow any further. 

RUNNING
=======
cd into /architecture
Modify broadcastServer.py and client.py so that they use the correct ip address.
Then, run client.py.

HOW CAN I FIGURE OUT WHAT YOUR SOURCE CODE DOES?
=================================================
We have tried to document the source code as well as possible in the time that we had, using the epytext 
(http://epydoc.sourceforge.net/manual-epytext.html) markup language. This type of markup lends itself to some very readable 
documentation that can be accessed through /docs/index.html. However, sadly, some of the documentation is probably out of date or lacking.


FUTURE
======
When we get a chance, we want to fix the networking and game loop code and rebuild CGD from the ground up as a full RTS.
In the meantime, there is nothing stopping anyone else from forking the project and addressing these problems themselves.
We will try to support anyone doing this as much as we are able.


LICENSE
=======
FreeBSD (Attribution by linking to this project on GitHub is fine)
