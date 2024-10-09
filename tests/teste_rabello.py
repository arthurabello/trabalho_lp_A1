import unittest
import pandas as pd
from io import StringIO
from rabello_hypothesis import load_dataset, group_goals_by_match, calculate_results, create_summary_dataframe, plot_summary

class TestFootballAnalytics(unittest.TestCase):

    def setUp(self):

        """
        Configura o ambiente para os testes, criando um DataFrame de exemplo
        """

        self.csv_data = StringIO("""
        id_odsp,side,event_type,is_goal
        1,home,1,1
        1,away,1,0
        2,home,1,0
        2,away,1,1
        3,home,1,1
        3,away,1,1
        """)
        self.df = pd.read_csv(self.csv_data)

    def test_load_dataset_success(self):

        """
        Testa a função load_dataset para verificar se o DataFrame é carregado corretamente
        """

        df = load_dataset('caminho_falso.csv')
        self.assertIsInstance(df, pd.DataFrame)

    def test_load_dataset_type_error(self):

        """
        Testa a função load_dataset para verificar se levanta TypeError para entrada inválida
        """
        
        with self.assertRaises(TypeError):
            load_dataset(123)

    def test_load_dataset_file_not_found(self):

        """
        Testa a função load_dataset para verificar se levanta FileNotFoundError para arquivo inexistente
        """

        with self.assertRaises(FileNotFoundError):
            load_dataset('arquivo_inexistente.csv')

    def test_group_goals_by_match_success(self):

        """
        Testa a função group_goals_by_match para verificar se os gols são agrupados corretamente
        """

        result = group_goals_by_match(self.df.copy())
        expected = pd.DataFrame({'home': [2, 0], 'away': [0, 1]}, index=[1, 2]).fillna(0)
        pd.testing.assert_frame_equal(result, expected)

    def test_group_goals_by_match_type_error(self):

        """
        Testa a função group_goals_by_match para verificar se levanta TypeError para entrada inválida
        """

        with self.assertRaises(TypeError):
            group_goals_by_match("string inválida")

    def test_group_goals_by_match_key_error(self):

        """
        Testa a função group_goals_by_match para verificar se levanta KeyError para colunas faltando
        """

        df_invalid = self.df.drop(columns=['id_odsp'])
        with self.assertRaises(KeyError):
            group_goals_by_match(df_invalid)

    def test_calculate_results_success(self):

        """
        Testa a função calculate_results para verificar se os resultados das partidas são calculados corretamente
        """

        goals_df = pd.DataFrame({'home': [2, 1], 'away': [1, 1]})
        result = calculate_results(goals_df.copy())
        expected = pd.DataFrame({'home': [2, 1], 'away': [1, 1], 'result': [1, -1]})
        pd.testing.assert_frame_equal(result, expected)

    def test_calculate_results_type_error(self):

        """
        Testa a função calculate_results para verificar se levanta TypeError para entrada inválida
        """

        with self.assertRaises(TypeError):
            calculate_results("string inválida")

    def test_calculate_results_key_error(self):

        """
        Testa a função calculate_results para verificar se levanta KeyError para colunas faltando
        """

        df_invalid = pd.DataFrame({'home': [2]})
        with self.assertRaises(KeyError):
            calculate_results(df_invalid)

    def test_create_summary_dataframe_success(self):

        """
        Testa a função create_summary_dataframe para verificar se o DataFrame de resumo é criado corretamente
        """

        results_df = pd.DataFrame({'result': [1, 0, -1]})
        summary = create_summary_dataframe(results_df.copy())
        expected_summary = pd.DataFrame({
            'home_percentage': [33.33, 33.33, 33.33]
        }, index=['victories', 'defeats', 'draws'])
        pd.testing.assert_frame_equal(summary, expected_summary)

    def test_create_summary_dataframe_type_error(self):

        """
        Testa a função create_summary_dataframe para verificar se levanta TypeError para entrada inválida
        """

        with self.assertRaises(TypeError):
            create_summary_dataframe("string inválida")

    def test_create_summary_dataframe_key_error(self):

        """
        Testa a função create_summary_dataframe para verificar se levanta KeyError para colunas faltando
        """

        df_invalid = pd.DataFrame({'home': [2]})
        with self.assertRaises(KeyError):
            create_summary_dataframe(df_invalid)

    def test_plot_summary_success(self):

        """
        Testa a função plot_summary para verificar se a plotagem não levanta exceções
        """

        summary_df = pd.DataFrame({'home_percentage': [50, 30, 20]}, index=['victories', 'defeats', 'draws'])
        plot_summary(summary_df)

if __name__ == '__main__':
    unittest.main()
