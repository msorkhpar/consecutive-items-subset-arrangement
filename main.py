import pandas as pd
from dotenv import load_dotenv

from generators.generate_bipartite_graph import construct_bipartite_graph
from generators.generate_consecutive_items_bipartite_graph import generate_random_edge_set

if __name__ == '__main__':
    load_dotenv()
    plans = pd.read_csv('plan.csv', dtype={
        'nodes': int,
        'min_pairs': int,
        'max_pairs': int,
        'samples': int
    })
    for index, row in plans.iterrows():
        no_samples = row['samples']
        for i in range(no_samples):
            items, players, edges = generate_random_edge_set(row['nodes'], row['min_pairs'], row['max_pairs'])
            G = construct_bipartite_graph(items, players, edges)