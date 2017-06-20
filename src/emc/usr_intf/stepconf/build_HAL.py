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
#    This builds the HAL files from the collected data.
#
import os
import time
import shutil
from stepconf.definitions import *

class HAL:
    def __init__(self,app):
        # access to:
        self.d = app.d  # collected data
        self.a = app    # The parent, stepconf

    def write_halfile(self, base):
        inputs = self.a.build_input_set()
        outputs = self.a.build_output_set()

        filename = os.path.join(base, self.d.machinename + ".hal")
        file = open(filename, "w")
        print >>file, _("# Generated by stepconf 1.1 at %s") % time.asctime()
        print >>file, _("# If you make changes to this file, they will be").encode('utf-8')
        print >>file, _("# overwritten when you run stepconf again").encode('utf-8')
        """
        if self.d.pyvcp:
            size = pos = geo = ""
            if self.d.pyvcpposition or self.d.pyvcpsize:
                if self.d.pyvcpposition:
                    pos = "+%d+%d"% (self.d.pyvcpxpos,self.d.pyvcpypos)
                if self.d.pyvcpsize:
                    size = "%dx%d"% (self.d.pyvcpwidth,self.d.pyvcpheight)
                geo = " -g %s%s"%(size,pos)
            print >>file, "loadusr -Wn pyvcp pyvcp%s -c pyvcp [DISPLAY](PYVCP)"%(geo)
            print >>file, "source postgui_call_list.hal"
        """
        if self.d.gladevcp and self.d.standalonegvcp:
            fmax = geo = pos = size =  ""
            if self.d.gladevcpposition or self.d.gladevcpsize:
                if self.d.gladevcpposition:
                    pos = "+%d+%d"% (self.d.gladevcpxpos,self.d.gladevcpypos)
                if self.d.gladevcpsize:
                    size = "%dx%d"% (self.d.gladevcpwidth,self.d.gladevcpheight)
                geo = " -g %s%s"%(size,pos)
            if self.d.gladevcpforcemax: fmax = " -m True"
            theme = self.d.gladevcptheme
            if theme == "Follow System Theme":theme = ""
            else: theme = " -t "+theme
            print >>file, "loadusr -Wn gladevcp gladevcp -c gladevcp%s%s%s -H gvcp_call_list.hal gvcp-panel.ui"%(theme,fmax,geo)
        print >>file, "loadrt [KINS]KINEMATICS"
        print >>file, "loadrt [EMCMOT]EMCMOT base_period_nsec=[EMCMOT]BASE_PERIOD servo_period_nsec=[EMCMOT]SERVO_PERIOD num_joints=[KINS]JOINTS"
        port3name=port2name=port2dir=port3dir=""
        if self.d.number_pports>2:
             port3name = ' '+self.d.ioaddr3
             if self.d.pp3_direction: # Input option
                port3dir =" in"
             else: 
                port3dir =" out"
        if self.d.number_pports>1:
             port2name = ' '+self.d.ioaddr2
             if self.d.pp2_direction: # Input option
                port2dir =" in"
             else: 
                port2dir =" out"
        if not self.d.sim_hardware:
            print >>file, "loadrt hal_parport cfg=\"%s out%s%s%s%s\"" % (self.d.ioaddr, port2name, port2dir, port3name, port3dir)
        else:
            name='parport.0'
            if self.d.number_pports>1:
                name='parport.0,parport.1'
            print >>file, "loadrt sim_parport names=%s"%name
        if self.a.doublestep():
            print >>file, "setp parport.0.reset-time %d" % self.d.steptime
        encoder = d_hal_input[PHA] in inputs
        counter = d_hal_input[PHB] not in inputs
        probe = d_hal_input[PROBE] in inputs
        limits_homes = d_hal_input[ALL_LIMIT_HOME] in inputs
        pwm = d_hal_output[PWM] in outputs
        pump = d_hal_output[PUMP] in outputs
        if self.d.axes == 0:
            print >>file, "loadrt stepgen step_type=0,0,0"
        elif self.d.axes in(1,3):
            print >>file, "loadrt stepgen step_type=0,0,0,0"
        elif self.d.axes == 2:
            print >>file, "loadrt stepgen step_type=0,0"


        if encoder:
            print >>file, "loadrt encoder num_chan=1"
        if self.d.pyvcphaltype == 1 and self.d.pyvcpconnect == 1:
            if encoder:
               print >>file, "loadrt abs count=1"
               print >>file, "loadrt scale count=1"
               print >>file, "loadrt lowpass count=1"
               if self.d.usespindleatspeed:
                   print >>file, "loadrt near"
        if pump:
            print >>file, "loadrt charge_pump"
            print >>file, "net estop-out charge-pump.enable iocontrol.0.user-enable-out"
            print >>file, "net charge-pump <= charge-pump.out"

        if limits_homes:
            print >>file, "loadrt lut5"

        if pwm:
            print >>file, "loadrt pwmgen output_type=1"


        if self.d.classicladder:
            print >>file, "loadrt classicladder_rt numPhysInputs=%d numPhysOutputs=%d numS32in=%d numS32out=%d numFloatIn=%d numFloatOut=%d" % (self.d.digitsin , self.d.digitsout , self.d.s32in, self.d.s32out, self.d.floatsin, self.d.floatsout)

        print >>file
        print >>file, "addf parport.0.read base-thread"
        if self.d.number_pports > 1:
            print >>file, "addf parport.1.read base-thread"
        if self.d.number_pports > 2:
            print >>file, "addf parport.2.read base-thread"
        if self.d.sim_hardware:
            print >>file, "source sim_hardware.hal"
            if encoder:
                print >>file, "addf sim-encoder.make-pulses base-thread"
        print >>file, "addf stepgen.make-pulses base-thread"
        if encoder: print >>file, "addf encoder.update-counters base-thread"
        if pump: print >>file, "addf charge-pump base-thread"
        if pwm: print >>file, "addf pwmgen.make-pulses base-thread"
        print >>file, "addf parport.0.write base-thread"
        if self.a.doublestep():
            print >>file, "addf parport.0.reset base-thread"
        if self.d.number_pports > 1:
            print >>file, "addf parport.1.write base-thread"
        if self.d.number_pports > 2:
            print >>file, "addf parport.2.write base-thread"
        print >>file
        print >>file, "addf stepgen.capture-position servo-thread"
        if self.d.sim_hardware:
            print >>file, "addf sim-hardware.update servo-thread"
            if encoder:
                print >>file, "addf sim-encoder.update-speed servo-thread"
        if encoder: print >>file, "addf encoder.capture-position servo-thread"
        print >>file, "addf motion-command-handler servo-thread"
        print >>file, "addf motion-controller servo-thread"
        if self.d.classicladder:
            print >>file,"addf classicladder.0.refresh servo-thread"
        print >>file, "addf stepgen.update-freq servo-thread"

        if limits_homes:
            print >>file, "addf lut5.0 servo-thread"

        if pwm: print >>file, "addf pwmgen.update servo-thread"
        if self.d.pyvcphaltype == 1 and self.d.pyvcpconnect == 1:
            if encoder:
               print >>file, "addf abs.0 servo-thread"
               print >>file, "addf scale.0 servo-thread"
               print >>file, "addf lowpass.0 servo-thread"
               if self.d.usespindleatspeed:
                   print >>file, "addf near.0 servo-thread"
        if pwm:
            x1 = self.d.spindlepwm1
            x2 = self.d.spindlepwm2
            y1 = self.d.spindlespeed1
            y2 = self.d.spindlespeed2
            scale = (y2-y1) / (x2-x1)
            offset = x1 - y1 / scale
            print >>file
            print >>file, "net spindle-cmd-rpm => pwmgen.0.value"
            print >>file, "net spindle-on <= motion.spindle-on => pwmgen.0.enable"
            print >>file, "net spindle-pwm <= pwmgen.0.pwm"
            print >>file, "setp pwmgen.0.pwm-freq %s" % self.d.spindlecarrier        
            print >>file, "setp pwmgen.0.scale %s" % scale
            print >>file, "setp pwmgen.0.offset %s" % offset
            print >>file, "setp pwmgen.0.dither-pwm true"

        print >>file, "net spindle-cmd-rpm     <= motion.spindle-speed-out"
        print >>file, "net spindle-cmd-rpm-abs <= motion.spindle-speed-out-abs"
        print >>file, "net spindle-cmd-rps     <= motion.spindle-speed-out-rps"
        print >>file, "net spindle-cmd-rps-abs <= motion.spindle-speed-out-rps-abs"
        print >>file, "net spindle-at-speed    => motion.spindle-at-speed"
        if d_hal_output[ON] in outputs and not pwm:
            print >>file, "net spindle-on <= motion.spindle-on"
        if d_hal_output[CW] in outputs:
            print >>file, "net spindle-cw <= motion.spindle-forward"
        if d_hal_output[CCW] in outputs:
            print >>file, "net spindle-ccw <= motion.spindle-reverse"
        if d_hal_output[BRAKE] in outputs:
            print >>file, "net spindle-brake <= motion.spindle-brake"

        if d_hal_output[MIST] in outputs:
            print >>file, "net coolant-mist <= iocontrol.0.coolant-mist"

        if d_hal_output[FLOOD] in outputs:
            print >>file, "net coolant-flood <= iocontrol.0.coolant-flood"

        if encoder:
            print >>file
            if d_hal_input[PHB] not in inputs:
                print >>file, "setp encoder.0.position-scale %f"\
                     % self.d.spindlecpr
                print >>file, "setp encoder.0.counter-mode 1"
            else:
                print >>file, "setp encoder.0.position-scale %f" \
                    % ( 4.0 * int(self.d.spindlecpr))
            print >>file, "net spindle-position encoder.0.position => motion.spindle-revs"
            print >>file, "net spindle-velocity-feedback-rps encoder.0.velocity => motion.spindle-speed-in"
            print >>file, "net spindle-index-enable encoder.0.index-enable <=> motion.spindle-index-enable"
            print >>file, "net spindle-phase-a encoder.0.phase-A"
            print >>file, "net spindle-phase-b encoder.0.phase-B"
            print >>file, "net spindle-index encoder.0.phase-Z"


        if probe:
            print >>file
            print >>file, "net probe-in => motion.probe-input"

        for i in range(4):
            dout = "dout-%02d" % i
            if dout in outputs:
                print >>file, "net %s <= motion.digital-out-%02d" % (dout, i)

        for i in range(4):
            din = "din-%02d" % i
            if din in inputs:
                print >>file, "net %s => motion.digital-in-%02d" % (din, i)

        print >>file
        for o in (1,2,3,4,5,6,7,8,9,14,16,17): self.connect_output(file, o)
        if self.d.number_pports>1:
            if self.d.pp2_direction:# Input option
                pinlist = (1,14,16,17)
            else:
                pinlist = (1,2,3,4,5,6,7,8,9,14,16,17)
            print >>file
            for i in pinlist: self.connect_output(file, i,1)
            print >>file

        for i in (10,11,12,13,15): self.connect_input(file, i)
        if self.d.number_pports>1:
            if self.d.pp2_direction: # Input option
                pinlist = (2,3,4,5,6,7,8,9,10,11,12,13,15)
            else:
                pinlist = (10,11,12,13,15)
            print >>file
            for i in pinlist: self.connect_input(file, i,1)
            print >>file

        if limits_homes:
            print >>file, "setp lut5.0.function 0x10000"
            print >>file, "net all-limit-home => lut5.0.in-4"
            print >>file, "net all-limit <= lut5.0.out"
            if self.d.axes == 2:
                print >>file, "net homing-x <= joint.0.homing => lut5.0.in-0"
                print >>file, "net homing-z <= joint.1.homing => lut5.0.in-1"
            elif self.d.axes == 0:
                print >>file, "net homing-x <= joint.0.homing => lut5.0.in-0"
                print >>file, "net homing-y <= joint.1.homing => lut5.0.in-1"
                print >>file, "net homing-z <= joint.2.homing => lut5.0.in-2"
            elif self.d.axes == 1:
                print >>file, "net homing-x <= joint.0.homing => lut5.0.in-0"
                print >>file, "net homing-y <= joint.1.homing => lut5.0.in-1"
                print >>file, "net homing-z <= joint.2.homing => lut5.0.in-2"
                print >>file, "net homing-a <= joint.3.homing => lut5.0.in-3"
            elif self.d.axes == 3:
                print >>file, "net homing-x <= joint.0.homing => lut5.0.in-0"
                print >>file, "net homing-y <= joint.1.homing => lut5.0.in-1"
                print >>file, "net homing-u <= joint.6.homing => lut5.0.in-2"
                print >>file, "net homing-v <= joint.7.homing => lut5.0.in-3"

        if self.d.axes == 2:
            self.connect_joint(file, 0, 'x')
            self.connect_joint(file, 1, 'z')
        elif self.d.axes == 0:
            self.connect_joint(file, 0, 'x')
            self.connect_joint(file, 1, 'y')
            self.connect_joint(file, 2, 'z')
        elif self.d.axes == 1:
            self.connect_joint(file, 0, 'x')
            self.connect_joint(file, 1, 'y')
            self.connect_joint(file, 2, 'z')
            self.connect_joint(file, 3, 'a')
        elif self.d.axes == 3:
            self.connect_joint(file, 0, 'x')
            self.connect_joint(file, 1, 'y')
            self.connect_joint(file, 2, 'u')
            self.connect_joint(file, 3, 'v')

        print >>file
        print >>file, "net estop-out <= iocontrol.0.user-enable-out"
        if  self.d.classicladder and self.d.ladderhaltype == 1 and self.d.ladderconnect: # external estop program
            print >>file 
            print >>file, _("# **** Setup for external estop ladder program -START ****")
            print >>file
            print >>file, "net estop-out => classicladder.0.in-00"
            print >>file, "net estop-ext => classicladder.0.in-01"
            print >>file, "net estop-strobe classicladder.0.in-02 <= iocontrol.0.user-request-enable"
            print >>file, "net estop-outcl classicladder.0.out-00 => iocontrol.0.emc-enable-in"
            print >>file
            print >>file, _("# **** Setup for external estop ladder program -END ****")
        elif d_hal_input[ESTOP_IN] in inputs:
            print >>file, "net estop-ext => iocontrol.0.emc-enable-in"
        else:
            print >>file, "net estop-out => iocontrol.0.emc-enable-in"

        print >>file
        if self.d.manualtoolchange:
            print >>file, "loadusr -W hal_manualtoolchange"
            print >>file, "net tool-change iocontrol.0.tool-change => hal_manualtoolchange.change"
            print >>file, "net tool-changed iocontrol.0.tool-changed <= hal_manualtoolchange.changed"
            print >>file, "net tool-number iocontrol.0.tool-prep-number => hal_manualtoolchange.number"

        else:
            print >>file, "net tool-number <= iocontrol.0.tool-prep-number"
            print >>file, "net tool-change-loopback iocontrol.0.tool-change => iocontrol.0.tool-changed"
        print >>file, "net tool-prepare-loopback iocontrol.0.tool-prepare => iocontrol.0.tool-prepared"
        if self.d.classicladder:
            print >>file
            if self.d.modbus:
                print >>file, _("# Load Classicladder with modbus master included (GUI must run for Modbus)")
                print >>file, "loadusr classicladder --modmaster custom.clp"
            else:
                print >>file, _("# Load Classicladder without GUI (can reload LADDER GUI in AXIS GUI")
                print >>file, "loadusr classicladder --nogui custom.clp"
        if self.d.pyvcp:
            vcp = os.path.join(base, self.d.pyvcpname)
            if not os.path.exists(vcp):
                f1 = open(vcp, "w")

                print >>f1, "<?xml version='1.0' encoding='UTF-8'?>"

                print >>f1, "<!-- "
                print >>f1, _("Include your PyVCP panel here.\n")
                print >>f1, "-->"
                print >>f1, "<pyvcp>"
                print >>f1, "</pyvcp>"

        # Same as from pncconf
        # the jump list allows multiple hal files to be loaded postgui
        # this simplifies the problem of overwritting the users custom HAL code
        # when they change pyvcp sample options
        # if the user picked existing pyvcp option and the postgui_call_list is present
        # don't overwrite it. otherwise write the file.
        calllist_filename = os.path.join(base, "postgui_call_list.hal")
        f1 = open(calllist_filename, "w")
        print >>f1, _("# These files are loaded post GUI, in the order they appear")
        print >>f1, _("# Generated by stepconf 1.1 at %s") % time.asctime()
        print >>f1, _("# If you make changes to this file, they will be").encode('utf-8')
        print >>f1, _("# overwritten when you run stepconf again").encode('utf-8')
        print >>f1
        if (self.d.pyvcp):
            print >>f1, "source pyvcp_options.hal"
        print >>f1, "source custom_postgui.hal"
        f1.close()

        # If the user asked for pyvcp sample panel add the HAL commands too
        pyfilename = os.path.join(base, "pyvcp_options.hal")
        f1 = open(pyfilename, "w")
        if self.d.pyvcp and self.d.pyvcphaltype == 1 and self.d.pyvcpconnect: # spindle speed/tool # display
            print >>f1, _("# These files are loaded post GUI, in the order they appear")
            print >>f1, _("# Generated by stepconf 1.1 at %s") % time.asctime()
            print >>f1, _("# If you make changes to this file, they will be").encode('utf-8')
            print >>f1, _("# overwritten when you run stepconf again").encode('utf-8')
            print >>f1, _("# **** Setup of spindle speed display using pyvcp -START ****")
            if encoder:
                print >>f1, _("# **** Use ACTUAL spindle velocity from spindle encoder")
                print >>f1, _("# **** spindle-velocity-feedback-rps bounces around so we filter it with lowpass")
                print >>f1, _("# **** spindle-velocity-feedback-rps is signed so we use absolute component to remove sign") 
                print >>f1, _("# **** ACTUAL velocity is in RPS not RPM so we scale it.")
                print >>f1
                print >>f1, ("setp scale.0.gain 60")
                print >>f1, ("setp lowpass.0.gain %f")% self.d.spindlefiltergain
                print >>f1, ("net spindle-velocity-feedback-rps               => lowpass.0.in")
                print >>f1, ("net spindle-fb-filtered-rps      lowpass.0.out  => abs.0.in")
                print >>f1, ("net spindle-fb-filtered-abs-rps  abs.0.out      => scale.0.in")
                print >>f1, ("net spindle-fb-filtered-abs-rpm  scale.0.out    => pyvcp.spindle-speed")
                print >>f1
                print >>f1, _("# **** set up spindle at speed indicator ****")
                if self.d.usespindleatspeed:
                    print >>f1
                    print >>f1, ("net spindle-cmd-rps-abs             =>  near.0.in1")
                    print >>f1, ("net spindle-velocity-feedback-rps   =>  near.0.in2")
                    print >>f1, ("net spindle-at-speed                <=  near.0.out")
                    print >>f1, ("setp near.0.scale %f")% self.d.spindlenearscale
                else:
                    print >>f1, ("# **** force spindle at speed indicator true because we chose no feedback ****")
                    print >>f1
                    print >>f1, ("sets spindle-at-speed true")
                print >>f1, ("net spindle-at-speed       => pyvcp.spindle-at-speed-led")
            else:
                print >>f1, _("# **** Use COMMANDED spindle velocity from LinuxCNC because no spindle encoder was specified")
                print >>f1
                print >>f1, ("net spindle-cmd-rpm-abs    => pyvcp.spindle-speed")
                print >>f1
                print >>f1, ("# **** force spindle at speed indicator true because we have no feedback ****")
                print >>f1
                print >>f1, ("net spindle-at-speed => pyvcp.spindle-at-speed-led")
                print >>f1, ("sets spindle-at-speed true")
            f1.close()
        else:
            print >>f1, _("# These files are loaded post GUI, in the order they appear")
            print >>f1, _("# Generated by stepconf 1.1 at %s") % time.asctime()
            print >>f1, _("# If you make changes to this file, they will be").encode('utf-8')
            print >>f1, _("# overwritten when you run stepconf again").encode('utf-8')
            print >>f1, ("sets spindle-at-speed true")
            f1.close()

        # stepconf adds custom.hal and custom_postgui.hal file if one is not present
        if self.d.customhal or self.d.classicladder or self.d.halui_custom:
            for i in ("custom","custom_postgui"):
                custom = os.path.join(base, i+".hal")
                if not os.path.exists(custom):
                    f1 = open(custom, "w")
                    print >>f1, _("# Include your %s HAL commands here")%i
                    print >>f1, _("# This file will not be overwritten when you run stepconf again").encode('utf-8')
                    print >>f1
                    f1.close()

        file.close()
        self.sim_hardware_halfile(base)
        self.d.add_md5sum(filename)

#******************
# HELPER FUNCTIONS
#******************

    def connect_joint(self, file, num, let):
        axnum = "xyzabcuvw".index(let)
        lat = self.d.latency
        print >>file
        print >>file, "setp stepgen.%d.position-scale [JOINT_%d]SCALE" % (num, num)
        print >>file, "setp stepgen.%d.steplen 1" % num
        if self.a.doublestep():
            print >>file, "setp stepgen.%d.stepspace 0" % num
        else:
            print >>file, "setp stepgen.%d.stepspace 1" % num
        print >>file, "setp stepgen.%d.dirhold %d" % (num, self.d.dirhold + lat)
        print >>file, "setp stepgen.%d.dirsetup %d" % (num, self.d.dirsetup + lat)
        print >>file, "setp stepgen.%d.maxaccel [JOINT_%d]STEPGEN_MAXACCEL" % (num, num)
        print >>file, "net %spos-cmd joint.%d.motor-pos-cmd => stepgen.%d.position-cmd" % (let, num, num)
        print >>file, "net %spos-fb stepgen.%d.position-fb => joint.%d.motor-pos-fb" % (let, num, num)
        print >>file, "net %sstep <= stepgen.%d.step" % (let, num)
        print >>file, "net %sdir <= stepgen.%d.dir" % (let, num)
        print >>file, "net %senable joint.%d.amp-enable-out => stepgen.%d.enable" % (let, num, num)
        homesig = self.a.home_sig(let)
        if homesig:
            print >>file, "net %s => joint.%d.home-sw-in" % (homesig, num)
        min_limsig = self.min_lim_sig(let)
        if min_limsig:
            print >>file, "net %s => joint.%d.neg-lim-sw-in" % (min_limsig, num)
        max_limsig = self.max_lim_sig(let)
        if max_limsig:
            print >>file, "net %s => joint.%d.pos-lim-sw-in" % (max_limsig, num)

    def sim_hardware_halfile(self,base):
        custom = os.path.join(base, "sim_hardware.hal")
        if self.d.sim_hardware:
            f1 = open(custom, "w")
            print >>f1, _("# This file sets up simulated limits/home/spindle encoder hardware.")
            print >>f1, _("# This is a generated file do not edit.")
            print >>f1
            inputs = self.a.build_input_set()
            if d_hal_input[PHA] in inputs:
                print >>f1, "loadrt sim_encoder names=sim-encoder"
                print >>f1, "setp sim-encoder.ppr %d"%int(self.d.spindlecpr)
                print >>f1, "setp sim-encoder.scale 1"
                print >>f1
                print >>f1, "net spindle-cmd-rps            sim-encoder.speed"
                print >>f1, "net fake-spindle-phase-a       sim-encoder.phase-A"
                print >>f1, "net fake-spindle-phase-b       sim-encoder.phase-B"
                print >>f1, "net fake-spindle-index         sim-encoder.phase-Z"
                print >>f1
            print >>f1, "loadrt sim_axis_hardware names=sim-hardware"
            print >>f1
            print >>f1, "net Xjoint-pos-fb      joint.0.pos-fb      sim-hardware.Xcurrent-pos"
            if self.d.axes in(0, 1): # XYZ XYZA
                print >>f1, "net Yjoint-pos-fb      joint.1.pos-fb      sim-hardware.Ycurrent-pos"
                print >>f1, "net Zjoint-pos-fb      joint.2.pos-fb      sim-hardware.Zcurrent-pos"
            if self.d.axes == 2: # XZ
                print >>f1, "net Zjoint-pos-fb      joint.1.pos-fb      sim-hardware.Zcurrent-pos"
            if self.d.axes == 1: # XYZA
                print >>f1, "net Ajoint-pos-fb      joint.3.pos-fb      sim-hardware.Acurrent-pos"
            if self.d.axes == 3: # XYUV
                print >>f1, "net Yjoint-pos-fb      joint.1.pos-fb      sim-hardware.Ycurrent-pos"
                print >>f1, "net Ujoint-pos-fb      joint.2.pos-fb      sim-hardware.Ucurrent-pos"
                print >>f1, "net Vjoint-pos-fb      joint.3.pos-fb      sim-hardware.Vcurrent-pos"
            print >>f1
            print >>f1, "setp sim-hardware.Xmaxsw-upper 1000"
            print >>f1, "setp sim-hardware.Xmaxsw-lower [JOINT_0]MAX_LIMIT"
            print >>f1, "setp sim-hardware.Xminsw-upper [JOINT_0]MIN_LIMIT"
            print >>f1, "setp sim-hardware.Xminsw-lower -1000"
            print >>f1, "setp sim-hardware.Xhomesw-pos [JOINT_0]HOME_OFFSET"
            print >>f1
            if self.d.axes in(0, 1): # XYZ XYZA
                print >>f1, "setp sim-hardware.Ymaxsw-upper 1000"
                print >>f1, "setp sim-hardware.Ymaxsw-lower [JOINT_1]MAX_LIMIT"
                print >>f1, "setp sim-hardware.Yminsw-upper [JOINT_1]MIN_LIMIT"
                print >>f1, "setp sim-hardware.Yminsw-lower -1000"
                print >>f1, "setp sim-hardware.Yhomesw-pos [JOINT_1]HOME_OFFSET"
                print >>f1
                print >>f1, "setp sim-hardware.Zmaxsw-upper 1000"
                print >>f1, "setp sim-hardware.Zmaxsw-lower [JOINT_2]MAX_LIMIT"
                print >>f1, "setp sim-hardware.Zminsw-upper [JOINT_2]MIN_LIMIT"
                print >>f1, "setp sim-hardware.Zminsw-lower -1000"
                print >>f1, "setp sim-hardware.Zhomesw-pos [JOINT_2]HOME_OFFSET"
                print >>f1
            if self.d.axes == 1: #  XYZA
                print >>f1, "setp sim-hardware.Amaxsw-upper 20000"
                print >>f1, "setp sim-hardware.Amaxsw-lower [JOINT_3]MAX_LIMIT"
                print >>f1, "setp sim-hardware.Aminsw-upper [JOINT_3]MIN_LIMIT"
                print >>f1, "setp sim-hardware.Aminsw-lower -20000"
                print >>f1, "setp sim-hardware.Ahomesw-pos [JOINT_3]HOME_OFFSET"
                print >>f1
            if self.d.axes == 2: # XZ
                print >>f1, "setp sim-hardware.Zmaxsw-upper 1000"
                print >>f1, "setp sim-hardware.Zmaxsw-lower [JOINT_1]MAX_LIMIT"
                print >>f1, "setp sim-hardware.Zminsw-upper [JOINT_1]MIN_LIMIT"
                print >>f1, "setp sim-hardware.Zminsw-lower -1000"
                print >>f1, "setp sim-hardware.Zhomesw-pos [JOINT_1]HOME_OFFSET"
                print >>f1
            if self.d.axes == 3: # XYUV
                print >>f1, "setp sim-hardware.Ymaxsw-upper 1000"
                print >>f1, "setp sim-hardware.Ymaxsw-lower [JOINT_1]MAX_LIMIT"
                print >>f1, "setp sim-hardware.Yminsw-upper [JOINT_1]MIN_LIMIT"
                print >>f1, "setp sim-hardware.Yminsw-lower -1000"
                print >>f1, "setp sim-hardware.Yhomesw-pos [JOINT_1]HOME_OFFSET"
                print >>f1
                print >>f1, "setp sim-hardware.Umaxsw-upper 1000"
                print >>f1, "setp sim-hardware.Umaxsw-lower [JOINT_2]MAX_LIMIT"
                print >>f1, "setp sim-hardware.Uminsw-upper [JOINT_2]MIN_LIMIT"
                print >>f1, "setp sim-hardware.Uminsw-lower -1000"
                print >>f1, "setp sim-hardware.Uhomesw-pos [JOINT_2]HOME_OFFSET"
                print >>f1
                print >>f1, "setp sim-hardware.Vmaxsw-upper 1000"
                print >>f1, "setp sim-hardware.Vmaxsw-lower [JOINT_3]MAX_LIMIT"
                print >>f1, "setp sim-hardware.Vminsw-upper [JOINT_3]MIN_LIMIT"
                print >>f1, "setp sim-hardware.Vminsw-lower -1000"
                print >>f1, "setp sim-hardware.Vhomesw-pos [JOINT_3]HOME_OFFSET"
                print >>f1
            for port in range(0,self.d.number_pports):
                print >>f1
                if port==0 or not self.d.pp2_direction: # output option
                    pinlist = (10,11,12,13,15)
                else:
                    pinlist = (2,3,4,5,6,7,8,9,10,11,12,13,15)
                for i in pinlist:
                    self.connect_input(f1, i, port, True)
                print >>f1
                if port==0 or not self.d.pp2_direction: # output option
                    pinlist = (1,2,3,4,5,6,7,8,9,14,16,17)
                else:
                    pinlist = (1,14,16,17)
                for o in pinlist:
                    self.connect_output(f1, o, port, True) 
            print >>f1
            print >>f1, "net fake-all-home          sim-hardware.homesw-all"
            print >>f1, "net fake-all-limit         sim-hardware.limitsw-all"
            print >>f1, "net fake-all-limit-home    sim-hardware.limitsw-homesw-all"
            print >>f1, "net fake-both-x            sim-hardware.Xbothsw-out"
            print >>f1, "net fake-max-x             sim-hardware.Xmaxsw-out"
            print >>f1, "net fake-min-x             sim-hardware.Xminsw-out"
            print >>f1, "net fake-both-y            sim-hardware.Ybothsw-out"
            print >>f1, "net fake-max-y             sim-hardware.Ymaxsw-out"
            print >>f1, "net fake-min-y             sim-hardware.Yminsw-out"
            print >>f1, "net fake-both-z            sim-hardware.Zbothsw-out"
            print >>f1, "net fake-max-z             sim-hardware.Zmaxsw-out"
            print >>f1, "net fake-min-z             sim-hardware.Zminsw-out"
            print >>f1, "net fake-both-a            sim-hardware.Abothsw-out"
            print >>f1, "net fake-max-a             sim-hardware.Amaxsw-out"
            print >>f1, "net fake-min-a             sim-hardware.Aminsw-out"
            print >>f1, "net fake-both-u            sim-hardware.Ubothsw-out"
            print >>f1, "net fake-max-u             sim-hardware.Umaxsw-out"
            print >>f1, "net fake-min-u             sim-hardware.Uminsw-out"
            print >>f1, "net fake-both-v            sim-hardware.Vbothsw-out"
            print >>f1, "net fake-max-v             sim-hardware.Vmaxsw-out"
            print >>f1, "net fake-min-v             sim-hardware.Vminsw-out"

            print >>f1, "net fake-home-x            sim-hardware.Xhomesw-out"
            print >>f1, "net fake-home-y            sim-hardware.Yhomesw-out"
            print >>f1, "net fake-home-z            sim-hardware.Zhomesw-out"
            print >>f1, "net fake-home-a            sim-hardware.Ahomesw-out"
            print >>f1, "net fake-home-u            sim-hardware.Uhomesw-out"
            print >>f1, "net fake-home-v            sim-hardware.Vhomesw-out"

            print >>f1, "net fake-both-home-x       sim-hardware.Xbothsw-homesw-out"
            print >>f1, "net fake-max-home-x        sim-hardware.Xmaxsw-homesw-out"
            print >>f1, "net fake-min-home-x        sim-hardware.Xminsw-homesw-out"

            print >>f1, "net fake-both-home-y       sim-hardware.Ybothsw-homesw-out"
            print >>f1, "net fake-max-home-y        sim-hardware.Ymaxsw-homesw-out"
            print >>f1, "net fake-min-home-y        sim-hardware.Yminsw-homesw-out"

            print >>f1, "net fake-both-home-z       sim-hardware.Zbothsw-homesw-out"
            print >>f1, "net fake-max-home-z        sim-hardware.Zmaxsw-homesw-out"
            print >>f1, "net fake-min-home-z        sim-hardware.Zminsw-homesw-out"

            print >>f1, "net fake-both-home-a       sim-hardware.Abothsw-homesw-out"
            print >>f1, "net fake-max-home-a        sim-hardware.Amaxsw-homesw-out"
            print >>f1, "net fake-min-home-a        sim-hardware.Aminsw-homesw-out"

            print >>f1, "net fake-both-home-u       sim-hardware.Ubothsw-homesw-out"
            print >>f1, "net fake-max-home-u        sim-hardware.Umaxsw-homesw-out"
            print >>f1, "net fake-min-home-u        sim-hardware.Uminsw-homesw-out"

            print >>f1, "net fake-both-home-v       sim-hardware.Vbothsw-homesw-out"
            print >>f1, "net fake-max-home-v        sim-hardware.Vmaxsw-homesw-out"
            print >>f1, "net fake-min-home-v        sim-hardware.Vminsw-homesw-out"
            f1.close()
        else:
            if os.path.exists(custom):
                os.remove(custom)

    def connect_input(self, file, num,port=0,fake=False):
        ending=''
        if port == 0:
            p = self.d['pin%d' % num]
            i = self.d['pin%dinv' % num]
        else:
            p = self.d['pp2_pin%d_in' % num]
            i = self.d['pp2_pin%d_in_inv' % num]

        if p == d_hal_input[UNUSED_INPUT]: return
        if fake:
            p='fake-'+p
            ending='-fake'
            p ='{0:<20}'.format(p)
        else:
            p ='{0:<15}'.format(p)
        if i and not fake:
            print >>file, "net %s <= parport.%d.pin-%02d-in-not%s" \
                % (p, port, num,ending)
        else:
            print >>file, "net %s <= parport.%d.pin-%02d-in%s" \
                % (p, port, num,ending)

    def connect_output(self, file, num,port=0,fake=False):
        ending=''
        if port == 0:
            p = self.d['pin%d' % num]
            i = self.d['pin%dinv' % num]
        else:
            p = self.d['pp2_pin%d' % num]
            i = self.d['pp2_pin%dinv' % num]
        if p == d_hal_output[UNUSED_OUTPUT]: return
        if fake:
            signame ='fake-'+p
            ending='-fake'
            signame ='{0:<20}'.format(signame)
        else:
            signame ='{0:<15}'.format(p)
        if i: print >>file, "setp parport.%d.pin-%02d-out-invert%s 1" %(port, num, ending)
        print >>file, "net %s => parport.%d.pin-%02d-out%s" % (signame, port, num, ending)
        if self.a.doublestep() and not fake:
            if p in (d_hal_output[XSTEP], d_hal_output[YSTEP], d_hal_output[ZSTEP], d_hal_output[ASTEP], d_hal_output[USTEP], d_hal_output[VSTEP]):
                print >>file, "setp parport.0.pin-%02d-out-reset%s 1" % (num,ending)

    def min_lim_sig(self, axis):
        inputs = self.a.build_input_set()
        thisaxisminlimits = set((d_hal_input[ALL_LIMIT], d_hal_input[ALL_LIMIT_HOME], "min-" + axis, "min-home-" + axis,
                               "both-" + axis, "both-home-" + axis))
        for i in inputs:
            if i in thisaxisminlimits:
                if i==d_hal_input[ALL_LIMIT_HOME]:
                    # ALL_LIMIT is reused here as filtered signal
                    return d_hal_input[ALL_LIMIT]
                else:
                    return i

    def max_lim_sig(self, axis):
        inputs = self.a.build_input_set()
        thisaxismaxlimits = set((d_hal_input[ALL_LIMIT], d_hal_input[ALL_LIMIT_HOME], "max-" + axis, "max-home-" + axis,
                               "both-" + axis, "both-home-" + axis))
        for i in inputs:
            if i in thisaxismaxlimits:
                if i==d_hal_input[ALL_LIMIT_HOME]:
                    # ALL_LIMIT is reused here as filtered signal
                    return d_hal_input[ALL_LIMIT]
                else:
                    return i
    # Boiler code
    def __getitem__(self, item):
        return getattr(self, item)
    def __setitem__(self, item, value):
        return setattr(self, item, value)
