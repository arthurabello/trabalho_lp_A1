import pandas as pd

def load_dataset(csv_path):
    
    """
    Carrega o dataset de eventos de futebol a partir de um arquivo CSV especificado.

    Args:
        csv_path (str): Caminho para o arquivo CSV contendo o dataset.

    Returns:
        pandas.DataFrame: Um DataFrame contendo todos os dados carregados do arquivo CSV.
    """

    return pd.read_csv(csv_path)

def group_goals_by_match(df):

    """
    Agrupa os eventos por partida e lado do time (casa ou visitante), focando especificamente nos gols.

    Esta função filtra os eventos que não estão relacionados aos gols e, em seguida, agrupa os eventos 
    relacionados a gols por partida e lado do time (casa ou visitante). O resultado é um DataFrame que 
    exibe o número de gols marcados pelos times da casa e visitantes para cada partida.

    Args:
        df (pandas.DataFrame): O dataset original contendo todos os eventos de futebol. Cada linha 
                               no dataset representa um evento em uma partida, incluindo gols, faltas, etc.

    Returns:
        pandas.DataFrame: Um DataFrame com duas colunas: 'home' e 'away', onde cada linha corresponde a 
                          uma partida, mostrando o número de gols marcados pelos times da casa e visitante.
                          Partidas sem gols estão incluídas com valores zero em ambas as colunas.
    """

    df_goals = df[(df['event_type'] == 1) & (df['is_goal'] == 1)]
    goals_per_match = df_goals.groupby(['id_odsp', 'side']).size().unstack(fill_value=0)
    goals_per_match.columns = ['home', 'away']
    goals_per_match = goals_per_match.reindex(columns=['away', 'home'], fill_value=0)
    return goals_per_match

def calculate_results(goals_per_match):

    """
    Calcula o resultado de cada partida com base nos gols marcados pelos times da casa e visitantes.

    A função compara o número de gols marcados pelo time da casa com aqueles marcados pelo time visitante 
    e determina o resultado da partida:
    - 1: Vitória do time da casa
    - 0: Vitória do time visitante
    - -1: Empate

    Args:
        goals_per_match (pandas.DataFrame): DataFrame contendo o número de gols por partida para ambos 
                                            os times da casa e visitantes.

    Returns:
        pandas.DataFrame: O DataFrame de entrada com uma coluna adicional 'result', que indica o 
                          resultado da partida.
    """

    goals_per_match['result'] = goals_per_match.apply(
        lambda x: 1 if x['home'] > x['away'] else (0 if x['home'] < x['away'] else -1), axis=1
    )
    return goals_per_match

def calculate_home_win_percentage_excluding_draws(goals_per_match):

    """
    Calcula a porcentagem de partidas vencidas pelo time da casa, excluindo empates.

    Esta função filtra as partidas que resultaram em empate e, em seguida, calcula a porcentagem 
    de vitórias do time da casa em relação ao número total de partidas que tiveram um vencedor claro.

    Args:
        goals_per_match (pandas.DataFrame): Um DataFrame contendo os resultados das partidas com colunas 
                                            para o número de gols marcados pelos times da casa e visitantes 
                                            e uma coluna 'result' indicando o resultado da partida.

    Returns:
        float: A porcentagem de partidas vencidas pelo time da casa, excluindo empates.
    """

    matches_without_draw = goals_per_match[goals_per_match['result'] != -1]
    home_wins = (matches_without_draw['result'] == 1).sum()
    total_matches_without_draw = matches_without_draw.shape[0]
    home_win_percentage = (home_wins / total_matches_without_draw) * 100
    return home_win_percentage

def calculate_home_win_percentage_including_draws(goals_per_match):

    """
    Calcula a porcentagem de partidas em que o time da casa venceu ou empatou, tratando empates como vitórias.

    Esta função conta tanto as vitórias do time da casa quanto os empates como "vitórias do time da casa" 
    e calcula sua porcentagem em relação ao número total de partidas jogadas.

    Args:
        goals_per_match (pandas.DataFrame): Um DataFrame contendo os resultados das partidas com colunas 
                                            para o número de gols marcados pelos times da casa e visitantes 
                                            e uma coluna 'result' indicando o resultado da partida.

    Returns:
        float: A porcentagem de partidas em que o time da casa venceu ou empatou, tratando empates como vitórias.
    """

    home_wins_or_draws = (goals_per_match['result'] == 1).sum() + (goals_per_match['result'] == -1).sum()
    total_matches = goals_per_match.shape[0]
    home_win_or_draw_percentage = (home_wins_or_draws / total_matches) * 100
    return home_win_or_draw_percentage

def calculate_draw_percentage(goals_per_match):

    """
    Calcula a porcentagem de partidas que terminaram em empate.

    Esta função calcula a porcentagem de partidas que terminaram com o mesmo número de gols marcados 
    pelos times da casa e visitantes (ou seja, empates) em relação ao número total de partidas jogadas.

    Args:
        goals_per_match (pandas.DataFrame): Um DataFrame contendo os resultados das partidas com colunas 
                                            para o número de gols marcados pelos times da casa e visitantes 
                                            e uma coluna 'result' indicando o resultado da partida.

    Returns:
        float: A porcentagem de partidas que terminaram em empate.
    """

    draws = (goals_per_match['result'] == -1).sum()
    total_matches = goals_per_match.shape[0]
    draw_percentage = (draws / total_matches) * 100
    return draw_percentage

def calculate_home_loss_percentage_excluding_draws(goals_per_match):

    """
    Calcula a porcentagem de partidas perdidas pelo time da casa, excluindo empates.

    Esta função filtra as partidas que resultaram em empate e calcula a porcentagem de derrotas 
    do time da casa em relação ao número total de partidas com um vencedor claro.

    Args:
        goals_per_match (pandas.DataFrame): Um DataFrame contendo os resultados das partidas com colunas 
                                            para o número de gols marcados pelos times da casa e visitantes 
                                            e uma coluna 'result' indicando o resultado da partida.

    Returns:
        float: A porcentagem de partidas perdidas pelo time da casa, excluindo empates.
    """

    matches_without_draw = goals_per_match[goals_per_match['result'] != -1]
    home_losses = (matches_without_draw['result'] == 0).sum()
    total_matches_without_draw = matches_without_draw.shape[0]
    home_loss_percentage = (home_losses / total_matches_without_draw) * 100
    return home_loss_percentage

def calculate_home_loss_percentage_including_draws(goals_per_match):

    """
    Calcula a porcentagem de partidas perdidas pelo time da casa, incluindo empates como derrotas.

    Esta função trata tanto as vitórias do time visitante quanto os empates como "derrotas do time da casa" 
    e calcula sua porcentagem em relação ao número total de partidas jogadas.

    Args:
        goals_per_match (pandas.DataFrame): Um DataFrame contendo os resultados das partidas com colunas 
                                            para o número de gols marcados pelos times da casa e visitantes 
                                            e uma coluna 'result' indicando o resultado da partida.

    Returns:
        float: A porcentagem de partidas em que o time da casa perdeu ou empatou, tratando empates como derrotas.
    """

    home_losses_or_draws = (goals_per_match['result'] == 0).sum() + (goals_per_match['result'] == -1).sum()
    total_matches = goals_per_match.shape[0]
    home_loss_percentage = (home_losses_or_draws / total_matches) * 100
    return home_loss_percentage

def calculate_draws_from_original_dataset(df):

    """
    Calcula o número total de partidas que terminaram em empate com base no dataset original.

    Esta função retorna ao dataset original e agrupa eventos relacionados a gols por partida para contar 
    o número total de empates. Ela compara o número de gols marcados pelos times da casa e visitantes 
    para cada partida e conta quantas terminaram com o mesmo número de gols para ambos os lados.

    Args:
        df (pandas.DataFrame): O dataset original contendo todos os eventos de futebol.

    Returns:
        int: O número total de partidas que terminaram em empate.
    """

    df_goals = df[df['is_goal'] == 1]
    df_grouped = df_goals.groupby(['id_odsp', 'side'])['is_goal'].sum().unstack(fill_value=0)
    df_grouped.columns = ['away', 'home']
    draws = df_grouped[df_grouped['home'] == df_grouped['away']].shape[0]
    return draws

def main():

    """
    Função principal que orquestra toda a análise. Todas as funções utilizadas já foram descritas neste script.
    """

    csv_path = '../data/events.csv'

    df = load_dataset(csv_path)
    goals_per_match = group_goals_by_match(df)
    goals_per_match = calculate_results(goals_per_match)

    home_win_percentage_excluding_draws = calculate_home_win_percentage_excluding_draws(goals_per_match)
    home_win_percentage_including_draws = calculate_home_win_percentage_including_draws(goals_per_match)

    draw_percentage = calculate_draw_percentage(goals_per_match)

    home_loss_percentage_excluding_draws = calculate_home_loss_percentage_excluding_draws(goals_per_match)
    home_loss_percentage_including_draws = calculate_home_loss_percentage_including_draws(goals_per_match)

    total_draws = calculate_draws_from_original_dataset(df)

    print(f'Percentage of home team wins (excluding draws): {home_win_percentage_excluding_draws:.2f}%')
    print(f'Percentage of home team wins (including draws as victories): {home_win_percentage_including_draws:.2f}%')
    print(f'Percentage of home team losses (excluding draws): {home_loss_percentage_excluding_draws:.2f}%')
    print(f'Percentage of home team losses (including draws as losses): {home_loss_percentage_including_draws:.2f}%')

if __name__ == '__main__':
    main()
