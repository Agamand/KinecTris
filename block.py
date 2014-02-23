
import bge
from materials import *

class Block():
	def __init__(self,c,width,height,cell,pos, variants = []):
		self.width = width
		self.height = height
		self.cell = cell
		self.color = c
		self.pos = pos


blocks = []

#Cube
blocks.append(Block(1,2,2,[[1,1],[1,1]],[4,0]))

#L reversed
blocks.append(Block(2,3,3,[[1,0,0],[1,1,1],[0,0,0]],[3,0], [[[0,1,1],[0,1,0],[0,1,0]],[[0,0,1],[0,0,1],[0,1,1]]]))

#S shape
blocks.append(Block(3,3,3,[[0,1,1],[1,1,0],[0,0,0]],[3,0], [[[1,0,0],[1,1,0],[0,1,0]]]))

#Z shape
blocks.append(Block(4,3,3,[[1,1,0],[0,1,1],[0,0,0]],[3,0], [[[0,0,1],[0,1,1],[1,0,0]]]))

#T shape
blocks.append(Block(5,3,3,[[1,1,1],[0,1,0],[0,0,0]],[3,0], [[[1,0,0],[1,1,0],[1,0,0]],[[0,0,0],[0,1,0],[1,1,1]],[[0,0,1],[0,1,1],[0,0,1]]]))

#L shape
blocks.append(Block(6,3,3,[[1,1,1],[1,0,0], [0,0,0]],[3,0], [[[1,0,0],[1,0,0], [1,1,0]],[[0,1,1],[0,0,1], [0,0,1]]]))

#Sraight shape
blocks.append(Block(6,4,4,[[1,1,1,1], [0,0,0,0], [0,0,0,0], [0,0,0,0]],[2,0],[[[1,0,0,0], [1,0,0,0], [1,0,0,0], [1,0,0,0]]]))


def getBlocks():
	return blocks

print('Import blocks')
