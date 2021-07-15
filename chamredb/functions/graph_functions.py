import pandas as pd
import networkx as nx
import os
import json

def add_rbh_hits_to_graph(sourceDB,targetDB, graph, debug = False):

    rbh_data = pd.read_csv(
                    os.path.join(
                        os.path.dirname(os.path.abspath(__file__)),
                        "..", "..", "results",
                        f"mmseqs_{sourceDB}_vs_{targetDB}.rbh.sorted.tsv"
                    ), sep="\t")

    sourceDB_metadata,targetDB_metadata = __load_metadata(sourceDB,targetDB)

    # print(sourceDB_metadata.keys())
    for _, row in rbh_data.iterrows():
        source_node_attributes = sourceDB_metadata[row['query']]
        source_node_attributes['database'] = sourceDB
        target_node_attributes = targetDB_metadata[row['target']]
        target_node_attributes['database'] = targetDB
        __add_connection(
            graph,
            row['query'],
            source_node_attributes,
            row['target'],
            target_node_attributes,
            {
                'type': 'RBH',
                'identity': row['fident'],
                'coverage': row['alnlen']/(row['qend'] - row['qstart'] + 1)
            },
            debug = debug
        )

def add_search_hits_to_graph(sourceDB,targetDB,graph,debug=False):

    search_data = pd.read_csv(
                    os.path.join(
                        os.path.dirname(os.path.abspath(__file__)),
                        "..", "..", "results",
                        f"mmseqs_{sourceDB}_vs_{targetDB}.search.sorted.tsv"
                    ), sep="\t")

    sourceDB_metadata,targetDB_metadata = __load_metadata(sourceDB,targetDB)

    # OWH == One Way Hit
    for _, row in search_data.iterrows():
        source_node_attributes = sourceDB_metadata[row['query']]
        source_node_attributes['database'] = sourceDB
        target_node_attributes = targetDB_metadata[row['target']]
        target_node_attributes['database'] = targetDB
        __add_connection(
            graph,
            row['query'],
            source_node_attributes,
            row['target'],
            target_node_attributes,
            {
                'type': 'OWH',
                'identity': row['fident'],
                'coverage': row['alnlen']/(row['qend'] - row['qstart'] + 1)
            },
            debug=debug
        )

def get_graph_node(identifier,database,graph):
    """
    gets node from graph first trying the id in the graph which is 'database:id', else searching name, else returning None
    """
    full_id = f'{database}:{identifier}'
    if full_id in graph.nodes:
        return(full_id, graph.nodes[full_id])
    else:
        for node_id, node_data in graph.nodes(data=True):
            if ((
                'alternative_id' in node_data and node_data['alternative_id'] == identifier
                )
                or
                node_data['name'] == identifier
            ) and node_data['database'] == database:
                return(node_id, graph.nodes[node_id])
        return(None, None)

# private methods
def __load_metadata(sourceDB,targetDB):
    sourceDB_metadata_path = os.path.join(
                    os.path.dirname(os.path.abspath(__file__)),
                    "..", "..", "db_metadata",
                    f"{sourceDB}.metadata.json"
                )
    with open(sourceDB_metadata_path) as sourceDB_metadata_file:
        sourceDB_metadata = json.load(sourceDB_metadata_file)

    targetDB_metadata_path = os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                "..", "..", "db_metadata",
                f"{targetDB}.metadata.json"
            )
    with open(targetDB_metadata_path) as targetDB_metadata_file:
        targetDB_metadata = json.load(targetDB_metadata_file)
    
    return(sourceDB_metadata,targetDB_metadata)

def __add_connection(graph,
                    source_node_id,
                    source_node_attributes,
                    target_node_id,
                    target_node_attributes,
                    edge_attributes,
                    debug=False):
    source_composite_key = f'{source_node_attributes["database"]}:{source_node_id}'
    target_composite_key = f'{target_node_attributes["database"]}:{target_node_id}'
    if not graph.has_node(source_composite_key):
        graph.add_node(source_composite_key, **source_node_attributes)
    if not graph.has_node(target_composite_key):
        graph.add_node(target_composite_key, **target_node_attributes)
    if graph.has_edge(source_composite_key, target_composite_key):
        if debug:
            print(f"Warning! Graph already has edge {source_composite_key} => {target_composite_key}")
    else:
        graph.add_edge(source_composite_key, target_composite_key, **edge_attributes)
    # add reciprocal edge if RBH
    if edge_attributes['type'] == 'RBH':
        if graph.has_edge(target_composite_key, source_composite_key):
            if debug:
                print(f"Warning! Graph already has edge {target_composite_key} => {source_composite_key}")
        else:
            graph.add_edge(target_composite_key, source_composite_key, **edge_attributes)
