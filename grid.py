import bge
import GameLogic
import random
from materials import *
from block import *

CONST_HEIGHT=20
CONST_WIDTH=10

CONST_SIZE_PREVIEW = 4

class Grid():

    def __init__(self):
        self.activeObject = None
        self.colors = getColors()
        self.cell = []
        self.nextBlock = Block(random.choice(getPattern()))
        self.isRunning = True
        self.init_grid()


    def init_grid(self):
        self.setColor(0)
    def setColor(self,i):
        colors = self.colors
        scene = bge.logic.getCurrentScene()
        for y in range(0, CONST_HEIGHT):
            self.cell.append([])
            for x in range(0, CONST_WIDTH):
                setColor(scene.objects['b_'+str(y)+'_'+str(x)],colors[i])
                self.cell[y].append(0)
    

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
            return 1
        if pos[1] >= CONST_HEIGHT or pos[1] < 0:
            return 1
        return self.cell[pos[1]][pos[0]]

    def addToCell(self):
        obj = self.activeObject
        for x in range(0, obj.width):
            for y in range(0, obj.height):
                if obj.cell[x][y] > 0 :
                    self.cell[y+obj.pos[1]][x+obj.pos[0]] = obj.color
        self.activeObject = None
        print('cell'+str(self.cell))

    def moveActiveObject(self):
        if self.move([0,1]) == 0:
            self.addToCell()
    def move(self,to):

        if self.isRunning == False:
            return

        if self.activeObject is None:
            return 2
        scene = bge.logic.getCurrentScene()
        me = self.activeObject
        pos = me.pos

        #if pos[1]+me.height >= CONST_HEIGHT:
        #    print("ok fuck1")
        #    return 0
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
        if self.isRunning == False:
            return

        self.moveActiveObject()
        if self.activeObject is None:
            self.spawn()


    def rotate(self,to):
        if self.isRunning == False:
            return

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

        if self.isRunning == False:
            return

        self.removeFullLine()

        newBlock = self.nextBlock

        if self.testPattern(newBlock.cell,newBlock.width,newBlock.height,newBlock.pos) < 1:
            print('game end !')
            self.isRunning = False
            return

        self.setActiveObject(newBlock)
        self.nextBlock = Block(random.choice(getPattern()))
        self.setNext();

    def setNext(self):
        scene = bge.logic.getCurrentScene()
        colors = self.colors
        me = self.nextBlock
        for y in range(0, CONST_SIZE_PREVIEW):
            for x in range(0, CONST_SIZE_PREVIEW):
                print('p_'+str(y)+'_'+str(x))
                if x < me.width and y < me.height:
                    if me.cell[x][y] > 0 :
                        setColor(scene.objects['p_'+str(y)+'_'+str(x)],colors[me.color])
                    else:
                        setColor(scene.objects['p_'+str(y)+'_'+str(x)],colors[0])
                else: 
                    setColor(scene.objects['p_'+str(y)+'_'+str(x)],colors[0])

    def removeFullLine(self):
        for y in range(0, CONST_HEIGHT):
            full = True
            for x in range(0, CONST_WIDTH):           
                if self.cell[y][x] < 1 :
                    full = False
            if full:
                print("remove "+str(y)+" line")
                del self.cell[y]
                self.cell.insert(0,[])
                for x in range(0, CONST_WIDTH):
                    self.cell[0].append(0)

        for y in range(0, CONST_HEIGHT):
            self.cell.append([])
            for x in range(0, CONST_WIDTH):
                self.setColorAt([x,y],self.cell[y][x])
                    

    def testPattern(self,pattern,h,w,pos):
        print('test at '+str(pos))
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

def onKey():
    keyboard = bge.logic.keyboard
    JUST_ACTIVATED = bge.logic.KX_INPUT_JUST_ACTIVATED
    if keyboard.events[bge.events.ZKEY] == JUST_ACTIVATED:
        Grid.getInstance().rotate(1)
    if keyboard.events[bge.events.QKEY] == JUST_ACTIVATED:
        move([-1,0])
    if keyboard.events[bge.events.DKEY] == JUST_ACTIVATED:
        move([1,0])
    if keyboard.events[bge.events.SKEY]:
        Grid.getInstance().move([0,1])
