# -*- coding: utf-8 -*-
import pandas as pd
import rdflib
import logging


def to_graph(df: pd.DataFrame) -> rdflib.Graph:
    """
    Takes Pandas DataFrame and returns RDFLib Graph using row indices as subjects
    and column indices as predictes. Object types are inferred from the Series 
    content type.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame to be converted into Graph.

    Returns
    -------
    rdflib.Graph
        Graph created from Pandas DataFrame

    """
    
    g = rdflib.Graph()
    
    for (index, series) in df.iterrows():
        for (column, value) in series.iteritems():
            if (type(value) == 'bytes'):
                g.add((rdflib.URIRef(index),
                       rdflib.URIRef(column), 
                       rdflib.Literal(value.decode('utf-8'))))
            else:
                g.add((rdflib.URIRef(index),
                       rdflib.URIRef(column), 
                       rdflib.Literal(value)))
        
    return g
