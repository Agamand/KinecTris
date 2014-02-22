import bge
import GameLogic

from materials import *

CONST_HEIGHT=20
CONST_WIDTH=10

class Grid():
	def __init__(self):
		self.init_grid()
		self.text = 'trololo'

	def init_grid(self):
		colors = getColors()
		scene = bge.logic.getCurrentScene()
		for x in range(0, CONST_WIDTH):
			for y in range(0, CONST_HEIGHT):
				setColor(scene.objects['b_'+str(y)+'_'+str(x)],colors[0])
	def setColors(seft):
		print(seft.text)
		colors = getColors()
		scene = bge.logic.getCurrentScene()
		for x in range(0, CONST_WIDTH):
			for y in range(0, CONST_HEIGHT):
				setColor(scene.objects['b_'+str(y)+'_'+str(x)],colors[4])

def main():
	if 'grid' in GameLogic.globalDict: 
		print('grid is already set')
		GameLogic.globalDict['grid'].setColors();
	else:
		print('set grid')
		GameLogic.globalDict['grid'] = Grid()


