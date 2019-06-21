from roll import MidiFile

if __name__ == "__main__":
    mid = MidiFile("Testing/threshold36/1voce.mid")

    roll = mid.get_roll()

    mid.draw_roll()