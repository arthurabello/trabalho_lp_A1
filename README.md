# Análise de Eventos de Futebol

Este projeto foi desenvolvido para a avaliação A1 da disciplina de Linguagens de Programação da FGV/EMAp. Consiste em uma análise do dataset [Football Events](https://www.kaggle.com/datasets/secareanualin/football-events).

## Objetivos

Avaliar as seguintes hipóteses:

1. O time da casa ganha mais? (Arthur Rabello Oliveira)
2. A maioria dos gols de cabeça surgem de bola parada? (Antonio Francisco Batista Filho)
3. Chute de fora da área tem menor chance de conversão a gol? (Rodrigo Severo Araújo)

## Estrutura do Projeto

- Branches individuais: `branch-rabello`, `branch-rodri`, `branch-batista`
  - Contêm scripts que avaliam as hipóteses usando bibliotecas de data science
- Branch `main`: 
  - Contém o script que sumariza os resultados
  - Gera DataFrames e visualizações gráficas

## Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/arthurabello/trabalho_lp_A1.git
   cd trabalho_lp_A1
   ```

2. Instale as dependências (recomenda-se usar um ambiente virtual):
   ```bash
   pip install -r requirements.txt
   ```

3. Execute o script principal:
   ```bash
   cd src
   python3 main.py
   ```
