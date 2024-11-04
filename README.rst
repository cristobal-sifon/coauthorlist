coauthorlist.py
===============

A simple python script to deal with large co-author lists.

Specifically, ``coauthorlist.py`` will automatically sort co-authors alphabetically, possibly in a tiered scheme, and adjust affiliation numbering accordingly.

**NOTE:** *This code currently only produces A&A-compliant output.*

Installation
------------

Requirements
------------

**NOTE:** *Versions listed are the ones I have installed and therefore the only ones* ``coauthorlist.py`` *has been tested with. However, it is simple enough that it should work with any versions, at least reasonably recent ones.*

* Python 3.11.7 (requres Python 3.x)
* numpy 1.26.3
* pandas 2.2.3 
* openpyxl 3.1.5 (for Excel files)

Usage
-----

**NOTE:** ``coauthorlist.py`` *reads the co-author list from a table file. The easiest form to get this is to request your co-authors to fill a google form with the required information and then linking the form to a google sheet (upper right corner of the screen).*

Download ``coauthorlist.py`` to your desired location and execute

.. code-block::

    python coauthorlist.py -h

to get help about the optional command-line arguments. The output is copied here for convenience:

.. code-block::

    usage: coauthorlist.py [-h] [--alphabetical [ALPHABETICAL ...]] [--orcidlink] [--output OUTPUT] [--output-ack OUTPUT_ACK] filename
    
    positional arguments:
      filename              Input file with author data. Easiest to use are Excel and CSV files
    
    options:
      -h, --help            show this help message and exit
      --alphabetical [ALPHABETICAL ...], -a [ALPHABETICAL ...]
                            Which tiers to sort alphabetically,counting from 1. Negative numbers indicate which tiers *not* to sort
                            alphabetically. Default (-1) means to sort all tiers except the first.
      --orcidlink, -l       Use \orcidlink macro instead of custom \orcid macro
      --output OUTPUT, -o OUTPUT
                            filename to write author and affiliation lists (tex A&A format; default authors.tex)
      --output-ack OUTPUT_ACK, -k OUTPUT_ACK
                            filename to write acknowledgement list (default acknowledgements.tex)

Features
---------------

The author file should contain at least contain columns for:

 * **author name** including first and last names;
 * **affiliations** with multiple affiliations for the same author separated by semi-colons;
 * **acknowledgements** for each author. Currently this column must exist although it could be completely empty.

See `rename_columns()`_ for more information.

In addition, it is possible to have a ``Tier`` column to specify different author tiers; typically there is a first tier of authors sorted by contribution and one (or more) tiers of authors sorted alphabetically (see help above). Authors whose ``Tier`` column is set to 0 (zero) will not be included in the author list.

Modifying the source code
-------------------------

Some parts of the source code will have to be modified for every project. These can be found at the beginning of the source code:

``general_acknowledgements``
++++++++++++++++++++++++++++

This is a string containing acknowledgements that should go before the authors' individual (typically funding) acknowledgements.


``rename_columns()``
++++++++++++++++++++

This is a function to rename cumbersome column names to names that are easier to use within the code. I recommend changing the input names as needed (e.g., change "Latex-formatted name" to what you called the question in the form) but not the output names (e.g., leave "name"), as the latter are used throughout the code.

``format_affiliation()``
++++++++++++++++++++++++

This function allows custom formatting according to specific journal requirements, e.g. adding (or removing) the ``\affiliation`` macro.

``last_name_index()``
+++++++++++++++++++++

This function contains special rules to identify last names. In most cases last names are the last word, however this is not always the case: sometimes there is a compound last name, or a suffix, etc.

