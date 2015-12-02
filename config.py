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


from quevent import quEvent



### general configuration

# GPIO handler

# Pin definitions - this is not GPIO numbers here, but pins on the socket
BTN1_PIN = 3
BTN2_PIN = 5
BTN3_PIN = 7
BTN4_PIN = 19 # actually my hardware has only 3 buttons, so this is untested

LED1_PIN = 8
LED2_PIN = 10
LED3_PIN = 11
LED4_PIN = 21 # actually my hardware has only 3 buttons, so this is untested

CONN_LED_PIN = 13 # connection status LED
SPARE = 15 # just for the sake of completeness

# invert on/off for buttons?
INV1 = True
INV2 = True
INV3 = True
INV4 = True


# Actions for buttons
# TODO: this should be in some kind of list/array, not fixed names
BTN1_MODE = "toggle" # "toggle" or "oneshot" or "off"
BTN1_ON_ACTION = quEvent.MUTE_GRP2_ON
BTN1_OFF_ACTION = quEvent.MUTE_GRP2_OFF

BTN2_MODE = "toggle" # "toggle" or "oneshot" or "off"
BTN2_ON_ACTION = quEvent.MUTE_GRP3_ON
BTN2_OFF_ACTION = quEvent.MUTE_GRP3_OFF

BTN3_MODE = "oneshot" # "toggle" or "oneshot" or "off"
BTN3_ON_ACTION = quEvent.TAP_FX2
BTN3_OFF_ACTION = quEvent.UNKNOWN

# actually my hardware has only 3 buttons, so this is untested
BTN4_MODE = "off" # "toggle" or "oneshot" or "off"
BTN4_ON_ACTION = quEvent.MUTE_GRP4_ON
BTN4_OFF_ACTION = quEvent.MUTE_GRP4_OFF

# shutdown LED:
# switch on this LED before system exits
# set to -1 to switch this off
SHUTDOWN_LED_PIN = LED3_PIN


# network connection
QU_HOSTNAME = '192.168.0.122'
#QU_HOSTNAME = '192.168.0.101'
QU_PORT = 51325

QU_MIDI_CH=1
 

