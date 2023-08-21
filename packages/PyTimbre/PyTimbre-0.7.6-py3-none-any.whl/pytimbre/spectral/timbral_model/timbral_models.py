from pytimbre.waveform import Waveform
from pytimbre.spectral.spectra import Spectrum
import numpy as np


class TimbralFeatures:
    """
    This collection of code was extracted from the Timbral_model package. The code is refactored to use the PyTimbre
    classes to read/write the audio data. Rather than using a series of different files and individual functions,
    this will combine all required functions into a single file and class.
    """

    @staticmethod
    def boominess_calculate(loudness_spectrum: Spectrum):
        """
        Calculates the Booming Index as described by Hatano, S., and Hashimoto, T. "Booming index as a measure for
        evaluating booming sensation", The 29th International congress and Exhibition on Noise Control Engineering, 2000.

        :param loudness_spectrum:
            The spectrum that is converted to the loudness spectrum rather than the one-third-octave band
        """
        #   TODO: Loudness is calculated only with one-third-octave band and must contain data from 25 Hz to 12.5 kHz.

        # generate the loudness spectrum from the loudness_1991 code results in values from 0.1 to 24 Bark in 0.1 steps,
        # and convert these Bark values to frequency
        z = np.arange(0.1, 24.05, 0.1)
        f = 600 * np.sinh(z / 6.0)
        center_frequencies = [25, 31.5, 40, 50, 63, 80, 100, 125, 160, 200, 250, 315, 400, 500, 630, 800, 1000, 1250,
                              1600,
                              2000, 2500, 3150, 4000, 5000, 6300, 8000, 10000, 12500]

        # now convert f onto the center_frequencies scale
        log_center_frequency = np.log10(center_frequencies)
        frequency_step = log_center_frequency[1] - log_center_frequency[0]
        minimum_frequency = log_center_frequency[0]

        # get the log version of estimated frequencies, and estimate the indexes of the bark scale on the 3rd octave
        # scale
        log_frequency = np.log10(f)
        estimated_index = ((log_frequency - minimum_frequency) / float(frequency_step)) + 1

        # weighting function based from the estimated indexes
        weighting_function = 2.13 * np.exp(-0.151 * estimated_index)

        # change the LF indexes to roll off
        weighting_function[0] = 0.8
        weighting_function[1] = 1.05
        weighting_function[2] = 1.10
        weighting_function[3] = 1.18

        # identify index where frequency is less than 280Hz
        below_280_idx = np.where(f >= 280)[0][0]

        band_sum = 10 * np.log10(np.sum(10 ** (loudness_spectrum.pressures_decibels * weighting_function / 10.0)))
        return band_sum * (np.sum(loudness_spectrum[:below_280_idx]) / np.sum(loudness_spectrum.pressures_decibels))

    @staticmethod
    def timbral_booming(wfm: Waveform):
        """
        This is an implementation of the hasimoto booming index feature. There are a few fudge factors with the code to
        convert between the internal representation of the sound using the same loudness calculation as the sharpness
        code.  The equation for calculating the booming index is not specifically quoted anywhere, so I've done the best I
        can with the code that was presented.

        Shin, SH, Ih, JG, Hashimoto, T., and Hatano, S.: "Sound quality evaluation of the booming sensation for passenger
        cars", Applied Acoustics, Vol. 70, 2009.

        Hatano, S., and Hashimoto, T. "Booming index as a measure for evaluating booming sensation",
        The 29th International congress and Exhibition on Noise Control Engineering, 2000.

        This function calculates the apparent Boominess of an audio Waveform.

        This version of timbral_booming contains self loudness normalising methods and can accept arrays as an input
        instead of a string filename. (FSM) This current version was modified from the original to use the PyTimbre
        features rather that the soundfile methods for reading the files and use the Waveform.

        Version 0.5

        Parameters
        ----------
        :param wfm:
            The representation of the audio

        Returns
        -------
        :returns:
            the boominess of the audio file

        Copyright 2018 Andy Pearce, Institute of Sound Recording, University of Surrey, UK.

        Licensed under the Apache License, Version 2.0 (the "License");
        you may not use this file except in compliance with the License.
        You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

        Unless required by applicable law or agreed to in writing, software
        distributed under the License is distributed on an "AS IS" BASIS,
        WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
        See the License for the specific language governing permissions and
        limitations under the License.
        """
        '''
          Read input
        '''
        audio_samples, fs = wfm.samples, wfm.sample_rate

        # window the audio file into 4096 sample sections
        windowed_audio = timbral_util.window_audio(audio_samples, window_length=4096)

        windowed_booming = []
        windowed_rms = []
        for i in range(windowed_audio.shape[0]):
            samples = windowed_audio[i, :]  # the current time window
            # get the rms value and append to list
            windowed_rms.append(np.sqrt(np.mean(samples * samples)))

            # calculate the specific loudness
            N_entire, N_single = timbral_util.specific_loudness(samples, Pref=100.0, fs=fs, Mod=0)

            # calculate the booming index is contains a level
            if N_entire > 0:
                # boom = boominess_calculate(N_single)
                BoomingIndex = boominess_calculate(N_single)
            else:
                BoomingIndex = 0

            windowed_booming.append(BoomingIndex)

        # get level of low frequencies
        ll, w_ll = timbral_util.weighted_bark_level(audio_samples, fs, 0, 70)

        ll = np.log10(ll)
        # convert to numpy arrays for fancy indexing
        windowed_booming = np.array(windowed_booming)
        windowed_rms = np.array(windowed_rms)

        # get the weighted average
        rms_boom = np.average(windowed_booming, weights=(windowed_rms * windowed_rms))
        rms_boom = np.log10(rms_boom)

        # perform thye linear regression
        all_metrics = np.ones(3)
        all_metrics[0] = rms_boom
        all_metrics[1] = ll

        coefficients = np.array([43.67402696195865, -10.90054738389845, 26.836530575185435])

        return np.sum(all_metrics * coefficients)