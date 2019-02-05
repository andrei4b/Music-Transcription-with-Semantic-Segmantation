import os
import h5py
import librosa
import argparse
import numpy as np

import matplotlib.pyplot as plt



def ProcessLabel(gt_path, t_unit=0.02, length=None, pitch_width=352, base=88):
    """
        The variable 'length' should be the number of total frames.
        ---
        - read lines from txt file
        - is there a serios problem with the \t in the txt files? DEBUG
        - extract onset (float), offset (float) and midi (int)
        - ?? start/end frame
        - calculate pitch (between 0 and 88)
        - add [start_frm, end_frm, pitch] to queue
        - queue[-1][1] = the value of the last end_frm. 
        - length = max frame number + 100
        - label = matrix with length lines and pitch_width (352) columns, init with 0
        - scale = 4
        - put 1's in label on corresponding onset/offset intervals, on 4 adiacent pitch values
        - print song length in seconds
    """

    with open(gt_path, "r") as ll_file:
        lines = ll_file.readlines()

    queue = []
    base_note = librosa.note_to_midi("A0")

    for i in range(1, len(lines)):
        if(len(lines[i].split("\t")) != 3):
            continue
        onset, offset, midi = lines[i].split("\t")
        onset, offset, midi = float(onset), float(offset), int(midi[:midi.find("\n")])
        
        start_frm, end_frm = round(onset/t_unit), round(offset/t_unit)
        pitch = midi - base_note
        
        queue.append([start_frm, end_frm, pitch])
    
    if length is not None:
        assert(length >= queue[-1][1]), "The given length cannot be shorter than the real length! Please specify a longer one."
    else:
        length = queue[-1][1] + 100
    
    
    assert(pitch_width % base == 0)
    label = np.zeros((length, pitch_width))
    scale = pitch_width // base

    for note in queue:
        on, off, p = note
        p_range = range(p*scale, (p+1)*scale)
        label[on:off, p_range] = 1

    print("Time (sec): ", length*t_unit)
    
    return label

if __name__ == "__main__":
    '''
        example for testing 
    '''
    ff_name = "./MapsDataset/ENSTDkCl/MUS/MAPS_MUS-bk_xmas4_ENSTDkCl.txt"
    
    label = ProcessLabel(ff_name)

    plt.imshow(label.transpose(), aspect='auto', origin='lower')
    plt.show()








    
    
    
    
