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
# a very simplistic event-based/driven MIDI parser
# that cares only about NoteOn and NoteOff stuff
# 
import sys
import binascii
from midimessagehandler import midiMessageHandler
from require import require

class midiStreamParser(object):
  
  NOTE_ON = 1
  NOTE_OFF = 2
  
  # midiChannel = [1..16]
  def __init__(self, midiChannel):
    self.reset()
    self.handlers = []
    self.onByte = 0x90 + (midiChannel-1)
    self.offByte = 0x80 + (midiChannel-1)
    self.currentMsgType = -1
    
  @require(object, midiMessageHandler)  
  def registerHandler(self, h):
    self.handlers.append(h)
  
  def callHandlers(self, msgType):
    # volume 0 of note on -> is note off
    if (msgType == self.NOTE_ON and self.buf[2] == 0):
      msgType = self.NOTE_OFF
    
    for h in self.handlers:
      h.handleMidiEvent(msgType, self.buf)
  
  def reset(self):
    self.buf =  bytearray([])
    self.insideSysex = False
    self.insideMsg = False
    self.twoByteMsg = False
    self.currentMsgType = -1

  # this is where the magic happens
  def eatByte(self,b):
    #sys.stderr.write(str(type(b)))
    
    
    # yiha, state machine
    if (self.insideMsg):
      #sys.stderr.write(".")
      #sys.stderr.write(binascii.hexlify(chr(b)))
      
      if (len(self.buf) == 1):
	#sys.stderr.write("1")
	self.buf.append(b)
	if (self.twoByteMsg):
	  insideMsg = False
      elif (len(self.buf) == 2):
	#sys.stderr.write("2")
	self.buf.append(b)
	if (self.currentMsgType == self.NOTE_ON or self.currentMsgType == self.NOTE_OFF):
	  self.callHandlers(self.currentMsgType)
	if ( not self.insideSysex ):  
	  self.insideMsg = False
      elif (len(self.buf) == 3):
	#sys.stderr.write("!")
	if (b == 0xF7):
	  self.insideSysex = False
	  self.insideMsg = False
    else:
       #sys.stderr.write("+")
       #sys.stderr.write(binascii.hexlify(chr(b)))
        
       # new messages begins, reset
       self.reset()
      
       # catch one byte messages:
       # active sensing, clock stuff, etc
       if ( (b >= 0xF8 and b <= 0xFF ) or b==0xF4 or b==0xF5 ): 
         pass
       else:
	 self.insideMsg = True
	 self.buf.append(b)
	 # two-byte messages:
	 if ( (b >= 0xC0 and b <= 0xCF) or
	      (b >= 0xD0 and b <= 0xDF) or
	       b == 0xF3 or b == 0xF1 or b == 0xF6  ):
	   self.twoByteMsg = True
	 # sysex begins
         elif (b == 0xF0): 
           #sys.stderr.write("SYSEX")
           self.insideSysex = True
         # all others are three byte messages but we care only  about note on and note off
         elif ( b == self.onByte ): 
	   self.currentMsgType = self.NOTE_ON
         elif ( b == self.offByte ):
	   self.currentMsgType = self.NOTE_OFF
