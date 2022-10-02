# midi2organette
Create discs for Ariston organettes or other by midi file import

## Prerequisites
You need [Python 3](https://www.python.org)  
Install Mido and svgwrite

	pip install mido
	pip install svgwrite

## Usage
	./midi2organette <organette> <midifile>

Create a test disk for Ariston:

	./midi2organette Ariston test > test.svg
