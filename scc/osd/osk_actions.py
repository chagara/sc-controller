#!/usr/bin/env python2
"""
SC Controller - On Screen Keyboard Actions

Special Actions that are used to bind functions like closing keyboard or moving
cursors around.

Actions defined here are *not* automatically added to ACTIONS dict.
OSD Keyboard and its binding editor enables them to use with 'OSK.something'
syntax.
"""
from __future__ import unicode_literals

from scc.lib import Enum
from scc.actions import Action, SpecialAction
from scc.constants import TRIGGER_HALF, LEFT, RIGHT
from scc.tools import strip_none

import time, logging
log = logging.getLogger("OSDKeyActs")
_ = lambda x : x


class OSKAction(Action, SpecialAction):
	def __init__(self, *a):
		Action.__init__(self, *a)
		self.speed = 1.0
	
	
	def set_speed(self, x, y, z):
		self.speed = x
		return True
	
	
	def trigger(self, mapper, p, old_p):
		if p * self.speed >= TRIGGER_HALF and old_p * self.speed < TRIGGER_HALF:
			self.button_press(mapper)
		elif p * self.speed < TRIGGER_HALF and old_p * self.speed >= TRIGGER_HALF:
			self.button_release(mapper)


class CloseOSKAction(OSKAction):
	SA = COMMAND = "close"
	
	def describe(self, context):
		return _("Hide Keyboard")
	
	
	def to_string(self, multiline=False, pad=0):
		return (" " * pad) + "OSK.%s()" % (self.COMMAND,)
	
	
	def button_press(self, mapper):
		self.execute(mapper)
	
	
	def button_release(self, mapper): pass


class OSKCursorAction(Action, SpecialAction):
	SA = COMMAND = "cursor"
	
	def __init__(self, side):
		Action.__init__(self, side)
		if hasattr(side, "name"): side = side.name
		self.speed = (1.0, 1.0)
		self.side = side
	
	
	def set_speed(self, x, y, z):
		self.speed = (x, y)
		return True	
	
	
	def whole(self, mapper, x, y, what):
		self.execute(mapper, x, y)
	
	
	def describe(self, context):
		if self.side == LEFT:
			return _("Move LEFT Cursor")
		else:
			return _("Move RIGHT Cursor")
	
	
	def to_string(self, multiline=False, pad=0):
		return (" " * pad) + "OSK.%s(%s)" % (self.COMMAND, self.side)


class MoveOSKAction(OSKAction):
	SA = COMMAND = "move"
	
	def whole(self, mapper, x, y, what):
		self.execute(mapper, x, y)
	
	
	def describe(self, context):
		return _("Move Keyboard")
	
	
	def to_string(self, multiline=False, pad=0):
		return (" " * pad) + "OSK.%s()" % (self.COMMAND,)


class OSKPressAction(OSKAction):
	SA = COMMAND = "press"
	
	def __init__(self, side):
		OSKAction.__init__(self, side)
		if hasattr(side, "name"): side = side.name
		self.side = side
	
	
	def describe(self, context):
		if self.side == LEFT:
			return _("Press Key Under LEFT Cursor")
		else:
			return _("Press Key Under RIGHT Cursor")	
	
	
	def button_press(self, mapper):
		self.execute(mapper, True)
	
	
	def button_release(self, mapper):
		self.execute(mapper, False)
	
	
	def to_string(self, multiline=False, pad=0):
		return (" " * pad) + "OSK.%s(%s)" % (self.COMMAND, self.side)


# Add stuff to OSK dict
OSK = {}
for i in [ globals()[x] for x in dir() if hasattr(globals()[x], 'COMMAND') ]:
	if i.COMMAND is not None:
		OSK[i.COMMAND] = i
