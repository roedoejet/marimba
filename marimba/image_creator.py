import parselmouth

import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
import os




class ImageGenerator:
    def __init__(self, wav_path, output_dir):
        self.wav_path = wav_path
        self.output_dir = output_dir
        self.snd = parselmouth.Sound(wav_path)
        sns.set() # Use seaborn's default style to make attractive graphs
        matplotlib.use('agg')

    def write_plot(self, fn):
        plt.savefig(os.path.join(self.output_dir, fn))

    # Plot nice figures using Python's "standard" matplotlib library
    def create_wave(self):
        plt.figure()
        plt.plot(self.snd.xs(), self.snd.values.T)
        plt.xlim([self.snd.xmin, self.snd.xmax])
        plt.xlabel("time [s]")
        plt.ylabel("amplitude")

    def create_spectrogram(self):
        pitch = self.snd.to_pitch()
        # If desired, pre-emphasize the sound fragment before calculating the spectrogram
        pre_emphasized_snd = self.snd.copy()
        pre_emphasized_snd.pre_emphasize()
        spectrogram = pre_emphasized_snd.to_spectrogram(window_length=0.03, maximum_frequency=8000)
        plt.figure()
        self.draw_spectrogram(spectrogram)
        plt.twinx()
        self.draw_pitch(pitch)
        plt.xlim([self.snd.xmin, self.snd.xmax])

    def draw_spectrogram(self, spectrogram, dynamic_range=70):
        X, Y = spectrogram.x_grid(), spectrogram.y_grid()
        sg_db = 10 * np.log10(spectrogram.values)
        plt.pcolormesh(X, Y, sg_db, vmin=sg_db.max() - dynamic_range, cmap='afmhot')
        plt.ylim([spectrogram.ymin, spectrogram.ymax])
        plt.xlabel("time [s]")
        plt.ylabel("frequency [Hz]")

    def draw_pitch(self, pitch):
        # Extract selected pitch contour, and
        # replace unvoiced samples by NaN to not plot
        pitch_values = pitch.selected_array['frequency']
        pitch_values[pitch_values==0] = np.nan
        plt.plot(pitch.xs(), pitch_values, 'o', markersize=5, color='w')
        plt.plot(pitch.xs(), pitch_values, 'o', markersize=2)
        plt.grid(False)
        plt.ylim(0, pitch.ceiling)
        plt.ylabel("fundamental frequency [Hz]")