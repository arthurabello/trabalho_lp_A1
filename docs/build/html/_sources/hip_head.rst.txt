====================================================
Relatório da Análise sobre Origem dos Gols de Cabeça
====================================================

Hipótese
--------

A maior parte dos *gols de cabeça* tem origem em lances de bola parada (escanteios, faltas e impedimentos)

Motivação  
---------

Devido à natureza mais organizada e previsível dos lances de **bola parada**, esses lances são comumente associados a gols de
cabeça, em especial, os escanteios, que é tradicionalmente cobrado com bola levantada na área com intenção de um jogador bem
posicionado conseguir cabecear. Assim, é natural esperar que parte considerável dos gols de cabeça tenham origem nesses lances. 

Metodologia
-----------

Utilizando o arquivo `cleaned_events.csv`, que contém dados sobre diversos eventos ocorridos em jogos de futebol, a análise com o 
objetivo de verificar a hipótese aprensentada seguiu da seguinte maneira:

1. **Preparação dos Dados:**
    - **Remoção de Colunas:** Foram removidas as colunas `'side'`, `'shot_outcome'` e `'location'`, que não seriam úteis para a análise.
    - **Filtragem de Linhas:** Apenas as linhas que correspondem a gols de cabeça e eventos anteriores a gols de cabeça foram mantidas, pois seriam as únicas necessárias.

2. **Cálculo das Estatísticas:**
    - **Gols de Cabeça Precedidos por Lances de Bola Parada:** Foi calculado o percentual de gols de cabeça que tinha como evento anterior, um escanteio, uma falta ou um impedimento que ocorreu em até 1 minuto antes do gol.

3. **Visualização dos Dados:**
    - **Gráfico de Barras:** Foi criado um gráfico de barras relacionado ao percentual de gols com origem em escanteio, falta, impedimento, bola parada (qualquer um dos três anteriores) e outras origens. 

Resultados
----------

Estatísticas
^^^^^^^^^^^^

============  ===========
ORIGEM        Porcentagem 
============  ===========
Escanteios    38.74       
Faltas        10.53
impedimentos  2.30
BOLA PARADA   51.58
Outros        48.42      
============  ===========

Gráfico

.. image:: ../../data/graph_head.png
   :width: 600px
   :height: 400px
   :align: center

Conclusão
--------------------
A análise mostra que, nos dados analisados, 51.58% dos gols de cabeça tiveram origem em gols de cabeça. Esse resultado reforça em parte
a hipótese de que a maioria dos gols desse tipo surgem de escanteios, faltas e impedimentos. Todavia, a margem não é tão grande quanto
o esperado. Dessa forma, embora a hipótese seja confirmada, a análise revela que grande parte dos gols de cabeça têm origem em lances
bola parada. Além disso, como esperado, os gols com origem em escanteio representam parte substancial do total.