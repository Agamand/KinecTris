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
		self.b = 0
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
			return 1;
		if pos[1] >= CONST_HEIGHT or pos[1] < 0:
			return 1;
		return self.cell[pos[0]][pos[1]]
	def addToCell(self):
		obj = self.activeObject
		for x in range(0, obj.width):
			for y in range(0, obj.height):
				if obj.cell[x][y] > 0 :
					self.cell[x+obj.pos[0]][y+obj.pos[1]] = obj.color
		self.activeObject = None
		print('cell'+str(self.cell))
	def moveActiveObject(self):
		if self.move([0,1]) == 0:
			self.addToCell()
	def move(self,to):
	
		if self.activeObject is None:
			return 2
		scene = bge.logic.getCurrentScene()
		me = self.activeObject
		pos = me.pos

		if pos[1]+me.height >= CONST_HEIGHT:
			print("ok fuck1")
			return 0
		print('obj pos : '+str(pos))

		#for x in range(0, me.width):
			#for y in range(0, me.height):
				#if me.cell[x][y] > 0 and self.getColor([pos[0]+to[0]+x,pos[1]+to[1]+y]) > 0:
					#print("ok fuck")
					#return 0
		if self.testPattern(me.cell,me.width,me.height,[pos[0]+to[0],pos[1]+to[1]]) < 1:
			return 0			

		for x in range(0, me.width):
			for y in range(0, me.height):
				if me.cell[x][y] > 0 :
					self.setColorAt([pos[0]+x,pos[1]+y],0)
		me.pos[0] = me.pos[0] + to[0]
		me.pos[1] = me.pos[1] + to[1]
		
		pos = me.pos
		for x in range(0, me.width):
			for y in range(0, me.height):
				if me.cell[x][y] > 0 :
					self.setColorAt([pos[0]+x,pos[1]+y],me.color)
		return 1

	def update(self):
		self.moveActiveObject()
		if self.activeObject is None:
			self.spawn()


	def rotate(self,to):

		if self.activeObject is None:
			return 2

		scene = bge.logic.getCurrentScene()
		me = self.activeObject
		pos = me.pos

		next_pattern = me.getPattern(to)
		print("next pattern"+str(next_pattern))
		if self.testPattern(next_pattern[0],me.width,me.height,[pos[0],pos[1]]) < 1:
			return 0

		for x in range(0, me.width):
			for y in range(0, me.height):
				if me.cell[x][y] > 0 :
					self.setColorAt([pos[0]+x,pos[1]+y],0)


		me.setPattern(to)

		for x in range(0, me.width):
			for y in range(0, me.height):
				if me.cell[x][y] > 0 :
					self.setColorAt([pos[0]+x,pos[1]+y],me.color)


	def spawn(self):
		self.setActiveObject(Block(getPattern()[self.b]))
		self.b = self.b + 1
		if self.b > 6:
			self.b = 0




	def testPattern(self,pattern,h,w,pos):
		for x in range(0, w):
			for y in range(0, h):
				if pattern[x][y] > 0 and self.getColor([pos[0]+x,pos[1]+y]) > 0:
					return 0
		return 1



def main():
	Grid.getInstance().spawn()

def update():
	Grid.getInstance().update()

def move(v):
	Grid.getInstance().move(v)

def onLeft():
	move([-1,0])
def onRight():
	move([1,0])

def onUp():
	Grid.getInstance().rotate(1)

def onBottom():
	Grid.getInstance().move([0,1])

