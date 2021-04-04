# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from rdflib import Graph, Literal, URIRef, BNode
from rdflib.term import Identifier
from rdflib.namespace import NamespaceManager
import re

def to_graph(df: pd.DataFrame, namespace_manager: NamespaceManager = None) -> Graph:
    """
    Takes Pandas DataFrame and returns RDFLib Graph.
    Row indices are used as subjects and column indices as predicates. 
    Object types are inferred from the column index pattern of 
    "predicate{rdfLib Identifier instance class name}(type)[index]@language".
    Index numbers simply create additoinal statements as opposed 
    to attempting to construct a new rdfs:List or rdfs:Container.
    Namespaces need to be bound by the user of the method prior
    to serialization.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame to be converted into Graph.
    namespace_manager : rdflib.namespace.NamespaceManager
        NamespaceManager to use to normalize URIs

    Returns
    -------
    rdflib.Graph
        Graph created from Pandas DataFrame.

    """
    
    g = Graph(namespace_manager = namespace_manager)

    prefixes = {}
    for (prefix, namespace) in g.namespace_manager.namespaces():
        prefixes[prefix] = namespace

    for (index, series) in df.iterrows():
        for (column, value) in series.iteritems():
            # Matching unreserved, gen-delims and sub-delims with exception of "(", ")", "@", "[" and "]" from RFC 3986
            match = re.search('([\w\-._~:/?#!$&\'*+,;=]*)(\{(\w*)\})?(\[(\d*)\])?(\(([\w?:/.]*)\))?(@(\w*))?', column)
            if pd.notna(value) and pd.notnull(value):
                s = _get_identifier(prefixes, index)
                p = _get_identifier(prefixes, match.group(1))
                if isinstance(value, bytes):
                    o = _get_identifier(prefixes, value.decode('utf-8'), match.group(3), match.group(7), match.group(9))
                else:
                    o = _get_identifier(prefixes, value, match.group(3), match.group(7), match.group(9))
                g.add((s, p, o))

    return g


def to_dataframe(g: Graph) -> pd.DataFrame:
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
                idl = _get_idl_for_identifier(o)
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
                series_name = f'{_get_str_for_uriref(g.namespace_manager, p)}{{{instance}}}'
                if idl_len > 1:
                    series_name = ''.join([series_name, f'[{index}]'])
                if datatype:
                    series_name = ''.join([series_name, f'({_get_str_for_uriref(g.namespace_manager, datatype)})'])
                if language:
                    series_name = ''.join([series_name, f'@{language}'])
                p_subjects = []
                p_objects = []
                if idls_len == 1 and idl_len == 1:
                    for s, o in sorted(g.subject_objects(p)):
                        p_subjects.append(_get_str_for_uriref(g.namespace_manager, s))
                        if isinstance(o, Literal):
                            p_objects.append(str(o))
                        else:
                            p_objects.append(_get_str_for_uriref(g.namespace_manager, o))
                else:
                    s_index = 0
                    last_seen_subject = None
                    for s, o in sorted(g.subject_objects(p)):
                        if s != last_seen_subject:
                            s_index = 0
                        o_idl = _get_idl_for_identifier(o)
                        if o_idl == idl:
                            if s_index == index:
                                p_subjects.append(_get_str_for_uriref(g.namespace_manager, s))
                                if isinstance(o, Literal):
                                    p_objects.append(str(o))
                                else:
                                    p_objects.append(_get_str_for_uriref(g.namespace_manager, o))
                            s_index = s_index + 1
                        last_seen_subject = s
                series[series_name] = pd.Series(data = p_objects, index = p_subjects, dtype = np.unicode_)

    return pd.DataFrame(series)

def _get_identifier(prefixes: dict, value: object, instance: str = None, datatype: str = None, language: str = None) -> Identifier:
    """
    Takes value extracted from the index, column or cell and returns
    an instance of Identifier (Literal, URIRef or BNode) using correct 
    datatype and language.

    Parameters
    ----------
    prefixes : dict
        Prefixes to use to normalize URIs
    value : object
        Value of index, column or cell
    instance : str
        Name of the rdfLib Identifier class to use
    datatype : str
        Datatype of rdfLib Literal to use 
        (see https://rdflib.readthedocs.io/en/stable/rdf_terms.html#python-support)
    language : str
        Language of rdfLib Literal to use 

    Returns
    -------
    rdflib.term.Identifier
        rdflib.term.Identifier instance - either URIRef or Literal.

    """

    if not instance:
        if language:
            return Literal(value, lang = language)
        elif datatype:
            return Literal(value, datatype = URIRef(datatype))
        elif _is_uri(value):
            return URIRef(value)
        elif _is_curie(value):
            return _get_uriref_for_curie(prefixes, value)
        else:
            return Literal(value)
    elif instance == Literal.__name__:
        if language:
            return Literal(value, lang = language)
        elif datatype:
            if _is_uri(datatype):
                datatype_uriref = URIRef(datatype)
            elif _is_curie(datatype):
                datatype_uriref = _get_uriref_for_curie(prefixes, datatype)
            else:
                ValueError(f'Not a valid URI for datatype {datatype}')  
            return Literal(value, datatype = datatype_uriref)
        else:
            return Literal(value)
    elif instance == URIRef.__name__:
        if _is_uri(value):
            return URIRef(value)
        elif _is_curie(value):
            return _get_uriref_for_curie(prefixes, value)
        else:
            ValueError(f'Not a valid URI {value}')  
    elif instance == BNode.__name__:
        return BNode(value)

    raise ValueError(f'Can only create Literal, URIRef or BNode but was {instance}')

def _get_idl_for_identifier(i: Identifier) -> tuple:
    """
    Takes rdfLib Identifier, and returns a tuple of 
    instance name (Literal, URIRef or BNode), datatype (XSD type) and language.

    Parameters
    ----------
    i : rdflib.term.Identifier
        rdfLib Identifier (parent of BNode, Literal or URIRef).

    Returns
    -------
    tuple
        tuple of instance, datatype and language.

    """

    instance = i.__class__.__name__
    datatype = None
    language = None
    if isinstance(i, Literal):
        datatype = i.datatype
        language = i.language

    return (instance, datatype, language)

def _get_str_for_uriref(namespace_manager: NamespaceManager, uriref: URIRef) -> str:
    """
    Reusing NamespaceManager.normalizeUri for transforming Graph to DataFrame.
    In effect we only need to strip < and > from N3 representation and
    forget the case of URIRef being a rdflib.term.Variable.

    Parameters
    ----------
    namespace_manager : rdflib.namespace.NamespaceManager
        NamespaceManager to use to normalize URIs
    uriref : rdflib.URIRef
        URI to normalize

    Returns
    -------
    str
        Normalised URI string.

    """

    return re.sub('<|>', '', namespace_manager.normalizeUri(uriref))

def _get_uriref_for_curie(prefixes: dict, value: object) -> URIRef:
    """
    Converts curie string into URIRef with fully qualified URI.

    Parameters
    ----------
    prefixes : dict
        Prefixes to use to normalize URIs
    value : object
        Value from DataFrame to be converted to URIRef.

    Returns
    -------
    rdflib.URIRef
        URIRef created from the string.

    """

    prefix, name = value.split(':')
    if prefix in prefixes:
        return URIRef(''.join((prefixes[prefix], name)))
    else:
        return URIRef(value)

def _is_curie(value: object) -> bool:
    """
    Checks if value from DataFrame is a CURIE.

    Parameters
    ----------
    value : object
        Value from DataFrame to be checked.

    Returns
    -------
    bool
        True if value is matching CURIE pattern, false otherwise.

    """

    return re.match('^\w*:\w*$', str(value))

def _is_uri(value: object) -> bool:
    """
    Checks if value from DataFrame is a URI.

    Parameters
    ----------
    value : object
        Value from DataFrame to be checked.

    Returns
    -------
    bool
        True if value is matching URI pattern, false otherwise.

    """

    return re.match('^http[s]?://.*$', str(value))

