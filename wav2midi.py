"""wav to midi for piano music
"""
import argparse
import os
import numpy as np
import pretty_midi

from Predict import model_info, predict
from Evaluation import peak_picking
from project.MelodyExt import feature_extraction
from project.utils import load_model

def piano_roll_to_pretty_midi(piano_roll, fs=50, program=0):
    notes, frames = piano_roll.shape
    pm = pretty_midi.PrettyMIDI()
    instrument = pretty_midi.Instrument(program=program)

    # pad 1 column of zeros so we can acknowledge inital and ending events (for diff)
    piano_roll = np.pad(piano_roll, [(0, 0), (1, 1)], 'constant')

    # use changes in velocities to find note on / note off events
    velocity_changes = np.nonzero(np.diff(piano_roll).T)

    # keep track on velocities and note on times
    prev_velocities = np.zeros(notes, dtype=int)
    note_on_time = np.zeros(notes)

    for time, note in zip(*velocity_changes):
        # use time + 1 because of padding above
        velocity = piano_roll[note, time + 1]
        time = time / fs
        if velocity > 0:
            if prev_velocities[note] == 0:
                note_on_time[note] = time
                prev_velocities[note] = velocity
        else:
            pm_note = pretty_midi.Note(
                velocity=prev_velocities[note] * 64,
                pitch=note + 21,
                start=note_on_time[note],
                end=time)
            instrument.notes.append(pm_note)
            prev_velocities[note] = 0
            
    pm.instruments.append(instrument)
    return pm

def main(args):
    assert(os.path.isfile(args.wav_file)), "The given path is not a file!. Please check your input again."
    
    print("Extracting features...")
    Z, tfrL0, tfrLF, tfrLQ, t, cenf, f = feature_extraction(args.wav_file)
    #get model configuration and prepare features for inference
    feature_type, channels, out_class = model_info(args.model_path)
    if feature_type == "HCFP":
        pass
    else:
        assert(len(channels) <= 4)
        feature = np.array([Z, tfrL0, tfrLF, tfrLQ])
        feature = np.transpose(feature, axes=(2, 1, 0))
    #load model
    model = load_model(args.model_path)
    
    print("Predicting...")
    pred = predict(feature, model, channels=channels, instruments=out_class-1)
    pred = pred[:,:,0]
    pred = peak_picking(pred) if pred.shape[1] > 88 else pred
    pred[pred < args.threshold] = 0
    pred[pred != 0] = 1
    
    print("Saving...")
    pm = piano_roll_to_pretty_midi(pred.T, fs=50, program=args.program)
    pm.remove_invalid_notes()
    pm.write(args.output_mid_name)

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description="Transcribe on the given audio.")
    parser.add_argument("-i", "--wav-file",
                        help="Path to the input audio you want to transcribe",
                        type=str)
    parser.add_argument("-m", "--model-path", 
                        help="Path to the pre-trained model.",
                        type=str)
    parser.add_argument("-o", "--output-mid-name",
                        help="Name of transcribed .mid file of piano roll to save.",
                        type=str, default="voila")
    parser.add_argument("-p", "--program",
                        help="What sound to use",
                        type=int, default=0)
    parser.add_argument("-t", "--threshold",
                        help="threshold value",
                        type=float, default=0.36)
    args = parser.parse_args()
    
    main(args)