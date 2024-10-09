# Análise da Hipótese - Arthur Rabello Oliveira

Esta branch foi construída para avaliar a seguinte hipótese:

**- O time da casa ganha mais do que perde na maioria dos jogos da database?**

Os resultados do script indicam que sim, de fato o time da casa ganha mais, e esta conclusão está defendida e demonstrada no script construído em `rabello_hypothesis.py`, cuja descrição segue abaixo:

## Funcionalidades

1. **Carregamento do Dataset**: A função `load_dataset(csv_path)` carrega os dados a partir de um arquivo CSV especificado. Ela garante que o caminho fornecido seja uma string e que qualquer erro apropriado seja reportado.

2. **Agrupamento de Gols por Partida**: A função `group_goals_by_match(df)` agrupa os eventos de gols por partida e lado do time (casa ou visitante). Ela valida a estrutura do DataFrame e garante que colunas essenciais estejam presentes.

3. **Cálculo de Resultados**: A função `calculate_results(goals_per_match)` determina o resultado de cada partida com base nos gols marcados pelos times da casa e visitantes, adicionando uma coluna `result` ao DataFrame.

4. **Criação do DataFrame Resumo**: A função `create_summary_dataframe(goals_per_match)` cria um DataFrame com as porcentagens de vitórias, derrotas e empates do time da casa, baseado nos resultados calculados.

5. **Plotagem do Resumo**: A função `plot_summary(summary_df)` gera um gráfico de barras visualizando as porcentagens de vitórias, derrotas e empates, facilitando a análise visual dos resultados.

6. **Função Principal**: A função `main()` orquestra a execução do código, chamando as funções em sequência e exibindo o DataFrame final com as porcentagens calculadas. O resultado é impresso no console e o gráfico é exibido ao usuário.

## Como Executar

Para executar o código, certifique-se de ter as requirements instaladas. Siga o comando de instalação (recomendamos que faça isto em um ambiente virtual `venv` para evitar conflitos com outros pacotes globais).

```bash
pip install -r requirements.txt
python rabello_hypothesis.py
