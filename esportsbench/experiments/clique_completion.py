import os 
import sys
import pathlib
import numpy as np
import polars as pl
import networkx as nx 
import matplotlib.pyplot as plt

# Add the parent directory to sys.path. This lets me import the riix_module functions. 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from riix.utils.data_utils import TimedPairDataset
from esportsbench.constants import GAME_NAME_MAP
from esportsbench.datasets import load_dataset

# need to go back two steps to point ot the data directory. 
BASE_DATA_DIR = pathlib.Path(__file__).resolve().parents[2] / 'data' 



def clique_completion(network, k = 2):
    """
    Code that takes as input an interaction network and checks to see whether 
    the maximum likelihood estimator associated with the mElo rating system 
    is uniquely defined. 

    inputs: network: TBD
            k: even integer  

    outputs: TBD

    The algorithm works as follows:
        - finds a clique of size k+1 group these in a 
        - if there exists 
    """
    # check that k is an even integer
    if k%2 != 0:
        raise Exception('k must be an even integer')
    
    pass


if __name__ == '__main__':
    game = 'smash_melee'
    data_dir = 'hf_data/v1_0'
    df = pl.read_parquet(BASE_DATA_DIR / data_dir / f'parquet/{game}.parquet')

    # parse the paerquet file into an edge_list. 

    # get a list of the nodes first 
    df_names_1 = df.get_column('competitor_1')
    df_names_1 = df_names_1.to_list()

    df_names_2 = df.get_column('competitor_2')
    df_names_2 = df_names_2.to_list()

    node_list = df_names_1 + df_names_2
    node_list = list(set(node_list))
    print('number of nodes: ', len(node_list))

    # Step 1: Create new columns with the names sorted alphabetically per row
    df_sorted = df.with_columns([
        pl.min_horizontal(['competitor_1', 'competitor_2']).alias('name_a'),
        pl.max_horizontal(['competitor_1', 'competitor_2']).alias('name_b')
        ])

    # Step 2: Select only the sorted name columns and drop duplicates
    unique_pairs_df = df_sorted.select(['name_a', 'name_b']).unique()

    # Step 3: Convert to a list of tuples
    unique_pairs = list(zip(unique_pairs_df['name_a'], unique_pairs_df['name_b']))

    print('number of edges: ', len(unique_pairs))
    p = 2*len(unique_pairs)/(len(node_list)*(len(node_list)-1))
    print('density of the graph ', p)
    print(len(node_list)*p)
    G = nx.from_edgelist(unique_pairs)
    degree_sequence = sorted((d for n, d in G.degree()), reverse=True)
    plt.plot(degree_sequence)
    plt.show()


