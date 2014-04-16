'''
Module that holds various statistical routines.
'''

__all__ = ['fit_lognormal_to_histogram', 'list_stats']

from . external import *
mylog = setup_custom_logger(__name__)
mylog.debug('Entering {0}'.format(__name__))

from . structures import ListStats, MeanSTD

def fit_lognormal_to_histogram(hist=None, bin_edges=None):
    '''Fit a lognormal distribution to histogram data using the
       cumulative lognormal distribution function.

    Takes output (hist, bin_edges) from either the matplotlib
    function ax.hist or numpy.histogram.

    hist, bin_edges = numpy.histogram(...)
    hist, bin_edges, patches = ax.hist(...)

    Parameters
    ==========
    hist : array
    
    bin_edges : array

    Returns
    =======
    x : x values of pdf at bin locations
    y : y values of pdf at bin locations
    stats : namedtuple(mean, standard_deviation)
    '''
    x_pdf = bin_edges[1:]
    y_cdf = hist.cumsum() / hist.cumsum().max()  # Normalise the cumulative sum

    def cdf_fn(x, shape, scale):
        return scipy_stats.lognorm.cdf(x, shape, loc=0, scale=scale)
        
    (shape_out, scale_out), pcov = scipy_curve_fit(cdf_fn, x_pdf, y_cdf)

    y_pdf = scipy_stats.lognorm.pdf(x_pdf, shape_out, loc=0, scale=scale_out)

    return x_pdf, y_pdf, MeanSTD(scale_out, shape_out)


def list_stats(number_iterable, tag=None):
    '''
    Evaluates a number of statistics for a list of numerical values.

    Parameters
    ==========

    number_iterable : any object that can be turned into a numpy.array
                      numpy.array(number_iterable)
    tag: str
         Optional information to include in the return object.

    Returns
    =======

    tuple_of_stats : ListStats namedtuple
    '''
    
    values = numpy.array(number_iterable)
    
    try:
        mean = values.mean()
    except Exception as e:
        mylog.info('Error evaluating mean for: {}'.format(number_iterable))
        raise e
        
    try:
        hv = values.max()
    except ValueError as e:
        mylog.info('Error evaluating max for: {}'.format(number_iterable))
        raise e
    except Exception as e:
        raise e
        
    lv = values.min()
    drange = hv - lv
    
    return ListStats(mean, hv, lv, drange, drange/float(mean), numpy.std(values),
                     numpy.median(values), values.size, values.sum(), tag)



