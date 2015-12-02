# This file is party of quPy, a program that allows to remotely control
# digital mixing consoles of Allen&Heath's Qu series from a RaspberryPi.
# Copyright (C) 2014-2015  Niels Ott
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
 
from require import require 
 
# event definitions used by all handlers
class quEvent():
  
   @require(object, int, list)
   def __init__(self, myType, arguments):
     self.myType = myType
     self.arguments=arguments
     
   def getType(self):
     return self.myType
     
   def getArguments(self):
     return self.arguments
     
   def getName(self):
     return quEvent.getEventName(self.getType())
     
  
  # instead of a reverse mapping, go into "reflection"
  # and provide a function that turns event values into names again
   @staticmethod
   def getEventName(eventType) :
     for key, value in quEvent.__dict__.items():
       if (value == eventType):
 	return key
	
   @staticmethod
   def getEventNumber(name) :
     for key, value in quEvent.__dict__.items():
       if (key == name):
         return value

	
   MUTE_GRP1_ON  = 1
   MUTE_GRP1_OFF = 2
   MUTE_GRP2_ON  = 3
   MUTE_GRP2_OFF = 4
   MUTE_GRP3_ON  = 5
   MUTE_GRP3_OFF = 6
   MUTE_GRP4_ON  = 7
   MUTE_GRP4_OFF = 8
  
   TAP_FX1 = 20
   TAP_FX2 = 21
   TAP_FX3 = 22
   TAP_FX4 = 23
   
   DELAY_TIME_FX1 = 30
   DELAY_TIME_FX2 = 31
   DELAY_TIME_FX3 = 32
   DELAY_TIME_FX4 = 33
     
   SOFT_KEY1 = 50
   SOFT_KEY2 = 51
   SOFT_KEY3 = 52
   SOFT_KEY4 = 53

   NET_OFFLINE = 1000
   NET_ONLINE  = 1001
   NET_KEEPALIVE = 1002
  
   SYS_SHUTDOWN = 2000
   SYS_TEST = 2001
  
   UNKNOWN = -1
  