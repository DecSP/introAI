import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from copy import deepcopy
import pygame
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

        self.screen = pygame.display.set_mode((self.W, self.W))
        pygame.display.set_caption("Visualizer %dx%d"%(self.n,self.n))
        
    def say(self,s,pos):
        text1 = self.font.render(s, 1, (0, 0, 0))
        self.screen.blit(text1, pos)
    
    # Highlight the cell selected
    def draw_box(self):
        sz=self.cellsize
        col=self.col['highlight']
        x,y=self.x,self.y
        thick=7
        for i in range(2):
            pygame.draw.line(self.screen, col, (x*sz-3, (y+i)*sz), (x*sz+sz+3,(y+i)*sz),thick)
            pygame.draw.line(self.screen, col, ((x+i)*sz, y*sz), ((x+i)*sz,(y+1)*sz),thick)
    
    # Function to draw required lines for making Sudoku grid        
    def draw(self):
        cellcol=self.col['cell']
        cellcol2=self.col['cell2']
        sz=self.cellsize
        linecol=self.col['line']
        for i in range (self.n):
            for j in range (self.n):
                if self.table[j][i]!= 0:
                    # Fill color in already numbered grid
                    if not self.orig[j][i]:
                        pygame.draw.rect(self.screen,cellcol, (i*sz,j*sz,sz+1,sz+1))
                        text1 = self.font.render(getChar(self.table[j][i]), 1, (0, 0, 0))
                        self.screen.blit(text1, (i*sz+15,j*sz+15))
                    else:
                        pygame.draw.rect(self.screen,cellcol2, (i*sz,j*sz,sz+1,sz+1))
                        text1 = self.font.render(getChar(self.table[j][i]), 1, (255, 255, 255))
                        self.screen.blit(text1, (i*sz+15,j*sz+15))
                    
        # Draw lines horizontally and verticallyto form grid          
        for i in range(self.n+1):
            if i % self.smn == 0 :
                thick = 7
            else:
                thick = 1
            pygame.draw.line(self.screen, linecol, (0, i * sz), (self.W, i * sz), thick)
            pygame.draw.line(self.screen, linecol, (i * sz, 0), (i * sz, self.W), thick)     
    
    def get_cord(self,pos):
        self.x = pos[0]//self.cellsize
        self.y = pos[1]//self.cellsize
 
    def solve(self):
        pygame.event.pump() 
        def func(r,c):
            self.x,self.y=c,r
            # white color background
            self.screen.fill((255, 255, 255))
            self.draw()
            self.draw_box()
            pygame.display.update()
            pygame.time.delay(100)
            self.cnt+=1
            if self.cnt%1000==0:
                print("Nodes count: %d"%self.cnt)
        return self.solver.solve(0,func)

    def run(self):
        run = True
        flag1=0
        flag2=0
        # The loop thats keep the window running
        while run:
            # White color background
            self.screen.fill((255, 255, 255))
            
            # Loop through the events stored in event.get()
            for event in pygame.event.get():
                # Quit the game window
                if event.type == pygame.QUIT:
                    run = False 
                # Get the mouse position to insert number   
                if event.type == pygame.MOUSEBUTTONDOWN:
                    flag1 = 1
                    pos = pygame.mouse.get_pos()
                    self.get_cord(pos)
                # Get the number to be inserted if key pressed   
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.x-= 1
                        flag1 = 1
                    if event.key == pygame.K_RIGHT:
                        self.x+= 1
                        flag1 = 1
                    if event.key == pygame.K_UP:
                        self.y-= 1
                        flag1 = 1
                    if event.key == pygame.K_DOWN:
                        self.y+= 1
                        flag1 = 1   
                    if event.key == pygame.K_RETURN:
                        if flag2==0: flag2 = 1  
                    
            if flag2 == 1:
                if self.solve():
                    print("Solved")
                    print("Node count: %d"%self.cnt)
                else:
                    print("Couldn't solved")
                flag2 = 2   
            self.draw() 
            if flag1:
                self.draw_box()    
                if flag1==1: 
                    self.solver.infoCell(self.y,self.x)
                    flag1=2

            # Update window
            pygame.display.update() 

        # Quit pygame window   
        pygame.quit()    
