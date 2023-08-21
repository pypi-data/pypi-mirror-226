import datetime
import numpy as np

from pytimbre.waveform import LeqDurationMode


class TemporalMetrics:

    # TODO: Frank - make this more generic
    @staticmethod
    def sound_exposure_level(times, levels, decibel_down) -> float:
        """
        The sound exposure level attempts to determine the equivalent level of the acoustic energy placed within a
        single second of the acoustic level.  The dB_down parameter determines how far below the peak that the algorithm
        seeks to integrate the data.

        times : datetime, array-like
            a collection of datetime objects that represent the times for the acoustic levels
        levels : double, array-like
            a collection of acoustic levels that are selected at the same time values as the times array
        dB_down : double
            the number of decibels below the peak that we will integrate the acoustics levels

        returns : double
            the integrated level between the times marking the location of the dB_down levels.
        """

        #   Find the indices for the integration

        start_index, stop_index = TemporalMetrics.find_decibel_down_limits(levels, decibel_down)

        #   Determine the equivalent level between these times
        if isinstance(times[0], datetime.datetime):
            tin = (times[stop_index] - times[start_index]).total_seconds()
        else:
            tin = times[stop_index] - times[start_index]

        return TemporalMetrics.leq(
            levels,
            tin,
            1,
            start_index,
            stop_index)

    @staticmethod
    def find_decibel_down_limits(levels, decibel_down_level):
        """
        Examine the array of levels and determine the points that were above the peak - dB_down_level

        levels : double, array-like
            the acoustic levels in an array that will be examined
        dB_down_level : double
            the level below the peak that will set the limits of the integration

        returns: double, tuple
            the start and stop index of the points to integrate
        """

        #   Find the maximum level

        max_level = max(levels)

        #   Find the index of the maximum value

        max_index = np.argmax(levels)

        #   Determine the start_index

        start_index = -1
        for i in range(max_index, -1, -1):
            if levels[i] <= (max_level - decibel_down_level):
                start_index = i
                break

        #   Determine the stop_index

        stop_index = -1
        for i in range(max_index, len(levels), 1):
            if levels[i] <= (max_level - decibel_down_level):
                stop_index = i
                break

        #   Apply some constraints to ensure that we are within the limits of the array

        if start_index < 0:
            start_index = 0
        if stop_index < 0:
            stop_index = len(levels) - 1

        #   Return the arrays

        return start_index, stop_index

    @staticmethod
    def leq_convert_duration(level: float, tin: float = 1.0, tout: float = 1.0):
        """
        Rescales the energy of a level from one equivalent time duration to another.  The equivalent durations tin
        and tout should be in the same units of time.

        :param level: float
            The sound pressure level representing the total acoustic intensity averaged evenly over the
            equivalent duration tin
        :param tin: float
            The equivalent duration time of the input level
        :param tout: float
            The desired equivalent duration time over which the total acoustic intensity is to be averaged.
         :return: The sound pressure level in decibels converted to the new equivalent duration
         :rtype: float
        """

        return level + 10 * np.log10(tin / tout)

    @staticmethod
    def leq(levels, tin, tout, start_index, stop_index):
        """
        The equivalent level is an integration of levels changing the temporal resolution of the acoustic levels.

        levels : double, array-like
            the list of acoustic levels
        tin : double
            the temporal integration of the input level
        tout : double
            the resultant temporal integration of the output level
        start_index : int
            the index within the levels array that we will begin the integration
        stop_index : int
            the index within the levels array that we will stop the integration

        returns : double
            the integrated, equivalent level
        """

        #   Initialize the acoustic equivalent level

        total_intensity_scaled = 0.0

        #   Sum the linear elements units of sound

        for i in range(start_index, stop_index + 1, 1):
            total_intensity_scaled += 10.0 ** (levels[i] / 10.0)

        total_intensity_level = 10 * np.log10(total_intensity_scaled)
        #   apply the logarithmic conversion and the application of the temporal ratio

        return TemporalMetrics.leq_convert_duration(total_intensity_level, tin, tout)

    @staticmethod
    def equivalent_level(
            times,
            levels,
            equivalent_duration: float = 8 * 3600,
            start_sample: int = 0,
            stop_sample: int = None,
            leq_mode: LeqDurationMode = None,
            exposure_duration: float = None
    ):

        """
        This function computes the equivalent level on a level time history. The duration of the summation
        is specified (in seconds) for the new value with a default of 8 hours. Finally, if there is a cause to exclude
        portions of the data (i.e. calculating the SEL for the 10 dB down points in community noise) you can specify
        the start and stop index. If the stop index is None, then the last level defines the limit of the summation.

        :param double, array-like times:
            The times in seconds corresponding to each sample in levels
        :param levels: double, array-like
            The sound pressure levels time history in decibels
        :param equivalent_duration:   float
            The denominator of the energy averaging - in seconds - representing the desired length of total exposure
            time (e.g. an 8-hour duty day, or a 1-second sound exposure level)
        :param start_sample:   int
            default = 0. The start sample of the pressure summation
        :param stop_sample:   int
            default = None. The stop sample, if the value is None, then it is replaced with the last sample index
        :param leq_mode:   LeqDurationMode --> Enum
            The enumeration to determine whether the input signal contains all energy
            of an exposure to the listener (transient) or the signal represents a sample of a longer-duration
            (steady_state) exposure
        :param exposure_duration:   float
            If leq_mode is steady_state, this is the actual time of noise exposure to the
            listener in seconds
       :return:
            The equivalent sound pressure level representing the total acoustic intensity averaged over
            equivalent_duration
        :raises ValueError: if the times and levels arrays are different lengths

        """

        if len(times) != len(levels):
            raise ValueError(
                f"times and levels must have same length, but have shapes {times.shape} and {levels.shape}")

        if stop_sample is None:
            stop_sample = len(times) - 1

        number_of_samples = stop_sample - start_sample + 1
        dt = np.mean(np.diff(times))
        signal_duration = number_of_samples * dt

        if leq_mode == LeqDurationMode.transient:
            tin = dt
        elif leq_mode == LeqDurationMode.steady_state:
            if exposure_duration is None:
                exposure_duration = signal_duration
            tin = dt * (exposure_duration / signal_duration)
        elif leq_mode is None:
            raise ValueError("User must specify a signal duration mode of class LeqDurationMode.")

        return TemporalMetrics.leq(
            levels=levels,
            tin=tin,
            tout=equivalent_duration,
            start_index=start_sample,
            stop_index=stop_sample
        )
