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


#
# handler for that sends all incoming messages 
# to controller again
#
# this should be done by the Qu16 over the network,
# but for debugging without network, one can use this as a substitute.
#

#from quevent import quEvents
from qumessagehandler import quMessageHandler

import time
from mythreading import synchronized
import sys

class echoHandler(quMessageHandler):
  
  def __init__(self, controller):  
    super(echoHandler, self).__init__(controller)
    
  # must not be synchronized here, otherwise reaching deadlock state
  def handleEvent(self, sender, event):
    if (sender != self):
      self.controller.handleEvent(self, event)
      
  def getName(self):
    return('ECO')    
