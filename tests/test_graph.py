# -*- coding: utf-8 -*-

from .context import rdfpandas

import pandas as pd
import numpy as np
import rdflib
import rdflib.compare
import rdflib.namespace

import unittest
import logging


class ConversionTestCase(unittest.TestCase):
    """Tests conversion from DataFrame to Graph."""

    def test_should_convert_empty_data_frame_to_empty_graph(self):
        """Should return empty Graph for empty DataFrame
        """
        df = pd.DataFrame()
        g_expected = rdflib.Graph()
        g_result = rdfpandas.to_graph(df)
        self.assertEquals(rdflib.compare.isomorphic(g_expected, g_result), True)
    
    def test_should_convert_data_frame_to_graph_no_instance(self):
        """Should apply default types.
        """
        
        idx1= pd.Index(data=['http://github.com/cadmiumkitty/rdfpandas/one'])

        ds01 = pd.Series(data=['Bytes'], index=[idx1], dtype = np.string_)

        ds02 = pd.Series(data=['String'], index=[idx1], dtype = np.unicode_)

        ds03 = pd.Series(data=[0], index=[idx1], dtype = np.int64)
        ds04 = pd.Series(data=[-9223372036854775808], index=[idx1], dtype = np.int64)
        ds05 = pd.Series(data=[9223372036854775807], index=[idx1], dtype = np.int64)

        ds06 = pd.Series(data=[0], index=[idx1], dtype = np.uint64)
        ds07 = pd.Series(data=[18446744073709551615], index=[idx1], dtype = np.uint64)

        ds08 = pd.Series(data=[0.0], index=[idx1], dtype = np.float64)
        ds09 = pd.Series(data=[-1.7976931348623157e+308], index=[idx1], dtype = np.float64)
        ds10 = pd.Series(data=[1.7976931348623157e+308], index=[idx1], dtype = np.float64)

        ds11 = pd.Series(data=[True], index=[idx1], dtype = np.bool_)
        ds12 = pd.Series(data=[False], index=[idx1], dtype = np.bool_)

        ds13 = pd.Series(data=['http://github.com/cadmiumkitty/rdfpandas/uri'], index=[idx1], dtype = np.string_)
        ds14 = pd.Series(data=['rdfpandas:curie'], index=[idx1], dtype = np.string_)

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
        
        g_expected = rdflib.Graph()
        g_expected.add((rdflib.URIRef('http://github.com/cadmiumkitty/rdfpandas/one'),
                        rdflib.URIRef('http://github.com/cadmiumkitty/rdfpandas/stringu'), 
                        rdflib.Literal('Bytes')))
        
        g_expected.add((rdflib.URIRef('http://github.com/cadmiumkitty/rdfpandas/one'),
                        rdflib.URIRef('http://github.com/cadmiumkitty/rdfpandas/unicodeu'), 
                        rdflib.Literal('String')))
        
        g_expected.add((rdflib.URIRef('http://github.com/cadmiumkitty/rdfpandas/one'),
                        rdflib.URIRef('http://github.com/cadmiumkitty/rdfpandas/int64_1'), 
                        rdflib.Literal(0)))
        g_expected.add((rdflib.URIRef('http://github.com/cadmiumkitty/rdfpandas/one'),
                        rdflib.URIRef('http://github.com/cadmiumkitty/rdfpandas/int64_2'), 
                        rdflib.Literal(-9223372036854775808)))
        g_expected.add((rdflib.URIRef('http://github.com/cadmiumkitty/rdfpandas/one'),
                        rdflib.URIRef('http://github.com/cadmiumkitty/rdfpandas/int64_3'), 
                        rdflib.Literal(9223372036854775807)))

        g_expected.add((rdflib.URIRef('http://github.com/cadmiumkitty/rdfpandas/one'),
                        rdflib.URIRef('http://github.com/cadmiumkitty/rdfpandas/uint64_1'), 
                        rdflib.Literal(0)))
        g_expected.add((rdflib.URIRef('http://github.com/cadmiumkitty/rdfpandas/one'),
                        rdflib.URIRef('http://github.com/cadmiumkitty/rdfpandas/uint64_2'), 
                        rdflib.Literal(18446744073709551615)))

        g_expected.add((rdflib.URIRef('http://github.com/cadmiumkitty/rdfpandas/one'),
                        rdflib.URIRef('http://github.com/cadmiumkitty/rdfpandas/float64_1'), 
                        rdflib.Literal(0.0)))
        g_expected.add((rdflib.URIRef('http://github.com/cadmiumkitty/rdfpandas/one'),
                        rdflib.URIRef('http://github.com/cadmiumkitty/rdfpandas/float64_2'), 
                        rdflib.Literal(-1.7976931348623157e+308)))
        g_expected.add((rdflib.URIRef('http://github.com/cadmiumkitty/rdfpandas/one'),
                        rdflib.URIRef('http://github.com/cadmiumkitty/rdfpandas/float64_3'), 
                        rdflib.Literal(1.7976931348623157e+308)))
        
        g_expected.add((rdflib.URIRef('http://github.com/cadmiumkitty/rdfpandas/one'),
                        rdflib.URIRef('http://github.com/cadmiumkitty/rdfpandas/true'), 
                        rdflib.Literal(True)))
        g_expected.add((rdflib.URIRef('http://github.com/cadmiumkitty/rdfpandas/one'),
                        rdflib.URIRef('http://github.com/cadmiumkitty/rdfpandas/false'), 
                        rdflib.Literal(False)))

        g_expected.add((rdflib.URIRef('http://github.com/cadmiumkitty/rdfpandas/one'),
                rdflib.URIRef('http://github.com/cadmiumkitty/rdfpandas/uri'), 
                rdflib.URIRef('http://github.com/cadmiumkitty/rdfpandas/uri')))
        g_expected.add((rdflib.URIRef('http://github.com/cadmiumkitty/rdfpandas/one'),
                rdflib.URIRef('http://github.com/cadmiumkitty/rdfpandas/curie'), 
                rdflib.URIRef('rdfpandas:curie')))
                
        g_result = rdfpandas.to_graph(df)
        
        self.assertEquals(rdflib.compare.isomorphic(g_expected, g_result), True)

    def test_should_convert_data_frame_to_graph_literal(self):
        """Should create triples based on Literal instance type, datatype and 
        language provided.
        """
        
        idx1= pd.Index(data=['http://github.com/cadmiumkitty/rdfpandas/one'])

        ds01 = pd.Series(data=['String'], index=[idx1], dtype = np.unicode_)
        ds02 = pd.Series(data=['String with type only'], index=[idx1], dtype = np.unicode_)
        ds03 = pd.Series(data=['String with language only in Nepali'], index=[idx1], dtype = np.unicode_)
        ds04 = pd.Series(data=['String In English 1'], index=[idx1], dtype = np.unicode_)
        ds05 = pd.Series(data=['String In English 2'], index=[idx1], dtype = np.unicode_)

        df = pd.DataFrame({
            'http://github.com/cadmiumkitty/rdfpandas/string{Literal}': ds01,
            'http://github.com/cadmiumkitty/rdfpandas/string{Literal}(xsd:string)': ds02,
            'http://github.com/cadmiumkitty/rdfpandas/string{Literal}@ne': ds03,
            'http://github.com/cadmiumkitty/rdfpandas/string{Literal}[0]@en': ds04,
            'http://github.com/cadmiumkitty/rdfpandas/string{Literal}[1]@en': ds05
            })
        
        g_expected = rdflib.Graph()

        g_expected.add((rdflib.URIRef('http://github.com/cadmiumkitty/rdfpandas/one'),
                        rdflib.URIRef('http://github.com/cadmiumkitty/rdfpandas/string'),
                        rdflib.Literal('String')))
        g_expected.add((rdflib.URIRef('http://github.com/cadmiumkitty/rdfpandas/one'),
                        rdflib.URIRef('http://github.com/cadmiumkitty/rdfpandas/string'),
                        rdflib.Literal('String with type only', datatype = rdflib.URIRef('xsd:string'))))
        g_expected.add((rdflib.URIRef('http://github.com/cadmiumkitty/rdfpandas/one'),
                        rdflib.URIRef('http://github.com/cadmiumkitty/rdfpandas/string'),
                        rdflib.Literal('String with language only in Nepali', lang = 'ne')))
        g_expected.add((rdflib.URIRef('http://github.com/cadmiumkitty/rdfpandas/one'),
                        rdflib.URIRef('http://github.com/cadmiumkitty/rdfpandas/string'),
                        rdflib.Literal('String In English 1', lang = 'en')))
        g_expected.add((rdflib.URIRef('http://github.com/cadmiumkitty/rdfpandas/one'),
                        rdflib.URIRef('http://github.com/cadmiumkitty/rdfpandas/string'),
                        rdflib.Literal('String In English 2', lang = 'en')))
                
        g_result = rdfpandas.to_graph(df)
        
        self.assertEquals(rdflib.compare.isomorphic(g_expected, g_result), True)

    def test_should_convert_data_frame_to_graph_uriref(self):
        """Should create triples based on URIRef instance type.
        """
        
        idx1= pd.Index(data=['http://github.com/cadmiumkitty/rdfpandas/one'])

        ds1 = pd.Series(data=['http://github.com/cadmiumkitty/rdfpandas/uri'], index=[idx1], dtype = np.string_)
        ds2 = pd.Series(data=['rdfpandas:curie'], index=[idx1], dtype = np.string_)

        df = pd.DataFrame({
            'http://github.com/cadmiumkitty/rdfpandas/uri{URIRef}': ds1,
            'http://github.com/cadmiumkitty/rdfpandas/curie{URIRef}': ds2
            })
        
        g_expected = rdflib.Graph()
        
        g_expected.add((rdflib.URIRef('http://github.com/cadmiumkitty/rdfpandas/one'),
                rdflib.URIRef('http://github.com/cadmiumkitty/rdfpandas/uri'), 
                rdflib.URIRef('http://github.com/cadmiumkitty/rdfpandas/uri')))
        g_expected.add((rdflib.URIRef('http://github.com/cadmiumkitty/rdfpandas/one'),
                rdflib.URIRef('http://github.com/cadmiumkitty/rdfpandas/curie'), 
                rdflib.URIRef('rdfpandas:curie')))
                
        g_result = rdfpandas.to_graph(df)
        
        self.assertEquals(rdflib.compare.isomorphic(g_expected, g_result), True)

    def test_should_convert_data_frame_to_graph_bnode(self):
        """Should create triples based on BNode instance type.
        """
        
        idx1= pd.Index(data=['http://github.com/cadmiumkitty/rdfpandas/one'])

        ds1 = pd.Series(data=['ub1bL39C14'], index=[idx1], dtype = np.string_)

        df = pd.DataFrame({
            'http://github.com/cadmiumkitty/rdfpandas/bnode{BNode}': ds1,
            })
        
        g_expected = rdflib.Graph()
        
        g_expected.add((rdflib.URIRef('http://github.com/cadmiumkitty/rdfpandas/one'),
                rdflib.URIRef('http://github.com/cadmiumkitty/rdfpandas/bnode'), 
                rdflib.BNode('ub1bL39C14')))
                
        g_result = rdfpandas.to_graph(df)
        
        self.assertEquals(rdflib.compare.isomorphic(g_expected, g_result), True)        

    def test_should_convert_empty_graph_to_empty_data_frame(self):
        """Should return empty DataFrame for empty Graph
        """

        g = rdflib.Graph()
        df_expected = pd.DataFrame()
        df_result = rdfpandas.to_dataframe(g)
        self.assertEquals(rdflib.compare.isomorphic(df_expected, df_result), True)

if __name__ == '__main__':
    unittest.main()