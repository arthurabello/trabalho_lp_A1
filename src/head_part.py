import pandas as pd
from typing import Dict, Union

from utils import remove_columns, filter_df

def get_rows_with_previous(df: pd.DataFrame, conditions: Dict[str, Union[str, int, float]]) -> pd.DataFrame:
    """Filtra as linhas de um DataFrame com base em um valor específico de uma coluna
    dada e inclui, se existir, a linha anterior a cada linha que corresponde a condição.

    Args:
        df (pd.DataFrame): Dataframe a ser filtrado.
        column (str): Coluna a ser usada para base do filtro.
        x (Union[str, int, float]): Elemento a ser filtrado.

    Returns:
        pd.DataFrame: Dataframe apenas com as linhas que corresponde a condição e as
        anteriores quando houver.
    """
    indices = filter_df(df, conditions).index
    indices_to_save = []

    for index in indices:
        if index > 0:
            indices_to_save.append(index - 1)
        indices_to_save.append(index)
    indices_to_save = sorted(set(indices_to_save))

    return df.iloc[indices_to_save].reset_index(drop=True)

def is_headed_goal(df: pd.DataFrame, row_index: int) -> bool:
    """Confere se um evento é um gol de cabeça.

    Args:
        df (pd.DataFrame): Dataframe que contém os eventos.
        row_index (int): Índice da linha do evento a ser conferido.

    Returns:
        bool: True se refere-se a um gol de cabeça, e False caso contrário.
    """
    if df.loc[row_index, 'is_goal'] == 1 and df.loc[row_index, 'bodypart'] == 3:
        return True
    else:
        return False

def is_same_match(df: pd.DataFrame, row_index_a: int, row_index_b: int) -> bool:
    """Confere se dois eventos ocorreram no mesmo jogo.

    Args:
        df (pd.DataFrame): Dataframe que contém os eventos.
        row_index_a (int): Índice da linha do primeiro evento.
        row_index_b (int): Índice da linha do segundo evento.

    Returns:
        bool: True se os eventos ocorreram no mesmo jogo, e False caso contrário.
    """
    if df.loc[row_index_a, 'id_odsp'] == df.loc[row_index_b, 'id_odsp']:
        return True
    else:
        return False

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
    corners = 0
    fouls = 0
    offsides = 0
    others = 0
    for i in range(df.shape[0]):
        if (is_headed_goal(df, i) and is_same_match(df, i, i-1) and
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

    results = pd.DataFrame({
    'Origem': ['Escanteios', 'Faltas', 'Impedimentos', 'Outros'],
    'Porcentagem': [round((corners / total) * 100, 2), 
                    round((fouls / total) * 100, 2),
                    round((offsides / total) * 100, 2), 
                    round((others / total) * 100, 2)]
})

    return results

def main():
    filepath = "../data/cleaned_events.csv"
    df = pd.read_csv(filepath)

    remove_columns(df, ['side', 'shot_outcome', 'location'])
    df = get_rows_with_previous(df, {'bodypart': 3, 'is_goal': 1})

    c = origin_of_headed_goals(df)
    print(c)

if __name__ == '__main__':
    main()