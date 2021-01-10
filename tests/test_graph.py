# -*- coding: utf-8 -*-

from .context import rdfpandas

import pandas as pd
import numpy as np

from rdflib import Graph, Literal, URIRef, BNode, Namespace
from rdflib.term import Identifier
from rdflib.namespace import NamespaceManager, SKOS, XSD
import rdflib.compare

import unittest


class ConversionTestCase(unittest.TestCase):
    """Tests conversion from DataFrame to Graph and from Graph to DataFrame"""

    def test_should_convert_empty_data_frame_to_empty_graph(self):
        """Should return empty Graph for empty DataFrame
        """

        df = pd.DataFrame()
        g_expected = Graph()
        g_result = rdfpandas.to_graph(df)

        self.assertEquals(rdflib.compare.isomorphic(g_expected, g_result), True)
    
    def test_should_convert_data_frame_to_graph_no_instance(self):
        """Should apply default types.
        """
        
        ds01 = pd.Series(data = ['Bytes'], index = ['http://github.com/cadmiumkitty/rdfpandas/one'], dtype = np.str_)

        ds02 = pd.Series(data = ['String'], index = ['http://github.com/cadmiumkitty/rdfpandas/one'], dtype = np.unicode_)

        ds03 = pd.Series(data = [0], index = ['http://github.com/cadmiumkitty/rdfpandas/one'], dtype = np.int64)
        ds04 = pd.Series(data = [-9223372036854775808], index = ['http://github.com/cadmiumkitty/rdfpandas/one'], dtype = np.int64)
        ds05 = pd.Series(data = [9223372036854775807], index = ['http://github.com/cadmiumkitty/rdfpandas/one'], dtype = np.int64)

        ds06 = pd.Series(data = [0], index = ['http://github.com/cadmiumkitty/rdfpandas/one'], dtype = np.uint64)
        ds07 = pd.Series(data = [18446744073709551615], index = ['http://github.com/cadmiumkitty/rdfpandas/one'], dtype = np.uint64)

        ds08 = pd.Series(data = [0.0], index = ['http://github.com/cadmiumkitty/rdfpandas/one'], dtype = np.float64)
        ds09 = pd.Series(data = [-1.7976931348623157e+308], index = ['http://github.com/cadmiumkitty/rdfpandas/one'], dtype = np.float64)
        ds10 = pd.Series(data = [1.7976931348623157e+308], index = ['http://github.com/cadmiumkitty/rdfpandas/one'], dtype = np.float64)

        ds11 = pd.Series(data = [True], index = ['http://github.com/cadmiumkitty/rdfpandas/one'], dtype = np.bool_)
        ds12 = pd.Series(data = [False], index = ['http://github.com/cadmiumkitty/rdfpandas/one'], dtype = np.bool_)

        ds13 = pd.Series(data = ['https://google.com'], index = ['http://github.com/cadmiumkitty/rdfpandas/one'], dtype = np.unicode_)
        ds14 = pd.Series(data = ['skos:broader'], index = ['http://github.com/cadmiumkitty/rdfpandas/one'], dtype = np.unicode_)

        df = pd.DataFrame({
            'http://github.com/cadmiumkitty/rdfpandas/stringu': ds01, 
            'http://github.com/cadmiumkitty/rdfpandas/unicodeu': ds02,
            'http://github.com/cadmiumkitty/rdfpandas/int64_1': ds03,
            'http://github.com/cadmiumkitty/rdfpandas/int64_2': ds04,
            'http://github.com/cadmiumkitty/rdfpandas/int64_3': ds05,
            'http://github.com/cadmiumkitty/rdfpandas/uint64_1': ds06,
            'http://github.com/cadmiumkitty/rdfpandas/uint64_2': ds07,
            'http://github.com/cadmiumkitty/rdfpandas/float64_1': ds08,
            'http://github.com/cadmiumkitty/rdfpandas/float64_2': ds09, 
            'http://github.com/cadmiumkitty/rdfpandas/float64_3': ds10, 
            'http://github.com/cadmiumkitty/rdfpandas/true': ds11,
            'http://github.com/cadmiumkitty/rdfpandas/false': ds12,
            'http://github.com/cadmiumkitty/rdfpandas/uri': ds13,
            'http://github.com/cadmiumkitty/rdfpandas/curie': ds14
            })
        
        g_expected = Graph()
        g_expected.add((URIRef('http://github.com/cadmiumkitty/rdfpandas/one'),
                        URIRef('http://github.com/cadmiumkitty/rdfpandas/stringu'), 
                        Literal('Bytes')))
        
        g_expected.add((URIRef('http://github.com/cadmiumkitty/rdfpandas/one'),
                        URIRef('http://github.com/cadmiumkitty/rdfpandas/unicodeu'), 
                        Literal('String')))
        
        g_expected.add((URIRef('http://github.com/cadmiumkitty/rdfpandas/one'),
                        URIRef('http://github.com/cadmiumkitty/rdfpandas/int64_1'), 
                        Literal(0)))
        g_expected.add((URIRef('http://github.com/cadmiumkitty/rdfpandas/one'),
                        URIRef('http://github.com/cadmiumkitty/rdfpandas/int64_2'), 
                        Literal(-9223372036854775808)))
        g_expected.add((URIRef('http://github.com/cadmiumkitty/rdfpandas/one'),
                        URIRef('http://github.com/cadmiumkitty/rdfpandas/int64_3'), 
                        Literal(9223372036854775807)))

        g_expected.add((URIRef('http://github.com/cadmiumkitty/rdfpandas/one'),
                        URIRef('http://github.com/cadmiumkitty/rdfpandas/uint64_1'), 
                        Literal(0)))
        g_expected.add((URIRef('http://github.com/cadmiumkitty/rdfpandas/one'),
                        URIRef('http://github.com/cadmiumkitty/rdfpandas/uint64_2'), 
                        Literal(18446744073709551615)))

        g_expected.add((URIRef('http://github.com/cadmiumkitty/rdfpandas/one'),
                        URIRef('http://github.com/cadmiumkitty/rdfpandas/float64_1'), 
                        Literal(0.0)))
        g_expected.add((URIRef('http://github.com/cadmiumkitty/rdfpandas/one'),
                        URIRef('http://github.com/cadmiumkitty/rdfpandas/float64_2'), 
                        Literal(-1.7976931348623157e+308)))
        g_expected.add((URIRef('http://github.com/cadmiumkitty/rdfpandas/one'),
                        URIRef('http://github.com/cadmiumkitty/rdfpandas/float64_3'), 
                        Literal(1.7976931348623157e+308)))
        
        g_expected.add((URIRef('http://github.com/cadmiumkitty/rdfpandas/one'),
                        URIRef('http://github.com/cadmiumkitty/rdfpandas/true'), 
                        Literal(True)))
        g_expected.add((URIRef('http://github.com/cadmiumkitty/rdfpandas/one'),
                        URIRef('http://github.com/cadmiumkitty/rdfpandas/false'), 
                        Literal(False)))

        g_expected.add((URIRef('http://github.com/cadmiumkitty/rdfpandas/one'),
                URIRef('http://github.com/cadmiumkitty/rdfpandas/uri'), 
                URIRef('https://google.com')))
        g_expected.add((URIRef('http://github.com/cadmiumkitty/rdfpandas/one'),
                URIRef('http://github.com/cadmiumkitty/rdfpandas/curie'), 
                URIRef('skos:broader')))
                
        g_result = rdfpandas.to_graph(df)

        for s, p, o in g_expected:
            print(s, p, o)

        print('===')

        for s, p, o in g_result:
            print(s, p, o)

        self.assertEquals(rdflib.compare.isomorphic(g_expected, g_result), True)

    def test_should_convert_data_frame_to_graph_literal(self):
        """Should create triples based on Literal instance type, datatype and 
        language provided.
        """
        
        ds01 = pd.Series(data = ['String'], index = ['http://github.com/cadmiumkitty/rdfpandas/one'], dtype = np.unicode_)
        ds02 = pd.Series(data = ['String with type only'], index = ['http://github.com/cadmiumkitty/rdfpandas/one'], dtype = np.unicode_)
        ds03 = pd.Series(data = ['String with language only in Nepali'], index = ['http://github.com/cadmiumkitty/rdfpandas/one'], dtype = np.unicode_)
        ds04 = pd.Series(data = ['String In English 1'], index = ['http://github.com/cadmiumkitty/rdfpandas/one'], dtype = np.unicode_)
        ds05 = pd.Series(data = ['String In English 2'], index = ['http://github.com/cadmiumkitty/rdfpandas/one'], dtype = np.unicode_)

        df = pd.DataFrame({
            'http://github.com/cadmiumkitty/rdfpandas/string{Literal}': ds01,
            'http://github.com/cadmiumkitty/rdfpandas/string{Literal}(xsd:string)': ds02,
            'http://github.com/cadmiumkitty/rdfpandas/string{Literal}@ne': ds03,
            'http://github.com/cadmiumkitty/rdfpandas/string{Literal}[0]@en': ds04,
            'http://github.com/cadmiumkitty/rdfpandas/string{Literal}[1]@en': ds05
            })
        
        g_expected = Graph()

        g_expected.add((URIRef('http://github.com/cadmiumkitty/rdfpandas/one'),
                        URIRef('http://github.com/cadmiumkitty/rdfpandas/string'),
                        Literal('String')))
        g_expected.add((URIRef('http://github.com/cadmiumkitty/rdfpandas/one'),
                        URIRef('http://github.com/cadmiumkitty/rdfpandas/string'),
                        Literal('String with type only', datatype = XSD.string)))
        g_expected.add((URIRef('http://github.com/cadmiumkitty/rdfpandas/one'),
                        URIRef('http://github.com/cadmiumkitty/rdfpandas/string'),
                        Literal('String with language only in Nepali', lang = 'ne')))
        g_expected.add((URIRef('http://github.com/cadmiumkitty/rdfpandas/one'),
                        URIRef('http://github.com/cadmiumkitty/rdfpandas/string'),
                        Literal('String In English 1', lang = 'en')))
        g_expected.add((URIRef('http://github.com/cadmiumkitty/rdfpandas/one'),
                        URIRef('http://github.com/cadmiumkitty/rdfpandas/string'),
                        Literal('String In English 2', lang = 'en')))
                
        g_result = rdfpandas.to_graph(df)
        
        self.assertEquals(rdflib.compare.isomorphic(g_expected, g_result), True)

    def test_should_convert_data_frame_to_graph_uriref(self):
        """Should create triples based on URIRef instance type.
        """
        
        ds1 = pd.Series(data=['https://google.com'], index = ['http://github.com/cadmiumkitty/rdfpandas/one'], dtype = np.unicode_)
        ds2 = pd.Series(data=['skos:broader'], index = ['http://github.com/cadmiumkitty/rdfpandas/one'], dtype = np.unicode_)

        df = pd.DataFrame({
            'http://github.com/cadmiumkitty/rdfpandas/uri{URIRef}': ds1,
            'http://github.com/cadmiumkitty/rdfpandas/curie{URIRef}': ds2
            })
        
        g_expected = Graph()
        
        g_expected.add((URIRef('http://github.com/cadmiumkitty/rdfpandas/one'),
                URIRef('http://github.com/cadmiumkitty/rdfpandas/uri'), 
                URIRef('https://google.com')))
        g_expected.add((URIRef('http://github.com/cadmiumkitty/rdfpandas/one'),
                URIRef('http://github.com/cadmiumkitty/rdfpandas/curie'), 
                URIRef('skos:broader')))
                
        g_result = rdfpandas.to_graph(df)
        
        self.assertEquals(rdflib.compare.isomorphic(g_expected, g_result), True)

    def test_should_convert_data_frame_to_graph_bnode(self):
        """Should create triples based on BNode instance type.
        """
        
        ds1 = pd.Series(data=['ub1bL39C14'], index = ['http://github.com/cadmiumkitty/rdfpandas/one'], dtype = np.unicode_)

        df = pd.DataFrame({
            'http://github.com/cadmiumkitty/rdfpandas/bnode{BNode}': ds1,
            })
        
        g_expected = Graph()
        
        g_expected.add((URIRef('http://github.com/cadmiumkitty/rdfpandas/one'),
                URIRef('http://github.com/cadmiumkitty/rdfpandas/bnode'), 
                BNode('ub1bL39C14')))
                
        g_result = rdfpandas.to_graph(df)
        
        self.assertEquals(rdflib.compare.isomorphic(g_expected, g_result), True)        


    def test_should_convert_empty_graph_to_empty_data_frame(self):
        """Should return empty DataFrame for empty Graph
        """

        g = Graph()
        df_result = rdfpandas.to_dataframe(g)

        self.assertEquals(df_result.empty, True)


    def test_should_convert_graph_to_data_frame(self):
        """Should return DataFrame for Graph
        """

        g = Graph()

        g.add((URIRef('http://github.com/cadmiumkitty/rdfpandas/one'),
                        URIRef('http://github.com/cadmiumkitty/rdfpandas/string'), 
                        Literal('String 1')))
        g.add((URIRef('http://github.com/cadmiumkitty/rdfpandas/one'),
                        URIRef('http://github.com/cadmiumkitty/rdfpandas/string'), 
                        Literal('String with type 1 (1)', datatype = URIRef('xsd:string'))))
        g.add((URIRef('http://github.com/cadmiumkitty/rdfpandas/one'),
                        URIRef('http://github.com/cadmiumkitty/rdfpandas/string'), 
                        Literal('String with type 2 (1)', datatype = URIRef('xsd:string'))))
        g.add((URIRef('http://github.com/cadmiumkitty/rdfpandas/one'),
                        URIRef('http://github.com/cadmiumkitty/rdfpandas/string'), 
                        Literal('String in Nepali 1 (1)', lang = 'ne')))
        g.add((URIRef('http://github.com/cadmiumkitty/rdfpandas/one'),
                        URIRef('http://github.com/cadmiumkitty/rdfpandas/string'), 
                        Literal('String in English 1 (1)', lang = 'en')))
        g.add((URIRef('http://github.com/cadmiumkitty/rdfpandas/one'),
                        URIRef('http://github.com/cadmiumkitty/rdfpandas/string'), 
                        Literal('String in English 2 (1)', lang = 'en')))
        g.add((URIRef('http://github.com/cadmiumkitty/rdfpandas/one'),
                        URIRef('http://github.com/cadmiumkitty/rdfpandas/string'), 
                        Literal('String in Russian 1 (1)', lang = 'ru')))

        g.add((URIRef('http://github.com/cadmiumkitty/rdfpandas/one'),
                        URIRef('http://github.com/cadmiumkitty/rdfpandas/integer'), 
                        Literal(10)))
        g.add((URIRef('http://github.com/cadmiumkitty/rdfpandas/one'),
                        URIRef('http://github.com/cadmiumkitty/rdfpandas/double'), 
                        Literal(10.0)))

        g.add((URIRef('http://github.com/cadmiumkitty/rdfpandas/one'),
                URIRef('http://github.com/cadmiumkitty/rdfpandas/uri'), 
                URIRef('https://google.com')))
        g.add((URIRef('http://github.com/cadmiumkitty/rdfpandas/one'),
                URIRef('http://github.com/cadmiumkitty/rdfpandas/curie'), 
                URIRef('skos:broader')))

        g.add((URIRef('http://github.com/cadmiumkitty/rdfpandas/one'),
                URIRef('http://github.com/cadmiumkitty/rdfpandas/bnode'), 
                BNode('12345')))

        g.add((URIRef('http://github.com/cadmiumkitty/rdfpandas/two'),
                        URIRef('http://github.com/cadmiumkitty/rdfpandas/anotherstring'), 
                        Literal('String 2')))
        g.add((URIRef('http://github.com/cadmiumkitty/rdfpandas/two'),
                        URIRef('http://github.com/cadmiumkitty/rdfpandas/string'), 
                        Literal('String with type 1 (2)', datatype = URIRef('xsd:string'))))
        g.add((URIRef('http://github.com/cadmiumkitty/rdfpandas/two'),
                        URIRef('http://github.com/cadmiumkitty/rdfpandas/string'), 
                        Literal('String with type 2 (2)', datatype = URIRef('xsd:string'))))
        g.add((URIRef('http://github.com/cadmiumkitty/rdfpandas/two'),
                        URIRef('http://github.com/cadmiumkitty/rdfpandas/string'), 
                        Literal('String in Nepali 1 (2)', lang = 'ne')))
        g.add((URIRef('http://github.com/cadmiumkitty/rdfpandas/two'),
                        URIRef('http://github.com/cadmiumkitty/rdfpandas/string'), 
                        Literal('String in Nepali 2 (2)', lang = 'ne')))
        g.add((URIRef('http://github.com/cadmiumkitty/rdfpandas/two'),
                        URIRef('http://github.com/cadmiumkitty/rdfpandas/string'), 
                        Literal('String in English 1 (2)', lang = 'en')))

        ds01 = pd.Series(data = ['String 1'], index = ['http://github.com/cadmiumkitty/rdfpandas/one'], dtype = np.unicode_)
        ds02 = pd.Series(data = ['String 2'], index = ['http://github.com/cadmiumkitty/rdfpandas/two'], dtype = np.unicode_)
        ds03 = pd.Series(data = ['String with type 1 (1)', 'String with type 1 (2)'], index = ['http://github.com/cadmiumkitty/rdfpandas/one', 'http://github.com/cadmiumkitty/rdfpandas/two'], dtype = np.unicode_)
        ds04 = pd.Series(data = ['String with type 2 (1)', 'String with type 2 (2)'], index = ['http://github.com/cadmiumkitty/rdfpandas/one', 'http://github.com/cadmiumkitty/rdfpandas/two'], dtype = np.unicode_)
        ds05 = pd.Series(data = ['String in Nepali 1 (1)', 'String in Nepali 1 (2)'], index = ['http://github.com/cadmiumkitty/rdfpandas/one', 'http://github.com/cadmiumkitty/rdfpandas/two'], dtype = np.unicode_)
        ds06 = pd.Series(data = ['String in Nepali 2 (2)'], index = ['http://github.com/cadmiumkitty/rdfpandas/two'], dtype = np.unicode_)
        ds07 = pd.Series(data = ['String in English 1 (1)', 'String in English 1 (2)'], index = ['http://github.com/cadmiumkitty/rdfpandas/one', 'http://github.com/cadmiumkitty/rdfpandas/two'], dtype = np.unicode_)
        ds08 = pd.Series(data = ['String in English 2 (1)'], index = ['http://github.com/cadmiumkitty/rdfpandas/one'], dtype = np.unicode_)
        ds09 = pd.Series(data = ['String in Russian 1 (1)'], index = ['http://github.com/cadmiumkitty/rdfpandas/one'], dtype = np.unicode_)
        ds10 = pd.Series(data = ['10'], index = ['http://github.com/cadmiumkitty/rdfpandas/one'], dtype = np.unicode_)
        ds11 = pd.Series(data = ['10.0'], index = ['http://github.com/cadmiumkitty/rdfpandas/one'], dtype = np.unicode_)
        ds12 = pd.Series(data = ['https://google.com'], index = ['http://github.com/cadmiumkitty/rdfpandas/one'], dtype = np.unicode_)
        ds13 = pd.Series(data = ['skos:broader'], index = ['http://github.com/cadmiumkitty/rdfpandas/one'], dtype = np.unicode_)
        ds14 = pd.Series(data = ['12345'], index = ['http://github.com/cadmiumkitty/rdfpandas/one'], dtype = np.unicode_)

        df_expected = pd.DataFrame({
            'http://github.com/cadmiumkitty/rdfpandas/string{Literal}': ds01,
            'http://github.com/cadmiumkitty/rdfpandas/anotherstring{Literal}': ds02,
            'http://github.com/cadmiumkitty/rdfpandas/string{Literal}[0](xsd:string)': ds03,
            'http://github.com/cadmiumkitty/rdfpandas/string{Literal}[1](xsd:string)': ds04,
            'http://github.com/cadmiumkitty/rdfpandas/string{Literal}[0]@ne': ds05,
            'http://github.com/cadmiumkitty/rdfpandas/string{Literal}[1]@ne': ds06,
            'http://github.com/cadmiumkitty/rdfpandas/string{Literal}[0]@en': ds07,
            'http://github.com/cadmiumkitty/rdfpandas/string{Literal}[1]@en': ds08,
            'http://github.com/cadmiumkitty/rdfpandas/string{Literal}@ru': ds09,
            'http://github.com/cadmiumkitty/rdfpandas/integer{Literal}(xsd:integer)': ds10,
            'http://github.com/cadmiumkitty/rdfpandas/double{Literal}(xsd:double)': ds11,
            'http://github.com/cadmiumkitty/rdfpandas/uri{URIRef}': ds12,
            'http://github.com/cadmiumkitty/rdfpandas/curie{URIRef}': ds13,
            'http://github.com/cadmiumkitty/rdfpandas/bnode{BNode}': ds14
            })

        df_result = rdfpandas.to_dataframe(g)

        pd.testing.assert_frame_equal(df_expected, df_result, check_like = True)


    def test_should_roundtrip_csv_to_graph_to_csv(self):
        """Should roundtrip DF -> Graph -> DF
        """

        df = pd.read_csv('./csv/test.csv', index_col = '@id', keep_default_na = True)
        namespace_manager = NamespaceManager(Graph())
        namespace_manager.bind('skos', SKOS)
        namespace_manager.bind('rdfpandas', Namespace('http://github.com/cadmiumkitty/rdfpandas/'))
        g = rdfpandas.to_graph(df, namespace_manager)
        df_result = rdfpandas.to_dataframe(g)

        pd.testing.assert_frame_equal(df.astype(np.unicode_), df_result.astype(np.unicode_), check_like = True, check_names = False)


    def test_should_roundtrip_graph_to_csv_to_graph(self):
        """Should roundtrip Graph -> DF -> Graph
        """

        g = rdflib.Graph()
        g.parse('./rdf/test.ttl', format = 'ttl')
        df = rdfpandas.to_dataframe(g)
        print(df.T)
        g_result = rdfpandas.to_graph(df, g.namespace_manager)
        self.assertEquals(rdflib.compare.isomorphic(g, g_result), True)


if __name__ == '__main__':
    unittest.main()