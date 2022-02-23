# img2sound.py
A Python script that converts image files to sound files with the image in the sound spectrum.

## Requirements
Tested in Python 3.9 and Windows 10.

## Installation
Clone img2sound project from GitHub using Git from command line:

``` console
git clone https://github.com/kzmo/img2sound.git
```

-OR-

Copy the img2sound directory into your python path. The zip file can be found
[here](https://github.com/kzmo/img2sound/zipball/master)

To install required libraries run
``` console
python -m pip install -r requirements.txt
```

## Running

Usage:
``` console
python img2sound.py [-h] [--sfreq SFREQ] [--size SIZE] [--linear] [--randomphases] [--overlap OVERLAP] inputfile
```

The output file will be inputfile + ".wav".

Positional arguments:
- **inputfile**: Input image file to be converted

Optional arguments:
- **-h**, **--help**:        Command line help
- **--sfreq SFREQ**:      Sampling frequency in Hz
- **--size SIZE**:        Frequency resolution (FFT block size). Default 1024
- **--linear**:           Use a linear frequency scale instead of logarithmic
- **--randomphases**:     Randomize phases
- **--overlap OVERLAP**:  ISTFT block overlap. Defaults to 0.75 blocks.

## Hints

The length of the generated sound file depends on the sampling frequency,
FFT block size and block overlap. It can be calculated by the formula:

``` console
Length in seconds = (FFT block size *  image horizontal resolution) * (1 - overlap) / sample rate
```

The higher the FFT block size the more vertical resolution there is.

If the sound starts pulsating you can try to increase the overlap.

Phase randomization can help with phase cancellation.

# License

Copyright (c) 2022 Janne Valtanen (janne.valtanen@infowader.com)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
OR OTHER DEALINGS IN THE SOFTWARE.
