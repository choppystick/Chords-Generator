# Music Chord Generator

This project is a Python-based music chord generator that creates MIDI files for various chord types and inversions. It's a useful tool for musicians, composers, and music theory students who want to explore different chord structures and hear them played back.

## Features

- Generate major, minor, dominant, suspended, augmented, diminished, and other chord types
- Support for chord inversions
- Create MIDI files for generated chords
- Convert between note names and MIDI note numbers
- Handle enharmonic equivalents (e.g., C# and Db)
- User-friendly command-line interface

## Requirements

- Python 3.x
- MIDIUtil library

## Installation

1. Clone this repository or download the `main.py` file.
2. Install the required library:

```
pip install MIDIUtil
```

## Usage

1. Run the script:

```
python main.py
```

2. Follow the prompts:
   - Enter the root note (e.g., F4, Bb3)
   - Choose a chord type from the provided list
   - Specify the inversion (0 for root position, 1 for first inversion, etc.)

3. The script will generate a MIDI file with the specified chord and display the notes in the chord.

4. Type 'Y' to quit or any other key to generate another chord.

## Supported Chord Types

- Major: maj
- Minor: m
- Dominant 7th: dom7
- Major 7th: maj7
- Minor 7th: m7
- Suspended: sus2, sus4
- Augmented: aug, aug7
- Diminished: dim, dim7
- Half-diminished: m7b5
- 9th, 11th, and 13th extensions for major, minor, and dominant chords
- Added tone chords: add2, add6, m6

## Future Plans

- Interval generators
- Chord identifying algorithm
- More chords support

## Contributing

Contributions to improve the project are welcome. Please feel free to submit issues or pull requests.

## License

This project is open-source and available under the MIT License.
