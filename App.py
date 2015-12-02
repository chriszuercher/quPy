#!/usr/bin/python

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


from qumessagecontroller import quMessageController
from debughandler import debugHandler
from keepalivehandler import keepAliveHandler
from echohandler import echoHandler
from gpiohandler import gpioHandler
from quevent import quEvent
from threading import Thread
from qunetworkhandler import quNetworkHandler
from taptimehandler import tapTimeHandler
import sys
import signal


# initialize the central messaging controller
control = quMessageController()

# initialize the I/O handlers
deb = debugHandler(control)
kal = keepAliveHandler(control)
gio = gpioHandler(control)
eco = echoHandler(control)
net = quNetworkHandler(control)
tap = tapTimeHandler(control)

# start a thread for each handler
debugThread = Thread(target=deb.run)
debugThread.start()
kalThread = Thread(target=kal.run)
kalThread.start()
gioThread = Thread(target=gio.run)
gioThread.start()
netThread = Thread(target=net.run)
netThread.start()

# install SIGTERM handler for proper shutdown
def signal_term_handler(signal, frame):
  # use debug handler to initiate a proper shutdown in SIGTERM
  sys.stderr.write("APP: Received SIGTERM, sending SYS_SHUTDOWN to all handlers.\n")
  deb.sendEvent(quEvent(quEvent.SYS_SHUTDOWN))
 
signal.signal(signal.SIGTERM, signal_term_handler)


# wait for thread(s) to finish
debugThread.join()
kalThread.join()
gioThread.join()
netThread.join()


 
