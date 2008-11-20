#! /usr/bin/python -O
# -*- coding: utf-8 -*-
#
#    CANTA - A free entertaining educational software for singing
#    Copyright (C) 2007  S. Huchler, A. Kattner, F. Lopez
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys, os
import pygst
pygst.require("0.10")
import gst

import os
import time
import random
import math

NUM_IMPL = 'numeric'

# needs to be tested:
#if pygame.version.vernum > (1,8):
#   NUM_IMPL = 'numpy'

if NUM_IMPL == 'numeric':
    import Numeric as N
elif NUM_IMPL == 'numpy':
    import numpy
from player import Player

class GSTPlayer(Player):
    
    def __init__(self, path=None, file=None, time=0.0):
        Player.__init__(self, path, file, time)
        self.playbin = gst.element_factory_make("playbin", "player")
        self.clock = None
        self.time_format = gst.Format(gst.FORMAT_TIME)


    def load(self, path=None, file=None):
        self.loaded = True
        if path != None:
            self.path=path
        if file != None:
            self.file=file
        filepath = os.path.abspath(os.path.join(self.path, self.file))
        self.playbin.set_state(gst.STATE_NULL)       
        self.playbin.set_property("uri", "file://" + filepath)
        self.clock = self.playbin.get_clock()

    def stop(self):
        self.playbin.set_state(gst.STATE_NULL)

    def play(self, start=0, length=None):
        result = self.playbin.set_state(gst.STATE_PAUSED)
        self.playbin.get_state() # block until the state is really changed
        seek_ns = start * 1000000000
        self.playbin.seek_simple(self.time_format, gst.SEEK_FLAG_FLUSH, seek_ns)
        self.playbin.set_state(gst.STATE_PLAYING)
        if length !=None:
            time.sleep(length)
            self.playbin.set_state(gst.STATE_NULL)
        self._play()

    def is_paused(self):
        """
            Returns True if the player is currently paused
        """
        return self._get_gst_state() == gst.STATE_PAUSED

    def _get_gst_state(self):
        """
            Returns the raw GStreamer state
        """
        return self.playbin.get_state(timeout=50*gst.MSECOND)[1]
               
    def get_pos(self):
        state = self.playbin.get_state(timeout=50*gst.MSECOND)[1]
        if self.is_paused():
            return "pause"
        elif state == gst.STATE_PLAYING:         
            try:
                duration, format = self.playbin.query_duration(gst.FORMAT_TIME)
                pos = self.playbin.query_position(gst.FORMAT_TIME)[0]
                if pos < duration:
                    return pos / 1000000000.
                else:
                    return "end"
            except gst.QueryError:
                return 0
        else:
            # catch some states like READY (others?)
            return None
        
    def pause(self):
        self.playbin.set_state(gst.STATE_PAUSED)
        self._pause()

    def beep(self, freq, dur=0.1):
        pipeline = gst.Pipeline("mypipeline")
        audiotestsrc = gst.element_factory_make("audiotestsrc", "audio")
        pipeline.add(audiotestsrc)
        sink = gst.element_factory_make("autoaudiosink", "sink")
        pipeline.add(sink)
        audiotestsrc.link(sink)
        audiotestsrc.set_property("freq", freq)
        pipeline.set_state(gst.STATE_PLAYING)
        time.sleep(dur)
        pipeline.set_state(gst.STATE_NULL)
        
    def fadeout(self):
        print "not implemented yet"

 

def main():
    x = GSTPlayer()
    if len(sys.argv) > 1:
        f = sys.argv[1]
    else:
        print "Usage:  %s [OPTION]... [FILE]" % (sys.argv[0])
        sys.exit()
    x.load('', f)
    x.play()
    raw_input('hit key to pause')
    x.pause()
    print "pause at: ", x.get_pos()
    raw_input('hit a key to unpause')
    x.play()
    raw_input('hit a key to stop')
    x.stop()
    
if __name__ == '__main__': main()


