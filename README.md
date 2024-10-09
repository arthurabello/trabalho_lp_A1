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
  - Cada hipótese foi escrita em scripts individuais:
    - `shots.py` -> Rodrigo (Chute de fora da área)
    - `head.py` -> Antonio (Gols de cabeça)
    - `matchs.py` -> Rabello (Time da casa)
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

## Executando os Testes

O projeto inclui testes unitários para cada uma das três hipóteses. Para executar os testes, siga estas etapas:

1. Navegue até o diretório de testes:
   ```bash
   cd tests
   ```

2. Execute os testes para cada hipótese:
   ```bash
   python3 -m unittest tests_shots.py
   python3 -m unittest tests_matches.py
   python3 -m unittest tests_head.py
   ```

Cada arquivo de teste corresponde a uma das hipóteses do projeto:
- `tests_shots.py`: Testes para a hipótese de chutes fora da área
- `tests_matches.py`: Testes para a hipótese do time da casa
- `tests_head.py`: Testes para a hipótese de gols de cabeça

## Contribuição

Para contribuir, abra um pull request. Certifique-se de que suas alterações estão alinhadas com o estilo do projeto e que todos os testes passam.

## Licença

Este projeto está licenciado sob a MIT License. Consulte o arquivo [LICENSE](LICENSE) para mais detalhes.