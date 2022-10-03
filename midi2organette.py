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

def midiNote2str(note):
    OCTAVE = ['C_','C#','D_','D#','E_','F_','F#','G_','G#','A_','B_','H_']
    return OCTAVE[note % 12] + str(int(note / 12) - 2)
    
def midiTime2ms(ticks_per_beat, tick):
    return tick * 250 / ticks_per_beat
    
def ms2str(ms):
    return '{:.0f}:{:02.0f}.{:02.0f}'.format(ms/60000, ms%60000/1000, ms%1000)

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

def extract_midi(svg_document, parameter):
    mid = mido.MidiFile(parameter.midfile)
    maxlen = 0
    notes = {}
    notelist = {}
    timestamp = 0
    for i, track in enumerate(mid.tracks):
        for msg in track:
            if msg.type == 'note_on':
                timestamp += msg.time
                note = {}
                note['start'] = timestamp
                notes[msg.note] = note
                
            if msg.type == 'note_off':
                timestamp += msg.time
                if parameter.end > 0 and midiTime2ms(mid.ticks_per_beat, timestamp) > parameter.end:
                    break
                    
                if msg.note in notes:
                    if midiTime2ms(mid.ticks_per_beat, notes[msg.note]['start']) >= parameter.start:
                        notes[msg.note]['end'] = timestamp
                        if msg.note in notelist:
                            notelist[msg.note].append(notes[msg.note])
                        else:
                            notelist[msg.note] = [notes[msg.note]]
                            
    return (notelist, mid.ticks_per_beat)
    
 
def midi2svg(svg_document, organette, parameter):
    (notelist, ticks_per_beat) = extract_midi(svg_document, parameter)          
    veryend = 0
    for n in notelist:
        start = notelist[n][0]['start']
        end = notelist[n][len(notelist[n])-1]['end']
        if end > veryend: veryend = end
    
    millisecs = midiTime2ms(ticks_per_beat, veryend) + parameter.pause
    
    incompat = False 
    for n in notelist:
        note = midiNote2str(n + parameter.transpose)
        if note in organette.tones:
            for t in notelist[n]:
                if not note in parameter.skip:
                    startangle = midiTime2ms(ticks_per_beat, t['start']) * 2 * math.pi / millisecs
                    endangle = midiTime2ms(ticks_per_beat, t['end']) * 2 * math.pi / millisecs
                    drawArcHole(svg_document, organette, note, startangle, endangle)
        else:
            incompat = True
  
    if parameter.svgfile != "":
        print('Length: ' + ms2str(millisecs))
 
        if(incompat):
            print("Instrument supports and uses:")
            for t in organette.tones:
                used = " "
                for n in notelist:
                    if midiNote2str(n + parameter.transpose) == t:
                        used = "*"
                        break
                print('note {} {}'.format(t, used))
                
        print("\r\nSong contains:")
        if parameter.transpose != 0:
            up = 'up'
            if parameter.transpose < 0: up = 'down'
            print('transposed {} halftones {}'.format(abs(parameter.transpose), up))
            
        sortlist = sorted(notelist)
        for n in sortlist:
            start = midiTime2ms(ticks_per_beat, notelist[n][0]['start'])
            end = midiTime2ms(ticks_per_beat, notelist[n][len(notelist[n])-1]['end'])
            no = " "
            if not midiNote2str(n + parameter.transpose) in organette.tones:
                no = "X"
            print('note {} {} time {} - {}'.format(midiNote2str(n + parameter.transpose), no, ms2str(start), ms2str(end)))
        
 
class MyParams:
    start = 0
    end = -1
    midfile = ""
    svgfile = ""
    skip = []
    pause = 0
    transpose = 0
    text = ""
    
    def __init__(self, argv):
        last = ""
        for a in argv:
            if last == '-start': self.start = int(a)
            elif last == '-end': self.end = int(a)
            elif last == '-mid': self.midfile = a
            elif last == '-svg': self.svgfile = a
            elif last == '-skip': self.skip.append(a)
            elif last == '-pause': self.pause = int(a)
            elif last == '-transpose': self.transpose = int(a)
            elif last == '-text': self.text = a
            last = a
                    
          
parameter = MyParams(sys.argv)      
organette = Ariston.Ariston()
diameter = str(organette.radius*2)
svg_document = svgwrite.Drawing(parameter.svgfile,
    size = (diameter+'mm', diameter+'mm'), 
    viewBox="0 0 " + diameter + " " + diameter)
    
organette.drawOutlines(svg_document)
organette.drawText(svg_document, parameter.text)

if parameter.midfile == "":
    CreateTestDisc(svg_document, organette)
else:
    midi2svg(svg_document, organette, parameter)  
    
if parameter.svgfile == "":
    print(svg_document.tostring())
else:
    svg_document.save()
