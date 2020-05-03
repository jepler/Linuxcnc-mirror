#!/usr/bin/env python
# -*- encoding: utf-8 -*-
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
#    Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
#    This builds the INI file from the collected data.
#

from __future__ import print_function
import os
import time
from stepconf.definitions import *
import sys
import importlib
importlib.reload(sys)
sys.setdefaultencoding('utf8')

class INI:
    def __init__(self,app):
        # access to:
        self.d = app.d  # collected data
        self.a = app    # The parent, stepconf
        self.p = app.p # pages
        self._p = app._p # private data
        
    def write_inifile(self, base):
        if self.d.axes == 2:
            maxvel = max(self.d.xmaxvel, self.d.zmaxvel)
        elif self.d.axes == 4:
            maxvel = max(self.d.xmaxvel, self.d.ymaxvel)
        else:
            maxvel = max(self.d.xmaxvel, self.d.ymaxvel, self.d.zmaxvel)
        hypotvel = (self.d.xmaxvel**2 + self.d.ymaxvel**2 + self.d.zmaxvel**2) **.5
        defvel = min(maxvel, max(.1, maxvel/10.))

        filename = os.path.join(base, self.d.machinename + ".ini")
        file = open(filename, "w")
<<<<<<< HEAD
        print >>file, _("# Generated by stepconf %(version)s at %(currenttime)s") % {'version':STEPCONF_VERSION, 'currenttime':time.asctime()}
        print >>file, _("# If you make changes to this file, they will be").encode('utf-8')
        print >>file, _("# overwritten when you run stepconf again").encode('utf-8')

        print >>file
        ##########################################
        ################### EMC ##################
        print >>file, "[EMC]"
        print >>file, "MACHINE = %s" % self.d.machinename
        print >>file, "DEBUG = 0"
=======
        print(_("# Generated by stepconf 1.1 at %s") % time.asctime(), file=file)
        print(_("# If you make changes to this file, they will be").encode('utf-8'), file=file)
        print(_("# overwritten when you run stepconf again").encode('utf-8'), file=file)

        print(file=file)
        print("[EMC]", file=file)
        print("MACHINE = %s" % self.d.machinename, file=file)
        print("DEBUG = 0", file=file)
>>>>>>> upstream/master

        # the joints_axes conversion script named 'update_ini'
        # will try to update for joints_axes if no VERSION is set
        print("VERSION = 1.1", file=file)

<<<<<<< HEAD
        print >>file

        ##########################################
        ################# DISPLAY ################
        print >>file, "[DISPLAY]"
=======
        print(file=file)
        print("[DISPLAY]", file=file)
>>>>>>> upstream/master
        if self.d.select_axis:
            print("DISPLAY = axis", file=file)
        elif self.d.select_gmoccapy:
<<<<<<< HEAD
            print >>file, "DISPLAY = gmoccapy"
            print >>file, "PREFERENCE_FILE_PATH = gmoccapy_preferences"
        print >>file, "EDITOR = gedit"
        print >>file, "POSITION_OFFSET = RELATIVE"
        print >>file, "POSITION_FEEDBACK = ACTUAL"
        print >>file, "ARCDIVISION = 64"
        print >>file, "GRIDS = 10mm 20mm 50mm 100mm 1in 2in 5in 10in"
        print >>file, "MAX_FEED_OVERRIDE = 1.2"
        print >>file, "MIN_SPINDLE_OVERRIDE = 0.5"
        print >>file, "MAX_SPINDLE_OVERRIDE = 1.2"
        print >>file, "DEFAULT_LINEAR_VELOCITY = %.2f" % defvel
        print >>file, "MIN_LINEAR_VELOCITY = 0"
        print >>file, "MAX_LINEAR_VELOCITY = %.2f" % maxvel

=======
            print("DISPLAY = gmoccapy", file=file)
        print("EDITOR = gedit", file=file)
        print("POSITION_OFFSET = RELATIVE", file=file)
        print("POSITION_FEEDBACK = ACTUAL", file=file)
        print("ARCDIVISION = 64", file=file)
        print("GRIDS = 10mm 20mm 50mm 100mm 1in 2in 5in 10in", file=file)
        print("MAX_FEED_OVERRIDE = 1.2", file=file)
        print("MIN_SPINDLE_OVERRIDE = 0.5", file=file)
        print("MAX_SPINDLE_OVERRIDE = 1.2", file=file)
        print("DEFAULT_LINEAR_VELOCITY = %.2f" % defvel, file=file)
        print("MIN_LINEAR_VELOCITY = 0", file=file)
        print("MAX_LINEAR_VELOCITY = %.2f" % maxvel, file=file)
>>>>>>> upstream/master
        if self.d.axes == 1:
            defvel = min(60, self.d.amaxvel/10.)
            print("DEFAULT_ANGULAR_VELOCITY = %.2f" % defvel, file=file)
            print("MIN_ANGULAR_VELOCITY = 0", file=file)
            print("MAX_ANGULAR_VELOCITY = %.2f" % self.d.amaxvel, file=file)

<<<<<<< HEAD
        print >>file, "INTRO_GRAPHIC = linuxcnc.gif"
        print >>file, "INTRO_TIME = 5"
        print >>file, "PROGRAM_PREFIX = %s" % os.path.expanduser("~/linuxcnc/nc_files")
        if self.d.units == MM:
            print >>file, "INCREMENTS = 5mm 1mm .5mm .1mm .05mm .01mm .005mm"
        else:
            print >>file, "INCREMENTS = .1in .05in .01in .005in .001in .0005in .0001in"
        if (self.d.guitype == GUI_IS_GLADEVCP and self.d.gladevcptype != GLADEVCP_NONE):
            if self.d.centerembededgvcp:
                print >>file, "EMBED_TAB_NAME = GladeVCP"
                print >>file, "EMBED_TAB_COMMAND = halcmd loadusr -Wn gladevcp gladevcp -c gladevcp -u %s -H %s -x {XID} %s" % \
                		(FILE_GLADEVCP_HANDLER, FILE_GLADEVCP_CALL_LIST, self.d.gladevcpname)
            elif self.d.sideembededgvcp:
                print >>file, "GLADEVCP = -u %s -H %s %s" % (FILE_GLADEVCP_HANDLER, FILE_GLADEVCP_CALL_LIST, self.d.gladevcpname)
        if (self.d.guitype == GUI_IS_PYVCP and self.d.pyvcptype != PYVCP_NONE):
            print >>file, "PYVCP = %s" % self.d.pyvcpname
        if self.d.axes == 2:
            print >>file, "LATHE = 1"
            print >>file, "BACK_TOOL_LATHE = 0"
=======
        print("INTRO_GRAPHIC = linuxcnc.gif", file=file)
        print("INTRO_TIME = 5", file=file)
        print("PROGRAM_PREFIX = %s" % os.path.expanduser("~/linuxcnc/nc_files"), file=file)
        if self.d.units:
            print("INCREMENTS = 5mm 1mm .5mm .1mm .05mm .01mm .005mm", file=file)
        else:
            print("INCREMENTS = .1in .05in .01in .005in .001in .0005in .0001in", file=file)
        if self.d.pyvcp:
            print("PYVCP = custompanel.xml", file=file)
        if self.d.axes == 2:
            print("LATHE = 1", file=file)
>>>>>>> upstream/master
        if self.d.axes == 3:
            print("FOAM = 1", file=file)
            print("GEOMETRY = XY;UZ", file=file)
            print("OPEN_FILE = ./foam.ngc", file=file)
        print(file=file)

        # self.d.axes is coded 0: X Y Z
        #                      1: X Y Z A
        #                      2: X Z
        #                      3: X Y U V
<<<<<<< HEAD
        if   self.d.axes == XYZ: num_joints = 3 # X Y Z
        elif self.d.axes == XYZA: num_joints = 4 # X Y Z A
        elif self.d.axes == XZ: num_joints = 2 # X Z
        elif self.d.axes == XYUV: num_joints = 4 # X Y U V
        else:
            print "___________________unknown self.d.axes",self.d.axes

        if   self.d.axes == XYZA: coords = "X Y Z A"
        elif self.d.axes == XYZ: coords = "X Y Z"
        elif self.d.axes == XZ: coords = "X Z"
        elif self.d.axes == XYUV: coords = "X Y U V"
=======
        if   self.d.axes == 0: num_joints = 3 # X Y Z
        elif self.d.axes == 1: num_joints = 4 # X Y Z A
        elif self.d.axes == 2: num_joints = 2 # X Z
        elif self.d.axes == 3: num_joints = 4 # X Y U V
        elif self.d.axes == 4: num_joints = 2 # X Y
        else:
            print("___________________unknown self.d.axes",self.d.axes)

        if   self.d.axes == 1: coords = "X Y Z A"
        elif self.d.axes == 0: coords = "X Y Z"
        elif self.d.axes == 2: coords = "X Z"
        elif self.d.axes == 3: coords = "X Y U V"
        elif self.d.axes == 4: coords = "X Y"
<<<<<<< HEAD
>>>>>>> upstream/master
=======
>>>>>>> upstream/master

<<<<<<< HEAD
        ##########################################
        ################## KINS ##################
        print >>file,  "[KINS]"
        # trivial kinematics: no. of joints == no.of axes)
        # with trivkins, axes do not have to be consecutive
        print >>file, "JOINTS = %d"%num_joints
        print >>file, "KINEMATICS = trivkins coordinates=%s"%coords.replace(" ","")
        print >>file
        
        ##########################################
        ################# FILTER #################
        print >>file, "[FILTER]"
        print >>file, "PROGRAM_EXTENSION = .png,.gif,.jpg Greyscale Depth Image"
        print >>file, "PROGRAM_EXTENSION = .py Python Script"
        print >>file, "PROGRAM_EXTENSION = .nc,.tap G-Code File"
        print >>file, "png = image-to-gcode"
        print >>file, "gif = image-to-gcode"
        print >>file, "jpg = image-to-gcode"
        print >>file, "py = python"        

        print >>file

        ##########################################
        ################## TASK ##################
        print >>file, "[TASK]"
        print >>file, "TASK = milltask"
        print >>file, "CYCLE_TIME = 0.010"
        print >>file

        ##########################################
        ################ RS274NGC ################
        print >>file, "[RS274NGC]"
        print >>file, "PARAMETER_FILE = linuxcnc.var"
        # Put my ngc file here
        subroutine_path = os.path.expanduser("~/linuxcnc/configs/%s" % (self.d.machinename))
        print >>file, "SUBROUTINE_PATH = ncsubroutines:%s" % subroutine_path
        # Test if exist manual change tool
        if(self.d.tool_change_type == TOOL_CHANGE_MANUAL):
            # From orangecat
            print >>file, "REMAP=M6 modalgroup=6 ngc=%s" % (FILE_TOOL_CHANGE)
            print >>file, "REMAP=M600 modalgroup=6 ngc=%s" % (FILE_TOOL_JOB_BEGIN)
            self.p.create_tool_change_routine()
            self.p.create_tool_job_begin_routine()
        print >>file
        ##########################################
        ################# EMCMOT #################
        base_period = self.p.ideal_period()
        print >>file, "[EMCMOT]"
        print >>file, "EMCMOT = motmod"
        print >>file, "COMM_TIMEOUT = 1.0"
        print >>file, "BASE_PERIOD = %d" % base_period
        print >>file, "SERVO_PERIOD = 1000000"

        print >>file
        ##########################################
        ################## HAL ###################
        print >>file, "[HAL]"
        if self.d.halui:
            print >>file,"HALUI = halui"
        print >>file, "HALFILE = %s.hal" % self.d.machinename
        if self.d.customhal:
            print >>file, "HALFILE = %s" % FILE_CUSTOM_HALFILE
        if (self.d.guitype == GUI_IS_PYVCP and self.d.pyvcptype != PYVCP_NONE):
            print >>file, "POSTGUI_HALFILE = %s" % FILE_POSTGUI_CALL_LIST

        ##########################################
        ################# HALUI ##################
        if (self.d.halui_custom == 1 or self.d.halui ==1):
           print >>file
           print >>file, "[HALUI]"
           print >>file, _("# add halui MDI commands here (max 64) ")
           # First put standard mdi_command
           for mdi_command in self._p.halui_list:
               print >>file, "MDI_COMMAND = %s" % mdi_command
           # Then custom command
           if(self.d.halui_custom):
               for mdi_command in self.d.halui_list_custom:
                   print >>file, "MDI_COMMAND = %s" % mdi_command

        print >>file
        ##########################################
        ################## TRAJ ##################
        print >>file, "[TRAJ]"
        # [TRAJ]AXES notused for joints_axes
        print >>file, "COORDINATES = ",coords
        if self.d.units == MM:
            print >>file, "LINEAR_UNITS = mm"
        else:
            print >>file, "LINEAR_UNITS = inch"
        print >>file, "ANGULAR_UNITS = degree"
        print >>file, "DEFAULT_LINEAR_VELOCITY = %.2f" % defvel
        print >>file, "MAX_LINEAR_VELOCITY = %.2f" % maxvel
        print >>file

        ##########################################
        ################# EMCIO ##################
        print >>file, "[EMCIO]"
        print >>file, "EMCIO = io"
        print >>file, "CYCLE_TIME = 0.100"
        print >>file, "TOOL_TABLE = tool.tbl"
=======
        print("[KINS]", file=file)
        # trivial kinematics: no. of joints == no.of axes)
        # with trivkins, axes do not have to be consecutive
        print("JOINTS = %d"%num_joints, file=file)
        print("KINEMATICS = trivkins coordinates=%s"%coords.replace(" ",""), file=file)
        print(file=file)
        print("[FILTER]", file=file)
        print("PROGRAM_EXTENSION = .png,.gif,.jpg Greyscale Depth Image", file=file)
        print("PROGRAM_EXTENSION = .py Python Script", file=file)
        print("PROGRAM_EXTENSION = .nc,.tap G-Code File", file=file)
        print("png = image-to-gcode", file=file)
        print("gif = image-to-gcode", file=file)
        print("jpg = image-to-gcode", file=file)
        print("py = python", file=file)        

        print(file=file)
        print("[TASK]", file=file)
        print("TASK = milltask", file=file)
        print("CYCLE_TIME = 0.010", file=file)

        print(file=file)
        print("[RS274NGC]", file=file)
        print("PARAMETER_FILE = linuxcnc.var", file=file)

        base_period = self.d.ideal_period()

        print(file=file)
        print("[EMCMOT]", file=file)
        print("EMCMOT = motmod", file=file)
        print("COMM_TIMEOUT = 1.0", file=file)
        print("BASE_PERIOD = %d" % base_period, file=file)
        print("SERVO_PERIOD = 1000000", file=file)

        print(file=file)
        print("[HAL]", file=file)
        if self.d.halui:
            print("HALUI = halui", file=file)          
        print("HALFILE = %s.hal" % self.d.machinename, file=file)
        if self.d.customhal:
            print("HALFILE = custom.hal", file=file)
            print("POSTGUI_HALFILE = postgui_call_list.hal", file=file)

        if self.d.halui:
           print(file=file)
           print("[HALUI]", file=file)
           print(_("# add halui MDI commands here (max 64) "), file=file)
           for mdi_command in self.d.halui_list:
               print("MDI_COMMAND = %s" % mdi_command, file=file)

        print(file=file)
        print("[TRAJ]", file=file)
        # [TRAJ]AXES notused for joints_axes
        print("COORDINATES = ",coords, file=file)
        if self.d.units:
            print("LINEAR_UNITS = mm", file=file)
        else:
            print("LINEAR_UNITS = inch", file=file)
        print("ANGULAR_UNITS = degree", file=file)
        print("DEFAULT_LINEAR_VELOCITY = %.2f" % defvel, file=file)
        print("MAX_LINEAR_VELOCITY = %.2f" % maxvel, file=file)
        print(file=file)
        print("[EMCIO]", file=file)
        print("EMCIO = io", file=file)
        print("CYCLE_TIME = 0.100", file=file)
        print("TOOL_TABLE = tool.tbl", file=file)
>>>>>>> upstream/master

        if self.d.axes == XZ: # XZ
            all_homes = self.p.home_sig("x") and self.p.home_sig("z")
        else:
            all_homes = self.p.home_sig("x") and self.p.home_sig("y")
            if self.d.axes == XYUV: # XYUV
                all_homes = all_homes and self.p.home_sig("u") and self.p.home_sig("v")
            elif self.d.axes == XYZ: # XYZ
                all_homes = all_homes and self.p.home_sig("z")
            elif self.d.axes == 1: # XYZA
                all_homes = all_homes and self.p.home_sig("z") and self.p.home_sig("a")

        self.write_one_axis(file, 0, "x", "LINEAR", all_homes)
        if self.d.axes in(0,1): # xyz or xyza
            self.write_one_axis(file, 1, "y", "LINEAR", all_homes)
            self.write_one_axis(file, 2, "z", "LINEAR", all_homes)
        if self.d.axes == 1: # xyza
            self.write_one_axis(file, 3, "a", "ANGULAR", all_homes)
        if self.d.axes == 2: # xZ
            self.write_one_axis(file, 1, "z", "LINEAR", all_homes)
        if self.d.axes == 3: # xyuv
            self.write_one_axis(file, 1, "y", "LINEAR", all_homes)
            self.write_one_axis(file, 2, "u", "LINEAR", all_homes)
            self.write_one_axis(file, 3, "v", "LINEAR", all_homes)
<<<<<<< HEAD
<<<<<<< HEAD

        if(self.d.tool_change_type == TOOL_CHANGE_MANUAL):
            # From orangecat
            print >>file, "TOOL_CHANGE_AT_G30 = 0"

        print >>file
=======
        if self.d.axes == 4: # xY
            self.write_one_axis(file, 1, "y", "LINEAR", all_homes)
>>>>>>> upstream/master
=======
        if self.d.axes == 4: # xY
            self.write_one_axis(file, 1, "y", "LINEAR", all_homes)
>>>>>>> upstream/master
        file.close()
        self.p.add_md5sum(filename)
        #print self.d.md5sums

####################################################################
#******************
# HELPER FUNCTIONS
#******************
    def write_one_axis(self, file, num, letter, type, all_homes):
        order = "1203"
        def get(s): return self.d[letter + s]
        scale = get("scale")
        vel = min(get("maxvel"), self.ideal_maxvel(scale))
        # linuxcnc doesn't like having home right on an end of travel,
        # so extend the travel limit by up to .01in or .1mm
        minlim = get("minlim")
        maxlim = get("maxlim")
        home = get("homepos")
        if self.d.units == MM:
            extend = .001
        else:
            extend = .01
        minlim = min(minlim, home - extend)
        maxlim = max(maxlim, home + extend)
        axis_letter = letter.upper()

        print(file=file)
        print("[AXIS_%s]" % axis_letter, file=file)
        print("MAX_VELOCITY = %s" % vel, file=file)
        print("MAX_ACCELERATION = %s" % get("maxacc"), file=file)
        print("MIN_LIMIT = %s" % minlim, file=file)
        print("MAX_LIMIT = %s" % maxlim, file=file)
        print(file=file)
        print("[JOINT_%d]" % num, file=file)
        print("TYPE = %s" % type, file=file)
        print("HOME = %s" % get("homepos"), file=file)
        print("MIN_LIMIT = %s" % minlim, file=file)
        print("MAX_LIMIT = %s" % maxlim, file=file)
        print("MAX_VELOCITY = %s" % vel, file=file)
        print("MAX_ACCELERATION = %s" % get("maxacc"), file=file)
        print("STEPGEN_MAXACCEL = %s" % (1.25 * get("maxacc")), file=file)
        print("SCALE = %s" % scale, file=file)
        if num == 3:
<<<<<<< HEAD
            print >>file, "FERROR = 1"
            print >>file, "MIN_FERROR = .25"
        elif self.d.units == MM:
            print >>file, "FERROR = 1"
            print >>file, "MIN_FERROR = .25"
=======
            print("FERROR = 1", file=file)
            print("MIN_FERROR = .25", file=file)
        elif self.d.units:
            print("FERROR = 1", file=file)
            print("MIN_FERROR = .25", file=file)
>>>>>>> upstream/master
        else:
            print("FERROR = 0.05", file=file)
            print("MIN_FERROR = 0.01", file=file)


        inputs = self.p.build_input_set()
        thisaxishome = set((d_hal_input[ALL_HOME], d_hal_input[ALL_LIMIT_HOME], "home-" + letter, "min-home-" + letter,
                            "max-home-" + letter, "both-home-" + letter))
        # no need to set HOME_IGNORE_LIMITS when ALL_LIMIT_HOME, HAL logic will do the trick
        ignore = set(("min-home-" + letter, "max-home-" + letter,
                            "both-home-" + letter))
        homes = bool(inputs & thisaxishome)
    
        if homes:
            print("HOME_OFFSET = %f" % get("homesw"), file=file)
            print("HOME_SEARCH_VEL = %f" % get("homevel"), file=file)
            latchvel = get("homevel") / abs(get("homevel"))
            if get("latchdir"): latchvel = -latchvel
            # set latch velocity to one step every two servo periods
            # to ensure that we can capture the position to within one step
            latchvel = latchvel * 500 / get("scale")
            # don't do the latch move faster than the search move
            if abs(latchvel) > abs(get("homevel")):
                latchvel = latchvel * (abs(get("homevel"))/abs(latchvel))
            print("HOME_LATCH_VEL = %f" % latchvel, file=file)
            if inputs & ignore:
                print("HOME_IGNORE_LIMITS = YES", file=file)
            if all_homes:
                if self.d.axes == XYUV: # XYUV
                    if letter in('y','v'): hs = 1
                    else: hs = 0
                    print("HOME_SEQUENCE = %d"% hs, file=file)
                else:
                    print("HOME_SEQUENCE = %s" % order[num], file=file)
        else:
            print("HOME_OFFSET = %s" % get("homepos"), file=file)

    def ideal_maxvel(self, scale):
        if self.p.doublestep():
            return abs(.95 * 1e9 / self.p.ideal_period() / scale)
        else:
            return abs(.95 * .5 * 1e9 / self.p.ideal_period() / scale)


    # Boiler code
    def __getitem__(self, item):
        return getattr(self, item)
    def __setitem__(self, item, value):
        return setattr(self, item, value)
