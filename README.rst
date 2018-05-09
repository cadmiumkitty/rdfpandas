RdfPandas
=========

RdfPandas is a module providing RDF support for Pandas. It consists initially 
of a simple function for graph conversion to create RDFLib Graph data from 
Pandas DataFrame.

The graph data can then be serialized using RDFLib serialize method on the 
graph.

Getting Started
---------------

For more information about Resource Description Framework (RDF) and Pandas see:

- RDF: https://www.w3.org/RDF/
- Pandas: https://pandas.pydata.org/

Prerequisites
-------------

You will need Python 3 to use Pandas and RdfPandas.

Installation
------------

::

  pip install rdfpandas

Usage
-----

Getting RDF out of the DataFrame
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

  import rdfpandas as pd
  import rdflib
  
  df = pd.DataFrame()
  g = to_graph(df)
  s = g.serialize(format='turtle')
