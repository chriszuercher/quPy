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

 
import time
import sys
import array

MUTE_GRP1_NOTE = 0x10
MUTE_GRP2_NOTE = 0x11
MUTE_GRP3_NOTE = 0x12
MUTE_GRP4_NOTE = 0x13

CHANNEL=1

DEV="/dev/midi"
#f = open(DEV, 'rb+')
f = open(DEV, 'wb')
 

# mute on
raw_msg_part1 = bytearray([0x9 + CHANNEL-1, MUTE_GRP2_NOTE, 0x40])
raw_msg_part2 = bytearray([0x8 + CHANNEL-1, MUTE_GRP2_NOTE, 0x00])
f.write(buffer(raw_msg_part1))
f.write(buffer(raw_msg_part2))
f.flush()

time.sleep(2)

# mute off
raw_msg_part1 = bytearray([0x9 + CHANNEL-1, MUTE_GRP2_NOTE, 0x40-1])
raw_msg_part2 = bytearray([0x8 + CHANNEL-1, MUTE_GRP2_NOTE, 0x00])
f.write(buffer(raw_msg_part1))
f.write(buffer(raw_msg_part2))
f.flush()

f.close()
