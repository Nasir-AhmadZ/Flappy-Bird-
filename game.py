from typing import Any
import pygame
from pygame.locals import *

pygame.init()

clock = pygame.time.Clock()#intializes the clock
fps = 60

screen_width  = 864;
screen_heigt = 936;

screen = pygame.display.set_mode((screen_width,screen_heigt))
pygame.display.set_caption('Flappy Bird')

#define game variables
ground_scroll = 0
scroll_speed = 4
flying = False
game_over = False
pipe_gap = 150
pipe_frequency = 1500 #milliseconds
last_pipe = pygame.time.get_ticks() - pipe_frequency


#load images
bg = pygame.image.load('img/bg.png') #background img
ground_img = pygame.image.load('img/ground.png') #ground img

class Bird(pygame.sprite.Sprite):
    def __init__(self,x,y):  
        pygame.sprite.Sprite.__init__(self)#this creates a sprite class
        self.images = []
        self.index = 0
        self.counter= 0
        for num in range (1,4):
            img = pygame.image.load(f'img/bird{num}.png')
            self.images.append(img)
            self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
        self.vel = 0
        self.clicked = False
        self.air = False

    def update(self):
        #gravity
        if flying == True:
            self.vel += 0.5
            if self.vel > 8:#limits the acceleration
                self.vel = 8
            if self.rect.bottom < 768: #creates a limit to the bottom
                self.rect.y += int(self.vel) #this adds it to the y co-ordinates of the bird

        if game_over == False:
            #jump mouse click
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                self.vel = -10
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

            #jump spacebar
            key = pygame.key.get_pressed()   
            if key[pygame.K_SPACE] and self.air==False:
                self.vel = -10
                self.air = True
            if not key[pygame.K_SPACE] and self.air==True:
                self.air = False
        


            #handle the animation
            self.counter += 1
            flap_cooldown = 5
        
            
            if self.counter > flap_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0
            self.image = self.images[self.index]

            #rotate the bird
            self.image = pygame.transform.rotate(self.images[self.index],self.vel*-2)
        else:
            self.image = pygame.transform.rotate(self.images[self.index],-90)

class Pipe(pygame.sprite.Sprite):
    def __init__(self,x,y,position) :
        pygame.sprite.Sprite.__init__(self) 
        self.image = pygame.image.load('img/pipe.png') 
        self.rect = self.image.get_rect()
        #position 1 is from the top, -1 is from the bottom
        if position == 1:
            self.image = pygame.transform.flip(self.image,False,True)
            self.rect.bottomleft = [x,y - int(pipe_gap/2)]
        if position == -1:
            self.rect.topleft = [x,y + int(pipe_gap/2)]
    
    def update(self):
        self.rect.x -= scroll_speed


bird_group = pygame.sprite.Group() #creates a group class for the bird
pipe_group = pygame.sprite.Group() #creates a group class for the pipes

flappy = Bird(100,int(screen_heigt/2)) #creates bird object
bird_group.add(flappy) #add object into the bird group



run = True
while run:

    clock.tick(fps)#sets the speed of the game

    #draw background
    screen.blit(bg,(0,0)) #this puts the background onto the screen

    bird_group.draw(screen)
    bird_group.update()
    pipe_group.draw(screen)
    pipe_group.update()

    #draw the ground
    screen.blit(ground_img,(ground_scroll,768))#this puts the ground onto the screen

    #check if bird has hit the ground
    if flappy.rect.bottom > 768:
        game_over = True
        flying = False

    if game_over == False:

        #generate new pipes
        time_now =  pygame.time.get_ticks()
        if time_now - last_pipe > pipe_frequency:
            pippy = Pipe(screen_width,int(screen_heigt/2,),-1) #bottom pipe
            pipboy =Pipe(screen_width,int(screen_heigt/2),1) #top pipe
            pipe_group.add(pippy) #add pippy object to the pipe group
            pipe_group.add(pipboy)
            last_pipe = time_now

        #scroll the ground
        ground_scroll -= scroll_speed
        if abs(ground_scroll)>35: #fakes the effect of scrolling background
            ground_scroll=0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and flying == False and game_over == False or event.type == pygame.KEYDOWN and flying == False and game_over == False:
            flying = True

    pygame.display.update()#allow the screen to update and display

pygame.quit()