#!/bin/sh

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


myDir="/home/niels/quPy"
myControl="/tmp/quControl.fifo"
startup="$myDir/startup.sh"

if [ "$1" = "start" ] ; then
	rm -f "$myControl"
	mkfifo "$myControl"
	nohup "$startup" "$myControl" &
	exit
fi

if [ "$1" = "stop" ] ; then
	if [ ! -p "$myControl" ] ; then
		echo "$myControl fifo does not exist or is not a named pipe (fifo)."
		exit 1
	fi	
	echo "exit" > "$myControl"
	exit
fi

echo "Usage: start|stop"
exit 1