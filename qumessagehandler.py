'''
Module/class that is an abstract/base implementation of a message handler
used by the quMessageController
'''

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
from abc import ABCMeta, abstractmethod
from quevent import quEvent

class quMessageHandler(object):
  __metaclass__ = ABCMeta

  # FIXME: object as controller is too vague here
  @require(object, object)
  def __init__(self, controller):
    self.controller=controller 
    self.controller.registerHandler(self)
    
  @require(object, quEvent)  
  def sendEvent(self, eventToSend):
    self.controller.handleEvent(self,eventToSend)    
  
  # FIXME: object as sender is too vague here
  @abstractmethod
  @require(object, object, quEvent)
  def handleEvent(self, sender, event):
    pass
