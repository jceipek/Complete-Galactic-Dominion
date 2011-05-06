
from visual import *
from emmath import *
from charges import *
from visual.graph import *	 # import graphing features
#from visual.controls import *
from panel import Panel
from control import Panel2
from display import *


vfield=Display()
panel=Panel2()
panel.field=vfield
vfield.panel=panel

panel.start()
