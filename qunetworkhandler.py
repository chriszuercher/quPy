'''
Module/handler managing the MIDI-over-TCP/IP communication with 
a Qu-series console.
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


import socket
import time
from quevent import quEvent
from mythreading import synchronized
from midiparser import midiStreamParser
import config
import sys
import qurawmidi
from qumessagehandler import quMessageHandler
from midimessagehandler import midiMessageHandler

class quNetworkHandler(quMessageHandler, midiMessageHandler):
  
  # reconnect wait time in seconds
  RECONNECT_TIME = 1
  
  # timeout for waiting on socket requests/network traffic in seconds
  # (the qu16 will send keepalive every 0.3 secs)
  NETWORK_TIMEOUT = 0.35

  fx_sends = {
    quEvent.DELAY_TIME_FX1 : qurawmidi.FX1_SEND,
    quEvent.DELAY_TIME_FX2 : qurawmidi.FX2_SEND,
    quEvent.DELAY_TIME_FX3 : qurawmidi.FX3_SEND,
    quEvent.DELAY_TIME_FX4 : qurawmidi.FX4_SEND 
    }     
   
  mute_grp_on = {
    quEvent.MUTE_GRP1_ON : qurawmidi.MUTE_GRP1_NOTE,
    quEvent.MUTE_GRP2_ON : qurawmidi.MUTE_GRP2_NOTE,
    quEvent.MUTE_GRP3_ON : qurawmidi.MUTE_GRP3_NOTE,
    quEvent.MUTE_GRP4_ON : qurawmidi.MUTE_GRP4_NOTE
    }
  mute_grp_off = {
    quEvent.MUTE_GRP1_OFF : qurawmidi.MUTE_GRP1_NOTE,
    quEvent.MUTE_GRP2_OFF : qurawmidi.MUTE_GRP2_NOTE,
    quEvent.MUTE_GRP3_OFF : qurawmidi.MUTE_GRP3_NOTE,
    quEvent.MUTE_GRP4_OFF : qurawmidi.MUTE_GRP4_NOTE
    }
    
  lastMidiData = bytearray([0,0,0])
  lastMidiType = -1
  shutdownState = False
  
  def __init__(self, controller):
    super(quNetworkHandler, self).__init__(controller)
    self.online=False
    self.midiParser = midiStreamParser(config.QU_MIDI_CH)
    self.midiParser.registerHandler(self)
    self.initSocket()
    
  def getName(self):
    '''
    Returns "NET"
    '''
    return('NET')
  
  @synchronized 
  def initSocket(self):
    self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.socket.settimeout(self.NETWORK_TIMEOUT)
  
    
  def handleEvent(self, sender, event):
    '''
    Handles MUTE_GRP_ON/OFF, DELAY_TIME_FX, NET_KEEPALIVE and SYS_SHUTDOWN events.
    Ignores events from self and echoHandler.
    '''
    
    # don't handle my own events, also ignore echoHandler
    if ( sender == self or sender.getName() == "ECO"):
      return()
      
    # handle system events
    if (event.getType() == quEvent.SYS_SHUTDOWN):
      self.shutdownState = True
      self.netDisconnect()
      return()      
      
    # do keepalive
    if (event.getType() == quEvent.NET_KEEPALIVE):
      self.sendKeepAlive()
      return()
    
    ### other events
    # handle mute group ON
    if event.getType() in self.mute_grp_on.keys() : 
      self.write2net(qurawmidi.generateMuteGroupOn(self.mute_grp_on[event.getType()]))
    # handle mute group OFF:  
    elif event.getType() in self.mute_grp_off.keys() : 
      self.write2net(qurawmidi.generateMuteGroupOff(self.mute_grp_off[event.getType()]))
    # handle tap button events
    elif event.getType() in self.fx_sends.keys() :
      midiValues = qurawmidi.computeDelayValues(event.getArguments()[0])
      self.write2net(qurawmidi.generateDelayMsg(self.fx_sends[event.getType()], midiValues))
      
    # TODO: implement other messages here?
  
  @synchronized
  def write2net(self,msgByteArray):
    '''
    Sends a byte string (bytearray) over the TCP/IP connection and initializes
    a re-connect if communication fails (in that case, the byte string is discarded).
    '''
    try:
      self.socket.sendall(msgByteArray)
    # if something goes wrong, notify others and reconnect
    except socket.error as emsg:
      self.netDisconnect()
      if (not self.shutdownState):
        self.netConnect()
  
  @synchronized
  def netDisconnect(self):
    self.midiParser.reset()
    self.sendEvent(quEvent(quEvent.NET_OFFLINE, []))
    self.socket.close()
    self.online=False
        
  @synchronized
  def netConnect(self):
    '''
    Connects via TCP/IP to the Qu console, going into a re-connect loop if
    the console is not reachable.
    '''
    
    # might have been connected otherwise
    if (not self.online):
      # keep trying to connect constantly
      self.initSocket()
      while (not self.shutdownState):
        try:
	  #sys.stderr.write("NET: connecting\n");
	  self.socket.connect((config.QU_HOSTNAME, config.QU_PORT))
	  self.online = True
	  # ask the conosole to dump its status
	  self.socket.sendall(qurawmidi.generateSystemStateRequest())
	  break
        except socket.error as emsg:
	  #sys.stderr.write("NET: connect failed \n");
          self.online = False
          time.sleep(self.RECONNECT_TIME)

      # if we ever got here and we're not dying, we are online
      if (not self.shutdownState):
        self.sendEvent(quEvent(quEvent.NET_ONLINE, []))
      
  def sendKeepAlive(self):
    self.write2net( bytearray([0xFE]) )
    
  def handleMidiEvent(self, type, data):
    
    # TODO: implement tap delay values received from console here
    
    # FIXME: this should be in an extra class, since it is to be used also by other components
    # previous msg was note on, and note values are the same
    if ( type == midiStreamParser.NOTE_OFF and self.lastMidiType == midiStreamParser.NOTE_ON 
     and self.lastMidiData[1] == data[1]):
       ## check for volume value and adjust event data accordingly
       if (self.lastMidiData[2] < 0x40):
         muteGrp = self.mute_grp_off
       else:  
         muteGrp = self.mute_grp_on
       # search the event for that midi note
       for ev in muteGrp.keys():
	  if ( muteGrp[ev] == self.lastMidiData[1] ):
	    self.sendEvent(quEvent(ev, []))
      
    
    self.lastMidiData = data
    self.lastMidiType = type
    
  def run(self):
    '''
    This method must be run in a thread. It constantly reads input from TCP/IP
    that is sent b the Qu console and feeds the input into the MIDI parser.
    '''
    
    # send initial active sensing message, this will also pull the connection up
    self.sendKeepAlive()
    
    while( not self.shutdownState):
      # read one byte (inefficient, grrr)
      try:
        oneByte = self.socket.recv(1)
        self.midiParser.eatByte(ord(oneByte[0]))
      except socket.error as emsg:
	self.netDisconnect() # kill socket
	self.sendKeepAlive() # this should pull up the connection again
      
      # would do the listening here
    
    
    
    # check shutdownState in net reading loop    
    