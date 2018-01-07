# coding:utf-8
import sys
import numpy as np
import math
from matplotlib import pylab as plt
import generate as gnrt

OUTPUT_DIR = "" #相対的な保存ディレクトリ
OUTPUT_NAME = "01_overtone" #書き出す.wavの名前

scale = {
    "c3":261.626, "cs3":277.183, "d3":293.665, "ds3":311.127,
    "e3":329.628, "f3":349.228, "fs3":369.994, "g3":391.995,
    "gs3":415.305, "a3":440.000,"as3":466.164, "b3":493.883,

    "c4":523.251
}

def overtone(gnrtr):
    f0 = 200
    r = math.pow(2, 1.0/12.0)

    gnrtr.generate(gnrtr.square(1.0, f0, 0.1, 0))
    gnrtr.generate(gnrtr.square(1.0, f0, 3.0, 1))
    gnrtr.generate(gnrtr.square(1.0, f0, 3.0, 2))
    gnrtr.generate(gnrtr.square(1.0, f0, 3.0, 3))
    gnrtr.generate(gnrtr.square(1.0, f0, 3.0, 4))

    gnrtr.generate(gnrtr.square(1.0, f0, 1.0, 4))
    gnrtr.generate(gnrtr.square(1.0, f0 * math.pow(r, 4), 1.0, 4))
    gnrtr.generate(gnrtr.square(1.0, f0 * math.pow(r, 7), 1.0, 4))

    gnrtr.generate(gnrtr.synthetic([gnrtr.square(0.6, f0 * math.pow(r, 0), 3.0, 4),
                              gnrtr.square(0.6, f0 * math.pow(r, 4), 3.0, 4),
                              gnrtr.square(0.6, f0 * math.pow(r, 7), 3.0, 4)]))

    gnrtr.output_wav("01_overtone.wav", gnrtr.wform)



def sweep():
    f0 = 440.0
    sr = 44100.0
    data = []

    octave = 15

    for i in xrange(44100*3):
        y = 0.0
        for k in xrange(1, octave+1):
            y += (0.5 / (2*k-1)) * np.sin((2.0*k-1) * 2 * np.pi * f0 * i / 44100.0)

        data.append(y)

    raise_ = []
    waves = []
    amp = 1.0
    for x in np.arange(-0.5, 0.5, 1 / 1000.0):
        #f = f0 * (2 ** (x / 12.0))
        f = f0
        T = 1 / f
        nsamp = int(sr * T)
        print nsamp

        for i in range(nsamp):
            raise_.append(amp if i < nsamp/2 else -amp)
    print len(raise_)
    return

    """
    raise_ = []
    hop = 1 / (sr * 10)
    x = 0.0
    for i in xrange(441000):
        hz = f0 * math.pow(2, ((2 / 24.0) * x - (1 / 24.0)))

        y = 0.0
        for k in xrange(1, octave+1):
            y += (1.0 / (2*k-1)) * np.sin((2.0*k-1) * 2 * np.pi * hz * i / 44100.0)

        raise_.append(y)

        if i == sr * 2:
            hop = 1.0 / ((sr * 10) * 3.0)
        elif i == sr * 6:
            hop = (1.0 - x) / (sr * 4)

        x += hop
    """

    inv = raise_[::-1]

    monotone = []
    for i in xrange(44100*23):
        y = 0.0
        for k in xrange(1, 16):
            y += (1.0 / (2*k-1)) * np.sin((2.0*k-1) * 2 * np.pi * f0 * i / 44100.0)
        monotone.append(y)

    #gnrtr.generate(gnrtr.square(1.0, f0, 3.0, octave+1))
    gnrtr.generate(gnrtr.synthetic([(gnrtr.process_window(data)+gnrtr.process_window(raise_)+gnrtr.process_window(inv)), gnrtr.process_window(monotone)]))
    #gnrtr.wform = data

def intonation():
    f0 = 440.0
    r = math.pow(2, 1.0/12.0)
    octave = 10

    aveC = f0
    aveG = f0 * math.pow(r, 7)
    aveE = f0 * math.pow(r, 16)
    justC = f0
    justG = f0 * (3 / 2.0)
    justE = f0 * (5 / 4.0) * 2

    wg.generate(wg.square(1.0, aveC, 1.0, octave))
    wg.generate(wg.square(1.0, aveG, 1.0, octave))
    wg.generate(wg.square(1.0, aveE, 1.0, octave))
    wg.generate(wg.synthetic([wg.square(1.0, aveC,  3.0, octave),
                              wg.square(1.0, aveG,  3.0, octave),
                              wg.square(1.0, aveE,  3.0, octave)]))

    wg.generate(wg.square(0.0, f0, 1.0, octave))

    wg.generate(wg.square(1.0, justC, 1.0, octave))
    wg.generate(wg.square(1.0, justG, 1.0, octave))
    wg.generate(wg.square(1.0, justE, 1.0, octave))

    wg.generate(wg.synthetic([wg.square(1.0, justC, 3.0, octave),
                              wg.square(1.0, justG, 3.0, octave),
                              wg.square(1.0, justE, 3.0, octave)]))

    wg.generate(wg.square(0.0, f0, 1.0, octave))

    wg.generate(wg.synthetic([wg.square(1.0, aveC,  4.0, octave),
                              wg.square(1.0, aveG,  4.0, octave),
                              wg.square(1.0, aveE,  4.0, octave)]))
    wg.generate(wg.synthetic([wg.square(1.0, justC, 4.0, octave),
                              wg.square(1.0, justG, 4.0, octave),
                              wg.square(1.0, justE, 4.0, octave)]))
    wg.generate(wg.synthetic([wg.square(1.0, aveC,  4.0, octave),
                              wg.square(1.0, aveG,  4.0, octave),
                              wg.square(1.0, aveE,  4.0, octave)]))
    wg.generate(wg.synthetic([wg.square(1.0, justC, 4.0, octave),
                              wg.square(1.0, justG, 4.0, octave),
                              wg.square(1.0, justE, 4.0, octave)]))



def main(outputpath):
    gnrtr = gnrt.Generater()
    gnrtr.generate(gnrtr.sine(1.0, 466.164, 3.0))

    #overtone(gnrtr)

    gnrtr.output_wav(outputpath + ".wav", gnrtr.wform)
    #wg.illustrate_wav()

if __name__ == "__main__":
    main(sys.argv[1])
