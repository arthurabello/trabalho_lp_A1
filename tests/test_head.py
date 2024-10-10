import unittest
import pandas as pd
import sys

sys.path.append('../src')

from head import (get_rows_with_previous, is_headed_goal, is_same_match,
                  origin_of_headed_goals)

#Dataframes utilizados para os testes
events_df = pd.DataFrame({
            'id_odsp': ['match1', 'match1', 'match1', 'match1', 'match2', 'match2',
                        'match2', 'match3', 'match3', 'match3'],
            'time': [10, 11, 30, 35, 5, 11, 12, 20, 27, 28],
            'event_type': [1, 1, 1, 9, 9, 2, 1, 2, 3, 1],
            'is_goal': [1, 1, 0, 0, 0, 0, 1, 0, 0, 1],
            'bodypart': [3, 2, 3, 1, 2, 1, 3, 1, 1, 3]
        })

zero_headed_goals_df = pd.DataFrame({
            'id_odsp': ['match1', 'match1', 'match1', 'match1', 'match2', 'match2',
                        'match2', 'match3', 'match3', 'match3'],
            'time': [10, 11, 30, 35, 5, 11, 12, 20, 27, 28],
            'event_type': [1, 1, 1, 9, 9, 2, 1, 2, 3, 1],
            'is_goal': [0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
            'bodypart': [3, 2, 3, 1, 2, 1, 3, 1, 1, 3]
        })


class TestGetRowsWithPrevious(unittest.TestCase):
    def test_get_rows_with_previous(self):
        """Testa o funcionamento da função get_rows_with_previous.
        """
        expected = pd.DataFrame({
            'id_odsp': ['match1', 'match1', 'match1', 'match2', 'match2', 'match3',
                        'match3'],
            'time': [10, 11, 30, 11, 12, 27, 28],
            'event_type': [1, 1, 1, 2, 1, 3, 1],
            'is_goal': [1, 1, 0, 0, 1, 0, 1],
            'bodypart': [3, 2, 3, 1, 3, 1, 3]
        })
        result = get_rows_with_previous(events_df.copy(), {'bodypart': 3})
        pd.testing.assert_frame_equal(result, expected)

        expected = pd.DataFrame({
            'id_odsp': ['match1', 'match1'],
            'time': [10, 11],
            'event_type': [1, 1],
            'is_goal': [1, 1],
            'bodypart': [3, 2]
        })
        result = get_rows_with_previous(events_df.copy(), {'is_goal': 1, 'bodypart': 2})
        pd.testing.assert_frame_equal(result, expected)

    def test_invalid_input_df_type(self):
        """Testa o funcionamento da função get_rows_with_previous ao receber um parâmetro
        do tipo errado para o df.
        """
        self.assertRaises(TypeError, get_rows_with_previous, 'events',
                          {'bodypart': 3})
        
    def test_invalid_condition_type(self):
        """Testa o funcionamento da função get_rows_with_previous ao receber um parâmetro
        do tipo errado para as condições.
        """
        self.assertRaises(TypeError, get_rows_with_previous,
                          (events_df.copy(), 'bodypart'))
        self.assertRaises(TypeError, get_rows_with_previous,
                          (events_df.copy(), 3))
        
    def test_non_existing_columns(self):
        """Testa o funcionamento da função get_rows_with_previous ao receber uma condição
        relacionada a uma coluna que não existe.
        """
        self.assertRaises(KeyError, get_rows_with_previous, events_df,
                          {'side': 1})
        

class TestIsHeadedGoal(unittest.TestCase):
    def test_is_headed_goal(self):
        """Testa o funcionamento da função is_headed_goal.
        """
        expected = True
        result = is_headed_goal(events_df, 6)
        self.assertEqual(result, expected)

        expected = False
        result = is_headed_goal(events_df, 7)
        self.assertEqual(result, expected)

    def test_invalid_input_df_type(self):
        """Testa o funcionamento da função is_headed_goal ao receber um parâmetro
        do tipo errado para o df.
        """
        self.assertRaises(TypeError, is_headed_goal, 'events', 3)

    def test_invalid_input_index_type(self):
        """Testa o funcionamento da função is_headed_goal ao receber um parâmetro
        do tipo errado para o índice.
        """
        self.assertRaises(TypeError, is_headed_goal, events_df, '3')

    def test_non_existing_index(self):
        """Testa o funcionamento da função is_headed_goal ao receber um índice
        que não existe.
        """
        self.assertRaises(KeyError, is_headed_goal, events_df, 10)


class TestIsSameMatch(unittest.TestCase):
    def test_is_same_match(self):
        """Testa o funcionamento da função is_same_match.
        """
        excepted = True
        result = is_same_match(events_df, 0, 2)
        self.assertEqual(result, excepted)

        excepted = False
        result = is_same_match(events_df, 0, 5)
        self.assertEqual(result, excepted)

    def test_invalid_input_df_type(self):
        """Testa o funcionamento da função is_same_match ao receber um parâmetro
        do tipo errado para o df.
        """
        self.assertRaises(TypeError, is_same_match, 'events', 0, 2)

    def test_invalid_input_index_type(self):
        """Testa o funcionamento da função is_same_match ao receber um parâmetro
        do tipo errado para os índices.
        """
        self.assertRaises(TypeError, is_same_match, events_df, '0', 2)
        self.assertRaises(TypeError, is_same_match, events_df, 0, '2')

    def test_non_existing_index(self):
        """Testa o funcionamento da função is_same_match ao receber um índice
        que não existe.
        """
        self.assertRaises(KeyError, is_same_match, events_df, 10, 2)
        self.assertRaises(KeyError, is_same_match, events_df, 0, 10)


class TestOriginOfHeadedGoals(unittest.TestCase):
    def test_origin_of_headed_goals(self):
        """Testa o funcionamento da função origin_of_headed_goals.
        """
        expected = pd.DataFrame({
                'ORIGEM': ['Escanteios', 'Faltas', 'Impedimentos', 'BOLA PARADA',
                           'Outros'],
                'PORCENTAGEM': [33.33, 33.33, 0.0, 66.67, 33.33]
            })
        result = origin_of_headed_goals(events_df)
        pd.testing.assert_frame_equal(result, expected)

    def test_zero_headed_goals(self):
        """Testa o funcionamento da função origin_of_headed_goals ao receber um
        df em que não há gols de cabeça.
        """
        expected = pd.DataFrame({
                '': ['Sem gols de cabeça']
            })
        result = origin_of_headed_goals(zero_headed_goals_df)
        pd.testing.assert_frame_equal(result, expected)    

    def test_invalid_input_df(self):
        """Testa o funcionamento da função origin_of_headed_goals ao receber um
        parâmetro do tipo errado para o df.
        """
        self.assertRaises(TypeError, origin_of_headed_goals, 'events')


if __name__ == '__main__':
    unittest.main()
