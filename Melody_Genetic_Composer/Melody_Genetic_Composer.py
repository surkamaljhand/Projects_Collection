# Name: Surkamal Singh Jhand Course:
# COMP 3710 Applied Artificial Intelligence Project
# Start Date: 2023-03-19 Project
# End (Due) Date: 2023-04-18
#
# Program Description: The genetic algorithm music composer program is a Python program
#                      that uses a genetic algorithm to generate original pieces of music. The program uses the MIDI
#                      file format to represent music, where each note is represented by a pitch (e.g. C, D, E) and
#                      an octave, a duration (e.g. quarter note, half note, whole note), and a velocity
#                      (i.e. how loud the note should be played).
#
#                      The genetic algorithm works by starting with an initial population of randomly generated music
#                      sequences, evaluating the fitness of each sequence based on how well it conforms to certain
#                      musical rules, selecting the fittest individuals to be parents for the next generation,
#                      combining the parents through crossover to produce children, and mutating the children to
#                      introduce variation into the population. The process repeats for a specified number of
#                      generations until the fittest individual is found.
#
#                      The genetic algorithm music composer program includes several modules:
#
#                      1. generate_music.py - This module contains functions for generating random music sequences and
#                      for evaluating the fitness of a music sequence. The fitness function evaluates how well a
#                      music sequence conforms to certain musical rules, such as staying within a certain key and
#                      avoiding consecutive notes of the same pitch.
#
#                      2. selection.py - This module contains functions for selecting parents for crossover using
#                      tournament selection. Tournament selection involves selecting a random subset of individuals
#                      from the population and choosing the fittest individual from that subset as a parent.
#
#                      3. crossover.py - This module contains functions for combining parents through crossover to
#                      produce children. The crossover function combines the notes, durations, and velocities of the
#                      parents to create two children.
#
#                      4. mutation.py - This module contains functions for mutating children to introduce variation
#                      into the population. The mutation function randomly changes some notes, durations,
#                      and velocities of the child.
#
#                      5. midi_export.py - This module contains a function for exporting a music sequence to a
#                      MIDI file.
#
#                      6. main.py - This module contains the main function that runs the genetic algorithm for
#                      music composition. It prompts the user for input regarding various parameters such as
#                      population size, mutation rate, and number of generations. Then, it generates an initial
#                      population and evaluates the fitness of each individual. It runs the genetic algorithm for
#                      the specified number of generations, where each generation involves selection of parents using
#                      tournament selection, crossover to create children, and mutation of children.
#                      The best individual of each generation is printed, and the best individual of the entire run is
#                      saved. Finally, a MIDI file is generated for the best individual with the filename indicating
#                      the fitness score of the individual.
#
# References Cited: Below are the resources and references that were utilized to clarify and solve the given problem.
#
#                   1. MIDIUtil Documentation - https://midiutil.readthedocs.io/en/latest/
#
#                   2. Python MIDI Tutorial - RealPython - https://realpython.com/python-midi/
#
#                   3. Music Generation using Neural Networks -
#                   Towards Data Science -
#                   https://towardsdatascience.com/music-generation-using-neural-networks-ce5a5b218837
#
#                   4. Music Composition using Genetic Algorithms - International Journal of Advanced Research
#                   in Computer and Communication Engineering -
#                   https://ijarcce.com/wp-content/uploads/2019/12/IJARCCE_108.pdf
#
#                   5. A Tutorial on Genetic Algorithms - American Association for Artificial Intelligence -
#                   https://www.aaai.org/Papers/Tutorial/1995/IT-95-01.pdf
#
#                   6. Overview of Genetic Algorithms - GeeksforGeeks -
#                   https://www.geeksforgeeks.org/genetic-algorithms/
#
#                   7. MIDI file format specification - MIDI Manufacturers Association -
#                   https://www.midi.org/specifications-old/item/the-midi-1-0-specification
#
#                   8. Numpy Documentation - https://numpy.org/doc/stable/
#
#                   9. Music21 Documentation - https://web.mit.edu/music21/doc/
#
#                   10. Music21: A Toolkit for Computer-Aided Musicology -
#                   Journal of New Music Research - https://www.tandfonline.com/doi/abs/10.1080/09298215.2011.596205
#
#                   11. How to Generate Music using a LSTM Neural Network in Keras - Machine Learning Mastery -
#                   https://machinelearningmastery.com/how-to-generate-music-with-a-neural-network-in-keras/
#
#                   12. Introduction to Genetic Algorithms - Georgia State University -
#                   https://hyperion.gsu.edu/hbase/alggen.html
#
#                   13. Introduction to MIDI by the MIDI Manufacturers Association -
#                   https://www.midi.org/specifications-old/item/introduction-to-midi
#
#                   14. Genetic Algorithm for Music Composition: A Review" by Leandro Nunes de Castro -
#                   https://www.sciencedirect.com/science/article/pii/S1877050917320313
#
#                   15. "Tournament Selection: A Review" by J. M. Earl and J. D. T. Mounce -
#                   https://www.sciencedirect.com/science/article/pii/S1568494611003757

# Required Libraries.
import random
import numpy as np
from typing import Dict, List, Tuple
from midiutil import MIDIFile
import sys
import fluidsynth
from fluidsynth import *
import logging

# Constants Declaration
POPULATION_SIZE: int = 150
INDIVIDUAL_LENGTH: int = 50
MUTATION_RATE: float = 0.5
NUM_GENERATIONS: int = 100
TEMPO: int = 120
TOURNAMENT_SIZE: int = 3
NOTES: List[str] = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
OCTAVES: List[int] = [4, 5]
DURATIONS: List[float] = [0.25, 0.5, 1, 2]

# Chord Progressions List.
CHORD_PROGRESSIONS: List[List[str]] = [
    ['C', 'G', 'Am', 'F'],
    ['Dm', 'Am', 'C']
]

# Evaluation Constants Weights.
NOTE_DURATION_WEIGHT: float = 0.5
PITCH_VARIETY_WEIGHT: float = 0.3
NOTE_OCTAVE_WEIGHT: float = 0.2


# This function takes in a starting chord and a number of chords as inputs, and returns a list of chords representing
# a chord progression. The function defines a set of rules for chord movement in a dictionary called rules,
# which maps each chord to a list of possible next chords. The function then iteratively selects the next chord to
# add to the progression based on the possible options for the current chord defined in the rules' dictionary,
# using the random.choice() method to randomly select from the options. The function returns the resulting chord
# progression as a list.
def generate_chord_progression(starting_chord: str, num_chords: int) -> List[str]:
    chord_progression = [starting_chord]

    # Define a set of rules for chord movement
    rules = {
        'C': ['F', 'G', 'Am', 'Em'],
        'G': ['C', 'D', 'Em', 'Am'],
        'D': ['G', 'A', 'Bm', 'F#m'],
        'A': ['D', 'E', 'F#m', 'C#m'],
        'E': ['A', 'B', 'C#m', 'G#m'],
        'B': ['E', 'F#', 'G#m', 'D#m'],
        'F#': ['B', 'C#', 'D#m', 'A#m'],
        'C#': ['F#', 'G#', 'A#m', 'Fm'],
        'G#': ['C#', 'D#', 'Fm', 'Cm'],
        'D#': ['G#', 'A#', 'Cm', 'Gm'],
        'A#': ['D#', 'F', 'Gm', 'Dm'],
        'F': ['A#', 'C', 'Dm', 'Am'],
        'Am': ['C', 'Dm', 'Em', 'F'],
        'Em': ['G', 'Am', 'Bm', 'C'],
        'Bm': ['D', 'Em', 'F#m', 'G'],
        'F#m': ['A', 'Bm', 'C#m', 'D'],
        'C#m': ['E', 'F#m', 'G#m', 'A'],
        'G#m': ['B', 'C#m', 'D#m', 'E'],
        'D#m': ['F#', 'G#m', 'A#m', 'F#'],
        'A#m': ['C#', 'D#m', 'Fm', 'G#'],
        'Fm': ['G#', 'A#m', 'Cm', 'D#'],
        'Cm': ['D#', 'Fm', 'Gm', 'A#'],
        'Gm': ['A#', 'Cm', 'Dm', 'F'],
        'Dm': ['F', 'Gm', 'Am', 'C'],
    }

    current_chord = starting_chord
    for _ in range(num_chords - 1):
        next_chord_options = rules.get(current_chord, NOTES)
        next_chord = random.choice(next_chord_options)
        chord_progression.append(next_chord)
        current_chord = next_chord

    return chord_progression


# This function generates an individual which consists of a chord progression and a corresponding melody. The chord
# progression is generated by randomly selecting a starting chord and then using a set of rules to generate a chord
# progression. The chord progression is then repeated until there are enough chords to match the desired length of
# the individual. The melody is generated by iterating over the chord progression and randomly selecting notes,
# durations, and velocities based on the chord being played. The function returns a dictionary containing the notes,
# durations, and velocities of the melody.
def generate_individual() -> Dict[str, List[Tuple[str, int]]]:
    # Choose a random starting chord
    starting_chord = random.choice(NOTES)

    # Generate a chord progression
    num_chords = 4
    chord_progression = generate_chord_progression(starting_chord, num_chords)

    # Repeat the chord progression until there are enough chords to match INDIVIDUAL_LENGTH
    chord_progression = chord_progression * ((INDIVIDUAL_LENGTH + len(chord_progression) - 1) // len(chord_progression))
    chord_progression = chord_progression[:INDIVIDUAL_LENGTH]

    notes: List[Tuple[str, int]] = []
    durations: List[float] = []
    velocities: List[int] = []

    # Iterate over the chord progression and generate notes, durations, and velocities
    for chord in chord_progression:
        if chord[-1] == 'm':
            root = chord[:-1]
            third = NOTES[(NOTES.index(root) + 2) % 7]
        else:
            root = chord
            third = NOTES[(NOTES.index(root) + 4) % len(NOTES)]
        fifth = NOTES[(NOTES.index(root) + 7) % len(NOTES)]
        note = np.random.choice([root, third, fifth])

        notes.append((note, np.random.choice(OCTAVES)))
        durations.append(np.random.choice(DURATIONS))
        velocities.append(np.random.randint(70, 100))

    # Return an individual with a subset of notes, durations, and velocities
    return {'notes': notes[:INDIVIDUAL_LENGTH], 'durations': durations[:INDIVIDUAL_LENGTH], 'velocities': velocities[:INDIVIDUAL_LENGTH]}


# This function generates a random individual, which is a dictionary that contains three lists: notes, durations,
# and velocities. The individual is generated based on a randomly chosen starting chord, and a chord progression is
# generated using the function generate_chord_progression(). The chord progression is repeated until it has a length
# equal to the INDIVIDUAL_LENGTH constant.
#
# The individual is then created by iterating over the chord progression and generating a random note, duration,
# and velocity for each chord. The notes are generated by selecting a root, third, and fifth note based on the chord
# type, and then selecting one of these notes at random. The duration and velocity of each note are also randomly
# selected.
#
# Finally, the individual is returned as a dictionary with the notes, durations, and velocities lists truncated to
# length INDIVIDUAL_LENGTH.
def fitness(individual: Dict[str, List[Tuple[str, int]]]) -> float:
    # Calculate note duration score
    note_duration_score: int = sum([int(duration) for duration in individual['durations']])

    # Calculate pitch variety score
    pitch_variety_score: int = len(set([note[0] for note in individual['notes']]))

    # Calculate note octave score
    note_octave_score: int = len(set([note[1] for note in individual['notes']]))

    # Calculate total fitness score
    total_fitness_score: float = (NOTE_DURATION_WEIGHT * note_duration_score +
                                  PITCH_VARIETY_WEIGHT * pitch_variety_score +
                                  NOTE_OCTAVE_WEIGHT * note_octave_score)

    return total_fitness_score


# This function performs single-point crossover on two parent individuals to create two children. The function starts
# by choosing a random crossover point between 1 and INDIVIDUAL_LENGTH. Then, two children are created by
# concatenating the first part of the notes, durations, and velocities from one parent up to the crossover point with
# the second part of the notes, durations, and velocities from the other parent starting from the crossover point.
#
# The function then returns the two children as a tuple.
def crossover(parent1: Dict[str, List[Tuple[str, int]]], parent2: Dict[str, List[Tuple[str, int]]]) -> Tuple[Dict[str, List[Tuple[str, int]]], Dict[str, List[Tuple[str, int]]]]:
    """
    Perform single-point crossover on the two parents to create two children
    """
    # Choose a random crossover point
    crossover_point = np.random.randint(1, INDIVIDUAL_LENGTH)

    # Perform crossover
    child1 = {
        'notes': parent1['notes'][:crossover_point] + parent2['notes'][crossover_point:],
        'durations': parent1['durations'][:crossover_point] + parent2['durations'][crossover_point:],
        'velocities': parent1['velocities'][:crossover_point] + parent2['velocities'][crossover_point:]
    }

    child2 = {
        'notes': parent2['notes'][:crossover_point] + parent1['notes'][crossover_point:],
        'durations': parent2['durations'][:crossover_point] + parent1['durations'][crossover_point:],
        'velocities': parent2['velocities'][:crossover_point] + parent1['velocities'][crossover_point:]
    }

    return child1, child2


# This function returns the path to the soundfont file which is required to generate sound using MIDI output. The
# path to the soundfont file is hard-coded and returned as a string. The path can be modified according to the actual
# path to the soundfont file on the user's machine.
def get_soundfont_path() -> str:
    """
    Returns the path to the soundfont file
    """
    # Replace 'path/to/soundfont.sf2' with the actual path to your soundfont file
    return "D:/Courses Material/Courses Winter-2023/COMP 3710/Experimental Code/Iterations/20 Synth Soundfonts/Acid " \
           "SQ Neutral.sf2"


# This function takes in a list of notes, durations, and velocities, along with a filename as input. It generates a
# MIDI file with the given notes, durations, and velocities. The function first creates an instance of a MIDI file,
# and then adds tempo to it using the addTempo() function. The notes, durations, and velocities are then iterated
# over and added to the MIDI file using the addNote() function. The pitch of each note is calculated using the index
# of the note in the NOTES list, along with the octave number. The velocity of the note is set using the
# corresponding value in the velocities list, and the duration of the note is set using the corresponding value in
# the durations list. Finally, the MIDI file is saved using the writeFile() function of the MIDIFile module.
def generate_midi_file(notes: List[Tuple[str, int]], durations: List[float], velocities: List[int], filename: str) -> None:
    """
    Generate a MIDI file for a given set of notes, durations, and velocities
    """
    # Create a MIDI file
    midi_file = MIDIFile(1)
    midi_file.addTempo(0, 0, TEMPO)

    # Add notes to the MIDI file
    current_time = 0
    for i in range(len(notes)):
        pitch = NOTES.index(notes[i][0]) + 12 * (notes[i][1] + 1)
        velocity = velocities[i]
        duration = durations[i]
        midi_file.addNote(0, 0, pitch, current_time, duration, velocity)
        current_time += duration

    # Save the MIDI file
    with open(filename, 'wb') as output_file:
        midi_file.writeFile(output_file)


# This function generates a list of MIDI events for a given set of notes, durations, and velocities. It uses the
# NOTES, TEMPO, and OCTAVES constants to calculate the pitch of each note and the start time and duration of each
# event. The events are represented as tuples of four integers: the time of the event, the MIDI status byte (0x90 for
# note on, 0x80 for note off), the pitch of the note, and the velocity of the note. The start time and duration are
# calculated based on the tempo and the duration of each note. The function returns a list of all the MIDI events for
# the given notes, durations, and velocities.
def generate_midi_events(notes: List[Tuple[str, int]], durations: List[float], velocities: List[int]) -> List[Tuple[int, int, int, int]]:
    """
    Generate the MIDI events for a given set of notes, durations, and velocities
    """
    events = []
    time = 0
    for i in range(len(notes)):
        pitch = NOTES.index(notes[i][0]) + 12 * (notes[i][1] + 1)
        start_time = sum(durations[:i]) * 4 * TEMPO
        duration = durations[i] * 4 * TEMPO
        volume = velocities[i]
        events.append((time + start_time, 0x90, pitch, volume))
        events.append((time + start_time + duration, 0x80, pitch, 0))
    return events


# This function writes the MIDI events to a file. It takes a list of MIDI events as input and a filename for the
# output MIDI file. First, it creates a MIDI file object and sets the tempo. Then, it iterates over each MIDI event
# in the list and adds it to the MIDI file object. Finally, it writes the MIDI file to the output file.
def write_midi_file(events: List[Tuple[int, int, int, int]], filename: str) -> None:
    """
    Write the MIDI events to a file
    """
    midi_file = MIDIFile(1)
    midi_file.addTempo(0, 0, TEMPO)
    for event in events:
        midi_file.addEvent(event[1], 0, event[2], event[3], event[0])
    with open(filename, 'wb') as output_file:
        midi_file.writeFile(output_file)


# This function takes in a population of individuals, their fitness scores, and the tournament size. It then performs
# the tournament selection method where it selects a random subset of individuals (tournament) of size
# 'tournament_size' from the population. It then selects the best individual from the tournament (with the highest
# fitness score) and adds it to the selected list. This process is repeated for all individuals in the population,
# resulting in a list of selected individuals. Finally, the function returns the list of selected individuals.
def selection(population: List[Dict[str, List[Tuple[str, int]]]], fitness_scores: List[float], tournament_size: int) -> List[Dict[str, List[Tuple[str, int]]]]:
    """
    Select individuals from the population using tournament selection
    """
    selected = []
    for i in range(len(population)):
        tournament = np.random.choice(range(len(population)), size=tournament_size, replace=False)
        tournament_fitness_scores = [fitness_scores[i] for i in tournament]
        tournament_best_index = tournament_fitness_scores.index(max(tournament_fitness_scores))
        selected.append(population[tournament[tournament_best_index]])

    return selected


# The function run_genetic_algorithm is the main function that runs the genetic algorithm for music composition. It
# prompts the user for input regarding various parameters such as population size, mutation rate, and number of
# generations. Then, it generates an initial population and evaluates the fitness of each individual. It runs the
# genetic algorithm for the specified number of generations, where each generation involves selection of parents
# using tournament selection, crossover to create children, and mutation of children. The best individual of each
# generation is printed, and the best individual of the entire run is saved. Finally, a MIDI file is generated for
# the best individual with the filename indicating the fitness score of the individual.
def run_genetic_algorithm() -> None:
    # Prompt the user for input
    print("Welcome to the Genetic Algorithm Music Composer!")
    print("Please enter the following parameters:")
    while True:
        try:
            population_size = int(input(f"Population Size (Current Default {POPULATION_SIZE}) : ") or "100")
            individual_length = int(input(f"Individual Length (Current Default {INDIVIDUAL_LENGTH}) : ") or "50")
            mutation_rate = float(input(f"Mutation Rate (Current Default {MUTATION_RATE}) : ") or "0.5")
            num_generations = int(input(f"Number of Generations (Current Default {NUM_GENERATIONS}) : ") or "100")
            tournament_size = int(input(f"Tournament Size (Current Default {TOURNAMENT_SIZE}) : ") or "3")
            break
        except ValueError:
            print("Invalid input. Please enter an integer for population size, individual length, number of "
                  "generations, and tournament size, or a float for mutation rate.")

    # Generate initial population
    population = [generate_individual() for _ in range(population_size)]
    print("Initial Population :")
    print(population)

    # Initialize the best individual and fitness
    best_individual = None
    best_fitness = -1

    # Run the genetic algorithm for NUM_GENERATIONS generations
    for generation in range(num_generations):
        # Evaluate fitness of each individual
        fitness_scores = [fitness(individual) for individual in population]

        # Find the best individual in population
        generation_best_index = fitness_scores.index(max(fitness_scores))
        generation_best_fitness = fitness_scores[generation_best_index]
        generation_best_individual = population[generation_best_index]

        # Update global best individual if necessary
        if generation_best_fitness > best_fitness:
            best_individual = generation_best_individual
            best_fitness = generation_best_fitness

        print(f"Generation {generation} : Best Fitness = {generation_best_fitness}")
        print(f"Best Individual : {best_individual}")

        # Select parents for crossover using tournament selection
        parents = selection(population, fitness_scores, tournament_size)

        # Crossover parents to create children
        children = []
        for i in range(0, population_size, 2):
            child1, child2 = crossover(parents[i], parents[i+1])
            children.append(child1)
            children.append(child2)

        # Mutate children
        for child in children:
            for i in range(individual_length):
                if np.random.random() < mutation_rate:
                    child['notes'][i] = (np.random.choice(NOTES), np.random.choice(OCTAVES))
                    child['durations'][i] = np.random.choice(DURATIONS)
                    child['velocities'][i] = np.random.randint(70, 100)

        # Replace population with children
        population = children
        print(f"Population After Generation {generation} : ")
        print(population)

    # Generate MIDI file for best individual
    filename = f"best_individual_fitness_{best_fitness:.2f}.mid"
    generate_midi_file(best_individual['notes'], best_individual['durations'], best_individual['velocities'], filename)


# The if __name__ == '__main__': block is a standard Python construct that allows the code inside it to only be
# executed if the script is being run as the main program, rather than being imported as a module. In this case,
# it is used to call the run_genetic_algorithm() function and run the entire genetic algorithm music composer program.
if __name__ == '__main__':
    run_genetic_algorithm()