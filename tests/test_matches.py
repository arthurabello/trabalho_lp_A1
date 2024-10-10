<<<<<<< HEAD
import sys
import pandas as pd
import unittest
=======
import unittest
import pandas as pd
import sys
>>>>>>> main

sys.path.append('../src')

from matches import (
    load_dataset,
    group_goals_by_match,
    calculate_results,
    create_summary_dataframe,
    plot_summary
)

class TestFootballAnalysis(unittest.TestCase):

    def test_load_dataset_valid(self):

        """
        Testa a função load_dataset com um caminho de arquivo CSV válido
        Verifica se o resultado é um DataFrame
        """
        
        df = load_dataset('../data/cleaned_events.csv')
        self.assertIsInstance(df, pd.DataFrame, "O resultado deve ser um DataFrame")

    def test_load_dataset_invalid_path(self):

        """
        Testa a função load_dataset com um caminho de arquivo CSV inválido
        Verifica se uma FileNotFoundError é levantada
        """

        with self.assertRaises(FileNotFoundError):
            load_dataset('invalid_path.csv')

    def test_group_goals_by_match_valid(self):

        """
        Testa a função group_goals_by_match com um DataFrame válido
        Verifica se o resultado contém as colunas 'home' e 'away'
        """

        data = {
            'id_odsp': [1, 1, 2, 2, 3, 3],
            'side': ['home', 'away', 'home', 'away', 'home', 'away'],
            'event_type': [1, 1, 1, 1, 1, 1],
            'is_goal': [1, 0, 0, 1, 1, 1]
        }
        df = pd.DataFrame(data)
        goals_per_match = group_goals_by_match(df)
        self.assertIsInstance(goals_per_match, pd.DataFrame, "O resultado deve ser um DataFrame")
        self.assertIn('home', goals_per_match.columns, "A coluna 'home' deve estar presente")
        self.assertIn('away', goals_per_match.columns, "A coluna 'away' deve estar presente")

    def test_group_goals_by_match_invalid_type(self):

        """
        Testa a função group_goals_by_match com um tipo de entrada inválido
        Verifica se uma TypeError é levantada
        """

        with self.assertRaises(TypeError):
            group_goals_by_match('invalid input')

    def test_calculate_results_valid(self):

        """
        Testa a função calculate_results com um DataFrame válido
        Verifica se a coluna 'result' está presente no resultado
        """

        data = {
            'id_odsp': [1, 1, 2, 2, 3, 3],
            'side': ['home', 'away', 'home', 'away', 'home', 'away'],
            'event_type': [1, 1, 1, 1, 1, 1],
            'is_goal': [1, 0, 0, 1, 1, 1]
        }
        df = pd.DataFrame(data)
        goals_per_match = group_goals_by_match(df)
        results = calculate_results(goals_per_match)
        self.assertIn('result', results.columns, "A coluna 'result' deve estar presente")

    def test_calculate_results_invalid_type(self):

        """
        Testa a função calculate_results com um tipo de entrada inválido
        Verifica se uma TypeError é levantada
        """

        with self.assertRaises(TypeError):
            calculate_results('invalid input')

    def test_create_summary_dataframe_valid(self):

        """
        Testa a função create_summary_dataframe com um DataFrame válido
        Verifica se a coluna 'home_percentage' está presente no resultado
        """

        data = {
            'id_odsp': [1, 1, 2, 2, 3, 3],
            'side': ['home', 'away', 'home', 'away', 'home', 'away'],
            'event_type': [1, 1, 1, 1, 1, 1],
            'is_goal': [1, 0, 0, 1, 1, 1]
        }
        df = pd.DataFrame(data)
        goals_per_match = group_goals_by_match(df)
        results = calculate_results(goals_per_match)
        summary_df = create_summary_dataframe(results)
        self.assertIsInstance(summary_df, pd.DataFrame, "O resultado deve ser um DataFrame")
        self.assertIn('home_percentage', summary_df.columns, "A coluna 'home_percentage' deve estar presente")

    def test_create_summary_dataframe_invalid_type(self):

        """
        Testa a função create_summary_dataframe com um tipo de entrada inválido
        Verifica se uma TypeError é levantada
        """

        with self.assertRaises(TypeError):
            create_summary_dataframe('invalid input')

    def test_plot_summary_valid(self):

        """
        Testa a função plot_summary com um DataFrame válido
        Verifica se não ocorre exceção durante a execução
        """

        data = {
            'id_odsp': [1, 1, 2, 2, 3, 3],
            'side': ['home', 'away', 'home', 'away', 'home', 'away'],
            'event_type': [1, 1, 1, 1, 1, 1],
            'is_goal': [1, 0, 0, 1, 1, 1]
        }
        df = pd.DataFrame(data)
        goals_per_match = group_goals_by_match(df)
        results = calculate_results(goals_per_match)
        summary_df = create_summary_dataframe(results)
        try:
            plot_summary(summary_df)
        except Exception as e:
            self.fail(f"plot_summary levantou uma exceção inesperada: {e}")

if __name__ == '__main__':
    unittest.main()
