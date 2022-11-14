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

import math
import svgwrite

class Ariston:
    radius = 165        # disc radius in mm
    hole_width = 2.5    # width of a pin hole in mm
    min_angle = 0.011    # minimum hole/gap size in radians
    
    # notes for each pipe      
    tones = [
        'A_2',
        'H_2',
        'D_3',
        'E_3',
        'A_3',
        'H_3',
        'C#4',
        'D_4',
        'E_4',
        'F#4',
        'G_4',
        'A_4',    
        'H_4',
        'C#5',
        'D_5',
        'D#5',
        'E_5',
        'F#5',
        'G_5',
        'G#5',
        'A_5',
        'H_5',
        'C#6',
        'D_6']
        
    # distance of a pin hole from center in mm
    def toneToX(self, tone):
        pipe = self.tones.index(tone)
        return 68 + pipe*3.9

    # draw the outer circle, the center hole and the mounting holes
    def drawOutlines(self, svg_document):
        svg_document.add(svg_document.circle(
            center = (str(self.radius), str(self.radius)), r = str(self.radius), stroke='black', fill='none'))
            
        svg_document.add(svg_document.circle(
            center = (str(self.radius), str(self.radius)), r = '5', stroke='blue', fill='none'))

        svg_document.add(svg_document.circle(
            center = (str(self.radius + 36.5), str(self.radius)), r = '3', stroke='blue', fill='none'))

        svg_document.add(svg_document.circle(
            center = (str(self.radius), str(self.radius + 36.5)), r = '3', stroke='blue', fill='none'))

        svg_document.add(svg_document.circle(
            center = (str(self.radius - 36.5), str(self.radius)), r = '3', stroke='blue', fill='none'))

        svg_document.add(svg_document.circle(
            center = (str(self.radius), str(self.radius - 36.5)), r = '3', stroke='blue', fill='none'))
            
        svg_document.add(svg_document.line(
            start=(self.radius, self.radius + self.toneToX(self.tones[0])), 
            end = (self.radius, self.radius + self.toneToX(self.tones[len(self.tones)-1])), 
            stroke='green'))
  
    # draw text onto the disc
    # may not be supported by all SVG viewers
    def drawText(self, svg_document, text):
        if(text == ""): return
        svg_document.add(svg_document.path('M165,215 a50,50 0 1 1 0.1,0', id='MyTextPath', stroke='none', fill='none'))
        path = svg_document.textPath('#MyTextPath', text, fill='none', stroke='red', font_size='1em')
        svgtxt = svg_document.text("")
        svgtxt.add(path)
        svg_document.add(svgtxt)

        
