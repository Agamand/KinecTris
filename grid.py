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
		self.cell = []
		self.init_grid()

	def init_grid(self):
		self.setColor(0)

	def setColor(self,i):
		colors = self.colors
		scene = bge.logic.getCurrentScene()
		for x in range(0, CONST_WIDTH):
			self.cell.append([])
			for y in range(0, CONST_HEIGHT):
				setColor(scene.objects['b_'+str(y)+'_'+str(x)],colors[i])
				self.cell[x].append(0)
	
	def setColorAt(self,pos,i):
		if pos[0] >= CONST_WIDTH or pos[0] < 0:
			return;
		if pos[1] >= CONST_HEIGHT or pos[1] < 0:
			return;
		scene = bge.logic.getCurrentScene()
		setColor(scene.objects['b_'+str(pos[1])+'_'+str(pos[0])],colors[i])
		#self.cell[pos[0]][pos[1]] = i

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
	def getColor(self,pos):
	
		if pos[0] >= CONST_WIDTH or pos[0] < 0:
			return 0;
		if pos[1] >= CONST_HEIGHT or pos[1] < 0:
			return 0;
		return self.cell[pos[0]][pos[1]]
	def addToCell(self):
		obj = self.activeObject
		for x in range(0, obj.width):
			for y in range(0, obj.height):
				if obj.cell[x][y] > 0 :
					self.cell[x+obj.pos[0]][y+obj.pos[1]] = obj.color
		self.activeObject = None
	def moveActiveObject(self):
		if self.activeObject is None:
			return
		scene = bge.logic.getCurrentScene()
		me = self.activeObject
		pos = me.pos

		if pos[1]+me.height+1 >= CONST_HEIGHT:
			self.addToCell()
			print("ok fuck1")
			return
		print('obj pos : '+str(pos))

		for x in range(0, me.width):
			for y in range(0, me.height):
				if me.cell[x][y] > 0 and self.getColor([pos[0]+x,pos[1]+y]) > 0:
					self.addToCell()
					print("ok fuck")
					return
					

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
		if self.activeObject is None:
			self.setActiveObject(Block(1,[4,0]))



def main():
	Grid.getInstance().setActiveObject(Block(1,[4,0]))

def update():
	Grid.getInstance().update()


