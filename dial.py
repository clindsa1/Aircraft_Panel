#!/usr/bin/python
"""
 * dial.py
 * 
 * Created on: 1 Nov 2010
 * Author:     Duncan Law
 * Updated on: 13 Dec 2018
 * Author:     Christopher Lindsay
 * 
 *      Copyright (C) 2010 Duncan Law
 *      Copyright (C) 2018-2019 Christopher Lindsay
 *      This program is free software; you can redistribute it and/or modify
 *      it under the terms of the GNU General Public License as published by
 *      the Free Software Foundation; either version 2 of the License, or
 *      (at your option) any later version.
 *
 *      This program is distributed in the hope that it will be useful,
 *      but WITHOUT ANY WARRANTY; without even the implied warranty of
 *      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *      GNU General Public License for more details.
 *
 *      You should have received a copy of the GNU General Public License
 *      along with this program; if not, write to the Free Software
 *      Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
 *
 *      Thanks to Chootair at http://www.codeproject.com/Members/Chootair 
 *      for the inspiration and the artwork that i based this code on.
 *      His full work is intended for C# and can be found here:
 *      http://www.codeproject.com/KB/miscctrl/Avionic_Instruments.aspx
 * Requires pyGame to run.
 * http://www.pygame.org
"""

import math, logging, threading
import pygame
from pygame.locals import *

BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
YELLOW   = ( 255, 255,   0) #transparent

class Dial:
   """
   Generic dial type.
   """
   def __init__(self, image, frameImage, x=0, y=0, w=0, h=0):
       """
       x,y = coordinates of top left of dial.
       w,h = Width and Height of dial.
       """
       self.x, self.y = x, y
       self.image = image
       self.frameImage = frameImage
       self.dial = pygame.Surface(self.frameImage.get_rect()[2:4])
       self.dial.fill(0xFFFF00)
       if(w==0):
          w = self.frameImage.get_rect()[2]
       if(h==0):
          h = self.frameImage.get_rect()[3]
       self.w, self.h = w, h
       self.pos = self.dial.get_rect()
       self.pos = self.pos.move(x, y)

   def position(self, x, y):
       """
       Reposition top,left of dial at x,y.
       """
       self.x, self.y = x, y
       self.pos[0] = x 
       self.pos[1] = y 

   def position_center(self, x, y):
       """
       Reposition centre of dial at x,y.
       """
       self.x, self.y = x, y
       self.pos[0] = x - self.pos[2]/2
       self.pos[1] = y - self.pos[3]/2

   def rotate(self, image, angle):
       """
       Rotate supplied image by "angle" degrees.
       This rotates round the centre of the image. 
       If you need to offset the centre, resize the image using self.clip.
       This is used to rotate dial needles and probably doesn't need to be used externally.
       """
       tmpImage = pygame.transform.rotate(image ,angle)
       imageCentreX = tmpImage.get_rect()[0] + tmpImage.get_rect()[2]/2
       imageCentreY = tmpImage.get_rect()[1] + tmpImage.get_rect()[3]/2

       targetWidth = tmpImage.get_rect()[2]
       targetHeight = tmpImage.get_rect()[3]

       imageOut = pygame.Surface((targetWidth, targetHeight))
       imageOut.fill(0xFFFF00)
       imageOut.set_colorkey(0xFFFF00)
       imageOut.blit(tmpImage,(0,0), pygame.Rect( imageCentreX-targetWidth/2,imageCentreY-targetHeight/2, targetWidth, targetHeight ) )
       return imageOut

   def clip(self, image, x=0, y=0, w=0, h=0, oX=0, oY=0):
       """
       Cuts out a part of the needle image at x,y position to the correct size (w,h).
       This is put on to "imageOut" at an offset of oX,oY if required.
       This is used to centre dial needles and probably doesn't need to be used externally.       
       """
       if(w==0):
           w = image.get_rect()[2]
       if(h==0):
           h = image.get_rect()[3]
       needleW = w + 2*math.sqrt(oX*oX)
       needleH = h + 2*math.sqrt(oY*oY)
       imageOut = pygame.Surface((needleW, needleH))
       imageOut.fill(0xFFFF00)
       imageOut.set_colorkey(0xFFFF00)
       imageOut.blit(image, (needleW/2-w/2+oX, needleH/2-h/2+oY), pygame.Rect(x,y,w,h))
       return imageOut

   def overlay(self, image, x, y, r=0):
       """
       Overlays one image on top of another using 0xFFFF00 (Yellow) as the overlay colour.
       """
       x -= (image.get_rect()[2] - self.dial.get_rect()[2])/2
       y -= (image.get_rect()[3] - self.dial.get_rect()[3])/2
       image.set_colorkey(0xFFFF00)
       self.dial.blit(image, (x,y))

class Generic(Dial):
   """
   Generic Dial. This is built on by other dials.
   """
   def __init__(self, x=0, y=0, w=0, h=0):
       """
       Initialise dial at x,y.
       Default size of 300px can be overidden using w,h.       
       """
       self.image = pygame.image.load('resources/AirSpeedNeedle.png').convert()
       self.frameImage = pygame.image.load('resources/Indicator_Background.png').convert()
       Dial.__init__(self, self.image, self.frameImage, x, y, w, h)
   def update(self, screen, angleX, iconLayer=0):
       """
       Called to update a Generic dial.
       "angleX" and "angleY" are the inputs.
       "screen" is the surface to draw the dial on.       
       """
       angleX %= 360
       angleX = 360 - angleX
       tmpImage = self.clip(self.image, 0, 0, 0, 0, 0, -35)
       tmpImage = self.rotate(tmpImage, angleX)
       self.overlay(self.frameImage, 0,0)
       if iconLayer:
          self.overlay(iconLayer[0],iconLayer[1],iconLayer[2])
       self.overlay(tmpImage, 0, 0)
       self.dial.set_colorkey(0xFFFF00)
       screen.blit( pygame.transform.scale(self.dial,(self.w,self.h)), self.pos )

class Altimeter(Dial):
	def __init__ (self, x=0, y=0, w=0, h=0):
		self.longNeedle = pygame.image.load('resources/LongNeedleAltimeter.png').convert()
		self.smallNeedle = pygame.image.load('resources/SmallNeedleAltimeter.png').convert()
		self.frameImage = pygame.image.load('resources/Altimeter_Background.png').convert()
		self.font = pygame.font.Font('freesansbold.ttf', 30)
		self.base, self.alt = 0, 0
		Dial.__init__(self, self.longNeedle, self.frameImage, x, y, w, h)
		logging.debug (threading.current_thread().name + " Altimeter CREATED")
	
	def __str__ (self):
		return "Altimeter"
		
	def update(self, screen, altitude, presure =-1):
		self.alt = altitude
		if (presure >= 0):
			self.base = presure
		small_angle = int((long(self.alt) % 1000) * 0.3600360036)
		large_angle = int(long(self.alt) * 0.03600360036)
						
		tmpSmall = self.clip(self.smallNeedle, 0, 0, 0, 0, 0, -35)
		tmpSmall = self.rotate(tmpSmall, 360 - small_angle)
		tmpLarge = self.clip(self.longNeedle, 0, 0, 0, 0, 0, -35)
		tmpLarge = self.rotate(tmpLarge, 360 - large_angle)
		
		if (self.base >= 0):
			#need to figure out how to clear background of text
			textBitmap = self.font.render(str(self.base), False, WHITE)

		self.overlay(self.frameImage, 0, 0)
		self.overlay(tmpLarge, 0, 0)
		self.overlay(tmpSmall, 0, 0)
		if (self.base >= 0):
			self.overlay(textBitmap, -80,0)
		self.dial.set_colorkey(0xFFFF00)
		screen.blit( pygame.transform.scale(self.dial,(self.w,self.h)), self.pos )

class AirSpeed(Dial):
	def __init__ (self, x=0, y=0, w=0, h=0):
		self.image = pygame.image.load('resources/AirSpeedNeedle.png').convert()
		self.frameImage = pygame.image.load('resources/AirSpeedIndicator_Background.png').convert()
		Dial.__init__(self, self.image, self.frameImage, x, y, w, h)
		logging.debug (threading.current_thread().name + " AirSpeed CREATED")

	def __str__ (self):
		return "AirSpeed"
			
	def update(self, screen, speed):	
		tmpImage = self.clip(self.image, 0, 0, 0, 0, 0, -40)
		tmpImage = self.rotate(tmpImage, 180 - speed * 0.3600360036)

		self.overlay(self.frameImage, 0,0)
		self.overlay(tmpImage, 0, 0)
		self.dial.set_colorkey(0xFFFF00)
		screen.blit( pygame.transform.scale(self.dial,(self.w,self.h)), self.pos )

class VerticalSpeed(Dial):
	def __init__(self, x=0, y=0, w=0, h=0):
		self.image = pygame.image.load('resources/VerticalSpeedNeedle.png').convert()
		self.frameImage = pygame.image.load('resources/VerticalSpeedIndicator_Background.png').convert()
		Dial.__init__(self, self.image, self.frameImage, x, y, w, h)
	
	def update(self, screen, speed):
		#need a way to clip speed in -6 to 6
		tmpImage = self.clip(self.image, 0, 0, 0, 0, 0, -35)
		tmpImage = self.rotate(tmpImage, 90 - (speed * 30))
		
		self.overlay(self.frameImage, 0,0)
		self.overlay(tmpImage, 0, 0)
		self.dial.set_colorkey(0xFFFF00)
		screen.blit( pygame.transform.scale(self.dial,(self.w,self.h)), self.pos )

class Heading(Dial):
	def __init__(self, x=0, y=0, w=0, h=0):
		self.image = pygame.image.load('resources/HeadingWheel.png').convert()
		self.frameImage = pygame.image.load('resources/HeadingIndicator_Background.png').convert()
		self.maquetteImage = pygame.image.load('resources/HeadingIndicator_Aircraft.png').convert()
		Dial.__init__(self, self.image, self.frameImage, x, y, w, h)
		logging.debug (threading.current_thread().name + " Heading CREATED")

	def update(self, screen, angle):
		angle %= 360
		tmpImage = self.clip(self.image, 0, 0, 0, 0)
		tmpImage = self.rotate(tmpImage, angle)
		
		self.overlay(self.frameImage, 0,0)
		self.overlay(tmpImage, 0, 0)
		self.overlay(self.maquetteImage, 0,0)
		self.dial.set_colorkey(0xFFFF00)
		screen.blit( pygame.transform.scale(self.dial,(self.w,self.h)), self.pos )

class Horizon(Dial):
   """
   Artificial horizon dial.
   """
   def __init__(self, x=0, y=0, w=0, h=0):
       """
       Initialise dial at x,y.
       Default size of 300px can be overidden using w,h.
       """
       self.image = pygame.image.load('resources/Horizon_GroundSky.png').convert()
       self.frameImage = pygame.image.load('resources/Horizon_Background.png').convert()
       self.maquetteImage = pygame.image.load('resources/Maquette_Avion.png').convert()
       self.angleX, self.angleY = 0, 0
       Dial.__init__(self, self.image, self.frameImage, x, y, w, h)
       logging.debug (threading.current_thread().name + " Horizon CREATED")
   def __str__ (self):
		return "Horizon"
   def update(self, screen, X, Y):
       """
       Called to update an Artificial horizon dial.
       "angleX" and "angleY" are the inputs.
       "screen" is the surface to draw the dial on.
       """
       self.angleX, self.angleY = X, Y
       #angleX, angleY = orient.split()
       self.angleX %= 360
       self.angleY %= 360
       if (self.angleX > 180):
           self.angleX -= 360 
       if (self.angleY > 90)and(self.angleY < 270):
           selfangleY = 180 - self.angleY 
       elif (self.angleY > 270):
           self.angleY -= 360
       tmpImage = self.clip(self.image, 0, (59-self.angleY)*720/180, 250, 250)
       tmpImage = self.rotate(tmpImage, self.angleX)
       self.overlay(tmpImage, 0, 0)
       self.overlay(self.frameImage, 0,0)
       self.overlay(self.maquetteImage, 0,0)
       self.dial.set_colorkey(0xFFFF00)
       screen.blit( pygame.transform.scale(self.dial,(self.w,self.h)), self.pos )

class TurnCoord(Dial):
   """
   Turn Coordinator dial.
   """
   def __init__(self, x=0, y=0, w=0, h=0):
       """
       Initialise dial at x,y.
       Default size of 300px can be overidden using w,h.
       """
       self.image = pygame.image.load('resources/TurnCoordinatorAircraft.png').convert()
       self.frameImage = pygame.image.load('resources/TurnCoordinator_Background.png').convert()
       self.marks = pygame.image.load('resources/TurnCoordinatorMarks.png').convert()
       self.ball = pygame.image.load('resources/TurnCoordinatorBall.png').convert()
       Dial.__init__(self, self.image, self.frameImage, x, y, w, h)
       logging.debug (threading.current_thread().name + " TurnCoord CREATED")
       
   def update(self, screen, angleX, angleY):
       """
       Called to update a Turn Coordinator dial.
       "angleX" and "angleY" are the inputs.
       "screen" is the surface to draw the dial on.       
       """
       angleX %= 360 
       angleY %= 360
       if (angleX > 180):
           angleX -= 360 
       if (angleY > 180):
           angleY -= 360
       if(angleY > 14): 
           angleY = 14
       if(angleY < -14): 
           angleY = -14
       tmpImage = self.clip(self.image, 0, 0, 0, 0, 0, -12)
       tmpImage = self.rotate(tmpImage, angleX)
       self.overlay(self.frameImage, 0,0)
       self.overlay(tmpImage, 0, 0)
       tmpImage = self.clip(self.marks, 0, 0, 0, 0, 0, 0)
       self.overlay(tmpImage, 0, 80)
       tmpImage = self.clip(self.ball, 0, 0, 0, 0, 0, 300)
       tmpImage = self.rotate(tmpImage, angleY)
       self.overlay(tmpImage, 0, -220)
       self.dial.set_colorkey(0xFFFF00)
       screen.blit( pygame.transform.scale(self.dial,(self.w,self.h)), self.pos )

class Battery(Generic):
   """
   Battery dial.
   """
   def __init__(self, x=0, y=0, w=0, h=0):
       """
       Initialise dial at x,y.
       Default size of 300px can be overidden using w,h.
       """
       self.icon = pygame.image.load('resources/battery2.png').convert()
       Generic.__init__(self, x, y, w, h)
       self.frameImage = pygame.image.load('resources/ledgend.png').convert()
       logging.debug (threading.current_thread().name + " Battery CREATED")
   def update(self, screen, angleX):
       """
       Called to update a Battery dial.
       "angleX" is the input.
       "screen" is the surface to draw the dial on.       
       """
       if angleX > 100:
          angleX = 100
       elif angleX < 0:
          angleX = 0
       angleX *= 2.7
       angleX -= 135
       Generic.update(self, screen, angleX, (self.icon, 0, 100))

class RfSignal(Generic):
   """
   RF Signal dial.
   """
   def __init__(self, x=0, y=0, w=0, h=0):
       """
       Initialise dial at x,y.
       Default size of 300px can be overidden using w,h.
       """
       self.image = pygame.Surface((0,0))
       self.frameImage = pygame.image.load('resources/RF_Dial_Background.png').convert()
       Dial.__init__(self, self.image, self.frameImage, x, y, w, h)
       logging.debug (threading.current_thread().name + " RfSignal CREATED")
   def update(self, screen, inputA, inputB, scanPos):
       """
       "screen" is the surface to draw the dial on.       
       """
       top = self.dial.get_rect()[0] +60
       left = self.dial.get_rect()[1] +30
       bottom = self.dial.get_rect()[0] + self.dial.get_rect()[2] -60
       right = self.dial.get_rect()[1] + self.dial.get_rect()[3] -30
       height = bottom - top
       middle = height/2 + top
       scanPos %= right -30
       scanPos += 30
       inputA %= 100
       inputB %= 100
       inputA = height * inputA / 200
       inputB = height * inputB / 200
       pygame.draw.line(self.dial, 0xFFFFFF, (scanPos,top), (scanPos,bottom), 1)
       pygame.draw.line(self.dial, 0x222222, (scanPos-1,top), (scanPos-1,bottom), 1)
       pygame.draw.line(self.dial, 0x00FFFF, (scanPos-1,middle-inputA), (scanPos-1,middle),4)
       pygame.draw.line(self.dial, 0xFF00FF, (scanPos-1,bottom-inputB), (scanPos-1,bottom),4)
       pygame.draw.line(self.dial, 0xFFFF00, (scanPos-1,middle), (scanPos-1,middle))
       self.overlay(self.frameImage, 0,0)
       self.dial.set_colorkey(0xFFFF00)
       screen.blit( pygame.transform.scale(self.dial,(self.w,self.h)), self.pos )
