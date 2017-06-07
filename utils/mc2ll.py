#!/usr/bin/env python
#coding:utf-8

import sys
import math
import coord_tool

if len(sys.argv) == 2:
    parts = sys.argv[1].split(",")
    print coord_tool.convert_mc2ll(float(parts[0].strip()), float(parts[1].strip()));
elif len(sys.argv) == 3:
    print coord_tool.convert_mc2ll(float(sys.argv[1]), float(sys.argv[2]));
else:
    print "Usage: %s mc_x mc_y, or %s mc_x,mc_y" % (sys.argv[0], sys.argv[0])
