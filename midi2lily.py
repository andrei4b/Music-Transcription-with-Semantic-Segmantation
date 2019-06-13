from unroll.MIDI import midi2keystrikes
import argparse

def midi2score(midi_file):
    ks = midi2keystrikes(midi_file)
    ks.transcribe('score.ly', quarter_durations=[200,250,0.2])    

def main():
    parser = argparse.ArgumentParser(description="Convert MIDI to lilypond file")
    parser.add_argument("--midi-file",
                        help="Path to midi file.",
                        type=str)
    args = parser.parse_args()
    midi2score(args.midi_file)    

if __name__ == '__main__':
    main()