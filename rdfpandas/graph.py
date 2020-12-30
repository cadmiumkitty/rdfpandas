# -*- coding: utf-8 -*-
import pandas as pd
import rdflib
import rdflib.namespace
import logging

def to_graph(df: pd.DataFrame, prefixes: dict) -> rdflib.Graph:
    """
    Takes Pandas DataFrame and returns RDFLib Graph.
    Row indices are used as subjects and column indices as predicates. 
    Object types are inferred from the column index pattern of 
    "predicate{rdfLib Identifier instance class name}(type)[index]@language".
    Index numbers simply create additoinal statements as opposed 
    to attempting to construct a new rdfs:List or rdfs:Container.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame to be converted into Graph.
    prefixes : dict
        Dictionary of prefixes to be used for CURIE deconstruction.
        for example {'skos': 'http://www.w3.org/2004/02/skos/core#'}
        or alternatively {'skos': rdflib.namespace.SKOS.uri}

    Returns
    -------
    rdflib.Graph
        Graph created from Pandas DataFrame.

    """
    
    g = rdflib.Graph()
    
    for (index, series) in df.iterrows():
        for (column, value) in series.iteritems():

            ## Parse column

            ## If value

                ## Get URI Node for index
                ## Get URI Node for column name
                ## If column has language => check if type is string or missing => Literal string with language
                ## Else If column has type => Literal with type
                ## Else If Get URI Node for value => URI
                ## Else => Literal with defaults

            if (type(value) == 'bytes'):
                g.add((rdflib.URIRef(index),
                       rdflib.URIRef(column), 
                       rdflib.Literal(value.decode('utf-8'))))
            else:
                g.add((rdflib.URIRef(index),
                       rdflib.URIRef(column), 
                       rdflib.Literal(value)))
        
    return g

def to_dataframe(g: rdflib.Graph) -> df: pd.DataFrame:
    """
    Takes rdfLib Graph object and creates Pandas DataFrame.
    Indices are subjects and attempt is made to construct CURIEs
    using namespace manager of the rdfLib Graph.
    Columns are predicates and attempt is made to construct CURIEs
    using namespace manager of the rdfLib Graph, similar to indices.
    Column names are created using 
    "predicate{rdfLib Identifier instance class name}(type)[index]@language"
    pattern to allow for round trip conversion.
    Multiple objects for the same subject and predicate
    result in columns with index in its name.
    No attemps are made at type conversion, all objects are strings in the
    DataFrame.

    Parameters
    ----------
    g : rdflib.Graph
        rdfLib Graph.

    Returns
    -------
    pd.DataFrame
        Pandas DataFrame created from rdfLib Graph.

    """

    subjects = {}
    predicates = {}

    for s in g.subjects():
        if s not in subjects:
            subjects[s] = s
            s_predicates = {}
            for p, o in sorted(g.predicate_objects(s)):
                idl = _idl_for_identifier(o)
                if p in s_predicates:
                    if idl in s_predicates[p]:
                        s_predicates[p][idl] = s_predicates[p][idl] + 1
                    else:
                        s_predicates[p][idl] = 1
                else:
                    s_predicates[p] = {idl: 1}
            for p in s_predicates:
                if p in predicates:
                    for idl in s_predicates[p]:
                        if idl in predicates[p]:
                            predicates[p][idl] = max(s_predicates[p][idl], predicates[p][idl])
                        else:
                            predicates[p][idl] = s_predicates[p][idl]
                else:
                    predicates[p] = s_predicates[p]

    series = {}

    for p in predicates:
        idls_len = len(predicates[p])
        for idl in predicates[p]:
            instance = idl[0]
            datatype = idl[1]
            language = idl[2]
            idl_len = predicates[p][idl]
            for index in range(idl_len):
                series_name = f'{g.namespace_manager.normalizeUri(p)}{{{instance}}}'
                if idl_len > 1:
                    series_name = ''.join([series_name, f'[{index}]'])
                if datatype:
                    series_name = ''.join([series_name, f'({g.namespace_manager.normalizeUri(datatype)})'])
                if language:
                    series_name = ''.join([series_name, f'@{language}'])
                p_subjects = []
                p_objects = []
                if idls_len == 1 and idl_len == 1:
                    for s, o in sorted(g.subject_objects(p)):
                        p_subjects.append(g.namespace_manager.normalizeUri(s))
                        if isinstance(o, rdflib.Literal):
                            p_objects.append(o)
                        else:
                            p_objects.append(g.namespace_manager.normalizeUri(o))
                else:
                    s_index = 0
                    last_seen_subject = None
                    for s, o in sorted(g.subject_objects(p)):
                        if last_seen_subject and s != last_seen_subject:
                            s_index = 0
                        o_idl = _idl_for_identifier(o)
                        if o_idl == idl:
                            if s_index == index:
                                p_subjects.append(g.namespace_manager.normalizeUri(s))
                                if isinstance(o, rdflib.Literal):
                                    p_objects.append(o)
                                else:
                                    p_objects.append(g.namespace_manager.normalizeUri(o))
                                last_seen_subject = s
                            s_index = s_index + 1
                series[series_name] = pd.Series(p_objects, p_subjects, 'string')

    df = pd.DataFrame(series)

    return pd.DataFrame(series)


def _idl_for_identifier(o: rdflib.term.Identifier) -> tuple:
    """
    Takes rdfLib Identifier, a parent of Literal and URIRef, and returns
    a tuple of instance name (Literal, URIRef or BNode), datatype (URIRef of 
    XSD type) and language.

    Parameters
    ----------
    o : rdflib.term.Identifier
        rdfLib Identifier (parent of BNode, Literal or URIRef).

    Returns
    -------
    tuple
        tuple of instance, datatype and language.

    """

    instance = o.__class__.__name__
    datatype = None
    language = None
    if isinstance(o, rdflib.Literal):
        datatype = o.datatype
        language = o.language

    return (instance, datatype, language)
