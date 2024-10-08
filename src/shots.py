import pandas as pd
import matplotlib.pyplot as plt

from utils import remove_columns, remove_lines_by_condition, filter_df, map_column_values, print_dataframe

# Hipotese: Chutes de dentro da area tem mais chance de conversão a gol

def calculate_goals(goals: pd.DataFrame) -> pd.DataFrame:
    """Recebe um Dataframe com todos os gols e calcula a porcentagem de gols que 
    foram feitos dentro da área e a porcentagem de gols feitos fora da área.

    Args:
        goals (pd.DataFrame): DataFrame a ser recebido pela função.
    
    Returns:
        pd.DataFrame: Um DataFrame contendo duas colunas:
                      - 'Situação': A situação do gol ('Dentro da área' ou 'Fora da área').
                      - 'Porcentagem': A porcentagem de gols feitos em cada situação.
    """

    total_goals = goals.shape[0]
    goals_inside = filter_df(goals, {'situation': 'inside'}).shape[0]
    goals_outside = filter_df(goals, {'situation': 'outside'}).shape[0]

    perc_inside = (goals_inside / total_goals) * 100
    perc_outside = (goals_outside / total_goals) * 100

    results = pd.DataFrame({
        'Situação': ['Dentro da área', 'Fora da área'],
        'Porcentagem': [round(perc_inside, 2), round(perc_outside, 2)]
    })

    return results

def shot_outcome_count(df: pd.DataFrame) -> pd.DataFrame:
    """Conta a frequência de cada resultado de chute (shot_outcome) dentro e fora da área.
    Os resultados são agrupados em um Dataframe com as contagens separadas para chutes feitos
    dentro e fora da área.

    Args:
        df (pd.DataFrame): DataFrame contendo os dados dos chutes, onde cada linha representa um chute
                           e inclui informações sobre o resultado do chute e a situação (dentro ou fora da área).

    Returns:
        pd.DataFrame: DataFrame contendo as seguintes colunas:
                      - 'Resultado': O tipo de resultado do chute ('Gol', 'Fora', 'Defendido' ou 'Trave').
                      - 'count_in': A contagem de resultados para chutes feitos dentro da área.
                      - 'count_out': A contagem de resultados para chutes feitos fora da área.
    """
    attempts_inside = filter_df(df, {'situation': 'inside'})['shot_outcome'].value_counts().reset_index()
    attempts_outside = filter_df(df, {'situation': 'outside'})['shot_outcome'].value_counts().reset_index()
    attempts = attempts_inside.merge(attempts_outside, on='shot_outcome', suffixes=('_in', '_out'))

    attempts.columns = ['Resultado', 'count_in', 'count_out']
    return attempts

def perc_shot_outcome(df: pd.DataFrame) -> pd.DataFrame:
    """Calcula a porcentagem de cada resultado de chute (shot_outcome) dentro e fora da área.
    Esta função transforma as contagens de cada um dos resultados de chute obtidos a partir da função 
    `shot_outcome_count` em porcentagens. Os resultados são agrupados em um Dataframe com as porcentagens 
    separadas para chutes feitos dentro e fora da área.

    Args:
        df (pd.DataFrame): DataFrame contendo os dados dos chutes, onde cada linha representa um chute
                           e inclui informações sobre o resultado do chute e a situação (dentro ou fora da área).

    Returns:
        pd.DataFrame: DataFrame contendo as seguintes colunas:
                      - 'Resultado': O tipo de resultado do chute.
                      - 'Porcentagem_in': A porcentagem de chutes dentro da área para cada resultado.
                      - 'Porcentagem_out': A porcentagem de chutes fora da área para cada resultado.
    """

    attempts = shot_outcome_count(df)
    attempts['Porcentagem_in'] = ((attempts['count_in'] / attempts['count_in'].sum()) * 100).round(2)
    attempts['Porcentagem_out'] = ((attempts['count_out'] / attempts['count_out'].sum()) * 100).round(2)

    remove_columns(attempts, ['count_in','count_out'])
    return attempts

def adjust_shot_outcome_df(df: pd.DataFrame) -> pd.DataFrame:
    """Ajusta a coluna 'shot_outcome' do DataFrame para criar uma nova categoria que separa
    os chutes no alvo ('On target') em 'Gol' e 'Defendido' com base no valor de 'is_goal'.
    
    Args:
        df (pd.DataFrame): DataFrame a ser recebido pela função.
    
    Returns:
        pd.DataFrame: DataFrame atualizado com a coluna 'shot_outcome' ajustada.
    """
    
    df['shot_outcome'] = df.apply(
        lambda row: 'Gol' if row['shot_outcome'] == 'No alvo' and row['is_goal'] == 1 
                    else 'Defendido' if row['shot_outcome'] == 'No alvo' and row['is_goal'] == 0
                    else row['shot_outcome'], axis=1
    )
    
    return df

def graph_view(df: pd.DataFrame) -> None:
    """Exibe um gráfico de barras duplas das porcentagens de resultados de chutes.

    Esta função cria e salva um gráfico de barras duplas que compara as porcentagens de resultados 
    de chutes dentro e fora da área para cada resultado de chute. O gráfico é salvo como uma imagem PNG.

    Args:
        df (pd.DataFrame): DataFrame contendo dados de chutes, que será utilizado para calcular as 
                           porcentagens que serão exibidas no gráfico.
    """
    attempts = perc_shot_outcome(df) 
    
    attempts.set_index('Resultado').plot.bar(title='Chutes dentro e fora da área', color=['lightblue', 'orange'])

    plt.xlabel('Resultado do chute')
    plt.ylabel('Porcentagem')
    plt.legend(title='Situação', labels=['Dentro da Área', 'Fora da Área'])
    plt.xticks(rotation=0)
    plt.ylim(0, 50) 

    plt.savefig('graph_shots.png',format='png', dpi=300)


def main():

    filepath = "../data/cleaned_events.csv"
    df = pd.read_csv(filepath)

    df = remove_columns(df, ['time', 'side', 'bodypart'])
    df = filter_df(df, {'event_type': 1})
    df = remove_lines_by_condition(df, 'location', [1, 2, 7, 8, 19])
    df = remove_columns(df, ['event_type'])

    locations_inside = [3, 9, 10, 11, 12, 13, 14]
    df['situation'] = df['location'].apply(lambda x: 'inside' if x in locations_inside else 'outside')

    df = remove_columns(df, ['location'])

    shots_mapping = {1.0: 'No alvo', 2.0: 'Fora', 3.0: 'Bloqueado', 4.0: 'Trave'}
    df = map_column_values(df, 'shot_outcome', shots_mapping)

    df = adjust_shot_outcome_df(df)
    
    goals = filter_df(df, {'is_goal': 1})
    stats_goals = calculate_goals(goals)

    perc_attempts = perc_shot_outcome(df)

    print_dataframe(stats_goals, "ESTATÍSTICAS POR GOL")
    print_dataframe(perc_attempts, "ESTATÍSTICAS POR CHUTE")

    graph_view(df)

if __name__ == '__main__':
    main()