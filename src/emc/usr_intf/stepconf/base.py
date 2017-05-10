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
#************
# BASIC PAGE
#************
from gi.repository import GObject
from stepconf.definitions import *
from stepconf import preset

def base_prepare(self):
	self.w.drivetime_expander.set_expanded(True)
	self.w.machinename.set_text(self.d.machinename)
	self.w.axes.set_active(self.d.axes)
	self.w.units.set_active(self.d.units)
	self.w.latency.set_value(self.d.latency)
	self.w.steptime.set_value(self.d.steptime)
	self.w.stepspace.set_value(self.d.stepspace)
	self.w.dirsetup.set_value(self.d.dirsetup)
	self.w.dirhold.set_value(self.d.dirhold)
	self.w.drivertype.set_active(self.drivertype_toindex())
	self.w.ioaddr.set_text(self.d.ioaddr)
	self.w.machinename.grab_focus()
	self.w.ioaddr2.set_text(self.d.ioaddr2) 
	#self.w.ioaddr3.set_text(self.d.ioaddr3)
	#self.w.pp3_direction.set_active(self.d.pp3_direction)
	if self.d.number_pports>2:
		 self.w.radio_pp3.set_active(True)
	elif self.d.number_pports>1:
		 self.w.radio_pp2.set_active(True)
	else:
		 self.w.radio_pp1.set_active(True)
		 
	ctx = self.w.base_preselect_button.get_style_context()
	ctx.remove_class('selected')
	ctx.add_class('normal')

def base_finish(self):
	self.w.drivetime_expander.set_expanded(False)
	machinename = self.w.machinename.get_text()
	self.d.machinename = machinename.replace(" ","_")
	self.d.axes = self.w.axes.get_active()
	self.d.units = self.w.units.get_active()
	self.d.drivertype = self.drivertype_toid(self.w.drivertype.get_active())
	self.d.steptime = self.w.steptime.get_value()
	self.d.stepspace = self.w.stepspace.get_value()
	self.d.dirsetup = self.w.dirsetup.get_value()
	self.d.dirhold = self.w.dirhold.get_value()
	self.d.latency = self.w.latency.get_value()
	if self.w.radio_pp3.get_active() and self.w.radio_pp2.get_active():
		self.d.number_pports = 3
	elif self.w.radio_pp2.get_active():
		self.d.number_pports = 2
	else:
		self.d.number_pports = 1
	self.page_set_state('pport2',self.w.radio_pp2.get_active())
	# Get item selected in combobox
	tree_iter = self.w.axes.get_active_iter()
	model = self.w.axes.get_model()
	text_selected = model[tree_iter][0]
	self.dbg("active axes: %s = %d"% (text_selected,self.d.axes))
	self.page_set_state('axisz','Z' in text_selected)
	self.page_set_state('axisy','Y' in text_selected)
	self.page_set_state('axisu','U' in text_selected)
	self.page_set_state('axisv','V' in text_selected)
	self.page_set_state('axisa','A' in text_selected)

# Driver functions
def on_drivertype_changed(self, *args):
	self.update_drivertype_info()

def update_drivertype_info(self):
	v = self.w.drivertype.get_active()
	if v < len(alldrivertypes):
		d = alldrivertypes[v]
		self.w.steptime.set_value(d[2])
		self.w.stepspace.set_value(d[3])
		self.w.dirhold.set_value(d[4])
		self.w.dirsetup.set_value(d[5])

		self.w.steptime.set_sensitive(0)
		self.w.stepspace.set_sensitive(0)
		self.w.dirhold.set_sensitive(0)
		self.w.dirsetup.set_sensitive(0)
	else:
		self.w.steptime.set_sensitive(1)
		self.w.stepspace.set_sensitive(1)
		self.w.dirhold.set_sensitive(1)
		self.w.dirsetup.set_sensitive(1)
	self.calculate_ideal_period()

def drivertype_fromid(self):
	for d in alldrivertypes:
		if d[0] == self.d.drivertype: return d[1]

def drivertype_toid(self, what=None):
	if not isinstance(what, int): what = self.drivertype_toindex(what)
	if what < len(alldrivertypes): return alldrivertypes[what][0]
	return "other"

def drivertype_toindex(self, what=None):
	if what is None: what = self.d.drivertype
	for i, d in enumerate(alldrivertypes):
		if d[0] == what: return i
	return len(alldrivertypes)

def drivertype_fromindex(self):
	i = self.w.drivertype.get_active()
	if i < len(alldrivertypes): return alldrivertypes[i][1]
	return _("Other")

def calculate_ideal_period(self):
	steptime = self.w.steptime.get_value()
	stepspace = self.w.stepspace.get_value()
	latency = self.w.latency.get_value()
	minperiod = self.d.minperiod(steptime, stepspace, latency)
	maxhz = int(1e9 / minperiod)
	if not self.d.doublestep(steptime): maxhz /= 2
	self.w.baseperiod.set_text("%d ns" % minperiod)
	self.w.maxsteprate.set_text("%d Hz" % maxhz)

#**************
# Latency test
#**************
def run_latency_test(self):
	self.latency_pid = os.spawnvp(os.P_NOWAIT, "latency-test", ["latency-test"])
	self.w['window1'].set_sensitive(0)
	GObject.timeout_add(15, self.latency_running_callback)

def latency_running_callback(self):
	pid, status = os.waitpid(self.latency_pid, os.WNOHANG)
	if pid:
		self.w['window1'].set_sensitive(1)
		return False
	return True
 
# Basic page callbacks
def on_pp2_checkbutton_toggled(self, *args): 
	i = self.w.pp2_checkbutton.get_active()   
	self.w.pp2_direction.set_sensitive(i)
	self.w.ioaddr2.set_sensitive(i)
	if i == 0:
		self.w.pp3_checkbutton.set_active(i)
		self.w.ioaddr3.set_sensitive(i)

def on_pp3_checkbutton_toggled(self, *args): 
	i = self.w.pp3_checkbutton.get_active() 
	if self.w.pp2_checkbutton.get_active() ==0:
		i=0
		self.w.pp3_checkbutton.set_active(0)
	self.w.pp3_direction.set_sensitive(i)
	self.w.ioaddr3.set_sensitive(i)

def on_latency_test_clicked(self, widget):
	self.run_latency_test()

def on_calculate_ideal_period(self, widget):
	self.calculate_ideal_period()

def on_units_changed(self, widget):
	if not self.d.units == widget.get_active():
		# change the XYZ axis defaults to metric or imperial
		# This erases any entered data that would make sense to change
		self.d.set_axis_unit_defaults(not widget.get_active())

def on_base_preselect_button_clicked(self, widget):
	current_machine = self.d.get_machine_preset(self.w.base_preset_combo)
	if current_machine:
		self.base_general_preset(current_machine)
		ctx = self.w.base_preselect_button.get_style_context()
		ctx.remove_class('normal')
		ctx.add_class('selected')

def base_general_preset(self, current_machine):
	# base
	
	# pport1
	self.pport1_prepare()
	self.d.select_combo_machine(self.w.pp1_preset_combo, current_machine["index"])
	self.on_pp1_preselect_button_clicked(None)
	self.pport1_finish()
	# axis
	for axis in ('x','y','z','u','v'):
		self.axis_prepare(axis)
		self.d.select_combo_machine(self.w[axis + "preset_combo"], current_machine["index"])
		self.preset_axis(axis)
		self.axis_done(axis)
	return


