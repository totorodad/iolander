#*************************************************************************************
# IO Lander: lander.py
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

#define colors
BG     = (0, 0, 0)
GREEN  = (0, 255, 0)
RED    = (255, 0, 0)
BLUE   = (0, 0, 255)
WHITE  = (255, 255, 255)
YELLOW = (255,255,0)
BLACK  = (0,0,0)

#create Lander class
class Lander(pygame.sprite.Sprite):
  def __init__(self):
    pygame.sprite.Sprite.__init__(self)
    landers = []

    # game over tracker
    self.game_over = False

    # keep collision status
    self.collision = False

    # lander postion data
    self.lander_images = pygame.image.load("assets/imgs/lander_sheet_53_43.png").convert_alpha()
    self.lander_no_thrust_image = self.lander_images.subsurface(0,0,53,43)
    self.image = self.lander_no_thrust_image
    self.image.set_colorkey(BG)
    self.rect = self.image.get_rect()
    self.rect.topleft = (0,0)
    self.mask = pygame.mask.from_surface(self.image)
    
    # Load the lander with left thrust 
    self.lander_left_thruster_image = self.lander_images.subsurface(1*53,0,53,43)
    self.lander_left_thruster_image.set_colorkey(BG)

    # Load the lander with left thrust 
    self.lander_right_thruster_image = self.lander_images.subsurface(2*53,0,53,43)
    self.lander_right_thruster_image.set_colorkey(BG)
    
    # Load the lander with left thrust 
    self.lander_bottom_thruster_image = self.lander_images.subsurface(3*53,0,53,43)
    self.lander_bottom_thruster_image.set_colorkey(BG)

    # Physics based variable (ignore z for now) [x,y,z]
    self.lander_g  = np.array([0,5,0])    # Assume gravity = 9.8 m/s2 (0 at the top so g = positive)
    self.lander_tr = np.array([0,0,0])    # tr=thrust accelleration vector
    self.lander_r  = np.array([50,20,0])  # r=position vector (initial potion is 50, 20)
    self.lander_v  = np.array([10,0,0])   # v=current lander velocity vector
    self.lander_dt = 0.01                 # This the discrete delta time to update the lander position

    #Set fuel level to 100%
    self.lander_fuel_level = 100.0

    #Set Lander score
    self.lander_score = 0

    #Set Lander lives
    self.lander_lives = 3

    #Crash status of Lander
    self.crashed_to_hard = False

    #Log the current velocty vector as heading (dot product of x and y velocity
    self.heading_velocity = 0

    #Scoring merit is based on how close to 0 velocity the lander is when landed
    self.scoring_merit = 0

    #Lander fuel bones is the score achieved in this level
    self.fuel_bonus = 0


  def update(self, screen_width, screen_height,chan1,left_right_thruster_fx,main_thruster_fx):

    self.LR_thruster_sound = left_right_thruster_fx
    self.M_thruster_sound = main_thruster_fx
    self.channel1 = chan1

    # Set inital thrust vector to only include gravity
    self.lander_tr = np.array([0,0,0])

    # set vehicle to no thrust image
    self.image = self.lander_no_thrust_image

    if (self.lander_fuel_level > 0 and self.collision == False):
      key = pygame.key.get_pressed()

      if key[pygame.K_LEFT]:
        self.image = self.lander_left_thruster_image
        self.lander_tr = np.array([10,0,0])
        if (self.lander_fuel_level > 0):
          self.lander_fuel_level -= 0.01 
        if (self.channel1.get_busy() == False):
          self.channel1.play(self.LR_thruster_sound, loops = -1)

      elif key[pygame.K_RIGHT]:
        self.image = self.lander_right_thruster_image
        self.lander_tr = np.array([-10,0,0])
        if (self.lander_fuel_level > 0):
          self.lander_fuel_level -= 0.01   
        if (self.channel1.get_busy() == False):
          self.channel1.play(self.LR_thruster_sound, loops = -1)
      
      elif key[pygame.K_UP] or key[pygame.K_DOWN]:
        self.image = self.lander_bottom_thruster_image
        self.lander_tr = np.array([0,-16.0,0])    
        if (self.lander_fuel_level > 0):
          self.lander_fuel_level -= 0.03   
        if (self.channel1.get_busy() == False):
          self.channel1.play(self.M_thruster_sound, loops = -1)
      else:
        self.channel1.stop()

    # Calculated Physics for lander
    if (self.collision == False):
      # add on gravity vector to thrust vector
      self.lander_tr = self.lander_tr + self.lander_g

      # computer new lander velocity
      self.lander_v = self.lander_v + self.lander_tr*self.lander_dt
     
      # Compute lander new position based on 
      self.lander_r = self.lander_r + self.lander_v*self.lander_dt
     
      # Grab x and y new positon for sprite rect
      self.rect.x = self.lander_r[0]
      self.rect.y = self.lander_r[1]

      # Detect Lander has got out of frame (too high)
      if (self.rect.y < -(self.lander_images.get_size()[1]-10)) :
        print (self.lander_r[1])
        self.lander_v[1] = 0
        self.lander_tr[1] = 0

      # Log the current velocity as the final velocity (find the resultant vector)
      self.heading_velocity = math.sqrt ((self.lander_v[0]*self.lander_v[0]) + (self.lander_v[1]*self.lander_v[1]))

    elif (self.collision == True):

      # set lander velocity to 0
      self.lander_v = np.array([0,0,0])

      #detect landed
      pad = self.islanded()

      if (self.crashed_to_hard == False):
        if (pad == 2):
          print ('Landed on pad 2X.  Winner')
          # Add to score
          self.lander_score += (self.scoring_merit * 2)
        elif (pad == 5):
          print ('Landed on pad 5x.  Winner')
          # Add to score
          self.lander_score += (self.scoring_merit * 5)
        elif (pad == 10):
          print ('Landed on pad 10x.  Winner')
          # Add to score
          self.lander_score += (self.scoring_merit * 10)
        elif (pad == 0):
          print ('You crashed.')

        # On successfull landing calculate how much fuel bonus to add based on socring merit which is landing velocity based.
        self.fuel_bonus = (self.scoring_merit)/100


      # let the user know they crashed to hard on a pad
      if (self.crashed_to_hard == True):
        if(pad > 0):
          print ('You landed to hard. Game over man.')
        else:
          print ('You crashed at high rate of velocity wow!.  Game over man.')
  
      self.lander_lives -= 1
      if (self.lander_lives == 0):
        self.game_over = True
    
  def islanded (self):
    # check 2x landing pad alignment
    if (self.rect.x >= 326 and (self.rect.x + 53) <= 446 and self.rect.y == 113-43):
      return (2)
    # check 5x landing pad alighnment
    elif (self.rect.x >= 82 and (self.rect.x + 53) <= 192 and self.rect.y == 396-43):
      return (5)
    # check 10x landing pad alighnment
    elif (self.rect.x >= 419 and (self.rect.x + 53) <= 498 and self.rect.y == 309-43):
      return (10)
    return (0) # no landing pad found
  
  def reset(self):
    self.lander_tr = np.array([0,0,0])    # tr=thrust accelleration vector
    self.lander_r  = np.array([50,20,0])  # r=position vector (initial potion is 50, 20)
    self.lander_v  = np.array([10,0,0])   # v=current lander velocity vector
    self.crashed_to_hard = False
    self.heading_velocity = 0