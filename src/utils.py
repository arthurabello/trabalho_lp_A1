import pandas as pd
from typing import List, Dict, Union

def remove_columns(df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
    """Remove colunas de um DataFrame

    Args:
        df (pd.DataFrame): DataFrame a ser recebido pela função
        columns (List[str]): Lista com os nomes das colunas a serem deletadas

    Returns:
        pd.DataFrame: Retorna o DataFrame com as colunas deletadas

    Raises:
        TypeError: Se `df` não for um pd.DataFrame ou `columns` não for uma lista.
        KeyError: Se alguma coluna em `columns` não existir no DataFrame.
        
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
    # raises
    if not isinstance(df, pd.DataFrame):
        raise TypeError("O parâmetro 'df' deve ser um pandas DataFrame.")
    
    if not isinstance(columns, List):
        raise TypeError("O parâmetro 'columns' deve ser uma lista")
    
    missing_columns = set(columns) - set(df.columns)
    if missing_columns:
        raise KeyError(f"As seguintes colunas não existem no DataFrame: {missing_columns}")


    # main code
    for column in columns:
            df.drop(column, axis=1, inplace=True)

    return df


def filter_df(df: pd.DataFrame, conditions: Dict[str, Union[str, int, float]]) -> pd.DataFrame:
    """Filtra o DataFrame com base em valores específicos de colunas dadas.

    Args:
        df (pd.DataFrame): DataFrame a ser recebido pela função.
        conditions (Dict[str, Union[str, int, float]]): Condições a serem usadas
        pelo filtro.

    Returns:
        pd.DataFrame: DataFrame filtrado contendo apenas as linhas que atendem as soluções.

    Raises:
        TypeError: Se `df` não for um pd.DataFrame ou `conditions` não for um dicionário.
        KeyError: Se alguma coluna em `conditions` não existir no DataFrame.

    Examples:
        >>> data = [
        ...        [1, 'Arnaldo', 7.0], 
        ...        [2, 'Bernaldo', 8.5], 
        ...        [3, 'Cernaldo', 7.0]
        ...        ]
        >>> df = pd.DataFrame(data, columns=['ID', 'Nome', 'Nota'])
        >>> filter_df(df, {'Nota': 7.0})
           ID      Nome  Nota
        0   1   Arnaldo   7.0
        2   3  Cernaldo   7.0
    """
    # raises
    if not isinstance(df, pd.DataFrame):
        raise TypeError("O parâmetro 'df' deve ser um pandas DataFrame.")
    
    if not isinstance(conditions, Dict):
        raise TypeError("O parâmetro 'conditions' deve ser um dicionário")
    
    for column in conditions:
        if column not in df.columns:
            raise KeyError(f"A coluna '{column}' não existe no DataFrame.")

    # main code
    for column, value in conditions.items():
        df = df[df[column] == value]
    
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

    Raises:
        TypeError: Se `df` não for um pd.DataFrame ou `conditions` não for uma lista.
        KeyError: Se a coluna 'column' não existir no DataFrame.
    
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
    
    # raises
    if not isinstance(df, pd.DataFrame):
        raise TypeError("O parâmetro 'df' deve ser um pandas DataFrame.")

    if not isinstance(conditions, List):
        raise TypeError("O parâmetro 'conditions' deve ser uma lista.")
    
    if column not in df.columns:
        raise KeyError(f"A coluna '{column}' não existe no DataFrame.")
    
    # main code
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
    
    Raises:
        TypeError: Se `df` não for um pd.DataFrame ou `map` não for um dicionário.
        KeyError: Se a coluna 'column' não existir no DataFrame.

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
    
    # raises
    if not isinstance(df, pd.DataFrame):
        raise TypeError("O parâmetro 'df' deve ser um pandas DataFrame.")

    if not isinstance(map, Dict):
        raise TypeError("O parâmetro 'map' deve ser um dicionário.")
    
    if column not in df.columns:
        raise KeyError(f"A coluna '{column}' não existe no DataFrame.")
    
    # main code
    df[column] = df[column].map(map)

    return df

def print_dataframe(df: pd.DataFrame, title: str) -> None:
    """Imprime o DataFrame com um título fornecido.

    Args:
        df (pd.DataFrame): O DataFrame a ser exibido.
        titulo (str): O título a ser exibido acima do DataFrame.
    
    Raises:
        TypeError: Se `df` não for um pd.DataFrame ou `title` não for uma string.
    """
    # raises
    if not isinstance(df, pd.DataFrame):
        raise TypeError("O parâmetro 'df' deve ser um pandas DataFrame.")
    
    if not isinstance(title, str):
        raise TypeError("O parâmetro 'title' deve ser uma string.")
    
    # main code
    print('-'*50)
    print(f'{f"  {title}  ":=^50}')
    print('-'*50)
    print(df.to_string(index=False))

