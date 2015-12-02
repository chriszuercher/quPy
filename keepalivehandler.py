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
# sending keepalive messages is simply done by this handler in its own thread
#
# only sends messages if nothing has happend for a while,
# but ignoring messages from NET since they are usually incoming all the time.
#

from quevent import quEvent
import time
from mythreading import synchronized
from qumessagehandler import quMessageHandler
 
class keepAliveHandler(quMessageHandler):
  
  # send keepalive signal to everybody every n seconds:
  KEEPALIVE_TIME = 4

  shutdownState = False
  internalInterval = 0.1
  sleepCounter = 0
    
  
  def __init__(self, controller):
    super(keepAliveHandler, self).__init__(controller)
  
  # handling events: reset keepalive counter on every event
  @synchronized
  def handleEvent(self, sender, event):
    # always ignore event from self to avoid loops. ECO will send what I need.
    if (sender == self):
      return
    if (event.getType() == quEvent.SYS_SHUTDOWN):
      self.shutdownState = True
    # ignore other (incoming) NET messages
    if (sender.getName() != "NET"):  
      self.sleepCounter = 0  
    
  def getName(self):
    return('KAL')
  
  # --> this method should be run in a thread
  def run(self):
    while (True):
      time.sleep(self.internalInterval)
      self.sleepCounter += self.internalInterval
      if (self.shutdownState):
	break
      if (self.sleepCounter > self.KEEPALIVE_TIME):
	self.sendEvent(quEvent(quEvent.NET_KEEPALIVE, []))
      
