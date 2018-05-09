# -*- coding: utf-8 -*-

from .context import rdfpandas

import pandas as pd
import numpy as np
import rdflib
import rdflib.compare

import unittest
import logging


class DataFrameToGraphConversionTestCase(unittest.TestCase):
    """Tests conversion from DataFrame to Graph."""

    def test_should_convert_empty_data_frame_to_emty_graph(self):
        """Should return empty Graph for empty DataFrame"""
        df = pd.DataFrame()
        g_expected = rdflib.Graph()
        g_result = rdfpandas.to_graph(df)
        self.assertEquals(rdflib.compare.isomorphic(g_expected, g_result), True)
    
    def test_should_convert_data_frame_to_graph_with_fully_qualified_indices(self):
        """Should return Graph with a single String literal.
        Assume that we rely on URIs for indices in the first release,
        that String is the only datatype supported, and that language handling
        of literals is not required.
        """
        
        idx1= pd.Index(data=['http://github.com/cadmiumkitty/rdfpandas/one'])

        ds01 = pd.Series(data=['Bytes'], index=[idx1], dtype = np.string_, name = 'http://github.com/cadmiumkitty/rdfpandas/stringu')

        ds02 = pd.Series(data=['String'], index=[idx1], dtype = np.unicode_, name = 'http://github.com/cadmiumkitty/rdfpandas/unicodeu')

        ds03 = pd.Series(data=[0], index=[idx1], dtype = np.int64, name = 'http://github.com/cadmiumkitty/rdfpandas/int64_1')
        ds04 = pd.Series(data=[-9223372036854775808], index=[idx1], dtype = np.int64, name = 'http://github.com/cadmiumkitty/rdfpandas/int64_2')
        ds05 = pd.Series(data=[9223372036854775807], index=[idx1], dtype = np.int64, name = 'http://github.com/cadmiumkitty/rdfpandas/int64_3')

        ds06 = pd.Series(data=[0], index=[idx1], dtype = np.uint64, name = 'http://github.com/cadmiumkitty/rdfpandas/uint64_1')
        ds07 = pd.Series(data=[18446744073709551615], index=[idx1], dtype = np.uint64, name = 'http://github.com/cadmiumkitty/rdfpandas/uint64_2')

        ds08 = pd.Series(data=[0.0], index=[idx1], dtype = np.float64, name = 'http://github.com/cadmiumkitty/rdfpandas/float64_1')
        ds09 = pd.Series(data=[-1.7976931348623157e+308], index=[idx1], dtype = np.float64, name = 'http://github.com/cadmiumkitty/rdfpandas/float64_2')
        ds10 = pd.Series(data=[1.7976931348623157e+308], index=[idx1], dtype = np.float64, name = 'http://github.com/cadmiumkitty/rdfpandas/float64_3')

        ds11 = pd.Series(data=[True], index=[idx1], dtype = np.bool_, name = 'http://github.com/cadmiumkitty/rdfpandas/true')
        ds12 = pd.Series(data=[False], index=[idx1], dtype = np.bool_, name = 'http://github.com/cadmiumkitty/rdfpandas/false')

        df = pd.DataFrame([ds01, ds02, ds03, ds04, ds05, ds06, ds07, ds08, ds09, ds10, ds11, ds12]).T
        
        logging.debug('DF: %s', df)
        
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
                
        g_result = rdfpandas.to_graph(df)
        
        self.assertEquals(rdflib.compare.isomorphic(g_expected, g_result), True)      


if __name__ == '__main__':
    unittest.main()