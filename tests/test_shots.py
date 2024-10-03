import unittest
import pandas as pd

import sys

sys.path.append('../src')

from shots import calculate_goals, shot_outcome_count, perc_shot_outcome

shots_data = [
    {'situation': 'inside', 'shot_outcome': 'Gol'},
    {'situation': 'inside', 'shot_outcome': 'Fora'},
    {'situation': 'inside', 'shot_outcome': 'Gol'},
    {'situation': 'outside', 'shot_outcome': 'Fora'},
    {'situation': 'outside', 'shot_outcome': 'Trave'},
    {'situation': 'inside', 'shot_outcome': 'Trave'},
    {'situation': 'outside', 'shot_outcome': 'Defendido'},
    {'situation': 'inside', 'shot_outcome': 'Gol'},
    {'situation': 'inside', 'shot_outcome': 'Defendido'},
    {'situation': 'outside', 'shot_outcome': 'Gol'}
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

class TestCalculateGoals(unittest.TestCase):
    
    def test_calculate_goals_success(self):
        expected = pd.DataFrame({
            'Situação': ['Dentro da área', 'Fora da área'],
            'Porcentagem': [60.0, 40.0]
        })
        result = calculate_goals(goals_df.copy())
        pd.testing.assert_frame_equal(result.reset_index(drop=True), expected)

    

class TestShotOutcomeCount(unittest.TestCase):
    def test_shot_outcome_count_success(self):
        expected = pd.DataFrame({
            'Resultado': ['Gol', 'Fora', 'Trave', 'Defendido'],
            'count_in': [3, 1, 1, 1],
            'count_out': [1, 1, 1, 1]
        })
        result = shot_outcome_count(shots_df.copy())
        pd.testing.assert_frame_equal(result.reset_index(drop=True), expected)

class TestShotOutcomePerc(unittest.TestCase):
        
    def test_perc_shot_outcome_sucess(self):
        expected = pd.DataFrame({
            'Resultado': ['Gol', 'Fora', 'Trave', 'Defendido'],
            'Porcentagem_in': [50.0, 16.67, 16.67, 16.67],
            'Porcentagem_out': [25.0, 25.0, 25.0, 25.0]
        })
        result = perc_shot_outcome(shots_df.copy())
        pd.testing.assert_frame_equal(result.reset_index(drop=True), expected)

if __name__ == '__main__':
    unittest.main()