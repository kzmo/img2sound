"""
.. module:: img2sound.py
   :synopsis: Converts image files to WAV files using Short-Time FFT

.. moduleauthor:: Janne Valtanen (janne.valtanen@infowader.com)
"""

import argparse
import math

from PIL import Image
import numpy as np
from scipy.signal import istft
import scipy.io.wavfile as wavfile

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Convert image file to audio spectrum \n' +
                    'HINT: Sound file length = (FFT block size *' +
                    ' image horizontal resolution) * (1 - overlap) /' +
                    ' sample rate',
        formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('inputfile', type=str,
                        help="Input image file to be converted.")
    parser.add_argument('--sfreq', type=int, default=44100,
                        help="Sampling frequency in Hz. Default 44100.")
    parser.add_argument('--size', type=int, default=1024,
                        help="Frequency resolution (FFT block size)." +
                        " Default 1024.")
    parser.add_argument('--linear', action='store_true', default=False,
                        help="Use a linear frequency scale instead of" +
                             " logarithmic.")
    parser.add_argument('--randomphases', action='store_true', default=False,
                        help="Randomize phases.")
    parser.add_argument('--overlap', type=float, default=0.75,
                        help="ISTFT block overlap. Defaults to 0.75 blocks.")
    args = parser.parse_args()

    print("Converting image to sound!")

    # Get the arguments
    filename = args.inputfile
    sfreq = args.sfreq
    nperseg = args.size

    # Load image and convert to grayscale using luminosity
    image = Image.open(filename).convert('L')

    # Flip the image upside down so that row 0 is the frequency at index 0
    image_data = np.flipud(np.exp(np.asarray(image) / 256) - 1)

    # Short Time FFT data table
    stft_data = np.zeros((nperseg, image_data.shape[1]))

    # Some scaling factors
    base = 2
    freq_min = 10

    if not args.linear:
        # Logarithmic scaling conversion table
        conv_table = (np.logspace(math.log(freq_min, base),
                                  math.log(nperseg, base),
                                  num=image_data.shape[0],
                                  base=base) - 1).astype(int)
    else:
        # Linear scaling conversion table
        conv_table = np.linspace(0,
                                 nperseg - 1,
                                 num=image_data.shape[0]).astype(int)

    # Scale to vertically to FFT block size using the conversion table
    for line_nr, line in zip(range(stft_data.shape[1]), image_data.T):
        for ogy, y in zip(conv_table, range(line.shape[0])):
            stft_data[ogy][line_nr] = line[y]

    # Randomize phases if requested
    if args.randomphases:
        phases = np.random.rand(stft_data.shape[0],
                                stft_data.shape[1]) * np.pi * 2
        factors = np.exp(1j * phases)
        stft_data = np.multiply(stft_data, factors)

    # Create time-domain audio from the frequency domain blocks
    times, sound_data = istft(stft_data, fs=sfreq, nperseg=nperseg,
                              noverlap=nperseg * 0.75)

    # Remove the DC level
    sound_data = sound_data - np.average(sound_data)

    # Normalize to -1 .. 1
    sound_data = sound_data / np.max(np.abs(sound_data))

    # Convert to writable 16bit binary image
    writable = (sound_data * (2 ** 15 - 1)).astype(np.int16)
    writable = np.int16(sound_data/np.max(np.abs(sound_data)) * 32767)

    # Write to file
    outfile = filename + ".wav"
    print(f"Writing to file: {outfile}")
    wavfile.write(outfile, int(sfreq), writable)
