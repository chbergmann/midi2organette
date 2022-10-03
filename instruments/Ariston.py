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
    radius = 160        # disc radius in mm
    hole_width = 2.5    # width of a pin hole in mm
    
    # midi notes for each pipe
    tones = ['A_1',
            'H_1',
            'D_2',
            'E_2',
            'A_2',
            'H_2',
            'C#3',
            'D_3',
            'E_3',
            'F#3',
            'G#3',
            'A_3',
            'H_3',
            'C#4',
            'D_4',
            'D#4',
            'E_4',
            'F#4',
            'G_4',
            'G#4',
            'A_4',
            'H_4',
            'C#5',
            'D_5']
        
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
  
    # draw text onto the disc
    # may not be supported by all SVG viewers
    def drawText(self, svg_document, text):
        svg_document.add(svg_document.path('M160,215 a55,55 0 1 1 0.1,0', id='MyTextPath', stroke='none', fill='none'))
        path = svg_document.textPath('#MyTextPath', text, fill='red', stroke='none')
        svgtxt = svg_document.text("")
        svgtxt.add(path)
        svg_document.add(svgtxt)

        