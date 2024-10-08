import pandas as pd

df = pd.read_csv('../data/cleaned_events.csv')

# Criar arquivo com cabeceio e eventos anteriores
head_index = df[df['bodypart'] == 3].index
index_to_save = []

for index in head_index:
    if index > 0:
        index_to_save.append(index - 1)
    index_to_save.append(index)
indices_to_save = sorted(set(index_to_save)) #evita repetição em caso de cabeceio seguido de cabeceio

new_df = df.iloc[indices_to_save]
new_df.to_csv('../data/head_part.csv', index=False)
print(new_df.head(50))
