import pandas as pd

df = pd.read_csv('../events.csv')

# Remover colunas e linhas desnecessárias

df.drop(['id_odsp', 'id_event', 'sort_order', 'text', 'event_type2', 'event_team', 'opponent', 'player', 'player2', 'player_in',
         'player_out', 'shot_place', 'shot_outcome', 'assist_method', 'situation', 'fast_break'], axis=1, inplace=True)

events_to_be_removed = [0, 4, 5, 6, 7, 8, 10]
for event in events_to_be_removed:
    df = df[df['event_type'] != event]

df.reset_index(drop=True, inplace=True)
df.to_csv('cleaned_file.csv', index=False)

# Criar arquivo com cabeceio e eventos anteriores

head_index = df[df['bodypart'] == 3].index
index_to_save = []

for index in head_index:
    if index > 0:
        index_to_save.append(index - 1)
    index_to_save.append(index)
indices_to_save = sorted(set(index_to_save)) #evita repetição em caso de cabeceio seguido de cabeceio

new_df = df.iloc[indices_to_save]
new_df.to_csv('head_part.csv', index=False)
print(new_df.head(50))
