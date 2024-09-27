import pandas as pd

filepath = "../data/cleaned_events.csv"
df = pd.read_csv(filepath)

# Removendo colunas que não acrescentam na analise
remove_colums = ['time', 'side', 'bodypart']

for column in remove_colums:
    df.drop(column, axis=1, inplace=True)


# Iremos verificar apenas Attempts 
df = df[df['event_type'] == 1]

# retirar não registrados e inuteis
df = df[df['location'] != 19]
df = df[df['location'] != 1]
df = df[df['location'] != 2]

# angulo dificil a direita ou a esquerda nao da informacao se é dentro
# ou fora da area, entao talvez seja mais vantajoso remover

df = df[df['location'] != 7]
df = df[df['location'] != 8]

# Agora, essa coluna não será mais necessaria

df.drop('event_type', axis=1, inplace=True)

df['situation'] = df['location'].apply(lambda x: 'inside' if x in [3, 9, 10, 11, 12, 13, 14] else 'outside')

# agora não precisaremos mais da linha de location


df.drop('location', axis=1, inplace=True)


# Verificando se "on target" == goal

'''

inconsistency = df[(df['is_goal'] == 1) & (df['shot_outcome'] != 1)]

if inconsistency.empty:
    return True

else:
    return False
'''

# É igual!!

# Traduzindo...
'''shot_outcome
1	On target
2	Off target
3	Blocked
4	Hit the bar'''

shots_mapping = {
    1.0: 'Gol', 
    2.0: 'Fora',
    3.0: 'Defendido',
    4.0: 'Trave'
}

df['shot_outcome'] = df['shot_outcome'].map(shots_mapping)


# Verificando o que foi gol e o que não foi e a relação com inside e outside
# Dos gols, vendo quantos são insides e quantos outsides

goals = df[df['is_goal'] == 1]

total_goals = len(goals)
goals_inside = len(goals[goals['situation'] == 'inside'])
goals_outside = len(goals[goals['situation'] == 'outside'])

# porcentagem
perc_inside = (goals_inside / total_goals) * 100
perc_outside = (goals_outside / total_goals) * 100

print(f'{" DOS GOLS ":=^40}')
print(f"Dentro da área: {perc_inside:.2f}%")
print(f"Fora da área:   {perc_outside:.2f}%")


def shot_outcome_by_situation(df, situation):
    attempts = df[df['situation'] == situation]
    return attempts['shot_outcome'].value_counts()

# Calculando porcentagens de outcomes fora e dentro da área
inside_attempts = shot_outcome_by_situation(df, 'inside')
sum_inside_attempts = sum(inside_attempts)

outside_attempts = shot_outcome_by_situation(df, 'outside')
sum_outside_attempts = sum(outside_attempts)


print(f'{" DOS CHUTES ":=^40}')

print()
print(f'Dentro da área: ')
for outcome, percentage in (inside_attempts / sum_inside_attempts).items():
    print(f"{outcome}: {percentage:.2%}")

print()
print(f'Fora da área: ')
for outcome, percentage in (outside_attempts / sum_outside_attempts).items():
    print(f"{outcome}: {percentage:.2%}")
