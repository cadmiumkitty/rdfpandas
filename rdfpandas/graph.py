# -*- coding: utf-8 -*-
import pandas as pd
import rdflib

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
    
    return g

def from_graph(g: rdflib.Graph) -> pd.DataFrame:
    """
    Takes RDFLib Graph and returns Pandas DataFrame using subjects as row 
    indices and predicates as column indices. Object types are inferred from 
    the object types.

    Parameters
    ----------
    g : rdflib.Graph
        Graph to be converted into Pandas DataFrame

    Returns
    -------
    pandas.DataFrame
        DataFrame created from Graph.
        
    """
    
    df = pd.DataFrame()
    
    return df
