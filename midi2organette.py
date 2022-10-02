#!/usr/bin/env python

# Copyright (C) 2022 Christian Bergmann
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
import mido
import svgwrite
import math
from instruments import Ariston

def drawArcHole(svg_document, organette, tone, startangle, endangle):
    r = organette.toneToX(tone)
    x = organette.radius + r * math.sin(startangle)
    y = organette.radius + r * math.cos(startangle)
    xe = organette.radius + r * math.sin(endangle)
    ye = organette.radius + r * math.cos(endangle)
    r2 = organette.toneToX(tone) + organette.hole_width
    x2 = organette.radius + r2 * math.sin(startangle)
    y2 = organette.radius + r2 * math.cos(startangle)
    xe2 = organette.radius + r2 * math.sin(endangle)
    ye2 = organette.radius + r2 * math.cos(endangle)
    path = "M" + str(x) + "," + str(y)
    path += " A" + str(r) + "," + str(r) + " 0 0 0 " + str(xe) + "," + str(ye)
    path += " L" + str(xe2) + "," + str(ye2)
    path += " A" + str(r2) + "," + str(r2) + " 0 0 1 " + str(x2) + "," + str(y2)
    path += " z"
    
    svg_document.add(svg_document.path(d = path, stroke='blue', fill='none'))
        
def CreateTestDisc(svg_document, organette): 
    i = 0   
    for tone in organette.tones:
        angle1 = 2*math.pi/len(organette.tones) * i
        angle2 = 2*math.pi/len(organette.tones) * (i+0.75)
        drawArcHole(svg_document, organette, tone, angle1, angle2)
        i += 1
        
        
organette = Ariston.Ariston()
diameter = str(organette.radius*2)
svg_document = svgwrite.Drawing(size = (diameter+'mm', diameter+'mm'), viewBox="0 0 " + diameter + " " + diameter)
organette.drawOutlines(svg_document)
CreateTestDisc(svg_document, organette)

print(svg_document.tostring())

