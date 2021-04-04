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

Creating RDF from DataFrame
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

As of version 1.1.0 NamespaceManager can be supplied to ``rdflib.to_graph`` for conversion to Graph.

::

  from rdfpandas.graph import to_graph
  import pandas as pd
  import rdflib
 
  df = pd.read_csv('to_graph_test.csv', index_col = '@id', keep_default_na = False)
  namespace_manager = NamespaceManager(Graph())
  namespace_manager.bind('skos', SKOS)
  namespace_manager.bind('rdfpandas', Namespace('http://github.com/cadmiumkitty/rdfpandas/'))
  g = to_graph(df, namespace_manager)
  s = g.serialize(format = 'turtle')

Creating DataFrame from RDF
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

  from rdfpandas.graph import to_dataframe
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
