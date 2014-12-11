import os
import inspect
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
import matplotlib.gridspec as mpl_gridspec
import matplotlib.cm as mpl_colour_maps
import matplotlib.colors as mpl_colours

def make_colour_map(minimum_value=0, maximum_value=1, colour_map='jet'):
    return mpl_colour_maps.ScalarMappable(norm=mpl_colours.Normalize(vmin=minimum_value,
                                                                     vmax=maximum_value),
                                          cmap=plt.get_cmap(colour_map))

from corefunctions import namedtuple, defaultdict, OrderedDict

from logbuilder import setup_custom_logger, log_with
###########################################################
#   End of external imports 
###########################################################

logging_directory = 'log'

mylog = setup_custom_logger(__name__, logging_directory=logging_directory)
mylog.debug('Finshed importing external libraries {}'.format(__name__))
