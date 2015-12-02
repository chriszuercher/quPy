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


import alsaseq
import alsamidi
import time
import sys

MUTE_GRP1_NOTE = 0x10
MUTE_GRP2_NOTE = 0x11
MUTE_GRP3_NOTE = 0x12
MUTE_GRP4_NOTE = 0x13

FX1_SEND = 0x00
FX2_SEND = 0x01
FX3_SEND = 0x02
FX4_SEND = 0x03

CHANNEL=1

# connect to qu-16 usb
#alsaseq.connectto( 0, 28, 0 )

alsaseq.client( 'quPy', 1, 1, False )
#alsaseq.connectfrom( 0, 28, 0 )
#qu16_conn = alsaseq.connectto( 1, 11, 0 ) # qu16
#alsaseq.connectto( 1, 28, 0 ) # qu16
#sys.stderr.write(str(qu16_conn) + "\n")

alsaseq.connectto( 1, 129, 0 ) # midi monitor

alsaseq.start()

# send tap
#alsaseq.output( (alsaseq.SND_SEQ_EVENT_NONREGPARAM, 1, 0, 1, (0,0), (0,0), (0,0), (CHANNEL-1,
#0xB0 + (CHANNEL-1), 0x63, FX2_SEND)) )
#alsaseq.output( (alsaseq.SND_SEQ_EVENT_NONREGPARAM, 1, 0, 1, (0,0), (0,0), (0,0), (CHANNEL-1,
#0xB0 + (CHANNEL-1), 0x62, 0x48)) )
#alsaseq.output( (alsaseq.SND_SEQ_EVENT_NONREGPARAM, 1, 0, 1, (0,0), (0,0), (0,0), (CHANNEL-1,
#0xB0 + (CHANNEL-1), 0x05, 0x00)) )
#alsaseq.output( (alsaseq.SND_SEQ_EVENT_NONREGPARAM, 1, 0, 1, (0,0), (0,0), (0,0), (CHANNEL-1,
#0xB0 + (CHANNEL-1), 0x26, 0x05)) )
#time.sleep(0.5)
#alsaseq.output( (alsaseq.SND_SEQ_EVENT_NONREGPARAM, 1, 0, 1, (0,0), (0,0), (0,0), (CHANNEL-1,
#0xB0 + (CHANNEL-1), 0x63, FX2_SEND)) )
#alsaseq.output( (alsaseq.SND_SEQ_EVENT_NONREGPARAM, 1, 0, 1, (0,0), (0,0), (0,0), (CHANNEL-1,
#0xB0 + (CHANNEL-1), 0x62, 0x48)) )
#alsaseq.output( (alsaseq.SND_SEQ_EVENT_NONREGPARAM, 1, 0, 1, (0,0), (0,0), (0,0), (CHANNEL-1,
#0xB0 + (CHANNEL-1), 0x05, 0x00)) )
#alsaseq.output( (alsaseq.SND_SEQ_EVENT_NONREGPARAM, 1, 0, 1, (0,0), (0,0), (0,0), (CHANNEL-1,
#0xB0 + (CHANNEL-1), 0x26, 0x05)) )

#while(True):
#  alsaseq.output( (alsaseq.SND_SEQ_EVENT_NONREGPARAM, 1, 0, 1, (0,0), (0,0), (0,0), (0x63, FX2_SEND)) )
#  alsaseq.output( (alsaseq.SND_SEQ_EVENT_NONREGPARAM, 1, 0, 1, (0,0), (0,0), (0,0), (0x62, 0x48)) )
#  alsaseq.output( (alsaseq.SND_SEQ_EVENT_NONREGPARAM, 1, 0, 1, (0,0), (0,0), (0,0), (0x05, 0x00)) )
#  alsaseq.output( (alsaseq.SND_SEQ_EVENT_NONREGPARAM, 1, 0, 1, (0,0), (0,0), (0,0), (0x26, 0x05)) )
#  time.sleep(0.5)

#alsaseq.output( (6, 1, 0, 1, (5, 0), (0, 0), (0, 0), (0, 60, 127, 0, 100)) )  
  
alsaseq.output( (alsaseq.SND_SEQ_EVENT_NONREGPARAM, 1, 0, alsamidi.SND_SEQ_QUEUE_DIRECT, (0, 0), (0, 0), (0, 0), (0xB0 + (CHANNEL-1), 0x63, FX2_SEND,   0xB0 + (CHANNEL-1), 0x62, 0x48,   0xB0 + (CHANNEL-1), 0x05,0x00,   0xB0 + (CHANNEL-1), 0x26,0x05)) )   


time.sleep(1000)


# mute group 2 -> muted
msg_part1 = alsamidi.noteonevent(CHANNEL-1, MUTE_GRP2_NOTE, 0x40)
msg_part2 = alsamidi.noteoffevent(CHANNEL-1, MUTE_GRP2_NOTE, 0)
alsaseq.output(msg_part1)
alsaseq.output(msg_part2)

time.sleep(2)

# mute group 2 -> unmuted
msg_part1 = alsamidi.noteonevent(CHANNEL-1, MUTE_GRP2_NOTE, 0x40-1)
msg_part2 = alsamidi.noteoffevent(CHANNEL-1, MUTE_GRP2_NOTE, 0)
alsaseq.output(msg_part1)
alsaseq.output(msg_part2)



time.sleep(1000)