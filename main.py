#*************************************************************************************
# IO Lander:main.py
# 13-Sept-2024
# Authors: J&C Games
# totorodad@gmail.com
# Game Description:  This game is a knock of of a knock off of the old original 
# lander game.  This version is more like the VIC-20 release of the game which was a 
# knock off of the original vector coil op game.  This was my son and my first game 
# we wrote together using python and pygame.
#
# This is freeware.
#
#*************************************************************************************
#
# This games requires the files in the /assets folder:
# /assets/audio/left_rigth_thruster_fx.wav
# /assets/audio/main_thruster_fx.wav
# /assets/font/turok.ttf
# /assets/background.png
# /assets/lander_sheet_53_43.png
#*************************************************************************************

import pygame
import numpy as np
import math
from lander import *

pygame.init()

#define screen size
SCREEN_WIDTH = 640 
SCREEN_HEIGHT = 480

#create game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("IOLander")

#define colors
BG     = (0, 0, 0)
GREEN  = (0, 255, 0)
RED    = (255, 0, 0)
BLUE   = (0, 0, 255)
WHITE  = (255, 255, 255)
YELLOW = (255,255,0)
BLACK  = (0,0,0)

#load music and sounds
left_right_thruster_fx = pygame.mixer.Sound("assets/audio/left_right_thruster_fx.wav")
left_right_thruster_fx.set_volume(0.5)
channel1 = pygame.mixer.Channel(0)

main_thruster_fx = pygame.mixer.Sound("assets/audio/main_thruster_fx.wav")
main_thruster_fx.set_volume(0.5)

score_font = pygame.font.Font("assets/fonts/turok.ttf", 20)
speed_font = pygame.font.Font("assets/fonts/turok.ttf", 13)
game_over_font = pygame.font.Font("assets/fonts/turok.ttf", 72)

#function for drawing text
def draw_text(text, font, text_col, x, y):
  img = font.render(text, True, text_col)
  screen.blit(img, (x, y))

#create Game_Background class
class Game_Background(pygame.sprite.Sprite):
  def __init__(self, x, y):
    pygame.sprite.Sprite.__init__(self)
    self.image = pygame.image.load("assets/imgs/background.png").convert_alpha()
    self.image.set_colorkey(BG)
    self.rect = self.image.get_rect()
    self.rect.topleft = (x, y)
    self.mask = pygame.mask.from_surface(self.image)
    
def draw_velocity_gauge(lander_velocity):
  width = 18
  x1 = 615
  y1 = 24
  x2 = 615 + width
  y2 = 365
  center_y = y1 +((y2-y1)/2)
  yellowbox_height = 20

  velocity_magnatude = lander_velocity
  pygame.draw.rect(screen, GREEN, (x1,y1,x2-x1,y2-y1))
  pygame.draw.rect(screen, YELLOW,(x1,center_y,width,yellowbox_height))
  pygame.draw.line(screen, BLACK,(x1,center_y+lander_velocity), (x2,center_y+lander_velocity),5)
  Lander.scoring_merit = round((lander_velocity/20) * 740)

def draw_fuel_gauge(lander_fuel_level):
  fuel_ratio = int((lander_fuel_level/100.0) * 510.0)
  draw_text ('FUEL:',score_font,WHITE,15,450)
  pygame.draw.rect(screen,BLUE,(100,455,fuel_ratio,18))
  draw_text ('m/s',speed_font,WHITE,615,4)

def draw_score_lives():
  draw_text ('SCORE:  ' + str(Lander.lander_score),score_font,WHITE,15,434)
  draw_text (str(Lander.lander_lives),score_font,WHITE,615,456)


#hide mouse cursor
pygame.mouse.set_visible(False)

#create instances of Game_Background and Lander
Game_Background = Game_Background(0,0)
Lander = Lander()

#create Game_Background and Lander groups
Game_Background_group = pygame.sprite.Group()
Lander_group = pygame.sprite.Group()

#add instances to groups
Game_Background_group.add(Game_Background)
Lander_group.add(Lander)

# initialize the postion and variables for Lander
# Lander_group.update returns the gamevoer status
Lander_group.update(SCREEN_WIDTH, SCREEN_HEIGHT,channel1,left_right_thruster_fx,main_thruster_fx)

#game loop
run = True
while run:

  #update background
  screen.fill(BG)
  
  # Check for lander sprite to background sprite collision   
  if pygame.sprite.spritecollide(Lander, Game_Background_group, False, pygame.sprite.collide_mask):
    Lander.collision = True
    channel1.stop() # turn of the FX

    if (Lander.heading_velocity<20):
      Lander.crashed_to_hard = False
    else:
      Lander.crashed_to_hard = True
  else:
    Lander.collision = False

  # Lander_group.update returns the gamevoer status
  Lander_group.update(SCREEN_WIDTH, SCREEN_HEIGHT,channel1,left_right_thruster_fx,main_thruster_fx)

  #Draw Background (which is a sprite)
  Game_Background_group.draw(screen)

  #Draw Lander
  Lander_group.draw(screen)
  
  # Draw velocity gauge
  draw_velocity_gauge (Lander.heading_velocity) #pass the lander Y velocity only

  # Draw Score
  draw_score_lives()

  # Draw fuel gauge
  draw_fuel_gauge(Lander.lander_fuel_level)
  

  #Handel next Life or game over

  if ((Lander.game_over == False) and (Lander.collision == True)):
    pygame.time.wait(500)
    draw_text ('Next Round!',game_over_font,WHITE,150,(SCREEN_HEIGHT/2)-50)
    pygame.display.flip()
    pygame.time.wait(500)
    Lander.collision = False
    Lander.lander_fuel_level += Lander.fuel_bonus
    if (Lander.lander_fuel_level > 100.0):
      Lander.lander_fuel_level = 100.0

    Lander.reset()
    Lander_group.update(SCREEN_WIDTH, SCREEN_HEIGHT, channel1,left_right_thruster_fx,main_thruster_fx)  

  #Check for gameover
  if Lander.game_over == True:
    pygame.time.wait(500)
    draw_text ('GAME OVER',game_over_font,WHITE,150,(SCREEN_HEIGHT/2)-50)
    pygame.display.flip()
    pygame.time.wait(500)
    Lander.collision = False
    Lander.lander_lives = 3
    Lander.lander_fuel_level = 100.0
    Lander.reset()  
    Lander.game_over = False
    Lander.lander_score = 0
    Lander_group.update(SCREEN_WIDTH, SCREEN_HEIGHT,channel1,left_right_thruster_fx,main_thruster_fx)

  #event handler
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      run = False

  #update display
  pygame.display.flip()

pygame.quit()