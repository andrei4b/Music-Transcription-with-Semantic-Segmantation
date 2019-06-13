from unroll.MIDI import midi2keystrikes
import argparse

def midi2score(midi_file):
    ks = midi2keystrikes(midi_file)
    lilyfile = midi_file[:-4] + ".mid"
    ks.transcribe(lilyfile, quarter_durations=[200,250,0.2])    

def main():
    parser = argparse.ArgumentParser(description="Convert MIDI to lilypond file")
    parser.add_argument("--midi-files",
                        help="Path to midi file.",
                        type=str, nargs="+")
    args = parser.parse_args()
    
    for file in midi_files:
        midi2score(file)    

if __name__ == '__main__':
    main()