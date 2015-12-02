'''
Module hosting functions that are needed create or analyze MIDI messages
sent to and received from the Qu(-16).
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


import config
import math
#import sys
#import binascii
 
MUTE_GRP1_NOTE = 0x50
MUTE_GRP2_NOTE = 0x51
MUTE_GRP3_NOTE = 0x52
MUTE_GRP4_NOTE = 0x53  

FX1_SEND = 0x00
FX2_SEND = 0x01
FX3_SEND = 0x02
FX4_SEND = 0x03

# maximum delay time that the Qu can do in seconds
MAX_DELAY_TIME = 1.360
MIN_DELAY_TIME = 0.005

def computeDelayValues(delaySeconds):
  '''
  Returns a tuple with MIDI parameter values representing the given delay (seconds as float).
  Returns (0x00,0x00) if delay time is below minimum time.
  (0x7F, 0x7F) if it is above maximum delay time.
  '''
  
  # shortcut for the borderline values
  if (delaySeconds <= MIN_DELAY_TIME):
    return( (0x00, 0x00) )
  if (delaySeconds >= MAX_DELAY_TIME):
    return( (0x7F, 0x7F) )
  
  mSec = delaySeconds * 1000
  
  # the next three lines are according to the specs from A&H, 30 June 2014, 15:19
  M = round( 16383 * (math.log10(mSec) - math.log10(5)) / 2.4346 )
  VAc = M // 128
  VAf = M % 128
  
  return( (int(VAc), int(VAf)) )
 

def generateMuteGroupOff(groupNote):
  '''
  Generates MIDI messages that unmute a channel or mute group.
  '''
  return(bytearray(
      [0x90 + config.QU_MIDI_CH-1, groupNote, 0x40-1, 
      0x80 + config.QU_MIDI_CH-1, groupNote, 0x00]))
      
def generateMuteGroupOn(groupNote):
  '''
  Generates MIDI messages that mute a channel or mute group.
  '''
  return(bytearray(
      [0x90 + config.QU_MIDI_CH-1, groupNote, 0x40, 
      0x80 + config.QU_MIDI_CH-1, groupNote, 0x00]))
      


def generateDelayMsg(FXnum, coarseAndFine):
  '''
  Create MIDI messages (NRPNs) that set the delay time of the FX engine given by
  FXnum, using the tuple returned by #computeDelayValues(delaySeconds).
  '''
  VAc = coarseAndFine[0]
  VAf = coarseAndFine[1]
  return(bytearray(
     [0xB0 + config.QU_MIDI_CH-1, 0x63, FXnum,
     0xB0 +  config.QU_MIDI_CH-1,  0x62, 0x49,
     0xB0 +  config.QU_MIDI_CH-1,  0x06, VAf,
     0xB0 +  config.QU_MIDI_CH-1,  0x26, 0x05, #0x05 <- left tap, right: 0x07
     0xB0 +  config.QU_MIDI_CH-1, 0x63, FXnum,
     0xB0 +  config.QU_MIDI_CH-1,  0x62, 0x48,
     0xB0 +  config.QU_MIDI_CH-1,  0x06, VAc,
     0xB0 +  config.QU_MIDI_CH-1,  0x26, 0x05]) ) #0x05 <- left tap, right: 0x07
     
def generateSystemStateRequest():
  '''
  Generates a SysEx MIDI message that requests a status dump from the Qu16.
  '''
  # TODO: what about other Qu desks here?
  return(bytearray(
   [0xF0,               # sysex start
   0x00, 0x00, 0x1A,    # A&H manufacturer ID
   0x50, 0x11,          # qu16 ID
   0x01, 0x00,          # major/minor version
   config.QU_MIDI_CH-1, # midi channel
   0x10,                # request system state
   0x00,                # iPadFlag flag off
   0xF7]))              # sysex end
   

  