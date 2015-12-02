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
# handler for communication with the GPIO interface of the Raspberry Pi
#
# TODO: this class uses fixedly named constants from config.py - which leads to shitloads of copy/paste code which is very ugly
# 

from quevent import quEvent
import time
from mythreading import synchronized
import config
import RPi.GPIO as GPIO
from threading import Thread
from qumessagehandler import quMessageHandler
 
# class for letting a LED twinkle (blink once)
class ledTwinkler(object):
  
  def __init__(self, ledPin):
    self.ledPin = ledPin
  
  @synchronized
  def ledOn(self):
     GPIO.output(self.ledPin, GPIO.HIGH)

  @synchronized
  def ledOff(self):
     GPIO.output(self.ledPin, GPIO.LOW)
    
  def run(self):
    self.ledOn()
    time.sleep(0.050)
    self.ledOff()
  
  def twinkle(self):
    t = Thread(target=self.run)
    t.start()

# class for letting an LED flash in a certain time interval
class ledFlasher(object):

  def __init__(self, ledPin, time):
    self.ledPin = ledPin
    self.time = time
    self.aborted = False
    
  def stop(self):
    self.aborted = True
    
  def start(self):
    tw = ledTwinkler(self.ledPin)
    tw.twinkle()    
    t = Thread(target=self.run)
    t.start()
    
  def run(self):
    while ( True ):
      time.sleep(self.time)
      if (self.aborted):
	break
      tw = ledTwinkler(self.ledPin)
      tw.twinkle()

    

    

class gpioHandler(quMessageHandler):
  
  shutdownState = False  
  onlineState = False
  btn_held = {
    config.BTN1_PIN : False,
    config.BTN2_PIN : False,
    config.BTN3_PIN : False,
    config.BTN4_PIN : False }
  btn_toggle = {  
    config.BTN1_ON_ACTION : False,
    config.BTN2_ON_ACTION : False,
    config.BTN3_ON_ACTION : False,
    config.BTN4_ON_ACTION : False }
  
  led_flashers = {
    quEvent.DELAY_TIME_FX1 : None,
    quEvent.DELAY_TIME_FX2 : None,
    quEvent.DELAY_TIME_FX3 : None,
    quEvent.DELAY_TIME_FX4 : None
    }
    
  tap_time_map = {
    quEvent.DELAY_TIME_FX1 : quEvent.TAP_FX1,
    quEvent.DELAY_TIME_FX2 : quEvent.TAP_FX2,
    quEvent.DELAY_TIME_FX3 : quEvent.TAP_FX3,
    quEvent.DELAY_TIME_FX4 : quEvent.TAP_FX4
    
    }
  
  def __init__(self, controller):  
    super(gpioHandler, self).__init__(controller)
    # init GPIO interface
    GPIO.setwarnings(False)
    GPIO.cleanup()
     # prepare IO modes
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(config.BTN1_PIN, GPIO.IN)
    GPIO.setup(config.BTN2_PIN, GPIO.IN)
    GPIO.setup(config.BTN3_PIN, GPIO.IN)
    GPIO.setup(config.BTN4_PIN, GPIO.IN)
    GPIO.setup(config.LED1_PIN, GPIO.OUT)
    GPIO.setup(config.LED2_PIN, GPIO.OUT)
    GPIO.setup(config.LED3_PIN, GPIO.OUT)
    GPIO.setup(config.LED4_PIN, GPIO.OUT)
    GPIO.setup(config.CONN_LED_PIN, GPIO.OUT)
    # default LEDs to OFF
    GPIO.output(config.LED1_PIN, GPIO.LOW)
    GPIO.output(config.LED2_PIN, GPIO.LOW)
    GPIO.output(config.LED3_PIN, GPIO.LOW)
    GPIO.output(config.LED4_PIN, GPIO.LOW)
    GPIO.output(config.CONN_LED_PIN, GPIO.LOW)
    
  # generic methods for checking events that are related
  # to buttons
  def checkLedEventGeneric(self, event, ledPin, isToggle, onAction, offAction):
    if (isToggle and event.getType() == onAction):
      self.btn_toggle[onAction] = True
      GPIO.output(ledPin, GPIO.HIGH)
    if (isToggle and event.getType() ==  offAction):
      self.btn_toggle[onAction] = False
      GPIO.output(ledPin, GPIO.LOW)

  # check the delay time events and set LED flashers up accordingly of necessary
  def checkDelayTimeEvent(self, event, led_pin, action_set):

    if ( action_set and event.getType() in self.led_flashers.keys() ):
      flasher = self.led_flashers[event.getType()]
      if (flasher != None):
	flasher.stop()
      flasher = ledFlasher(led_pin, event.getArguments()[0])
      flasher.start()
      self.led_flashers[event.getType()] = flasher
  
  
  # switch on/off LEDs depending on event
  def checkLedEvent(self,event):
    # check events that relate to LED status
    self.checkLedEventGeneric(event, config.LED1_PIN, (config.BTN1_MODE=="toggle"), config.BTN1_ON_ACTION, config.BTN1_OFF_ACTION)
    self.checkLedEventGeneric(event, config.LED2_PIN, (config.BTN2_MODE=="toggle"), config.BTN2_ON_ACTION, config.BTN2_OFF_ACTION)
    self.checkLedEventGeneric(event, config.LED3_PIN, (config.BTN3_MODE=="toggle"), config.BTN3_ON_ACTION, config.BTN3_OFF_ACTION)
    self.checkLedEventGeneric(event, config.LED4_PIN, (config.BTN4_MODE=="toggle"), config.BTN4_ON_ACTION, config.BTN4_OFF_ACTION)
    
    # check events that involve tap LEDs flashing
    self.checkDelayTimeEvent(event, config.LED1_PIN, (config.BTN1_MODE=="oneshot" and event.getType() in self.tap_time_map.keys() and config.BTN1_ON_ACTION == self.tap_time_map[event.getType()]))
    self.checkDelayTimeEvent(event, config.LED2_PIN, (config.BTN2_MODE=="oneshot" and event.getType() in self.tap_time_map.keys() and config.BTN2_ON_ACTION == self.tap_time_map[event.getType()]))
    self.checkDelayTimeEvent(event, config.LED3_PIN, (config.BTN3_MODE=="oneshot" and event.getType() in self.tap_time_map.keys() and config.BTN3_ON_ACTION == self.tap_time_map[event.getType()]))
    self.checkDelayTimeEvent(event, config.LED4_PIN, (config.BTN4_MODE=="oneshot" and event.getType() in self.tap_time_map.keys() and config.BTN4_ON_ACTION == self.tap_time_map[event.getType()]))

    # handle network online/offline LED status
    if (event.getType() == quEvent.NET_ONLINE):
      GPIO.output(config.CONN_LED_PIN, GPIO.HIGH)
    if (event.getType() == quEvent.NET_OFFLINE):
      GPIO.output(config.CONN_LED_PIN, GPIO.LOW)
  
  # handle incoming events and update display
  @synchronized
  def handleEvent(self, sender, event):
    # always ignore events from myself to avoid loops, 
    # those of my own I need to react to come from ECO handler
    if (self == sender):
      return
    
    # handle system events
    if (event.getType() == quEvent.SYS_SHUTDOWN):
      # stop LED flashers
      for f in self.led_flashers.values():
	if (f != None):
	  f.stop()
      
      self.shutdownState = True
    elif (event.getType() == quEvent.NET_ONLINE):
      self.onlineState = True
    elif (event.getType() == quEvent.NET_OFFLINE):
      self.onlineState = False
      
    # update LED status 
    self.checkLedEvent(event)
    
  
  def getName(self):
    return('GIO')

  # generic method to poll the state of a button from the GPIO interface and take required action  
  def pollButton(self, buttonPin, isToggle, invert, onAction, offAction):
    # button is pushed down and held
    if ( (not self.btn_held[buttonPin]) and (( not GPIO.input(buttonPin) == GPIO.HIGH) and invert) ):
      self.btn_held[buttonPin] = True
      # if this is a not a toggle (so oneshot), or a toggle and ON is the required action,
      # send event
      if ((not isToggle) or (not self.btn_toggle[onAction])):
	self.sendEvent(quEvent(onAction, []))
      # otherwise, (toggle and OFF is required) send event 	
      else: 
	self.sendEvent(quEvent(offAction, []))
    #button is released	  
    if ( (self.btn_held[buttonPin]) and (( not GPIO.input(buttonPin) == GPIO.LOW) and invert) ):
      self.btn_held[buttonPin] = False
  
  # switch on shutdown status LED
  @synchronized
  def setShutdownLEDs(self):
    # switch off all button LEDs
    if (config.BTN1_MODE != "off"):
      GPIO.output(config.LED1_PIN, GPIO.LOW)
    if (config.BTN2_MODE != "off"):
      GPIO.output(config.LED2_PIN, GPIO.LOW)
    if (config.BTN3_MODE != "off"):
      GPIO.output(config.LED3_PIN, GPIO.LOW)
    if (config.BTN4_MODE != "off"):
      GPIO.output(config.LED4_PIN, GPIO.LOW)
    
    # switch on shutdown LED 
    if ( config.SHUTDOWN_LED_PIN >= 0 ): 
       GPIO.output(config.SHUTDOWN_LED_PIN, GPIO.HIGH)
    

  # --> this method should be run in a thread
  def run(self):   

  
    while (True):
      # quit on system shutdown
      if (self.shutdownState):
	self.setShutdownLEDs()
	break
      if (not self.onlineState):
	continue
      
      # do IO
      if (config.BTN1_MODE != "off"):
        self.pollButton(config.BTN1_PIN, (config.BTN1_MODE=="toggle"), config.INV1, config.BTN1_ON_ACTION, config.BTN1_OFF_ACTION)
      if (config.BTN2_MODE != "off"):
	self.pollButton(config.BTN2_PIN, (config.BTN2_MODE=="toggle"), config.INV2, config.BTN2_ON_ACTION, config.BTN2_OFF_ACTION)
      if (config.BTN3_MODE != "off"):
        self.pollButton(config.BTN3_PIN, (config.BTN3_MODE=="toggle"), config.INV3, config.BTN3_ON_ACTION, config.BTN3_OFF_ACTION)
      if (config.BTN4_MODE != "off"):
        self.pollButton(config.BTN4_PIN, (config.BTN4_MODE=="toggle"), config.INV4, config.BTN4_ON_ACTION, config.BTN4_OFF_ACTION)
      
      # wait a bit
      time.sleep(0.002)
      
      