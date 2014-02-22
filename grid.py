import bge
import GameLogic

from materials import *
from block import *
CONST_HEIGHT=20
CONST_WIDTH=10

class Grid():
	def __init__(self):
		self.activeObject = None
		self.colors = getColors()
		self.init_grid()

	def init_grid(self):
		self.setColor(0)

	def setColor(self,i):
		colors = self.colors
		scene = bge.logic.getCurrentScene()
		for x in range(0, CONST_WIDTH):
			for y in range(0, CONST_HEIGHT):
				setColor(scene.objects['b_'+str(y)+'_'+str(x)],colors[i])
	
	def setColorAt(self,pos,i):
		if pos[0] >= CONST_WIDTH or pos[0] < 0:
			return;
		if pos[1] >= CONST_HEIGHT or pos[1] < 0:
			return;
		scene = bge.logic.getCurrentScene()
		setColor(scene.objects['b_'+str(pos[1])+'_'+str(pos[0])],colors[i])

	def getInstance():
		if 'grid' in GameLogic.globalDict: 
			print('grid is already set')
		else:
			print('set grid')
			GameLogic.globalDict['grid'] = Grid()
		return GameLogic.globalDict['grid']


	def setActiveObject(self,obj):
		self.activeObject = obj
		me = obj
		pos = me.pos
		for x in range(0, me.width):
			for y in range(0, me.height):
				if me.cell[x][y] > 0 :
					self.setColorAt([pos[0]+x,pos[1]+y],me.color)
	def moveActiveObject(self):
		if self.activeObject is None:
			return
		scene = bge.logic.getCurrentScene()
		me = self.activeObject
		pos = me.pos
		print('obj pos : '+str(pos))
		for x in range(0, me.width):
			for y in range(0, me.height):
				if me.cell[x][y] > 0 :
					self.setColorAt([pos[0]+x,pos[1]+y],0)
		me.pos[1] = me.pos[1] + 1
		
		pos = me.pos
		for x in range(0, me.width):
			for y in range(0, me.height):
				if me.cell[x][y] > 0 :
					self.setColorAt([pos[0]+x,pos[1]+y],me.color)
					
	def update(self):
		self.moveActiveObject()



def main():
	Grid.getInstance().setActiveObject(Block(1,[4,0]))

def update():
	Grid.getInstance().update()


