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

    def update(self):

        #handle the animation
        self.counter += 1
        flap_cooldown = 5
    
        
        if self.counter > flap_cooldown:
            self.counter = 0
            self.index += 1
            if self.index >= len(self.images):
                self.index = 0
        self.image = self.images[self.index]

bird_group = pygame.sprite.Group() #creates a group class

flappy = Bird(100,int(screen_heigt/2)) #creates object

bird_group.add(flappy) #add object into the bird group




run = True
while run:

    clock.tick(fps)#sets the speed of the game

    screen.blit(bg,(0,0)) #this puts the background onto the screen

    bird_group.draw(screen)
    bird_group.update()

    screen.blit(ground_img,(ground_scroll,768))#this puts the ground onto the screen
    ground_scroll -= scroll_speed
    if abs(ground_scroll)>35: #fakes the effect of scrolling background
        ground_scroll=0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()#allow the screen to update and display

pygame.quit()