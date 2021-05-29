#%%
import pandas as pd
import networkx as nx
from networkx_query import search_nodes, search_edges

#%%
resfinder_vs_card_rbh_data = pd.read_csv("../results/mmseqs_resfinder_vs_card.rbh.sorted.tsv", sep="\t")

# %%
def add_connection(
    graph,
    source_node_attributes,
    target_node_attributes,
    edge_attributes
):
    source_composite_key = f'{source_node_attributes["database"]}:{source_node_attributes["name"]}'
    target_composite_key = f'{target_node_attributes["database"]}:{target_node_attributes["name"]}'
    if not graph.has_node(source_composite_key):
        graph.add_node(source_composite_key, **source_node_attributes)
    if not graph.has_node(target_composite_key):
        graph.add_node(target_composite_key, **target_node_attributes)
    graph.add_edge(source_composite_key, target_composite_key, **edge_attributes)
    # add reciprocal edge if RBH
    if edge_attributes['type'] == 'RBH':
        graph.add_edge(target_composite_key, source_composite_key, **edge_attributes)




G = nx.DiGraph()
for index, row in resfinder_vs_card_rbh_data.iterrows():
    add_connection(
        G,
        {'name': row['query'], 'database':'resfinder'},
        {'name': row['target'], 'database':'card'},
        {'type': 'RBH'}
    )

# %%
search = {
    'and': [
        {
            'eq': [('name'), 'blaCMY-1']
        },
        {
            'eq': [('database'), 'resfinder']
        }
    ]
}
for node_id in search_nodes(G, search):
    print(list(G.neighbors(node_id)))
# %%
print(G.has_edge('resfinder:blaCMY-1', 'card:CMY-1'))
print(G.has_edge('card:CMY-1', 'resfinder:blaCMY-1'))

# %%
