"""
 *
 * Created on: 	1/14/2019
 * Author:		Chris Lindsay
 *
 *      Copyright (C) 2019 Christopher Lindsay
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
"""

import math, logging, threading
import pygame
from pygame.locals import *
from dial import *

#single interface for all dials on screen
class Panel:
	_namespace = {} #dictionary of attributes
	def __init__ (self, screen, parts = {}):
		self.__dict__ = Panel._namespace #get the attributes of Panel into a dictionary
		for k, v in parts.items(): #add to local via dictionary
			try:
				self.__dict__[k] = eval(v[0] + '()') #this creates a new kv pair and attribute object in Panel
			except: #currently unsupported object type
				logging.warning (threading.current_thread().name + "unsupported dial type")
				self.__dict__[k] = Dial()
		self._screen = screen #this is the pyGame screen
	def batch_pos(self ):
		#set positions of all dials in panel
		for k, v in data.items():
			self.__dict__[k].position(100, 100) #get the X and Y from argument dictionary
	def __getitem__(self, i): #allows [] opperator
		return self.__dict__[i]
	def __setitem__(self, i, value): #don't use this
		self.__dict__[i] = value
	def dp(self): #prints out the dictionary
		print(self.__dict__.items())
	def batch_update(self, data):
		for k, v in data.items():
			try:
				eval ("self.__dict__[k].update(self.screen, " + str(v[1:])[1:-1] + ")")
			except:
				pass #the screen attribute triggers this
