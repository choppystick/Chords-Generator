from midiutil import MIDIFile
from typing import List, Tuple


def note_to_midi(note: str) -> int:
    notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    enharmonic_equivalents = {'Db': 'C#', 'Eb': 'D#', 'Fb': 'E', 'Gb': 'F#', 'Ab': 'G#', 'Bb': 'A#', 'Cb': 'B',
                              'E#': 'F', 'B#': 'C'}

    octave = int(note[-1])
    pitch = note[:-1]

    if pitch in enharmonic_equivalents:
        pitch = enharmonic_equivalents[pitch]

    return notes.index(pitch) + ((octave + 1) * 12)


def midi_to_note(midi: int, flat: bool) -> str:
    sharp_notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    flat_notes = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']

    notes = flat_notes if flat else sharp_notes

    octave = (midi // 12) - 1
    note = notes[midi % 12]
    return f"{note}{octave}"


def create_chord(root: str, chord_type: str) -> Tuple[List[int], bool]:
    chord_structures = {
        "maj": [0, 4, 7],  # major
        "m": [0, 3, 7],  # minor
        "add6": [0, 4, 7, 9],  # major sixth
        "m6": [0, 3, 7, 9],  # minor sixth
        "dom7": [0, 4, 7, 10],  # dominant seventh
        "dom9": [0, 4, 7, 10, 14],  # dominant ninth
        "dom11": [0, 4, 7, 10, 14, 17],  # dominant eleventh
        "dom13": [0, 4, 7, 10, 14, 17, 21],  # dominant thirteenth
        "maj7": [0, 4, 7, 11],  # major seventh
        "maj9": [0, 4, 7, 11, 14],  # major ninth
        "maj11": [0, 4, 7, 11, 14, 17],  # major eleventh
        "maj13": [0, 4, 7, 11, 14, 17, 21],  # major thirteenth
        "m7": [0, 3, 7, 10],  # minor seventh
        "m9": [0, 3, 7, 10, 14],  # minor ninth
        "m11": [0, 3, 7, 10, 14, 17],  # minor eleventh
        "m13": [0, 3, 7, 10, 14, 17, 21],  # minor eleventh
        "dim": [0, 3, 6],  # diminished
        "dim7": [0, 3, 6, 9],  # diminished
        "sus2": [0, 2, 7],  # suspended second
        "sus4": [0, 5, 7],  # suspended fourth
        "aug": [0, 4, 8],  # augmented
        "aug7": [0, 4, 8, 10],  # augmented seventh
        "m7b5": [0, 3, 6, 10],  # half-diminished
        "add2": [0, 2, 4, 7]  # added second
    }

    root_midi = note_to_midi(root)
    use_flat = 'b' in root or (root[-2] not in ['#', 'b'] and chord_type != "aug" and chord_type != "aug7")

    return [root_midi + interval for interval in chord_structures[chord_type]], use_flat


def apply_inversion(chord: List[int], inversion: int) -> List[int]:
    if inversion == 0:  # root chord
        return chord

    chord_length = len(chord)
    normalized_inversion = inversion % chord_length

    inverted_chord = chord[normalized_inversion:] + chord[:normalized_inversion]

    # Adjust octaves
    for i in range(normalized_inversion):
        inverted_chord[chord_length - normalized_inversion + i] += 12

    return inverted_chord


def get_inversion_notation(root: str, chord_type: str, inverted_chord: List[int], use_flat: bool) -> str:
    if len(inverted_chord) == 0:
        return f"{root}{chord_type}"

    bass_note = midi_to_note(inverted_chord[0], use_flat)
    bass_note = bass_note[:-1]  # Remove the octave number

    if bass_note == root[:-1]:  # If the bass note is the same as the root (ignoring octave)
        return f"{root}{chord_type}"
    else:
        return f"{root}{chord_type}_{bass_note}"


def create_midi_file(filename: str, chord: List[int], duration: float = 4):
    midi = MIDIFile(1)
    track, time = 0, 0
    midi.addTrackName(track, time, "Chord Track")
    midi.addTempo(track, time, 60)

    for note in chord:
        midi.addNote(track, 0, note, time, duration, 100)

    with open(filename, "wb") as output_file:
        midi.writeFile(output_file)


def main():
    while True:
        root = input("Enter the root note (e.g., F4, Bb3): ")
        print("Chord types:")
        print("- Major and Major nth: maj, maj7, maj9, maj11, maj13")
        print("- Minor and Minor nth: m, m7, m9, m11, m13")
        print("- Dominant 7th and Dominant nth: dom7, dom9, dom11, dom13")
        print("- Suspended: sus2, sus4")
        print("- Augmented: aug, aug7")
        print("- Diminished: dim, dim7")
        print("- Half diminished: m7b5")
        print("- Major and minor sixth: add2, add6, m6")
        chord_type = input("Enter the chord type: ")

        try:
            chord, use_flat = create_chord(root, chord_type)
        except KeyError:
            print(f"Invalid chord type: {chord_type}")
            continue

        max_inversion = len(chord) - 1
        while True:
            try:
                inversion = int(input(f"Enter inversion (0 to {max_inversion} for this chord): "))
                if 0 <= inversion <= max_inversion:
                    break
                else:
                    print(f"Invalid inversion. Please enter a number between 0 and {max_inversion}.")
            except ValueError:
                print("Invalid input. Please enter a valid integer.")

        inverted_chord = apply_inversion(chord, inversion)
        notation = get_inversion_notation(root, chord_type, inverted_chord, use_flat)
        filename = f"{notation}.mid"
        create_midi_file(filename, inverted_chord)
        print(f"MIDI file '{filename}' has been created.")

        notes = [midi_to_note(note, use_flat) for note in inverted_chord]
        print(f"The chord {notation} consists of the following notes: {' '.join(notes)}")

        answer = input("Type Y to quit.").lower()
        if answer == "y":
            break

        else:
            continue


if __name__ == "__main__":
    main()
