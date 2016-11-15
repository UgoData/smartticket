# coding: utf-8

from unittest import TestCase
from loadAndCleanData import LoadCleanData
import pandas as pd
import warnings
warnings.filterwarnings("ignore")


class TestLoadCleanData(TestCase):

    def test_load_classes(self):
        l = LoadCleanData()
        df = l.load_classes()
        self.assertEqual(df.shape, (19, 1), 'Function Load Class not working')

    def test_load_open_food_facts(self):
        l = LoadCleanData()
        df = l.load_open_food_facts()
        self.assertEqual(df.shape, (25332, 19), 'Function Load Open Food Facts not working')

    def test_load_open_beauty_facts(self):
        l = LoadCleanData()
        df = l.load_open_beauty_facts()
        self.assertEqual(df.shape, (1626, 10), 'Function Load Open Beauty Facts not working')

    # def test_shape_df(self):
        # self.fail()

    def test_only_fr_data_from_open_ff(self):
        l = LoadCleanData()
        df = l.only_fr_data_from_open_ff()
        self.assertEqual(df.shape, (25332, 19), 'Function keep only french data not working')

    def test_add_merge_columns(self):
        df_test = pd.DataFrame({"product_name": ['a', 'b', 'c'], 'two': ['a', 'b', 'c']})
        col_test = ['two']
        l = LoadCleanData()
        l.add_merge_columns(df_test, col_test)
        self.assertIn("merge_col", df_test.columns, "Problem with columns merge")
        self.assertEqual('a a', df_test.iloc[0, 2], "Problem with columns merge")

    def test_select_col_beauty_fact(self):
        l = LoadCleanData()
        l.select_col_beauty_fact()

    def test_load_clean_data(self):
        self.fail()

    def test_print_outputs(self):
        self.fail()
