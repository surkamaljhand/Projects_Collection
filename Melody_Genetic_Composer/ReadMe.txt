Music Generation with Genetic Algorithm

This repository contains a Python-based music generation program that utilizes a genetic algorithm to create melodies. The program uses MIDI files to generate and export musical compositions.

Table of Contents
1. Requirements
2. Installation
2. Usage
3. Customization
5. Future Plans
6. License
7. Requirements
   i. Python 3.6 or higher
   ii. MIDIUtil library

# Installation

1. Clone the repository: git clone https://github.com/yourusername/music-generation.git

2. Change to the project directory:cd music-generation

3. Install the required library using pip: pip install MIDIUtil

# Usage
1. Run the MelodyGeneticComposer.py script:

2. python MelodyGeneticComposer.py
The program will generate a new MIDI file named output.mid in the project directory. You can play this file using any MIDI player software.

# Customization
The following sections in the music_generation.py file can be modified to customize the program:

1. Parameters
Change the parameters such as population size, number of generations, mutation rate, and crossover rate according to your preferences. Experiment with different values to see how it affects the generated music.

2. Fitness Function
Modify the fitness function to experiment with different methods of evaluating the melodies. This will impact how the genetic algorithm evolves the population over time.

3. Note Mapping
Modify the note mapping to include different sets of notes or scales. This will affect the overall tonality and harmony of the generated music.

4. MIDI File Export
Customize the MIDI file export settings, such as tempo, instrument selection, and time signature, to produce different styles of music.

# Future Plans
1. Fine-tune the program to improve the quality of the generated music.
2. Implement a graphical user interface (GUI) to make the program more user-friendly and accessible.
3. Incorporate a notes dataset to expand the available musical material.
4. Experiment with different fitness functions and compare them using standardized tests.

# License
This project is licensed under the MIT License.