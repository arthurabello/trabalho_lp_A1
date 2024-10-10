"""
Este módulo é responsável por calcular a porcentagem de cada possível origem dos gols de
cabeça em eventos de futebol. Ele analisa jogadas anteriores aos gols de cabeça e
categorizando-as em escanteios, faltas, impedimentos ou outros. Também gera uma
visualização gráfica das porcentagens das origens dos gols de cabeça.

Funções
-------
get_rows_with_previous(df, conditions)
    Filtra linhas de eventos e inclui o evento anterior ao gol.
is_headed_goal(df, row_index)
    Verifica se um evento é um gol marcado de cabeça.
is_same_match(df, row_index_a, row_index_b):
    Verifica se dois eventos ocorreram na mesma partida.
origin_of_headed_goals(df):
    Calcula a porcentagem de gols de cabeça com base na origem.
graph_view(df)
    Gera um gráfico de barras das porcentagens das origens dos gols de cabeça.
head_main(df)
    Função principal que executa a análise e a visualização.

Autor
-----
    Antonio Francisco Batista Filho
"""

import pandas as pd
from typing import Dict, Union
import matplotlib.pyplot as plt

from utils import remove_columns, filter_df, print_dataframe

# Hipótese: maior parte dos gols de cabeça tem origem em lances de bola parada.
# Lances de bola parada: escanteios, faltas e impedimentos. 

def get_rows_with_previous(df: pd.DataFrame,
                        conditions: Dict[str, Union[str, int, float]]) -> pd.DataFrame:
    """Filtra as linhas de um DataFrame com base em condições dadas e inclui, se existir,
    a linha anterior a cada linha que corresponde às condições.

    Args:
        df (pd.DataFrame): Dataframe a ser filtrado.
        conditions (Dict[str, Union[str, int, float]]): Dicionário onde as chaves
        são as colunas e os valores que devem aparecer nessas colunas.

    Returns:
        pd.DataFrame: Dataframe apenas com as linhas que corresponde às condições e as
        anteriores quando existir.
    """
    indices = filter_df(df, conditions).index
    
    indices_to_save = []
    for index in indices:
        if index > 0:
            indices_to_save.append(index - 1)
        indices_to_save.append(index)
    indices_to_save = sorted(set(indices_to_save)) #evitar repetição

    return df.iloc[indices_to_save].reset_index(drop=True)


def is_headed_goal(df: pd.DataFrame, row_index: int) -> bool:
    """Confere se um evento é um gol de cabeça.

    Args:
        df (pd.DataFrame): Dataframe que contém os eventos.
        row_index (int): Índice da linha do evento a ser conferido.

    Returns:
        bool: True se refere-se a um gol de cabeça, e False caso contrário.
    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError("O primeiro argumento deve ser um DataFrame.")
    if not isinstance(row_index, int):
        raise TypeError("O segundo argumento deve ser um Int.")
    
    return df.loc[row_index, 'is_goal'] == 1 and df.loc[row_index, 'bodypart'] == 3


def is_same_match(df: pd.DataFrame, row_index_a: int, row_index_b: int) -> bool:
    """Confere se dois eventos ocorreram no mesmo jogo.

    Args:
        df (pd.DataFrame): Dataframe que contém os eventos.
        row_index_a (int): Índice da linha do primeiro evento.
        row_index_b (int): Índice da linha do segundo evento.

    Returns:
        bool: True se os eventos ocorreram no mesmo jogo, e False caso contrário.
    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError("O primeiro argumento deve ser um DataFrame.")
    if not isinstance(row_index_a, int):
        raise TypeError("O segundo argumento deve ser um Int.")
    if not isinstance(row_index_b, int):
        raise TypeError("O terceiro argumento deve ser um Int.")
    
    return df.loc[row_index_a, 'id_odsp'] == df.loc[row_index_b, 'id_odsp']


def origin_of_headed_goals(df: pd.DataFrame) -> pd.DataFrame:
    """Calcula a porcentagem das origens dos gols de cabeça.

    Args:
        df (pd.DataFrame): Dataframe que contém os gols de cabeça e os eventos
        anteriores.

    Returns:
        pd.DataFrame: DataFrame contendo as seguintes colunas:
                      - 'Origem': O tipo do evento anterior ao gol de cabeça.
                      - 'Porcentagem': A porcentagem referente a cada origem.
    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError("O argumento deve ser um DataFrame.")
    
    corners = 0
    fouls = 0
    offsides = 0
    others = 0

    for i in range(df.shape[0]):
        if i == 0 and is_headed_goal(df, i):
            others += 1
        elif (is_headed_goal(df, i) and is_same_match(df, i, i-1) and
            (df.loc[i, 'time'] - df.loc[i-1, 'time']) <= 1):

            if df.loc[i-1, 'event_type'] == 2:
                corners += 1
            elif df.loc[i-1, 'event_type'] == 3:
                fouls += 1
            elif df.loc[i-1, 'event_type'] == 9:
                offsides += 1
            else:
                others += 1

    total = corners + fouls + offsides + others
    if total == 0:
        return pd.DataFrame({'': ['Sem gols de cabeça']})
    results = pd.DataFrame({
        'ORIGEM': ['Escanteios', 'Faltas', 'Impedimentos', 'BOLA PARADA', 'Outros'],
        'PORCENTAGEM': [round((corners / total) * 100, 2), 
                        round((fouls / total) * 100, 2),
                        round((offsides / total) * 100, 2),
                        round(((corners + fouls + offsides) / total) * 100, 2), 
                        round((others / total) * 100, 2)]
        })

    return results


def graph_view(df: pd.DataFrame) -> None:
    """Salva um gráfico de barras que indicam as porcentagens das origens dos gols de
    cabeça.

    Args:
        df (pd.DataFrame): DataFrame que contém as porcentagens de cada origem.
    """
    plt.figure(figsize=(8, 6))
    plt.bar(df['ORIGEM'], df['PORCENTAGEM'],
            color=['#3889ce', '#3889ce', '#3889ce', '#3889ce', '#3889ce'])
    
    plt.title('Porcentagem das Origens dos Gols de Cabeça', color='white')
    plt.xlabel('Origem', color='white')
    plt.ylabel('Porcentagem', color='white')

    ax = plt.gca()
    ax.spines['bottom'].set_color('white')
    ax.spines['left'].set_color('white')
    ax.spines['top'].set_color('white')
    ax.spines['right'].set_color('white')

    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')

    plt.savefig('../data/graph_head.png',format='png', dpi=300, transparent=True)
    plt.plot()


def head_main(df: pd.DataFrame):
    """Função principal que executa a análise e visilação das origens dos gols de cabeça,
    utilizando as funções documentadas anteriormentes.

    Args:
        df (pd.DataFrame): DataFrame que contém os eventos.
    """
    remove_columns(df, ['side', 'shot_outcome', 'location'])
    df = get_rows_with_previous(df, {'bodypart': 3, 'is_goal': 1})

    percent_of_origins = origin_of_headed_goals(df)
    print_dataframe(percent_of_origins, "ORIGEM DOS GOLS DE CABEÇA")
    graph_view(percent_of_origins)
