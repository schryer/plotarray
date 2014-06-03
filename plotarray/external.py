import os
import inspect
import logging
import webcolors
import itertools

###########################################################
#   Start of external imports 
###########################################################
import numpy
from scipy import stats as scipy_stats
from scipy.optimize import curve_fit as scipy_curve_fit
import h5py

import matplotlib
matplotlib.use('Agg')

from matplotlib import rcParams

rcParams['font.family'] = 'sans-serif'
rcParams['font.serif'] = ['Computer Modern Sans Serif']
rcParams['mathtext.default'] = 'regular'

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

from corefunctions import namedtuple, defaultdict, OrderedDict

from logbuilder import setup_custom_logger, log_with
###########################################################
#   End of external imports 
###########################################################

_log_dir = 'log'

mylog = setup_custom_logger(__name__, logging_directory=_log_dir)
mylog.debug('Finshed importing external libraries {}'.format(__name__))
