import pandas as pd
from typing import List

def remove_columns(df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
    for column in columns:
        df.drop(column, axis=1, inplace=True)
    
    return df


def filter(df: pd.DataFrame, column: str ,x: int) -> pd.DataFrame: # melhorar nome
    df = df[df[column] == x]
    return df


def remove_lines_by_condition(df: pd.DataFrame, column: str, conditions: List[int]) -> pd.DataFrame:
    for cond in conditions:
        df = df[df[column] != cond]
    return df

'''def checking_on_target(df: pd.DataFrame):
    inconsistency = df[(df['is_goal'] == 1) & (df['shot_outcome'] != 1)]
    if inconsistency.empty:
        return True
    else:
        return False
    return inconsistency
'''
def map_shot_outcomes(df: pd.DataFrame) -> pd.DataFrame:
    shots_mapping = {
        1.0: 'Gol', 
        2.0: 'Fora',
        3.0: 'Defendido',
        4.0: 'Trave'
    }
    df['shot_outcome'] = df['shot_outcome'].map(shots_mapping)
    return df


def calculate_goal_percentages(goals: pd.DataFrame) -> tuple:
    total_goals = len(goals)
    goals_inside = len(goals[goals['situation'] == 'inside'])
    goals_outside = len(goals[goals['situation'] == 'outside'])

    perc_inside = (goals_inside / total_goals) * 100
    perc_outside = (goals_outside / total_goals) * 100

    return perc_inside, perc_outside


def print_goal_percentages(perc_inside, perc_outside):

    print(f'{" DOS GOLS ":=^40}')
    print(f"Dentro da área: {perc_inside:.2f}%")
    print(f"Fora da área:   {perc_outside:.2f}%\n")


def shot_outcome_by_situation(df: pd.DataFrame, situation: str) -> dict:
        attempts = df[df['situation'] == situation]
        return attempts['shot_outcome'].value_counts()


def print_shot_outcome_percent(df: pd.DataFrame) -> None:
    inside_attempts = shot_outcome_by_situation(df, 'inside')
    sum_inside_attempts = sum(inside_attempts)

    outside_attempts = shot_outcome_by_situation(df, 'outside')
    sum_outside_attempts = sum(outside_attempts)

    print(f'{" DOS CHUTES ":=^40}')

    print(f'\nDentro da área: ')
    for outcome, percent in (inside_attempts / sum_inside_attempts).items():
        print(f"{outcome:>10}: {percent:.2%}")

    print(f'\nFora da área: ')
    for outcome, percent in (outside_attempts / sum_outside_attempts).items():
        print(f"{outcome:>10}: {percent:.2%}")

def main():

    filepath = "../data/cleaned_events.csv"
    df = pd.read_csv(filepath)

    # Removendo colunas que não acrescentam na analise
    remove_columns(df, ['time', 'side', 'bodypart'])

    # Iremos verificar apenas Attempts 
    filter(df, 'event_type', 1)

    # retirar não registrados e inuteis
    # 7 e 8 angulo dificil a direita ou a esquerda nao da informacao se é dentro
    # ou fora da area, entao sera mais vantajoso remover
    remove_lines_by_condition(df, 'location', [1, 2, 7, 8, 19])

    # Agora, essa coluna não será mais necessaria

    remove_columns(df, ['event_type'])

    locations_inside = [3, 9, 10, 11, 12, 13, 14]
    df['situation'] = df['location'].apply(lambda x: 'inside' if x in locations_inside else 'outside')

    # agora não precisaremos mais da linha de location

    remove_columns(df, ['location'])

    # Verificando o que foi gol e o que não foi e a relação com inside e outside
    # Dos gols, vendo quantos são insides e quantos outsides

    map_shot_outcomes(df)
    
    goals = filter(df,'is_goal', 1)

    perc_inside, perc_outside = calculate_goal_percentages(goals)

    # Imprimir porcentagens de gols
    print_goal_percentages(perc_inside, perc_outside)

    # Calculando porcentagens de outcomes fora e dentro da área
    print_shot_outcome_percent(df)

if __name__ == '__main__':
    main()