RdfPandas
=========

RdfPandas is a module providing RDF support for Pandas. It consists of
two simple functions for Graph to DataFrame conversion and 
DataFrame to Graph conversion.

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

Creating RDF from the DataFrame
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

  import rdfpandas.graph
  import pandas as pd
  import rdflib
 
  df = pd.read_csv('to_graph_test.csv', index_col = '@id', keep_default_na = False)
  g = to_graph(df)
  s = g.serialize(format='turtle')

Creating DataFrame from RDF
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

  import rdfpandas.graph
  import pandas as pd
  import rdflib
 
  g = rdflib.Graph()
  g.parse('to_df_test.ttl', format = 'ttl')
  df = to_dataframe(g)  
  df.to_csv('test.csv', index = True, index_label = "@id")

Gotchas
-------

No special effort is made for dealing with types, so please be aware of Pandas
features such as https://pandas.pydata.org/pandas-docs/stable/user_guide/gotchas.html#support-for-integer-na
that may result in surprising RDF statements like ``"10.0"^^<xsd:integer>``.
