import unittest
import pandas as pd

import sys
sys.path.append('../src')

from utils import remove_columns,filter_df, remove_lines_by_condition, map_column_values, print_dataframe

grades = [
        [1, 'Arnaldo', 7.0], 
        [2, 'Bernaldo', 8.5], 
        [3, 'Cernaldo', 7.0]
        ]
grades_df = pd.DataFrame(grades, columns=['ID', 'Nome', 'Nota'])

class TestRemoveColumns(unittest.TestCase):
    def test_remove_columns_success(self):
        expected = pd.DataFrame({
            'ID': [1, 2, 3],
            'Nota': [7.0, 8.5, 7.0]
        })
        result = remove_columns(grades_df.copy(), ['Nome'])
        pd.testing.assert_frame_equal(result.reset_index(drop=True), expected)

class TestFilterDf(unittest.TestCase):
    def test_filter_df_success(self):
        expected = pd.DataFrame({
            'ID': [1, 3],
            'Nome': ["Arnaldo", "Cernaldo"],
            'Nota': [7.0, 7.0]
        })
        result = filter_df(grades_df.copy(), 'Nota', 7)
        pd.testing.assert_frame_equal(result.reset_index(drop=True), expected)

class TestRemoveLinesByCondition(unittest.TestCase):
    def test_remove_lines_by_condition_success(self):
        expected = pd.DataFrame({
            'ID': [2],
            'Nome': ["Bernaldo"],
            'Nota': [8.5]
        })
        result = remove_lines_by_condition(grades_df.copy(), 'Nota', [7.0])
        pd.testing.assert_frame_equal(result.reset_index(drop=True), expected)


class MapColumnValues(unittest.TestCase):
    def test_map_column_values(self):
        expected = pd.DataFrame({
            'ID': [1, 2, 3],
            'Nome': ["Aluno 1", "Aluno 2", "Aluno 3"],
            'Nota': [7.0, 8.5, 7.0]
        })
        mapping = {"Arnaldo": "Aluno 1", "Bernaldo": "Aluno 2", "Cernaldo": "Aluno 3"}
        result = map_column_values(grades_df.copy(), 'Nome', mapping)
        pd.testing.assert_frame_equal(result.reset_index(drop=True), expected)

if __name__ == '__main__':
    unittest.main()