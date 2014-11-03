import numpy

from plotarray import make_plot_array

def test_hinton():

    plot_data = dict(TEST=dict(matrix=numpy.array([[1,2,3], [4,5,6], [7,8,9]])))

    plot_info = {'shape':(1,1),
                 'figsize':(8,8),
                 'title':'Hinton plot test',
                 'topspace':0.96,
                 ((0,0),1,1):dict(mpl=dict(title='Hinton test subplot',
                                           xlabel='Column',
                                           ylabel='Row',
                                       ),
                                  series=dict(TEST='green')
                                  type='hinton',
                          ),
             }

    make_plot_array(plot_data, plot_info, 'hinton_test_A.pdf')   