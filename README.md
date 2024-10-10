# Análise de Eventos de Futebol

Este projeto foi desenvolvido como parte da avaliação A1 da disciplina de Linguagens de Programação da FGV/EMAp. O objetivo é realizar uma análise aprofundada do dataset [Football Events](https://www.kaggle.com/datasets/secareanualin/football-events) para testar três hipóteses relacionadas ao desempenho em partidas de futebol.

## Objetivos

As hipóteses avaliadas são:

1. **O time da casa ganha mais partidas?**  
   Autor: *Arthur Rabello Oliveira*

2. **A maioria dos gols de cabeça ocorre após uma bola parada?**  
   Autor: *Antonio Francisco Batista Filho*

3. **Chutes de fora da área têm menor chance de conversão em gol?**  
   Autor: *Rodrigo Severo Araújo*

## Estrutura do Projeto

O projeto está organizado em diferentes branches e diretórios, cada um com seu propósito:

- **Branches individuais**: `branch-rabello`, `branch-rodri`, `branch-batista`  
  Contêm os scripts desenvolvidos individualmente por cada autor para avaliação das hipóteses.
  
- **Branch `main`**:  
  Contém o código final e consolidado, além dos seguintes diretórios:
  
  - **docs/**:  
    Documentação gerada com Sphinx. O relatório final pode ser acessado em formato HTML. Para gerar e visualizar a documentação:
    ```bash
    make html
    ```

  - **data/**:  
    - `cleaned_events.csv`: Dados processados, contendo apenas as informações relevantes para análise.
    - `events.csv`: Dataset bruto conforme lido diretamente do Kaggle.
    - `graph_head.png`: Gráfico referente à análise da hipótese 2.
    - `graph_matches.png`: Gráfico referente à análise da hipótese 1.
    - `graph_shots.png`: Gráfico referente à análise da hipótese 3.

  - **src/**:  
    Contém os scripts principais para processamento e análise dos dados:
    - `clean_data.py`: Função para pré-processamento e limpeza do dataset.
    - `head.py`: Script para avaliação da hipótese 2.
    - `shots.py`: Script para avaliação da hipótese 3.
    - `matches.py`: Script para avaliação da hipótese 1.
    - `utils.py`: Funções auxiliares utilizadas em vários scripts.
    - `main.py`: Integra os scripts anteriores e gera as visualizações dos resultados.

  - **tests/**:  
    Scripts de testes unitários para validar o funcionamento do código:
    - `test_head.py`: Testes para a hipótese 2 (gols de cabeça).
    - `test_matches.py`: Testes para a hipótese 1 (vitórias do time da casa).
    - `test_shots.py`: Testes para a hipótese 3 (chutes de fora da área).
    - `test_utils.py`: Testes para as funções auxiliares em `utils.py`.

  - **requirements.txt**:  
    Lista de dependências necessárias para executar o projeto.

  - **LICENSE**:  
    Arquivo contendo a licença para o projeto.

## Instalação

Siga os passos abaixo para configurar o projeto em seu ambiente local:

1. Clone o repositório:
   ```bash
   git clone https://github.com/arthurabello/trabalho_lp_A1.git
   cd trabalho_lp_A1
   ```

2. Crie e ative um ambiente virtual (recomendado):
   ```bash
   python3 -m venv venv
   source venv/bin/activate 
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

4. Execute o script principal para visualizar os resultados:
   ```bash
   cd src
   python3 main.py
   ```

## Executando os Testes

O projeto inclui testes unitários para garantir a correção das análises. Para executá-los:

1. Navegue até o diretório de testes:
   ```bash
   cd tests
   ```

2. Execute os testes para cada script:
   ```bash
   python3 -m unittest test_shots.py
   python3 -m unittest test_matches.py
   python3 -m unittest test_head.py
   python3 -m unittest test_utils.py
   ```
