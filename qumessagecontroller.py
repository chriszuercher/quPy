'''
Central message controller for passing around
events in the entire systen.
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
from qumessagehandler import quMessageHandler
from quevent import quEvent

class quMessageController(object):
  
  handlers = []
  
  def __init__(self):
    pass
  
  # register a handler for any events
  @require(object,quMessageHandler)
  def registerHandler(self, handler):
      self.handlers.append(handler)
  
  # accept and event and call all handlers, also the sender itself
  @require(object,quMessageHandler, quEvent)
  def handleEvent(self, sender, event):
    for h in self.handlers:
	h.handleEvent(sender,event)
