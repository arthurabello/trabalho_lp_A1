import pandas as pd
import doctest
from typing import List, Tuple, Dict, Union

def remove_columns(df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
    """Remove colunas de um DataFrame

    Args:
        df (pd.DataFrame): DataFrame a ser recebido pela função
        columns (List[str]): Lista com os nomes das colunas a serem deletadas

    Returns:
        pd.DataFrame: Retorna o DataFrame com as colunas deletadas
    
    Examples:
        >>> data = [
        ...        [1, 'Arnaldo', 7.0], 
        ...        [2, 'Bernaldo', 8.5], 
        ...        [3, 'Cernaldo', 9.7]
        ...        ]
        >>> df = pd.DataFrame(data, columns=['ID', 'Nome', 'Nota'])
        >>> remove_columns(df, ['ID', 'Nome'])
           Nota
        0   7.0
        1   8.5
        2   9.7
    """
    for column in columns:
        df.drop(column, axis=1, inplace=True)
    
    return df


def filter_df(df: pd.DataFrame, column: str , x: Union[str, int, float]) -> pd.DataFrame:
    """Filtra o DataFrame com base em um valor específico de uma coluna dada.

    Args:
        df (pd.DataFrame): DataFrame a ser recebido pela função.
        column (str): Nome da coluna a ser usada para o filtro.
        x (Union[str, int, float]): Elemento a ser filtrado na coluna especificada.

    Returns:
        pd.DataFrame: DataFrame filtrado contendo apenas as linhas onde o valor da coluna é igual a x.
    
    Examples:
        >>> data = [
        ...        [1, 'Arnaldo', 7.0], 
        ...        [2, 'Bernaldo', 8.5], 
        ...        [3, 'Cernaldo', 7.0]
        ...        ]
        >>> df = pd.DataFrame(data, columns=['ID', 'Nome', 'Nota'])
        >>> filter_df(df, 'Nota', 7.0)
           ID      Nome  Nota
        0   1   Arnaldo   7.0
        2   3  Cernaldo   7.0
    """
    df = df[df[column] == x]
    
    return df


def remove_lines_by_condition(df: pd.DataFrame, column: str, conditions: List[Union[str, int, float]]) -> pd.DataFrame:
    """Remove linhas de um DataFrame com base em condições específicas.

    Args:
        df (pd.DataFrame): DataFrame a ser recebido pela função.
        column (str): Nome da coluna a ser usada para verificar as condições.
        conditions (List[Union[str, int, float]]): Lista de valores que, se encontrados 
        na coluna especificada, resultarão na remoção das linhas correspondentes.

    Returns:
        pd.DataFrame: DataFrame filtrado sem as linhas que atendem às condições.

    Examples:
        >>> data = [
        ...        [1, 'Arnaldo', 7.0], 
        ...        [2, 'Bernaldo', 8.5], 
        ...        [3, 'Cernaldo', 7.0]
        ...        ]
        >>> df = pd.DataFrame(data, columns=['ID', 'Nome', 'Nota'])
        >>> remove_lines_by_condition(df, 'Nota', [7.0])
           ID      Nome  Nota
        1   2  Bernaldo   8.5

    """
    for cond in conditions:
        df = df[df[column] != cond]
    return df

def map_column_values(df: pd.DataFrame, column: str, map: Dict) -> pd.DataFrame:
    """Mapeia os valores de uma coluna específica de acordo com um mapeamento
    dado por meio de um dicionário.

    Args:
        df (pd.DataFrame): DataFrame a ser recebido pela função.
        column (str): Nome da coluna que será mapeada.
        map (Dict): Dicionário de mapeamento dos valores.

    Returns:
        pd.DataFrame: Dataframe com a coluna mapeada.
    
    Examples:
        >>> data = [
        ...        [1, 'Arnaldo', 7.0], 
        ...        [2, 'Bernaldo', 8.5], 
        ...        [3, 'Cernaldo', 7.0]
        ...        ]
        >>> df = pd.DataFrame(data, columns=['ID', 'Nome', 'Nota'])
        >>> mapping = {'Arnaldo': 'Aluno 1', 'Bernaldo': 'Aluno 2', 'Cernaldo': 'Aluno 3'}
        >>> map_column_values(df, 'Nome', mapping)
           ID     Nome  Nota
        0   1  Aluno 1   7.0
        1   2  Aluno 2   8.5
        2   3  Aluno 3   7.0"""
    
    df[column] = df[column].map(map)

    return df


def calculate_goals(goals: pd.DataFrame) -> Tuple:

    total_goals = goals.shape[0]
    goals_inside = filter_df(goals, 'situation', 'inside').shape[0]
    goals_outside = filter_df(goals, 'situation', 'outside').shape[0]

    perc_inside = (goals_inside / total_goals) * 100
    perc_outside = (goals_outside / total_goals) * 100

    return perc_inside, perc_outside


def print_goals(perc_inside: float, perc_outside: float) -> None:
    print(f'{" ESTATÍSTICAS POR GOLS ":=^40}')
    print('-'*40)
    print(f'Dentro da área | {perc_inside:.2f}%')
    print(f'Fora da área   | {perc_outside:.2f}%')
    print('-'*40)

# Usando dataframe
def shot_outcome_by_situation(df: pd.DataFrame, situation: str) -> pd.DataFrame:
    attempts = filter_df(df, 'situation', situation)['shot_outcome'].value_counts().reset_index()
    attempts.columns = ['Resultado', 'count']
    return attempts

def perc_attempts(df: pd.DataFrame, situation: str) -> pd.DataFrame:
    attempts = shot_outcome_by_situation(df, situation)
    attempts['Porcentagem'] = (attempts['count'] / attempts['count'].sum()) * 100
    attempts['Porcentagem'] = attempts['Porcentagem'].round(2)
    remove_columns(attempts, ['count'])
    return attempts

def print_shot_outcome(df: pd.DataFrame) -> None:

    perc_inside_attempts = perc_attempts(df, 'inside')
    perc_outside_attempts = perc_attempts(df, 'outside')

    print(f'{" ESTATÍSTICAS POR CHUTE ":=^40}')
    print('-'*40)
    print(f'Dentro da área: ')
    print(perc_inside_attempts)

    print('-'*40)
    print(f'Fora da área: ')
    print(perc_outside_attempts)
    print('-'*40)

def main():

    filepath = "../data/cleaned_events.csv"
    df = pd.read_csv(filepath)

    df = remove_columns(df, ['time', 'side', 'bodypart'])
    df = filter_df(df, 'event_type', 1)
    df = remove_lines_by_condition(df, 'location', [1, 2, 7, 8, 19])
    df = remove_columns(df, ['event_type'])

    locations_inside = [3, 9, 10, 11, 12, 13, 14]
    df['situation'] = df['location'].apply(lambda x: 'inside' if x in locations_inside else 'outside')

    df = remove_columns(df, ['location'])

    shots_mapping = {1.0: 'Gol', 2.0: 'Fora',3.0: 'Defendido', 4.0: 'Trave'}
    df = map_column_values(df, 'shot_outcome', shots_mapping)
    
    goals = filter_df(df,'is_goal', 1)
    perc_inside, perc_outside = calculate_goals(goals)

    print_goals(perc_inside, perc_outside)
    
    print_shot_outcome(df)

if __name__ == '__main__':
    main()