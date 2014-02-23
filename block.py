
import bge
from materials import *



class Pattern():
	def __init__(self,c,width,height,cell,pos):
		self.width = width
		self.height = height
		self.cell = cell
		self.color = c
		self.size = len(cell)
		self.initPos = [pos[0],pos[1]]


class Block():
	def __init__(self,pattern):
		self.width = pattern.width
		self.height = pattern.height
		self.cell = pattern.cell[0]
		self.current = 0
		self.color = pattern.color
		self.pattern = pattern
		self.pos = [pattern.initPos[0],pattern.initPos[1]]
		print("spawn at "+str(self.pos))
	def getPattern(self, index):
		i = self.current+index;
		if i < 0:
			i = self.pattern.size-i
		i = i%self.pattern.size
		return [self.pattern.cell[i],i]

	def setPattern(self, index):
		pattern = self.getPattern(index)
		self.current = pattern[1]
		self.cell = pattern[0]


blocks = []

#Cube
blocks.append(Pattern(1,2,2,[[[1,1],[1,1]]],[4,0]))

#L reversed
blocks.append(Pattern(2,3,3,[[[0,1,1],[0,1,0],[0,1,0]],[[0,0,0],[1,1,1],[0,0,1]],[[0,1,0],[0,1,0],[1,1,0]],[[1,0,0],[1,1,1],[0,0,0]]],[3,0]))

#S shape
blocks.append(Pattern(3,3,3,[[[1,0,0],[1,1,0],[0,1,0]],[[0,1,1],[1,1,0],[0,0,0]]],[3,0]))

#Z shape
blocks.append(Pattern(4,3,3,[[[0,0,1],[0,1,1],[0,1,0]],[[1,1,0],[0,1,1],[0,0,0]]],[3,0]))

#T shape
blocks.append(Pattern(5,3,3,[[[0,1,0],[0,1,1],[0,1,0]],[[0,1,0],[1,1,1],[0,0,0]],[[0,1,0],[1,1,0],[0,1,0]],[[0,0,0],[1,1,1],[0,1,0]]],[3,0]))

#L shape
blocks.append(Pattern(6,3,3,[[[0,1,0],[0,1,0],[0,1,1]], [[0,0,1],[1,1,1], [0,0,0]],[[1,1,0],[0,1,0], [0,1,0]],[[0,0,0],[1,1,1], [1,0,0]]],[3,0]))

#Sraight shape
blocks.append(Pattern(7,4,4,[[[0,1,0,0], [0,1,0,0], [0,1,0,0], [0,1,0,0]],[[1,1,1,1], [0,0,0,0], [0,0,0,0], [0,0,0,0]]],[3,0]))


def getPattern():
	return blocks

print('Import blocks')
