#coding: utf-8

import wave
import pyaudio
import numpy as np
from matplotlib import pylab as plt
import struct

sr = 44100.0
overlap = 2000

def sigmoid(x):
    x = (1 / (1 + np.exp(-x)))

    return x

def clipping(data):
    #サイン波を-32768から32767の整数値に変換(signed 16bit pcmへ)
    diff = np.max(data) - np.min(data)
    min_ = np.min(data)
    data -= min_
    data /= diff

    return data


class Generater(object):
    def __init__(self):
        self.wform = []

        x = np.arange(-5.0, 5.0, 10.0 / overlap)
        self.sig = sigmoid(x)
        self.invsig = self.sig[::-1]

    def process_window(self, data):
        for i in range(overlap):
            data[i] *= (self.sig[i] ** 2)

        for i in range(overlap):
            data[len(data)-1-i] *= (self.invsig[len(self.invsig)-1-i] ** 2)

        return data

    def generate(self, s):
        self.wform = np.r_[self.wform, s]

    def sine(self, amp, hz, sec):
        s = []

        for n in np.arange(sr * sec):
            #サイン波を生成
            #s = amp * np.sin(2.0 * np.pi * hz * n / sr)
            #self.wform.append(s)
            s.append(amp * np.sin(2.0 * np.pi * hz * n / sr))

        return self.process_window(s)

    def square(self, amp, hz, sec, overtone):
        data = []

        for n in np.arange(sr * sec):
            y = 0.0
            for k in xrange(1, overtone+1):
                y += (amp / (2*k-1)) * np.sin((2.0*k-1) * 2 * np.pi * hz * n / sr)


            #if y > 1.0: y = 1.0
            #if y < -1.0: y = -1.0

            data.append(y)

        return self.process_window(data)

    def synthetic(self, wavlist):
        return np.sum(wavlist, axis=0)

    def output_wav(self, filename, wavelist):
        #サイン波を-32768から32767の整数値に変換(signed 16bit pcmへ)
        clipping(wavelist)

        #r = 32767.0 / (np.max(self.wform) - np.min(self.wform))
        #r = r if r > 1.0 else 1.0

        swav = []
        for x in wavelist:
            swav.append(int(x * 32767.0))


        #バイナリ化
        binwave = struct.pack("h" * len(swav), *swav)

        #サイン波をwavファイルとして書き出し
        w = wave.Wave_write(filename)
        p = (1, 2, sr, len(binwave), 'NONE', 'not compressed')
        w.setparams(p)
        w.writeframes(binwave)
        w.close()


    def illustrate_wav(self):
        x = np.arange(0.0, len(self.wform)/sr, 1/sr)
        y = self.wform
        plt.plot(x, y)
        plt.title("f0 + f1 + f2 + f3")
        plt.xlabel("time [s]")
        plt.ylabel("amplitude")
        plt.axis([0.0, 0.01, -1.0, 1.0])
        plt.show()
