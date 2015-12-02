"""
Handler module for creating DELAY_TIME_FX events from TAP_FX events.
"""
#
# message handler that deals with tap time
#


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


from qumessagehandler import quMessageHandler

import time
from mythreading import synchronized
import sys
import qurawmidi
from quevent import quEvent

class tapTimer(object):
  ''' 
  class that encapsulates the determining the time between two taps, taking care of 
  minimum and maximum delay times.
  '''
  
  
  # initialize with maximum time between two taps (float)
  def __init__(self, maxSeconds, minSeconds):
    '''
    Initialize with maximum delay time and minimum delay time (seconds as float)
    '''
    self.maxSeconds = maxSeconds
    self.minSeconds = minSeconds
    self.lastTap = 0
    self.time = -1
 
  @synchronized
  def tap(self):
    '''
    Handles a tap event and updates the interal delay  time
    '''
    now = time.time()
    delta = now - self.lastTap
    if ( delta > self.maxSeconds or delta < self.minSeconds ):
      self.time = -1
    else:
      self.time = delta
    
    self.lastTap = now
  
  def getTime(self):  
    '''
    Returns the delay time in seconds computed by this class or -1 if there is no valid
    delay time (too long or too short delay)
    '''
    return(self.time)
    

class tapTimeHandler(quMessageHandler):

  # tap delay timers
  timers = {
    quEvent.TAP_FX1 : tapTimer(qurawmidi.MAX_DELAY_TIME, qurawmidi.MIN_DELAY_TIME),
    quEvent.TAP_FX2 : tapTimer(qurawmidi.MAX_DELAY_TIME, qurawmidi.MIN_DELAY_TIME),
    quEvent.TAP_FX3 : tapTimer(qurawmidi.MAX_DELAY_TIME, qurawmidi.MIN_DELAY_TIME),
    quEvent.TAP_FX4 : tapTimer(qurawmidi.MAX_DELAY_TIME, qurawmidi.MIN_DELAY_TIME) 
    }
  events = {
    quEvent.TAP_FX1 : quEvent.DELAY_TIME_FX1,
    quEvent.TAP_FX2 : quEvent.DELAY_TIME_FX2,
    quEvent.TAP_FX3 : quEvent.DELAY_TIME_FX3,
    quEvent.TAP_FX4 : quEvent.DELAY_TIME_FX4
    }
    

  def __init__(self, controller):  
    super(tapTimeHandler, self).__init__(controller)
    
  def handleEvent(self, sender, event):
    '''
    Handles incoming TAP events, ignores events from self and echoHandler
    '''
    if (sender == self or sender.getName() == "ECO"):
      return()
    
    if ( event.getType() in self.timers.keys() ):
      self.timers[event.getType()].tap()
      delay = self.timers[event.getType()].getTime()
      # if there is a usable delay, send it out
      if ( delay > 0 ):
	self.sendEvent(quEvent(self.events[event.getType()], [delay]))
  
      
  def getName(self):
    '''
    Returns "TAP"
    '''
    return('TAP')    
