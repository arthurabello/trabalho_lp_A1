import pandas as pd
import matplotlib.pyplot as plt
from utils import filter_df

def load_dataset(csv_path):

    """
    Carrega o dataset de eventos de futebol a partir de um arquivo CSV especificado

    Args:
        csv_path (str): Caminho para o arquivo CSV contendo o dataset

    Returns:
        pandas.DataFrame: Um DataFrame contendo todos os dados carregados do arquivo CSV

    Raises:
        TypeError: Se `csv_path` não for uma string
        FileNotFoundError: Se o arquivo CSV não for encontrado
    """

    #raises
    if not isinstance(csv_path, str):
        raise TypeError("O parâmetro 'csv_path' deve ser uma string")
    #actual code
    try:
        return pd.read_csv(csv_path)
    except FileNotFoundError:
        raise FileNotFoundError(f"O arquivo '{csv_path}' não foi encontrado")

def group_goals_by_match(df):

    """
    Agrupa os eventos por partida e lado do time (casa ou visitante), focando especificamente nos gols

    Args:
        df (pandas.DataFrame): O dataset original contendo todos os eventos de futebol

    Returns:
        pandas.DataFrame: Um DataFrame com colunas 'home' e 'away' representando os gols marcados pelos times da casa e visitantes

    Raises:
        TypeError: Se `df` não for um pandas DataFrame
        KeyError: Se colunas essenciais não forem encontradas no DataFrame
    """

    #raises
    if not isinstance(df, pd.DataFrame):
        raise TypeError("O parâmetro 'df' deve ser um pandas DataFrame")
    
    required_columns = ['id_odsp', 'side', 'event_type', 'is_goal']
    missing_columns = set(required_columns) - set(df.columns)
    if missing_columns:
        raise KeyError(f"As seguintes colunas estão faltando no DataFrame: {missing_columns}")

    #actual code
    df_goals = filter_df(df, {'event_type': 1, 'is_goal': 1})
    goals_per_match = df_goals.groupby(['id_odsp', 'side']).size().unstack(fill_value=0)
    goals_per_match.columns = ['home', 'away']
    goals_per_match = goals_per_match.reindex(columns=['away', 'home'], fill_value=0)
    return goals_per_match

def calculate_results(goals_per_match):

    """
    Calcula o resultado de cada partida com base nos gols marcados pelos times da casa e visitantes

    Args:
        goals_per_match (pandas.DataFrame): DataFrame contendo os gols por partida

    Returns:
        pandas.DataFrame: O DataFrame com uma coluna adicional 'result', indicando o resultado da partida

    Raises:
        TypeError: Se `goals_per_match` não for um pandas DataFrame
        KeyError: Se as colunas 'home' ou 'away' não existirem no DataFrame
    """

    #raises
    if not isinstance(goals_per_match, pd.DataFrame):
        raise TypeError("O parâmetro 'goals_per_match' deve ser um pandas DataFrame")
    
    if 'home' not in goals_per_match.columns or 'away' not in goals_per_match.columns:
        raise KeyError("As colunas 'home' e 'away' são necessárias no DataFrame")
    
    #actual code
    goals_per_match['result'] = goals_per_match.apply(
        lambda x: 1 if x['home'] > x['away'] else (0 if x['home'] < x['away'] else -1), axis=1
    )
    return goals_per_match

def create_summary_dataframe(goals_per_match):

    """
    Cria um DataFrame com porcentagens: 'home_percentage' para vitórias, derrotas e empates do time da casa

    Args:
        goals_per_match (pandas.DataFrame): DataFrame contendo os resultados das partidas

    Returns:
        pandas.DataFrame: DataFrame com as porcentagens de vitórias, derrotas e empates para o time da casa

    Raises:
        TypeError: Se `goals_per_match` não for um pandas DataFrame
        KeyError: Se a coluna 'result' não existir no DataFrame
    """

    #raises
    if not isinstance(goals_per_match, pd.DataFrame):
        raise TypeError("O parâmetro 'goals_per_match' deve ser um pandas DataFrame")
    
    if 'result' not in goals_per_match.columns:
        raise KeyError("A coluna 'result' é necessária no DataFrame")

    #actual code
    home_victories = (goals_per_match['result'] == 1).sum()
    home_defeats = (goals_per_match['result'] == 0).sum()
    home_draws = (goals_per_match['result'] == -1).sum()

    total_matches = home_victories + home_defeats + home_draws

    summary_df = pd.DataFrame({
        'home_percentage': [home_victories / total_matches * 100, home_defeats / total_matches * 100, home_draws / total_matches * 100]
    }, index=['victories', 'defeats', 'draws'])

    return summary_df

def plot_summary(summary_df):

    """
    Plota um gráfico de barras com as porcentagens de vitórias, derrotas e empates do time da casa

    Args:
        summary_df (pandas.DataFrame): DataFrame contendo as porcentagens de vitórias, derrotas e empates

    Raises:
        TypeError: Se 'summary_df' não for um pandas DataFrame
    """

    #raises
    if not isinstance(summary_df, pd.DataFrame):
        raise TypeError("O parâmetro 'summary_df' deve ser um pandas DataFrame")

    #actual code
    plt.figure(figsize=(8, 5))
    summary_df['home_percentage'].plot(kind='bar', color=['#4CAF50', '#FF9800', '#2196F3'])

    plt.title('Porcentagem de vitórias, derrotas e empates do time da casa', fontsize=16)
    plt.xlabel('Resultados', fontsize=14)
    plt.ylabel('Porcentagem (%)', fontsize=14)
    plt.xticks(rotation=0)

    for index, value in enumerate(summary_df['home_percentage']):
        plt.text(index, value + 1, f'{value:.2f}%', ha='center', fontsize=12)

    plt.tight_layout()
    plt.show()

def main():

    """
    Função principal para orquestrar a análise e exibir os resultados

    Returns:
        pandas.DataFrame: DataFrame contendo as porcentagens de vitórias, derrotas e empates do time da casa
    """

    #actual code
    csv_path = '../data/cleaned_events.csv'
    df = load_dataset(csv_path)
    goals_per_match = group_goals_by_match(df)
    goals_per_match = calculate_results(goals_per_match)
    summary_df = create_summary_dataframe(goals_per_match)

    plot_summary(summary_df)
    print(summary_df)

if __name__ == '__main__':
    main()
