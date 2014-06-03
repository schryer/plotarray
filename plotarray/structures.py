'''
Module that holds various data structures.
'''

__all__ = ['ListStats', 'MeanSTD', 'colour_dic', 'colours']

from . external import *
mylog = setup_custom_logger(__name__)
mylog.debug('Entering {0}'.format(__name__))

ListStats = namedtuple('ListStats', ['mean', 'high_value', 'low_value', 'range',
                                     'range_over_mean', 'standard_deviation', 'median', 'N', 'sum', 'tag'])

MeanSTD = namedtuple('MeanSTD', ['mean', 'standard_deviation'])


colour_dic = OrderedDict(webcolors.css3_names_to_hex)
colour_dic.update(OrderedDict([('red', '#900000'),
                               ('blue', '#0066CC'),
                               ('green', '#339933'),
                               ('darkgreen', '#006400'),
                               ('orange', '#FF9933'),
                               ('yellow', '#DAA520'),
                               ('teal', '#008080'),
                               ('indigo', '#4B0082'),
                               ('ERY', '#CC0066'),
                               ('TEL', '#006600'),
                               ('control', '#000099')])
              )

colour_name_cycle = itertools.cycle(colour_dic)

_TC = namedtuple('TemporaryContainer', colour_dic.keys())
colours = _TC(*colour_dic.values())
