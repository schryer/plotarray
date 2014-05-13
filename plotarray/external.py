import os
import inspect
import logging
import webcolors
import itertools

from collections import namedtuple, defaultdict, OrderedDict

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

###########################################################
#   End of external imports 
###########################################################

_log_dir = 'log'
        
def setup_custom_logger(name, level=logging.DEBUG, logging_directory=_log_dir):
    '''
    Creates a logger that outputs to its own file (logging_directory/name.log).
    
    Parameters
    ==========
    
    name  : str
            Name used to store this log under (typically the module name stored under __name__)
    
    level : int
            Default level to initiate log with (Default is set using logging.DEBUG)
            Can be changed with the custom_logger.setLevel function.
    
    logging_directory : str
            Directory to store log file in (defaults to logs) 
    
    Returns
    =======
    
    custom_logger
    '''
    
    if not os.path.exists(logging_directory):
        os.mkdir(logging_directory)
   
    class LevelFilter(logging.Filter):
        def __init__(self, level):
            self.level = level

        def filter(self, record):
            return record.levelno == self.level

    log_file = os.path.join(logging_directory, '{}.log'.format(name))
    fh = logging.FileHandler(log_file)
    #fh.setLevel(logging.INFO)
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(logging.Formatter('%(asctime)s | %(name)s | %(levelname)s | %(message)s'))

    sh = logging.StreamHandler()
    sh.setLevel(logging.INFO)
    sh.addFilter(LevelFilter(logging.INFO))
    
    logger = logging.getLogger(name)

    logger.addHandler(fh)
    logger.addHandler(sh)

    logger.setLevel(level)
    
    logger.debug('Finished creating log file {} with logging level {}'.format(log_file, level)) 
    
    return logger    

mylog = setup_custom_logger(__name__)
mylog.debug('Finshed importing external libraries {}'.format(__name__))
