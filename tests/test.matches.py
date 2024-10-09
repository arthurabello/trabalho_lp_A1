import sys
import pandas as pd
import unittest

sys.path.append('../src')

from matches import (
    load_dataset,
    group_goals_by_match,
    calculate_results,
    create_summary_dataframe,
    plot_summary
)

def test_load_dataset_valid():

    """
    Testa a função load_dataset com um caminho de arquivo CSV válido
    Verifica se o resultado é um DataFrame
    """

    df = load_dataset('../data/cleaned_events.csv')
    assert isinstance(df, pd.DataFrame), "O resultado deve ser um DataFrame"

def test_load_dataset_invalid_path():

    """
    Testa a função load_dataset com um caminho de arquivo CSV inválido
    Verifica se uma FileNotFoundError é levantada
    """

    try:
        load_dataset('invalid_path.csv')
    except FileNotFoundError:
        pass
    else:
        assert False, "Esperava FileNotFoundError"

def test_group_goals_by_match_valid():

    """
    Testa a função group_goals_by_match com um DataFrame válido
    Verifica se o resultado contém as colunas 'home' e 'away'
    """

    data = {
        'id_odsp': [1, 1, 2, 2, 3, 3],
        'side': ['home', 'away', 'home', 'away', 'home', 'away'],
        'event_type': [1, 1, 1, 1, 1, 1],
        'is_goal': [1, 0, 0, 1, 1, 1]
    }
    df = pd.DataFrame(data)

    goals_per_match = group_goals_by_match(df)
    assert isinstance(goals_per_match, pd.DataFrame), "O resultado deve ser um DataFrame"
    assert 'home' in goals_per_match.columns, "A coluna 'home' deve estar presente"
    assert 'away' in goals_per_match.columns, "A coluna 'away' deve estar presente"

def test_group_goals_by_match_invalid_type():

    """
    Testa a função group_goals_by_match com um tipo de entrada inválido
    Verifica se uma TypeError é levantada
    """

    try:
        group_goals_by_match('invalid input')
    except TypeError:
        pass
    else:
        assert False, "Esperava TypeError"

def test_calculate_results_valid():

    """
    Testa a função calculate_results com um DataFrame válido
    Verifica se a coluna 'result' está presente no resultado
    """

    data = {
        'id_odsp': [1, 1, 2, 2, 3, 3],
        'side': ['home', 'away', 'home', 'away', 'home', 'away'],
        'event_type': [1, 1, 1, 1, 1, 1],
        'is_goal': [1, 0, 0, 1, 1, 1]
    }
    df = pd.DataFrame(data)
    goals_per_match = group_goals_by_match(df)

    results = calculate_results(goals_per_match)
    assert 'result' in results.columns, "A coluna 'result' deve estar presente"

def test_calculate_results_invalid_type():

    """
    Testa a função calculate_results com um tipo de entrada inválido
    Verifica se uma TypeError é levantada
    """

    try:
        calculate_results('invalid input')
    except TypeError:
        pass
    else:
        assert False, "Esperava TypeError"

def test_create_summary_dataframe_valid():

    """
    Testa a função create_summary_dataframe com um DataFrame válido
    Verifica se a coluna 'home_percentage' está presente no resultado
    """

    data = {
        'id_odsp': [1, 1, 2, 2, 3, 3],
        'side': ['home', 'away', 'home', 'away', 'home', 'away'],
        'event_type': [1, 1, 1, 1, 1, 1],
        'is_goal': [1, 0, 0, 1, 1, 1]
    }
    df = pd.DataFrame(data)
    goals_per_match = group_goals_by_match(df)
    results = calculate_results(goals_per_match)

    summary_df = create_summary_dataframe(results)
    assert isinstance(summary_df, pd.DataFrame), "O resultado deve ser um DataFrame"
    assert 'home_percentage' in summary_df.columns, "A coluna 'home_percentage' deve estar presente"

def test_create_summary_dataframe_invalid_type():

    """
    Testa a função create_summary_dataframe com um tipo de entrada inválido
    Verifica se uma TypeError é levantada
    """

    try:
        create_summary_dataframe('invalid input')
    except TypeError:
        pass
    else:
        assert False, "Esperava TypeError"

def test_plot_summary_valid():

    """
    Testa a função plot_summary com um DataFrame válido
    Verifica se não ocorre exceção durante a execução
    """

    data = {
        'id_odsp': [1, 1, 2, 2, 3, 3],
        'side': ['home', 'away', 'home', 'away', 'home', 'away'],
        'event_type': [1, 1, 1, 1, 1, 1],
        'is_goal': [1, 0, 0, 1, 1, 1]
    }
    df = pd.DataFrame(data)
    goals_per_match = group_goals_by_match(df)
    results = calculate_results(goals_per_match)
    summary_df = create_summary_dataframe(results)

    try:
        plot_summary(summary_df)
    except Exception as e:
        assert False, f"plot_summary levantou uma exceção inesperada: {e}"

if __name__ == '__main__':
    
    test_load_dataset_valid()
    test_load_dataset_invalid_path()
    test_group_goals_by_match_valid()
    test_group_goals_by_match_invalid_type()
    test_calculate_results_valid()
    test_calculate_results_invalid_type()
    test_create_summary_dataframe_valid()
    test_create_summary_dataframe_invalid_type()
    test_plot_summary_valid()

    print("Todos os testes passaram!")
