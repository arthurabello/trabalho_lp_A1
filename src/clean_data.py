import pandas as pd
from utils import remove_columns, remove_lines_by_condition

def main():
    filepath = "../data/events.csv"
    df = pd.read_csv(filepath)

    columns_to_remove = ['id_event','sort_order','text','event_type2','event_team',
                        'opponent', 'player', 'player2','player_in','player_out', 'shot_place'
                        ,'assist_method', 'situation', 'fast_break']

    remove_columns(df, columns_to_remove)

    events_to_remove = [0, 4, 5, 6, 7, 8, 10]
    remove_lines_by_condition(df, 'event_type', events_to_remove)
    
    new_filepath = "../data/cleaned_events.csv"
    df.to_csv(new_filepath, index=False)

if __name__ == '__main__':
    main()
