
import bge
from materials import *

class Block():
	def __init__(self,c,pos):
		self.width = 2
		self.height = 2
		self.cell = [[1,1],[1,1]]
		self.color = c
		self.pos = pos;


		