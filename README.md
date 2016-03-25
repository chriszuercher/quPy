# quPy
quPy - Software controlling the DIY Foot Switch for the Allen &amp; Heath Qu-Series
       
Original source: (C) 2014-2015, Niels Ott <niels@drni.de>
http://zwei.drni.de/archives/1553-Kick-the-Qu-A-DIY-Foot-Switch-for-the-Allen-Heath-Qu-Series.html

Forked by chriszuercher

Release 0.1, 2015-07-05

-------------------------------------------------------------------------------


GET IT GOING
============

1. Built your foot switch. qu-foot-switch-raspberry-gpio.png in the docs folder contains the  
   schematics. There you can also find the original wiki post.

2. Copy all files from the directory somewhere to your Raspberry Pi. 
3. Configure neede things:
```
config.py – needs the correct IP address for your QU desk – you can also edit mute group numbers vs buttons/leds on the footswitch in that file.

quPy.sh – needs the correct path info to files on your Pi

startup.sh – needed some attention on correct path as well – not sure why, but it’s maybe the way I have Linux set up on the Pi or something to do with the ‘dirname’ command?
```

4. Run as root: ./startup.sh
   You will get debug output.

5. You might get error messages if you're missing Python modules such
   as the one for the GPIO of the Pi. If so, install those modules
   via the package manager and retry.
   
6. Assuming, you're using TinyCore Linux, you can use quPy.sh as
   a startup script in your boot sequence.
   This will even redirect the debug to the system log.


   
MISSING STUFF
=============

* The quPy software does not care for tap tempo messages from the console
  yet. This needs to be implemented in qunetworkhandler.py where
  the events from the MIDI-parser are dealt with
  
* Reading large amounts of MIDI data from the net is slow. This is while
  receiving the status dump after connecting takes quite a while.
  qunetworkhandler.py could probably have a better implementation
  for reading the data other than bytewise.
 
   
   
LICENSE AND LEGAL STUFF
=======================

Most of the files in this directory were written by Niels Ott.
They are released under the terms of GNU GPL V3, which can
be found in LICENSE.txt

Other files are third party. Their status is a bit unclear, since
they mostly are from Python tutorial sites or some FAQs. Sources
are stated in comments.
