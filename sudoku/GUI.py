import os
from pygments import highlight
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from copy import deepcopy
import pygame
from threading import Thread

getChar=lambda k:str(k) if k <10 else chr(ord('A')+k-10)
class Visualizer:
    def __init__(self,solver,origtable):
        pygame.font.init()

        # Constant
        self.x,self.y=0,0        
        self.cellsize = 60
        self.orig=deepcopy(origtable)
        self.solver=solver
        self.table=solver.table
        self.n=solver.n
        self.smn=solver.smn
        self.W=self.cellsize*self.n
        self.font = pygame.font.SysFont("comicsans", 30)
        self.col={
            'highlight':(255,0,0),
            'cell':(173, 216, 230),
            'cell2':(105, 105, 105),
            'line':(0,0,0)
        }
        self.cnt=0
        self.demomode=0

        self.screen = pygame.display.set_mode((self.W, self.W))
        pygame.display.set_caption("Visualizer %dx%d"%(self.n,self.n))
        
    def draw_box(self):
        sz=self.cellsize
        col=self.col['highlight']
        x,y=self.x,self.y
        thick=7
        for i in range(2):
            pygame.draw.line(self.screen, col, (x*sz-3, (y+i)*sz), (x*sz+sz+3,(y+i)*sz),thick)
            pygame.draw.line(self.screen, col, ((x+i)*sz, y*sz), ((x+i)*sz,(y+1)*sz),thick)
    
    def draw(self):
        cellcol=self.col['cell']
        cellcol2=self.col['cell2']
        sz=self.cellsize
        linecol=self.col['line']
        for i in range (self.n):
            for j in range (self.n):
                if self.table[j][i]!= 0:
                    if not self.orig[j][i]:
                        pygame.draw.rect(self.screen,cellcol, (i*sz,j*sz,sz+1,sz+1))
                        text1 = self.font.render(getChar(self.table[j][i]), 1, (0, 0, 0))
                        self.screen.blit(text1, (i*sz+15,j*sz+15))
                    else:
                        pygame.draw.rect(self.screen,cellcol2, (i*sz,j*sz,sz+1,sz+1))
                        text1 = self.font.render(getChar(self.table[j][i]), 1, (255, 255, 255))
                        self.screen.blit(text1, (i*sz+15,j*sz+15))
                    
        for i in range(self.n+1):
            if i % self.smn == 0 :
                thick = 7
            else:
                thick = 1
            pygame.draw.line(self.screen, linecol, (0, i * sz), (self.W, i * sz), thick)
            pygame.draw.line(self.screen, linecol, (i * sz, 0), (i * sz, self.W), thick)     
    
    def getXY(self,pos):
        self.x = pos[0]//self.cellsize
        self.y = pos[1]//self.cellsize
 
    def solve(self):
        pygame.event.pump() 
        def func(r,c):
            self.x,self.y=c,r
            if self.demomode==1:
                self.demomode=0
                while self.demomode==0:
                    pass
            else:
                pygame.time.delay(100)
            self.cnt+=1
        re=self.solver.solve(0,func)
        if re:
            print("Solved")
            print("Node count: %d"%self.cnt)
        else:
            print("Couldn't solved")

    def run(self):
        run = True
        boxflag,solveflag=0,0
        while run:
            self.screen.fill((255, 255, 255))
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False 
                if event.type == pygame.MOUSEBUTTONDOWN:
                    boxflag = 1
                    pos = pygame.mouse.get_pos()
                    self.getXY(pos)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.demomode=2
                        if solveflag==0: solveflag = 1  
                    if event.key == pygame.K_SPACE:
                        self.demomode=1
                        if solveflag==0: solveflag = 1  
                    
            if solveflag == 1:
                thread=Thread(target=self.solve)
                thread.start()
                solveflag = 2
                boxflag = 2
            
            self.draw()
            
            if  boxflag:
                self.draw_box()    
                if  boxflag==1: 
                    self.solver.infoCell(self.y,self.x)
                    boxflag = 2
            pygame.display.update() 

        pygame.quit()    
