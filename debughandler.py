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
# Debug handler: Prints all incoming events (except those from self) to STDERR,
# waits for commands or any event name on STDIN and sends events typed in
# to the controller
#
 
from quevent import quEvent
import sys
from mythreading import synchronized
from qumessagehandler import quMessageHandler

class debugHandler(quMessageHandler):
  
  def __init__(self, controller):
    super(debugHandler, self).__init__(controller)
    #self-register
    sys.stderr.write("Debug handler commands: exit, test, or any event name\n")
  
  # handling events: simply dropping their senders and names to STDERR
  @synchronized
  def handleEvent(self, sender, event):
    # always ignore self, ECO will do the rest
    if (sender == self):
      return()

    sys.stderr.write("%s : %s %s\n" % (sender.getName(), event.getName(), event.getArguments() ) )
    
    
  def getName(self):
    return('DEB')
  
  # --> this method should be run in a thread
  # debug handler simply asks for STDIN commands in its thread
  def run(self):
    while True:
      input = sys.stdin.readline()
      if (input.strip() == "exit"):
	self.sendEvent(quEvent(quEvent.SYS_SHUTDOWN, []))
	break
      elif (input.strip() == "test") :
	self.sendEvent(quEvent(quEvent.SYS_TEST, []))
      else:
        event = quEvent.getEventNumber(input.strip())
        if (event == __doc__):
	  sys.stderr.write("Unknown event name\n")
	else:  
          self.sendEvent(quEvent(event, []))
        