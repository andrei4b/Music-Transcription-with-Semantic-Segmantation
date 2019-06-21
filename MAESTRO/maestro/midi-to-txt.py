#https://github.com/jongwook/onsets-and-frames/blob/master/onsets_and_frames/midi.py

import sys
import os

import mido
import numpy as np
from tqdm import tqdm


def parse_midi(path):
    """open midi file and return np.array of (onset, offset, note, velocity) rows"""
    midi = mido.MidiFile(path)

    time = 0
    sustain = False
    events = []
    for message in midi:
        time += message.time

        if message.type == 'control_change' and message.control == 64 and (message.value >= 64) != sustain:
            # sustain pedal state has just changed
            sustain = message.value >= 64
            event_type = 'sustain_on' if sustain else 'sustain_off'
            event = dict(index=len(events), time=time, type=event_type, note=None, velocity=0)
            events.append(event)

        if 'note' in message.type:
            # MIDI offsets can be either 'note_off' events or 'note_on' with zero velocity
            velocity = message.velocity if message.type == 'note_on' else 0
            event = dict(index=len(events), time=time, type='note', note=message.note, velocity=velocity, sustain=sustain)
            events.append(event)

    notes = []
    for i, onset in enumerate(events):
        if onset['velocity'] == 0:
            continue

        # find the next note_off message
        offset = next(n for n in events[i + 1:] if n['note'] == onset['note'] or n is events[-1])

        if offset['sustain'] and offset is not events[-1]:
            # if the sustain pedal is active at offset, find when the sustain ends
            offset = next(n for n in events[offset['index'] + 1:] if n['type'] == 'sustain_off' or n['note'] == offset['note'] or n is events[-1])

        note = (onset['time'], offset['time'], onset['note'], onset['velocity'])
        notes.append(note)

    return np.array(notes)

if __name__ == '__main__':

    def process(input_file, output_file):
        midi_data = parse_midi(input_file)
        np.savetxt(output_file, midi_data, '%.6f', '\t', header='onset\toffset\tnote\tvelocity')

    def files():
        path = sys.argv[1]
        for input_file in tqdm(os.listdir(path)):
            if input_file.endswith('.mid'):
                output_file = input_file[:-4] + '.txt'
            elif input_file.endswith('.midi'):
                output_file = input_file[:-5] + '.txt'
            else:
                print('ignoring non-MIDI file %s' % input_file, file=sys.stderr)
                continue
            
            process(path + '\\' + input_file, path + '\\' + output_file)
            #yield (input_file, output_file)
    files()
