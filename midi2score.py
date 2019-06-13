# Unroll method
#from unroll import midi2keystrikes
#ks = midi2keystrikes('voila.mid')
#ks.transcribe('score.ly', quarter_durations = [50,100,0.02])

# Sigliati version

import subprocess
import argparse
from music21 import *
import sys
from xml.etree import ElementTree
from CompleteTranscription.CompleteTranscription import complete_transcription

musescore_path = "C:\Program Files (x86)\MuseScore 2\\bin\MuseScore.exe"

def midi2score(midi_file):
    music21score = complete_transcription(midi_file)
    SX = musicxml.m21ToXml.ScoreExporter(music21score)
    xml_score = SX.parse()
    xml_score_string = ElementTree.tostring(xml_score, encoding='unicode')
    xml_file = midi_file[:-4] + '.xml'
    
    f = open(xml_file, "w")
    f.write(xml_score_string)
    f.close()
    
    subprocess.call([musescore_path, xml_file])

def main():
    parser = argparse.ArgumentParser(description="Convert MIDI to musicXML and open it in MuseScore.")
    parser.add_argument("--midi-file",
                        help="Path to midi file.",
                        type=str)
    args = parser.parse_args()
    midi2score(args.midi_file)    

if __name__ == '__main__':
    main()