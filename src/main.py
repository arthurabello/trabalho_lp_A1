import pandas as pd
from clean_data import clean_data
from utils import load_dataset
from head import head_main
from matches import matches_main
from shots import shots_main

def main():
    """Função principal que orquestra todas as hipóteses da análise exploratória"""
    filepath = "../data/events.csv"
    df = load_dataset(filepath)
    
    clean_data(df)

    matches_main(df.copy())
    shots_main(df.copy())
    head_main(df.copy())

if __name__ == "__main__":
    main()

    