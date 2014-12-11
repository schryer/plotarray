# -*- coding: utf-8 -*-
"""
Attributes
==========

colour_name_cycle : itertools.cycle
    A cycle of colour names from colour_dic.

colour_dic : collections.OrderedDict
    A dictionary of colour names.
"""

from . core import retrieve_plot_data, save_plot_data, make_plot_array
from . structures import colour_name_cycle, colour_dic, colours
from . external import make_colour_map

__all__ = ['retrieve_plot_data', 'save_plot_data', 'make_plot_array', 'colours',
           'colour_name_cycle', 'colour_dic', 'make_colour_map']

