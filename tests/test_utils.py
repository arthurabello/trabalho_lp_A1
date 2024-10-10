import unittest
import pandas as pd
import sys

sys.path.append('../src')

from utils import remove_columns, filter_df, remove_lines_by_condition, map_column_values, print_dataframe

grades = [
        [1, 'Arnaldo', 7.0], 
        [2, 'Bernaldo', 8.5], 
        [3, 'Cernaldo', 7.0]
        ]
grades_df = pd.DataFrame(grades, columns=['ID', 'Nome', 'Nota'])

class TestRemoveColumns(unittest.TestCase):
    def test_remove_columns_success(self):
        """Testa o funcionamento da função remove_columns."""
        expected = pd.DataFrame({
            'ID': [1, 2, 3],
            'Nota': [7.0, 8.5, 7.0]
        })
        result = remove_columns(grades_df.copy(), ['Nome'])
        pd.testing.assert_frame_equal(result.reset_index(drop=True), expected)
    
    def test_invalid_input_df(self):
        """Testa o funcionamento da função remove_columns ao receber 
        um parâmetro do tipo errado para df."""
        self.assertRaises(TypeError, remove_columns, grades, ['ID'])

    def test_invalid_input_columns(self):
        """Testa o funcionamento da função remove_columns ao receber 
        um parâmetro do tipo errado para columns."""
        self.assertRaises(TypeError, remove_columns, grades_df, 'ID')
        self.assertRaises(TypeError, remove_columns, grades_df, 3)
        self.assertRaises(TypeError, remove_columns, grades_df, ('ID', 'Nota'))
    
    def test_non_existing_columns(self):
        """Testa o funcionamento da função remove_columns caso alguma
        coluna no parâmetro 'columns' não existir."""
        self.assertRaises(KeyError, remove_columns, grades_df, ['Situação'])
        self.assertRaises(KeyError, remove_columns, grades_df, ['ID', 'Situação'])


class TestFilterDf(unittest.TestCase):
    def test_filter_df_success(self):
        """Testa o funcionamento da função filter_df."""
        expected = pd.DataFrame({
            'ID': [1, 3],
            'Nome': ["Arnaldo", "Cernaldo"],
            'Nota': [7.0, 7.0]
        })
        result = filter_df(grades_df.copy(), {'Nota': 7})
        pd.testing.assert_frame_equal(result.reset_index(drop=True), expected)

    def test_filter_df_sucess2(self):
        """Testa o funcionamento da função filter_df."""
        expected = pd.DataFrame({
            'ID': [1],
            'Nome': ["Arnaldo"],
            'Nota': [7.0]
        })
        result = filter_df(grades_df.copy(), {'Nome': "Arnaldo"})
        pd.testing.assert_frame_equal(result.reset_index(drop=True), expected)
    
    def test_invalid_input_df(self):
        """Testa o funcionamento da função filter_df ao receber 
        um parâmetro do tipo errado para df."""
        self.assertRaises(TypeError, filter_df, grades, {'ID': 2})
        self.assertRaises(TypeError, filter_df, grades, {'Nome', "Arnaldo"})

    def test_non_existing_columns(self):
        """Testa o funcionamento da função remove_columns caso alguma
        coluna não existir no dataframe"""
        self.assertRaises(KeyError, filter_df, grades_df, {'Situação': "Aprovado"})


class TestRemoveLinesByCondition(unittest.TestCase):
    def test_remove_lines_by_condition_success(self):
        """Testa o funcionamento da função remove_lines_by_condition."""
        expected = pd.DataFrame({
            'ID': [2],
            'Nome': ["Bernaldo"],
            'Nota': [8.5]
        })
        result = remove_lines_by_condition(grades_df.copy(), 'Nota', [7.0])
        pd.testing.assert_frame_equal(result.reset_index(drop=True), expected)

    def test_remove_lines_by_condition_success2(self):
        """Testa o funcionamento da função remove_lines_by_condition."""
        expected = pd.DataFrame({
            'ID': [3],
            'Nome': ["Cernaldo"],
            'Nota': [7.0]
        })
        result = remove_lines_by_condition(grades_df.copy(), 'ID', [1, 2])
        pd.testing.assert_frame_equal(result.reset_index(drop=True), expected)
  
    def test_invalid_input_df(self):
        """Testa o funcionamento da função remove_lines_by_condition ao receber 
        um parâmetro do tipo errado para df."""
        self.assertRaises(TypeError, remove_lines_by_condition, grades, 'ID', [2])

    def test_invalid_input_conditions(self):
        """Testa o funcionamento da função remove_lines_by_condition ao receber
        uma entrada inválida para conditions."""
        self.assertRaises(TypeError, remove_lines_by_condition, grades_df, 'ID', 2)
        self.assertRaises(TypeError, remove_lines_by_condition, grades_df, 'Nota', 7.0)
        self.assertRaises(TypeError, remove_lines_by_condition, grades_df, 'ID', (1, 2))
    
    def test_non_existing_columns(self):
        """Testa o funcionamento da função remove_lines_by_condition ao receber
        alguma coluna que não existe no dataframe."""
        self.assertRaises(KeyError, remove_lines_by_condition, grades_df, 'Situação', ["Aprovado"])


class MapColumnValues(unittest.TestCase):
    def test_map_column_values_sucess(self):
        """Testa o funcionamento da função map_column_values"""
        expected = pd.DataFrame({
            'ID': [1, 2, 3],
            'Nome': ["Aluno 1", "Aluno 2", "Aluno 3"],
            'Nota': [7.0, 8.5, 7.0]
        })
        mapping = {"Arnaldo": "Aluno 1", "Bernaldo": "Aluno 2", "Cernaldo": "Aluno 3"}
        result = map_column_values(grades_df.copy(), 'Nome', mapping)
        pd.testing.assert_frame_equal(result.reset_index(drop=True), expected)

    def test_partial_mapping(self):
        """Testa o funcionamento da função map_column_values para mapeamento parcial"""
        expected = pd.DataFrame({
            'ID': [1, 2, 3],
            'Nome': ["Aluno 1", None, "Aluno 3"],
            'Nota': [7.0, 8.5, 7.0]
        })
        mapping = {'Arnaldo': 'Aluno 1', 'Cernaldo': 'Aluno 3'}
        result = map_column_values(grades_df.copy(), 'Nome', mapping)
        pd.testing.assert_frame_equal(result.reset_index(drop=True), expected)
    
    def test_invalid_input_df(self):
        """Testa o funcionamento da função map_column_values ao receber 
        um parâmetro do tipo errado para df. """
        mapping = {"Arnaldo": "Aluno 1", "Bernaldo": "Aluno 2", "Cernaldo": "Aluno 3"}
        self.assertRaises(TypeError, map_column_values, grades, 'Nome', mapping)

    def test_invalid_input_map(self):
        """Testa o funcionamento da função map_column_values ao receber 
        um parâmetro do tipo errado para map."""
        mapping = [("Arnaldo", "Aluno 1"), ("Bernaldo", "Aluno 2"), ("Cernaldo", "Aluno 3")]
        self.assertRaises(TypeError, map_column_values, grades_df, 'Situação', mapping)

    def test_non_existing_columns(self):
        """Testa o funcionamento da função map_column_values ao receber
        alguma coluna que não existe no dataframe."""
        mapping = {"Aprovado": ">=6", "Reprovado": "<6"}
        self.assertRaises(KeyError, map_column_values, grades_df, 'Situação', mapping)


class PrintDataFrame(unittest.TestCase):
    def test_invalid_df(self):
        """Testa o funcionamento da função print_dataframe ao receber 
        um parâmetro do tipo errado para df."""
        self.assertRaises(TypeError, print_dataframe, grades, "Notas dos Alunos")
    
    def test_invalid_title(self):
        """Testa o funcionamento da função print_dataframe ao receber 
        um parâmetro do tipo errado para title."""
        self.assertRaises(TypeError, print_dataframe, grades_df, 7)


if __name__ == '__main__':
    unittest.main()
