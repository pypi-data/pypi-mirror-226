import numpy as np
from pytimbre.spectral.spectra import Spectrum


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
    center_frequencies = [25, 31.5, 40, 50, 63, 80, 100, 125, 160, 200, 250, 315, 400, 500, 630, 800, 1000, 1250, 1600,
                          2000, 2500, 3150, 4000, 5000, 6300, 8000, 10000, 12500]

    # now convert f onto the center_frequencies scale
    log_center_frequency = np.log10(center_frequencies)
    frequency_step = log_center_frequency[1] - log_center_frequency[0]
    minimum_frequency = log_center_frequency[0]

    # get the log version of estimated frequencies, and estimate the indexes of the bark scale on the 3rd octave scale
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