import pandas as pd
from utils import remove_columns, remove_lines_by_condition

def clean_data(df: pd.DataFrame) -> None:
    """Remove todas as colunas que não serão necessárias para a análise exploratória
    e salva em um novo arquivo "cleaned_events.csv"

    Args:
        df (pd.DataFrame): DataFrame de events.csv

    """
    columns_to_remove = ['id_event','sort_order','text','event_type2','event_team',
                        'opponent', 'player', 'player2','player_in','player_out',
                        'shot_place','assist_method', 'situation', 'fast_break']
    remove_columns(df, columns_to_remove)

    events_to_remove = [0, 4, 5, 6, 7, 8, 10]
    remove_lines_by_condition(df, 'event_type', events_to_remove)
    
    new_filepath = "../data/cleaned_events.csv"
    df.to_csv(new_filepath, index=False)
