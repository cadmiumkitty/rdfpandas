# -*- coding: utf-8 -*-

from .context import rdfpandas

import pandas as pd
import rdflib
import rdflib.compare

import unittest


class DataFrameToGraphConversionTestCase(unittest.TestCase):
    """Tests conversion from DataFrame to Graph."""

    def test_should_convert_empty_data_frame_to_emty_graph(self):
        """Should return empty Graph for empty DataFrame"""
        df = pd.DataFrame()
        g_expected = rdflib.Graph()
        g_result = rdfpandas.to_graph(df)
        self.assertEquals(rdflib.compare.isomorphic(g_expected, g_result), True)

    def test_should_convert_empty_graph_to_empty_data_frame(self):
        """Should return empty DataFrame for empty Graph"""
        g = rdflib.Graph()
        df_expected = pd.DataFrame()
        df_result = rdfpandas.from_graph(g)
        self.assertEquals(df_expected.equals(df_result), True)
        

if __name__ == '__main__':
    unittest.main()