import pandas as pd

filepath = "../data/events.csv"
df = pd.read_csv(filepath)

# Removendo colunas desnecessárias
remove_colums = ['id_odsp', 'id_event','sort_order','text','event_type2','event_team',
                 'opponent', 'player', 'player2','player_in','player_out', 'shot_place'
                ,'shot_outcome', 'assist_method', 'situation', 'fast_break']

for column in remove_colums:
    df.drop(column, axis=1, inplace=True)

# Removendo linhas com eventos desnecessários
# [Announcement, yellow card, second yellow card, red card, substitution, offside, hand ball]
remove_events = [0, 4, 5, 6, 7, 8, 10]
for events in remove_events: 
    df = df[df['event_type'] != events]

new_filepath = "../data/cleaned_events.csv"
df.to_csv(new_filepath)