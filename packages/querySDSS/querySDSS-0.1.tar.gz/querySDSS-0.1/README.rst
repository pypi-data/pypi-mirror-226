

 querySDSS
===============
This is a python script that queries the latest realease from SDSS and returns a table with cotaining all observations 
of 'spaceobjid', 'z', 'rec', 'dec', 'flux_i', 'flux_u','flux_r','flux_g', 'flux_z'

Installing
============

.. code-block:: bash

    pip install querySDSS

Usage
=====

.. code-block:: bash

    >>> from querySDSS import query_sdss_data
    >>> query_sdss_data()
    

The result is a table containing the data associated.
