import pygame
import os
import random
from enum import Enum
from collections import namedtuple
pygame.font.init()

width,height = 1920,1080
FPS = 60
VEL = 12
CLR = 10
FOOD_AREA = 0.8
Grid = (192,108)

Hit_red = pygame.USEREVENT + 1
Hit_blue = pygame.USEREVENT + 2

font = pygame.font.SysFont('comicsans',40)
font2 = pygame.font.SysFont('comicsans',100)

Head_Image = pygame.image.load(os.path.join("Assets","head.png")) 
Apple_Image = pygame.image.load(os.path.join("Assets","apple.png")) 

space = pygame.transform.scale(pygame.image.load(os.path.join("Assets","space.png")),(width,height))


class Snake_Game :

    def __init__(self,w=width,h=height) :

        self.score = 0
        self.highscore = 0
        self.dir=0

        self.area = FOOD_AREA*Grid[0]*Grid[1]
        self.area = int(self.area)
        if(self.area==0) : self.area = 1
        
        self.width = w
        self.height = h

        self.w = self.width/Grid[0]
        self.h = self.height/Grid[1]

        self.Head_Image = pygame.transform.scale(Head_Image,(self.w,self.h)) 
        self.Apple_Image = pygame.transform.scale(Apple_Image,(self.w,self.h))
        
        self.win = pygame.display.set_mode((self.width,self.height))
        pygame.display.set_caption("Snake")
        
        self.reset()

        self.clock = pygame.time.Clock()

    def reset(self) : 
        if(self.score>self.highscore) : self.highscore = self.score
        self.score = 0
        self.snake = []
        self.head = [random.randint(1,Grid[0]),random.randint(1,Grid[1])]
        for i in range(self.dir) : 
            self.Head_Image = pygame.transform.rotate(self.Head_Image,-90)
        self.dir = random.randint(0,3) # 0:up 1:left 2:down 3:right
        for i in range(self.dir) : 
            self.Head_Image = pygame.transform.rotate(self.Head_Image,90)
        self.newdir = []
        self.food = []
        for i in range(self.area) : 
            self.place_food()
        self.run = True

    def draw_snake(self) :
        red = 0
        grn = 255
        blu = 0
        r = True
        g = False
        b = True 
        n = 0
        cyc = 0
        for block in self.snake : 
            pygame.draw.rect(self.win,(red,grn,blu),pygame.Rect(self.w*(block[0]-1),self.h*(block[1]-1),self.w,self.h))
            if(n+CLR>255) : 
                n = 0
                if(cyc!=1) : r = not r
                if(cyc!=2) : g = not g
                if(cyc!=3) : b = not b
                cyc+=1
                if(cyc==5) : cyc=0
            if(cyc!=1) : 
                if(r) : red+=CLR
                else : red-=CLR
            if(cyc!=2) : 
                if(g) : grn+=CLR
                else : grn-=CLR
            if(cyc!=3) : 
                if(b) : blu+=CLR
                else : blu-=CLR
            n+=CLR            
            # if(self.r>(255-CLR)) : self.neg = True
            # if(self.r<CLR) : self.neg = False
            # if self.neg : self.n-=CLR
            # else : self.n+=CLR

    def draw_window(self) : 
        self.win.blit(space,(0,0))
        for i in range(Grid[0]) : 
            pygame.draw.line(self.win,(25,25,25),(i*self.w,0),(i*self.w,self.height),1)
        for i in range(Grid[1]) : 
            pygame.draw.line(self.win,(25,25,25),(0,i*self.h),(self.width,i*self.h),1)
        score_text = font.render(f"Score : {str(self.score)}",1,(255,255,255))
        self.win.blit(score_text,(self.width-score_text.get_width()-10,10))
        self.win.blit(self.Head_Image,(int(self.w*(self.head[0]-1)),int(self.h*(self.head[1]-1))))
        self.draw_snake()
        for apple in self.food :
            self.win.blit(self.Apple_Image,(int(self.w*(apple[0]-1)),int(self.h*(apple[1]-1))))       
        pygame.display.update()

    def snake_move(self) : 
        over = False
        self.snake.insert(0,self.head.copy())
        if self.dir==0 : 
            if self.head[1]==1 : over = True
            else : self.head[1]-=1
        if self.dir==1 : 
            if self.head[0]==1 : over = True
            else : self.head[0]-=1
        if self.dir==2 : 
            if self.head[1]==Grid[1] : over = True
            else : self.head[1]+=1
        if self.dir==3 : 
            if self.head[0]==Grid[0] : over = True
            else : self.head[0]+=1
        if not self.check_eat() : self.snake.pop()  
        else : 
            self.place_food()
            self.score+=1
        if self.head in self.snake : over = True 
        if over : self.reset()

    def check_eat(self) : 
        eat = False
        for food in self.food : 
            if(self.head==food) : 
                self.food.remove(food)
                eat = True
                break 
        return eat

    def place_food(self) : 
        food = [random.randint(1,Grid[0]),random.randint(1,Grid[1])]
        while (food==self.head or food in self.snake or food in self.food) : food = [random.randint(1,Grid[0]),random.randint(1,Grid[1])]
        self.food.append(food) 
        

    def step(self) :

        for event in pygame.event.get() :
            if event.type == pygame.QUIT : 
                self.run = False
                pygame.quit()               
            if event.type == pygame.KEYDOWN:
                self.change = self.dir
                if(len(self.newdir)>0) : self.change = self.newdir[-1]
                if (event.key == pygame.K_LEFT and self.change!=3) :
                    self.newdir.append(1)
                elif (event.key == pygame.K_RIGHT and self.change!=1) :
                    self.newdir.append(3)
                elif (event.key == pygame.K_UP and self.change!=2) :
                    self.newdir.append(0)
                elif (event.key == pygame.K_DOWN and self.change!=0) :
                    self.newdir.append(2) 
            
        #reward = 0
        #over = False

        
        #winner = self.check_win()
        #keys_pressed = pygame.key.get_pressed()
        if(len(self.newdir)>0) : 
            self.rotate = self.newdir[0]-self.dir
            if(self.rotate==-3) : self.rotate = 1
            if(self.rotate==3) : self.rotate = -1
            self.Head_Image = pygame.transform.rotate(self.Head_Image,90*self.rotate)
            self.dir = self.newdir[0]
            del self.newdir[0]
        self.snake_move()
        self.draw_window()
        #rew = self.bullets_move(self.red,self.blue,self.bullets_red,self.bullets_blue)
        #if reward==0 : reward = rew

        #return reward,over,winner


if __name__ == '__main__':

    game = Snake_Game()

    try : 

        while game.run : 

            game.clock.tick(VEL)

            game.step()

    except : pass
    
    print(f"Highscore : {game.highscore}")

