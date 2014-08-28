.. plotarray documentation master file, created by
   sphinx-quickstart on Wed Aug 27 21:05:56 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

plotarray documentation
=======================

.. toctree::
   :maxdepth: 2

|  The plotarray package tries to separate plot data from the representation 
|  of a plot. All plots are made by passing the data and a dictionary specifying 
|  how it should be represented to a single function :func:`plotarray.make_plot_array`.

|  To speed up plotting large amounts of data, two convenience functions have 
|  been included to save and retrieve data from **HDF5** files using the h5py_ 
|  package (:func:`plotarray.save_plot_data` and :func:`plotarray.retrieve_plot_data`).


.. _h5py: http://www.h5py.org/

.. |br| raw:: html

   <br />

.. autofunction:: plotarray.make_plot_array

.. autofunction:: plotarray.save_plot_data

.. autofunction:: plotarray.retrieve_plot_data

.. automodule:: plotarray


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

