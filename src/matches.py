"""
Este módulo contém funções para analisar e visualizar dados relacionados aos resultados
de jogos de futebol, com foco em agrupar os gols por partida, calcular resultados de
jogos (vitórias, derrotas, empates) e visualizar as porcentagens de cada um.

Funções
-------
group_goals_by_match(df):
    Agrupa os eventos por partida e lado do time (casa ou visitante), focando
    especificamente nos gols.

calculate_results(goals_per_match):
    Calcula o resultado de cada partida (vitória, derrota ou empate do time da casa) com
    base nos gols marcados.

create_summary_dataframe(goals_per_match):
    Cria um DataFrame com as porcentagens de vitórias, derrotas e empates do time da casa.

graph_view(df):
    Plota um gráfico de barras com as porcentagens de vitórias, derrotas e empates do
    time da casa.

matches_main(df):
    Função principal que orquestra a análise e visualização dos resultados das partidas.

Autor
-----
    Arthur Rabello Oliveira
"""

import pandas as pd
import matplotlib.pyplot as plt

from utils import filter_df, print_dataframe

# Hipótese: Times que jogam em casa têm maior percentual de vitórias

def group_goals_by_match(df):
    """
    Agrupa os eventos por partida e lado do time (casa ou visitante), focando
    especificamente nos gols

    Args:
        df (pandas.DataFrame): O dataset original contendo todos os eventos de futebol

    Returns:
        pandas.DataFrame: Um DataFrame com colunas 'home' e 'away' representando os gols
        marcados pelos times da casa e visitantes

    Raises:
        TypeError: Se df não for um pandas DataFrame
        KeyError: Se colunas essenciais não forem encontradas no DataFrame
    """

    #raises
    if not isinstance(df, pd.DataFrame):
        raise TypeError("O parâmetro 'df' deve ser um pandas DataFrame")
    
    required_columns = ['id_odsp', 'side', 'event_type', 'is_goal']
    missing_columns = set(required_columns) - set(df.columns)
    if missing_columns:
        raise KeyError(f"As seguintes colunas estão faltando no DataFrame:
                       {missing_columns}")

    #actual code
    df_goals = filter_df(df, {'event_type': 1, 'is_goal': 1})
    goals_per_match = df_goals.groupby(['id_odsp', 'side']).size().unstack(fill_value=0)
    goals_per_match.columns = ['home', 'away']
    goals_per_match = goals_per_match.reindex(columns=['away', 'home'], fill_value=0)
    return goals_per_match


def calculate_results(goals_per_match):
    """
    Calcula o resultado de cada partida com base nos gols marcados pelos times da casa e
    visitantes

    Args:
        goals_per_match (pandas.DataFrame): DataFrame contendo os gols por partida

    Returns:
        pandas.DataFrame: O DataFrame com uma coluna adicional 'result', indicando o
        resultado da partida

    Raises:
        TypeError: Se goals_per_match não for um pandas DataFrame
        KeyError: Se as colunas 'home' ou 'away' não existirem no DataFrame
    """
    #raises
    if not isinstance(goals_per_match, pd.DataFrame):
        raise TypeError("O parâmetro 'goals_per_match' deve ser um pandas DataFrame")
    
    if 'home' not in goals_per_match.columns or 'away' not in goals_per_match.columns:
        raise KeyError("As colunas 'home' e 'away' são necessárias no DataFrame")
    
    #actual code
    goals_per_match['result'] = goals_per_match.apply(
        lambda x: 1 if x['home'] > x['away'] else (0 if x['home'] < x['away'] else -1),
        axis=1
    )
    return goals_per_match

def create_summary_dataframe(goals_per_match):
    """
    Cria um DataFrame com porcentagens: 'home_percentage' para vitórias, derrotas e
    empates do time da casa

    Args:
        goals_per_match (pandas.DataFrame): DataFrame contendo os resultados das partidas

    Returns:
        pandas.DataFrame: DataFrame com as porcentagens de vitórias, derrotas e empates
        para o time da casa

    Raises:
        TypeError: Se goals_per_match não for um pandas DataFrame
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
        'results': ['Vitórias', 'Derrotas', 'Empates'],
        'home_percentage': [home_victories / total_matches * 100,
                            home_defeats / total_matches * 100,
                            home_draws / total_matches * 100]
    })

    return summary_df

def graph_view(df: pd.DataFrame) -> None:   
    """
    Plota um gráfico de barras com as porcentagens de vitórias, derrotas e empates do
    time da casa

    Args:
        summary_df (pandas.DataFrame): DataFrame contendo as porcentagens de vitórias,
        derrotas e empates

    Raises:
        TypeError: Se 'summary_df' não for um pandas DataFrame
    """
    #raises
    if not isinstance(df, pd.DataFrame):
        raise TypeError("O parâmetro 'df' deve ser um pandas DataFrame")
    
    #actual code
    plt.figure(figsize=(8, 6))
    plt.bar(df['results'], df['home_percentage'],
            color=['#3889ce', '#3889ce', '#3889ce'])
    
    plt.title('Porcentagem de vitórias , derrotas e empates', color='white')
    plt.ylabel('Porcentagem', color='white')

    ax = plt.gca()
    ax.spines['bottom'].set_color('white')
    ax.spines['left'].set_color('white')
    ax.spines['top'].set_color('white')
    ax.spines['right'].set_color('white')

 
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')

<<<<<<< HEAD
    plt.tight_layout()
    plt.savefig('../data/home_results_summary.png',format='png', dpi=300)
    plt.show()
=======
    plt.savefig('../data/graph_matches.png',format='png', dpi=300, transparent=True)
    plt.plot()
>>>>>>> main


def matches_main(df: pd.DataFrame):
    """
    Função principal para orquestrar a análise e exibir os resultados

    Returns:
        pandas.DataFrame: DataFrame contendo as porcentagens de vitórias, derrotas e
        empates do time da casa
    """

    goals_per_match = group_goals_by_match(df)
    goals_per_match = calculate_results(goals_per_match)
    summary_df = create_summary_dataframe(goals_per_match)

    graph_view(summary_df)
    print_dataframe(summary_df, "RESULTADOS DOS JOGOS")
