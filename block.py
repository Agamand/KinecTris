
import bge
from materials import *

CONST_HEIGHT = 20
CONST_WIDTH = 10

class Block
	def __init__(self):
		self.init_grid()

	def init_grid():
		colors = getColors()
		scene = bge.logic.getCurrentScene()
		for x in range(0, CONST_WIDTH):
			for y in range(0, CONST_HEIGHT)
				setMaterial(scene.objects['b_'+y+'_'+x],colors[0])



		