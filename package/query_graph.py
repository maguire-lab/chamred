from networkx.readwrite import json_graph
import json
import os
from functions import graph_functions

json_path = os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                "..", "results", "graph.json"
            )
with open(json_path) as json_file:
    G = json_graph.node_link_graph(json.load(json_file))

print(G.has_edge('resfinder:blaCMY-1', 'card:ARO:3002012'))
print(G.has_edge('card:ARO:3002012', 'resfinder:blaCMY-1'))

graph_functions.print_edge_info('resfinder:blaACC-2', G)
graph_functions.print_edge_info('resfinder:blaACC-7', G)
graph_functions.print_edge_info('card:ARO:3001816', G)

graph_functions.print_edge_info('resfinder:aac(3)-IIIb', G)

# SHV-24
graph_functions.print_edge_info('ncbi:WP_063864670.1', G)
# SHV-180
graph_functions.print_edge_info('ncbi:WP_063864659.1', G)