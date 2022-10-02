# Copyright (C) 2022 Christian Bergman
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

import math
import svgwrite

class Ariston:
    radius = 160        #disc radius in 
    hole_width = 2.5    # width of a pin hole in 
    
    # midi notes for each pipe
    tones = [
        45,
        47,
        50,
        52,
        57,
        59,
        61,
        62,
        64,
        66,
        68,
        69,
        71,
        73,
        74,
        75,
        76,
        78,
        79,
        80,
        81,
        83,
        85,
        86]
        
    # distance of a pin hole from center in 
    def toneToX(self, tone):
        pipe = self.tones.index(tone)
        return 70 + pipe*3.75

    # draw the outer circle, the center hole and the mounting holes
    def drawOutlines(self, svg_document):
        svg_document.add(svg_document.circle(
            center = ('160', '160'), r = '160', stroke='black', fill='none'))

        svg_document.add(svg_document.circle(
            center = ('160', '160'), r = '5', stroke='blue', fill='none'))

        svg_document.add(svg_document.circle(
            center = ('195', '160'), r = '3', stroke='blue', fill='none'))

        svg_document.add(svg_document.circle(
            center = ('160', '195'), r = '3', stroke='blue', fill='none'))

        svg_document.add(svg_document.circle(
            center = ('125', '160'), r = '3', stroke='blue', fill='none'))

        svg_document.add(svg_document.circle(
            center = ('160', '125'), r = '3', stroke='blue', fill='none'))
  
    