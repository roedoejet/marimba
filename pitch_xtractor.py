import parselmouth
import math
from midiutil.MidiFile import MIDIFile

class MarimbaXtractor:
    def __init__(self, path_to_wav, tuning=440):
        self.tuning = tuning
        self.sound = parselmouth.Sound(path_to_wav)
        self.pitch = self.sound.to_pitch()
        self.f0_hz = self.pitch.selected_array['frequency']
        self.midi_time_frames = self.tfs_to_midi()
        # lumped_notes = self.remove_notes_shorter_than(self.lump_notes(self.midi_time_frames))
        # self.midi_notes = self.lump_notes(lumped_notes)
        self.midi_notes = self.lump_notes(self.midi_time_frames)
        self.allowable_notes = [43, 51, 52, 53, 57]
     
    def tfs_to_midi(self):
        notes = []
        for f in range(len(self.pitch)):
            hz = self.pitch.selected_array['frequency'][f]
            try:
                t0 = self.pitch.get_time_from_frame_number(f)
            except TypeError:
                t0 = 0
            t1 = self.pitch.get_time_from_frame_number(f+1)
            d = t1 - t0
            note = self.pitch_to_midi(hz)
            notes.append({'note': note, 'start': t0, 'duration': d})
        return notes

    def pitch_to_midi(self, f0):
        ''' midi = 69 + 12log2(f/440Hz)
        '''
        if f0:
            return int(69+(12*math.log(float(f0)/self.tuning))/(math.log(2)))
        else:
            return 0

    def lump_notes(self, midi_time_frames):
        '''Lump notes together
        '''
        current_midi_note = midi_time_frames[0]['note']
        start_time = midi_time_frames[0]['start']
        notes = []
        for tf in midi_time_frames:
            if tf['note'] != current_midi_note:
                # Get duration
                duration = (tf['start'] + tf['duration']) - start_time
                # Add the note
                notes.append({'note': current_midi_note, 'start': start_time, 'duration': duration})
                # Reset start time and current note
                start_time = tf['start'] + tf['duration']
                current_midi_note = tf['note']
        return notes

    def remove_notes_shorter_than(self, midi_time_frames, t=0.03):
        '''Remove all notes shorter than t, and add the duration of 
        the deleted note to the previous midi time frame
        '''
        to_delete = []
        for n in range(len(midi_time_frames)):
            if midi_time_frames[n]['duration'] < t:
                midi_time_frames[n-1]['duration'] += midi_time_frames[n]['duration']
                to_delete.append(n)
        for i in sorted(to_delete, reverse=True):
            del midi_time_frames[i]
        return midi_time_frames

    def write_to_midi(self, midi_time_frames, tempo=60):
        mf = MIDIFile(1)
        track = 0
        time = 0
        tempo_multiplier = 60/tempo
        mf.addTrackName(track, time, 'Marimba')
        mf.addTempo(track, time, tempo)

        channel = 0
        volume = 100
        beat = 1

        for tf in midi_time_frames:
            if tf['note'] > 0:
                # breakpoint()
                print(f"Adding note {tf['note']} starting at {beat} lasting for {1} beat")
                mf.addNote(track, channel, tf['note'], beat, 1, volume)
                beat += 1

        with open('output.mid', 'wb') as outf:
            mf.writeFile(outf)            


if __name__ == "__main__":
    mx = MarimbaXtractor('marimba_cut.wav')
    mx.write_to_midi(mx.midi_notes)
    mx2 = MarimbaXtractor('marimba_cut_lpf.wav')
    mx2.write_to_midi(mx.midi_notes)
    # notes = mx.lump_notes(mx.midi_time_frames)
    breakpoint()