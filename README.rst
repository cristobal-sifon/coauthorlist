coauthorlist.py
===============

A simple python script to deal with large co-author lists

.. note::

    This code currently only produces A&A-compliant output

Installation
------------

Requirements
------------

.. note::

    Versions listed are the ones I have installed and therefore the only ones ``coauthorlist.py`` hass been tested with. However, it is simple enough that it should work with any versions, at least reasonably recent ones.

* Python 3.11.7 (requres Python 3.x)
* numpy 1.26.3
* pandas 2.2.3 
* openpyxl 3.1.5 (for Excel files)

Usage
-----

.. note::

    ``coauthorlist.py`` reads the co-author list from a table file. The easiest form to get this is to request your co-authors to fill a google form with the required information and then linking the form to a google sheet (upper right corner of the screen). 

Download ``coauthorlist.py`` to your desired location and execute

.. code-block::

    python coauthorlist.py -h

to get help about the optional command-line arguments. 

Features
---------------

The author file should contain at least contain columns for:

 * **author name** including first and last names;
 * **affiliations** with multiple affiliations for the same author separated by semi-colons;
 * **acknowledgements** for each author. Currently this column must exist although it could be completely empty.

See :ref:`renamecols` for more information.

In addition, it is possible to have a ``Tier`` column to specify different author tiers; typically there is a first tier of authors sorted by contribution and one (or more) tiers of authors sorted alphabetically. Run :code:`python coauthorlist.py -h` for more information.

Modifying the source code
-------------------------

Some parts of the source code will have to be modified for every project. These can be found at the beginning of the source code:

``general_acknowledgements``
++++++++++++++++++++++++++++

This is a string containing acknowledgements that should go before the authors' individual (typically funding) acknowledgements.

.. _renamecols:

``rename_columns()``
++++++++++++++++++++

This is a function to rename cumbersome column names to names that are easier to use within the code. I recommend changing the input names as needed (e.g., change "Latex-formatted name" to what you called the question in the form) but not the output names (e.g., leave "name"), as the latter are used throughout the code.

``format_affiliation()``

This function allows custom formatting according to specific journal requirements, e.g. adding (or removing) the ``\affiliation`` macro.

``last_name_index()``
+++++++++++++++++++++

This function contains special rules to identify last names. In most cases last names are the last word, however this is not always the case: sometimes there is a compound last name, or a suffix, etc.

