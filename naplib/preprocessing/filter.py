from scipy import signal as sig

from ..data import Data
from ..utils import _parse_outstruct_args

def filter_butter(data=None, field='resp', btype='bandpass', Wn=[70,150], fs='dataf', order=2, return_filters=False):
    '''
    Filter time series signals using an Nth order digital Butterworth filter. The filter
    is applied to each column of each trial in the field data.
    
    Parameters
    ----------
    data : naplib.Data object, optional
        Data object containing data to be normalized in one of the field. If not given, must give
        the data to be normalized directly as the ``data`` argument. 
    field : string | list of np.ndarrays or a multidimensional np.ndarray
        Field to bandpass filter. If a string, it must specify one of the fields of the Data
        provided in the first argument. If a multidimensional array, first dimension
        indicates the trial/instances. Each trial's data must be of shape (time, channels)
    Wn : float, list or array-like, default=[70,150]
        Critical frequencies, in Hz. The critical frequency or frequencies. For lowpass and highpass filters,
        Wn is a scalar; for bandpass and bandstop filters, Wn is a length-2 sequence.
    btype : string, defualt='bandpass
        Filter type, one of {‘lowpass’, ‘highpass’, ‘bandpass’, ‘bandstop’}
    fs : string | float
        Sampling rate of the field to filter. If a string, must specify a field of the Data
        object. Can be a single float if all trial's have the same sampling rate, or can be
        a list of floats specifying the sampling rate for each trial.
    order : int
        The order of the filter.
    return_filters : bool, default=False
        If True, return the filter transfer function coefficients from each trial's filtering.
    
    Returns
    -------
    filtered_data : list of np.ndarrays
        Filtered time series.
    filter : list
        Filter transfer function coefficients returned as a list of (b, a) tuples. Only
        returned if ``return_filters`` is True.
    '''
    
    field, fs = _parse_outstruct_args(data, field, fs, allow_different_lengths=True, allow_strings_without_outstruct=False)

    if not isinstance(fs, list):
        fs = [fs for _ in field]
        
    filtered_data = []
    
    filters = []
    
    for trial_data, trial_fs in zip(field, fs):
    
        b, a = sig.butter(order, Wn, btype=btype, fs=trial_fs, output='ba')
        
        filters.append((b, a))
        
        filtered_data.append(sig.filtfilt(b, a, trial_data, axis=0))
        
    if return_filters:
        return filtered_data, filters

    return filtered_data