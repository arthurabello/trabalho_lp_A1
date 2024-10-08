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

def main():
    filepath = "../data/cleaned_events.csv"
    df = pd.read_csv(filepath)

    remove_columns(df, ['side', 'shot_outcome', 'location'])
    df = get_rows_with_previous(df, {'bodypart': 3, 'is_goal': 1})

    dead_ball_types = [2, 3, 9]

    print(df.head(50))

if __name__ == '__main__':
    main()