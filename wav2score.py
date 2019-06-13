import argparse
from wav2midi import wav2midi
from midi2lily import midi2score

def main(args):
    wav2midi(args.wav_file, args.model_path, args.program, args.threshold)
    
    midi_file = args.wav_file[:-4] + ".mid"
    midi2score(midi_file)        

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Transcribe on the given audio.")
    parser.add_argument("-i", "--wav-file",
                        help="Path to the input audio you want to transcribe",
                        type=str)
    parser.add_argument("-m", "--model-path", 
                        help="Path to the pre-trained model.",
                        type=str)
    parser.add_argument("-p", "--program",
                        help="What sound to use",
                        type=int, default=0)
    parser.add_argument("-t", "--threshold",
                        help="threshold value",
                        type=float, default=0.36)
    args = parser.parse_args()
    
    main(args)