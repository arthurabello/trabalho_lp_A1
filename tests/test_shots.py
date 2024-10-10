import unittest
import pandas as pd
import sys

sys.path.append('../src')

from shots import (calculate_goals, shot_outcome_count, perc_shot_outcome,
                   adjust_shot_outcome_df)

# dados para os testes
grades = [
        [1, 'Arnaldo', 7.0], 
        [2, 'Bernaldo', 8.5], 
        [3, 'Cernaldo', 7.0]
        ]
grades_df = pd.DataFrame(grades, columns=['ID', 'Nome', 'Nota'])

shots_data = [
    {'situation': 'inside', 'shot_outcome': 'Gol'},
    {'situation': 'inside', 'shot_outcome': 'Fora'},
    {'situation': 'inside', 'shot_outcome': 'Trave'},
    {'situation': 'inside', 'shot_outcome': 'Defendido'},
    {'situation': 'inside', 'shot_outcome': 'Bloqueado'},
    {'situation': 'inside', 'shot_outcome': 'Gol'},
    {'situation': 'inside', 'shot_outcome': 'Gol'},
    {'situation': 'inside', 'shot_outcome': 'Trave'},
    {'situation': 'inside', 'shot_outcome': 'Defendido'},
    {'situation': 'inside', 'shot_outcome': 'Fora'},
    {'situation': 'outside', 'shot_outcome': 'Gol'},
    {'situation': 'outside', 'shot_outcome': 'Fora'},
    {'situation': 'outside', 'shot_outcome': 'Fora'},
    {'situation': 'outside', 'shot_outcome': 'Trave'},
    {'situation': 'outside', 'shot_outcome': 'Defendido'},
    {'situation': 'outside', 'shot_outcome': 'Gol'},
    {'situation': 'outside', 'shot_outcome': 'Bloqueado'},
    {'situation': 'outside', 'shot_outcome': 'Bloqueado'},
    {'situation': 'outside', 'shot_outcome': 'Fora'},
    {'situation': 'outside', 'shot_outcome': 'Defendido'}
    
]
shots_df = pd.DataFrame(shots_data)

goals_data = [
        {'situation': 'inside'},
        {'situation': 'outside'},
        {'situation': 'inside'},
        {'situation': 'outside'},
        {'situation': 'inside'}
    ]
goals_df = pd.DataFrame(goals_data)

adjust_shots_data = [
    {'is_goal': 1, 'shot_outcome': 'No alvo'},
    {'is_goal': 0, 'shot_outcome': 'Fora'},
    {'is_goal': 0, 'shot_outcome': 'Trave'},
    {'is_goal': 0, 'shot_outcome': 'No alvo'},
    {'is_goal': 0, 'shot_outcome': 'Bloqueado'},
    {'is_goal': 1, 'shot_outcome': 'No alvo'},   
]

adjust_shots_df = pd.DataFrame(adjust_shots_data)

# testes unitários

class TestCalculateGoals(unittest.TestCase):
    def test_calculate_goals_success(self):
        """Testa o funcionamento da função calculate_goals. """
        expected = pd.DataFrame({
            'Situação': ['Dentro da área', 'Fora da área'],
            'Porcentagem': [60.0, 40.0]
        })
        result = calculate_goals(goals_df.copy())
        pd.testing.assert_frame_equal(result.reset_index(drop=True), expected)
    
    def test_invalid_input_df(self):
        """Testa o funcionamento da função calculate_goals ao receber 
        um parâmetro do tipo errado para df."""
        self.assertRaises(TypeError, calculate_goals, goals_data)
    
    def test_non_existing_columns(self):
        """Testa o funcionamento da função calculate_goals ao receber 
        um dataframe que não contém as colunas requeridas."""
        self.assertRaises(KeyError, calculate_goals, grades_df)


class TestShotOutcomeCount(unittest.TestCase):
    def test_shot_outcome_count_success(self):
        """Testa o funcionamento da função shot_outcome_count. """
        expected = pd.DataFrame({
            'Resultado': ['Gol', 'Fora', 'Trave', 'Defendido', 'Bloqueado'],
            'count_in': [3, 2, 2, 2, 1],
            'count_out': [2, 3, 1, 2, 2]
        })
        result = shot_outcome_count(shots_df.copy())
        pd.testing.assert_frame_equal(result.reset_index(drop=True), expected)
    
    def test_invalid_df(self):
        """Testa o funcionamento da função shot_outcome_count ao receber 
        um parâmetro do tipo errado para df."""
        self.assertRaises(TypeError, shot_outcome_count, shots_data)

    def test_non_existing_columns(self):
        """Testa o funcionamento da função shot_outcome_count ao receber 
        um dataframe que não contém as colunas requeridas."""
        self.assertRaises(KeyError, shot_outcome_count, goals_df)


class TestShotOutcomePerc(unittest.TestCase):     
    def test_perc_shot_outcome_sucess(self):
        """Testa o funcionamento da função perc_shot_outcome."""
        expected = pd.DataFrame({
            'Resultado': ['Gol', 'Fora', 'Trave', 'Defendido', 'Bloqueado'],
            'Porcentagem_in': [30.0, 20.0, 20.0, 20.0, 10.0],
            'Porcentagem_out': [20.0, 30.0, 10.0, 20.0, 20.0]
        })
        result = perc_shot_outcome(shots_df.copy())
        pd.testing.assert_frame_equal(result.reset_index(drop=True), expected)
    
    def test_invalid_df(self):
        """Testa o funcionamento da função perc_shot_outcome ao receber 
        um parâmetro do tipo errado para df."""
        self.assertRaises(TypeError, perc_shot_outcome, shots_data)


class TestAdjustShotOutcomeDf(unittest.TestCase):
    def test_adjust_shot_outcome_df_sucess(self):
        """Testa o funcionamento da função adjust_shot_outcome_df."""
        expected = pd.DataFrame([
            {'is_goal': 1, 'shot_outcome': 'Gol'},
            {'is_goal': 0, 'shot_outcome': 'Fora'},
            {'is_goal': 0, 'shot_outcome': 'Trave'},
            {'is_goal': 0, 'shot_outcome': 'Defendido'},
            {'is_goal': 0, 'shot_outcome': 'Bloqueado'},
            {'is_goal': 1, 'shot_outcome': 'Gol'},   
        ])
        result = adjust_shot_outcome_df(adjust_shots_df)
        pd.testing.assert_frame_equal(result.reset_index(drop=True), expected)
    
    def test_invalid_df(self):
        """Testa o funcionamento da função adjust_shot_outcome_df ao receber 
        um parâmetro do tipo errado para df."""
        self.assertRaises(TypeError, adjust_shot_outcome_df, adjust_shots_data)

    def test_non_existing_columns(self):
        """Testa o funcionamento da função adjust_shot_outcome_df ao receber 
        um dataframe que não contém as colunas requeridas."""
        self.assertRaises(KeyError, adjust_shot_outcome_df, shots_df)


if __name__ == '__main__':
    unittest.main()
