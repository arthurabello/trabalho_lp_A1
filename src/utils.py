import pandas as pd
from typing import List, Dict, Union

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

def print_dataframe(df: pd.DataFrame, title: str) -> None:
    """Imprime o DataFrame com um título fornecido.

    Args:
        df (pd.DataFrame): O DataFrame a ser exibido.
        titulo (str): O título a ser exibido acima do DataFrame.
    """
    print('-'*50)
    print(f'{f"  {title}  ":=^50}')
    print('-'*50)
    print(df.to_string(index=False))

