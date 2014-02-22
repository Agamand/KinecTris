import bge

from materials import *

CONST_HEIGHT=20
CONST_WIDTH=10

class Grid():
	def __init__(self):
		self.init_grid()

	def init_grid(self):
		colors = getColors()
		scene = bge.logic.getCurrentScene()
		for x in range(0, CONST_WIDTH):
			for y in range(0, CONST_HEIGHT):
				setColor(scene.objects['b_'+str(y)+'_'+str(x)],colors[0])




grid = Grid()


