#!/usr/bin/env python
#
#    This is stepconf, a graphical configuration editor for LinuxCNC
#    Copyright 2007 Jeff Epler <jepler@unpythonic.net>
#    stepconf 1.1 revamped by Chris Morley 2014
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
#********************
# AXIS Z PAGE
#********************
def axisz_prepare(self):
	self.axis_prepare('z')
def axisz_finish(self):
	self.axis_done('z')
# AXIS Z callbacks
def on_zsteprev_changed(self, *args): self.a.update_pps('z')
def on_zmicrostep_changed(self, *args): self.a.update_pps('z')
def on_zpulleyden_changed(self, *args): self.a.update_pps('z')
def on_zpulleynum_changed(self, *args): self.a.update_pps('z')
def on_zleadscrew_changed(self, *args): self.a.update_pps('z')
def on_zmaxvel_changed(self, *args): self.a.update_pps('z')
def on_zmaxacc_changed(self, *args): self.a.update_pps('z')
def on_zaxistest_clicked(self, *args): self.a.test_axis('z')
def on_zpreset_button_clicked(self, *args): self.preset_axis('z')
