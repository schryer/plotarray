'''
This module holds the core routines of plotarray.
'''
__all__ = ['retrieve_plot_data', 'save_plot_data', 'make_plot_array']

from . external import *
mylog = setup_custom_logger(__name__, logging_directory=logging_directory)
mylog.debug('Entering {0}'.format(__name__))

from . structures import colours, colour_dic
from . stats import list_stats, fit_lognormal_to_histogram

@log_with(mylog)
def retrieve_plot_data(filename, verbose=True):
    '''
    Used to retrieve plot_data from an HDF5 file.

    :param filename: The HDF5 filename to retrieve the plot_data from.
    :type filename: :py:obj:`str`
    :returns: :py:obj:`None` if filename does not exist, otherwise plot_data (:py:obj:`dict`)
    '''
    if os.path.exists(filename):
        try:
            h5_file = h5py.File(filename, 'r')
        except OSError as e:
            return None
        except Exception as e:
            raise Exception('Error trying to read {}'.format(filename), e)

        plot_data = defaultdict(dict)
        for series_key, series_dic in h5_file.items():
            for data_key, data_list in series_dic.items():
                if hasattr(data_list, 'value'):
                    plot_data[series_key][data_key] = data_list.value
                else:
                    dl = [v for k, v in data_list.items()]
                    print(dl, type(dl), data_key)

        if verbose:
            mylog.info('Retrieving plot data from: {}'.format(filename))

        return plot_data
        
    return None

@log_with(mylog)
def save_plot_data(plot_data, filename):
    '''
    Used to save plot_data to an HDF5 file.

    :param plot_data: The plot_data dictionary to be saved.
    :type plot_data: :py:obj:`dict`
    :param filename: The HDF5 filename to save plot_data into.
    :type filename: :py:obj:`str`
    '''

    def get_dtype(item):
        return_item = item
        
        if hasattr(item, '__len__'):
            data_length = len(item)
            if any([type(i)  == numpy.ndarray for i in item]):
                dtype = 'array_of_arrays'
            elif  any([type(i) == list for i in item]):
                dtype = 'array_of_arrays'
                return_item = [numpy.array(i) for i in item]
            elif any([type(i) in (float, numpy.float64) for i in item]):
                dtype = 'float64'
            elif all([type(i) in (int, numpy.int64) for i in item]):
                dtype = 'int64'
            elif all([type(i) == str for i in item]):
                max_length = max([len(i) for i in item])
                dtype = '|S{}'.format(max_length)
            else:
                #print(item, type(item))
                raise NotImplementedError('This data type has not yet been implemented.', type(item[0]))
        else:
            data_length = 1
            if type(item) in (float, numpy.float64):
                dtype = 'float64'
            elif type(item) in (int, numpy.int64):
                dtype = 'int64'
            elif type(item) == str:
                dtype = '|S{}'.format(len(item))
            else:
                raise NotImplementedError('This data type has not yet been implemented.', type(item))
        return dtype, data_length, return_item
    
    mylog.info('Saving table: {}'.format(filename))

    h5_file = h5py.File(filename, 'w')

    for series_key, series_dic in plot_data.items():
        series_length = None
        for data_key, data_list in series_dic.items():
            if data_key in ['X', 'Y']:
                if len(data_list) < 1:
                    msg_tmpl = 'Skipping series {} with data type {} because it has zero length.'
                    mylog.info(msg_tmpl.format(series_key, data_key))
                    continue
                if not series_length:
                    series_length == len(data_list)
                elif len(data_list) != series_length:
                    msg_tmpl = 'Skippping {} with data type {} because its length does not match the series length.'
                    mylog.info(msg_tmpl.format(series_key, data_key))
                    continue

            dtype, data_length, d_list = get_dtype(data_list)

            h5_key = '{}/{}'.format(series_key, data_key)
            msg_tmpl = 'Adding data series {} to HDF5 file with {} data points of type {}'
            
            if dtype == 'array_of_arrays':
                mylog.debug(msg_tmpl.format(h5_key, (len(d_list), len(d_list[0])), 'numpy.ndarray'))
                h5_file.create_dataset(h5_key, data=numpy.array(d_list))
            else:
                mylog.debug(msg_tmpl.format(h5_key, data_length, dtype))
                h5_file.create_dataset(h5_key, data=numpy.array(d_list, dtype=dtype))

@log_with(mylog)
def _get_figure(plot_info):
    
    fig = plt.figure(figsize=plot_info['figsize'])
    plt.suptitle(plot_info['title'])
    
    ax_dic = {}
    for key, value in plot_info.items():
        if key in ['shape', 'figsize', 'title', 'topspace']:
            continue
        loc, colspan, rowspan = key
        mylog.debug('loc:{} colspan:{} rowspan:{}'.format(loc, colspan, rowspan))

        gs = mpl_gridspec.GridSpec(plot_info['shape'][0], plot_info['shape'][1])
        subplotspec = gs.new_subplotspec(loc, rowspan, colspan)        
        ax = plt.subplot(subplotspec)

        ax_dic[key] = ax
            
    return fig, ax_dic

@log_with(mylog)
def _plot_scatter(plot_dic, ax, defaults):
    
    X, Y = plot_dic['x'], plot_dic['y']

    if len(X) != len(Y):
        raise UserWarning('You have supplied data that is not the same shape.', len(X), len(Y), defaults)
    
    ax.plot(X, Y, marker=defaults['marker'], linestyle='None', label=defaults['legend'],
            markersize=defaults['markersize'], markerfacecolor=defaults['colour'], markeredgewidth=0,
            alpha=defaults['alpha'])

    if defaults['addvline']:
        ax.axvline(list_stats(X).median, color=defaults['colour'], ls='-')

    if defaults['trendline']:
        X[X == float('-inf')] = 0
        Y[Y == float('-inf')] = 0

        if defaults['trendline_through_zero']:
            A = numpy.vstack([X, numpy.zeros(len(X))]).T
        else:
            A = numpy.vstack([X, numpy.ones(len(X))]).T
            
        slope, intercept = numpy.linalg.lstsq(A, Y)[0]
        
        x_fit = numpy.linspace(numpy.min(X), numpy.max(X), 2)
        ax.plot(x_fit, slope*x_fit + intercept, color=defaults['colour'], linestyle=defaults['trendline_style'])
        
    return ax

@log_with(mylog)
def _plot_hinton(plot_dic, ax, defaults):

    matrix = plot_dic['matrix']

    if not defaults['max_weight']:
        max_weight = 2 ** numpy.ceil(numpy.log(numpy.abs(matrix).max()) / numpy.log(2))

    ax.patch.set_facecolor('gray')
    ax.set_aspect('equal', 'box')
    ax.xaxis.set_major_locator(plt.NullLocator())
    ax.yaxis.set_major_locator(plt.NullLocator())

    for (x,y), w in numpy.ndenumerate(matrix):
        color = 'white' if w > 0 else 'black'
        size = numpy.sqrt(numpy.abs(w))
        rect = plt.Rectangle([x - size / 2, y - size / 2], size, size,
                             facecolor=color, edgecolor=color)
        ax.add_patch(rect)

    return ax
    
@log_with(mylog)
def _plot_histogram(plot_dic, ax, defaults):
                    
    raw_X = plot_dic['x']

    if defaults['function']:
        raw_X = defaults['function'](raw_X)
    
    if defaults['xlim']:
        X = []
        for index, Xvalue in enumerate(raw_X):
            if Xvalue < defaults['xlim'][0]:
                continue
            if Xvalue > defaults['xlim'][1]:
                continue
            X.append(Xvalue)
        if len(X) < 1:
            msg_tmpl = '{} No data found within xlim of ({}, {})'
            mylog.info(msg_tmpl.format(defaults['info_key'], defaults['xlim'][0], defaults['xlim'][1]))
            return ax
    else:
        X = raw_X

    mX = list_stats(X).mean
        
    try:
        hist, bin_edges, patches = ax.hist(X, defaults['N_bins'], color=defaults['colour'], alpha=defaults['alpha'])        
    except AttributeError as e:
        mylog.info('{} No data found.'.format(defaults['info_key']))
        return ax
        
    xmin, xmax = min(X)-mX/2.0, max(X)+mX/2.0 
    ax.set_xlim([xmin, xmax])

    # Number of bins with data
    N_bars = sum([1 if value > 0 else 0 for value in hist])
    
    if defaults.get('lognormal_fit', False) and N_bars > 10:
        x_pdf, y_pdf, stats_pdf = fit_lognormal_to_histogram(hist=hist, bin_edges=bin_edges)

        mylog.info('{0} Mean:{1.mean} SD:{1.standard_deviation}'.format(defaults['info_key'], stats_pdf))
        
        ax2 = ax.twinx()
        ax2.plot(x_pdf, y_pdf, 'k', linewidth=2)
        ax2.set_ylabel('y of PDF')
        ax2.text(0.85, 0.9,'mu={0.mean:.2f} SD={0.standard_deviation:.2f}'.format(stats_pdf),
                 ha='center', va='center', transform=ax.transAxes)
    
    return ax
    
@log_with(mylog)
def _get_plot_defaults(ax_key, plot_series, plot_info, filename):
    info_key = 'Filename:{} plot_series:{}'.format(filename, plot_series)
    
    msg_tmpl = 'Processing ax_key:{} plot_series:{} plot_info:{} {}'
    mylog.debug(msg_tmpl.format(ax_key, plot_series, plot_info[ax_key], info_key))
    
    colour_key = plot_info[ax_key]['series'][plot_series]
    mylog.debug('{} has colour_key: {}'.format(info_key, colour_key))

    defaults = dict(alpha=0.25, markersize=2, marker='o', legend=None, addvline=False, lognormal_fit=False)
    if plot_info[ax_key]['type'] == 'histogram':
        defaults['N_bins'] = 50
        
    for mpl_key in defaults.keys():
        value_dic = plot_info[ax_key].get(mpl_key, None)
        if value_dic:
            mylog.debug('{} Setting plot parameter {} using value dic: {}'.format(info_key, mpl_key, value_dic))
            defaults[mpl_key] = value_dic.get(plot_series, defaults[mpl_key])

    defaults['colour'] = colour_dic[colour_key]
    defaults['plot_series'] = plot_series
    if plot_info[ax_key]['type'] == 'histogram':
        defaults['xlim'] = plot_info[ax_key]['mpl'].get('xlim', None)
        defaults['function'] = plot_info[ax_key].get('function', None)

    if plot_info[ax_key]['type'] == 'scatter':
        defaults['trendline'] = plot_info[ax_key].get('trendline', {}).get(plot_series, None)
        defaults['trendline_style'] = plot_info[ax_key].get('trendline_style', {}).get(plot_series, '-')
        defaults['trendline_through_zero'] = plot_info[ax_key].get('trendline_through_zero', {}).get(plot_series, False)
        

    defaults['info_key'] = info_key
    mylog.debug('Plot defaults: {}'.format(defaults))

    return defaults

@log_with(mylog)
def make_plot_array(plot_data, plot_info, filename='default_plotarray_filename.pdf'):
    '''The workhorse function that makes all plots in the array and saves them together in a file.

    |  The functions :func:`plotarray.retrieve_plot_data` and :func:`plotarray.save_plot_data`
    |  can be used together to speed up the loading of plot_data from an HDF5 file prior to
    |  calling this function.
    
    :param plot_data: All data series referred to in plot_info are contained in plot_data.
    :type plot_data: :py:obj:`dict`
    :param plot_info: All information about how to construct the plot is contained in plot_info.
    :type plot_info: :py:obj:`dict`
    :param filename: The filename to save the plot as. The extension of this filename |br|
                     should be one that is recognized by matplotlib.
    :type filename: :py:obj:`str`
    '''
    fig, ax_dic = _get_figure(plot_info)

    for ax_key, ax in ax_dic.items():
        for plot_series, plot_dic in plot_data.items():
            if plot_series not in plot_info[ax_key]['series']:
                continue
            if len(plot_dic['x']) < 1:
                mylog.info('Skipping plot_series {} because it has zero data points.'.format(plot_series))
                continue
            if len(plot_dic['y']) != len(plot_dic['x']):
                mylog.info('Skipping plot_series {} because len(y) != len(x).'.format(plot_series))
                continue
            #print((len(plot_dic['x']), len(plot_dic['y'])))

            defaults = _get_plot_defaults(ax_key, plot_series, plot_info, filename)
                
            if plot_info[ax_key]['type'] == 'scatter':
                ax_dic[ax_key] = _plot_scatter(plot_dic, ax, defaults)

            elif plot_info[ax_key]['type'] == 'histogram':
                ax_dic[ax_key] = _plot_histogram(plot_dic, ax, defaults)

        for line_key in ('axvlines', 'axhlines'):
            if line_key in plot_info[ax_key]['mpl'].keys():
                for axl in plot_info[ax_key]['mpl'][line_key]: 
                    if axl.get('color', False):
                        if axl['color'] in colour_dic.keys():
                            axl['color'] = colour_dic[axl['color']]
                    if line_key == 'axvlines':
                        ax.axvline(**axl)
                    if line_key == 'axhlines':
                        ax.axhline(**axl)

                del plot_info[ax_key]['mpl'][line_key]

        if plot_info[ax_key]['mpl'].get('xticklabels'):
            if plot_info[ax_key]['mpl'].get('rotate_xticklabels'):
                rotation = plot_info[ax_key]['mpl']['rotate_xticklabels']
                del plot_info[ax_key]['mpl']['rotate_xticklabels']
                
            ax.set_xticklabels(plot_info[ax_key]['mpl']['xticklabels'], rotation=rotation)
            del plot_info[ax_key]['mpl']['xticklabels']
                
        plt.setp(ax, **plot_info[ax_key]['mpl'])

    plt.tight_layout(rect=(0, 0, 1, plot_info.get('topspace', 1)))
        
    mylog.info('Saving figure: {0}'.format(filename))
    plt.savefig(filename)
    fig.clf()
    plt.close()
