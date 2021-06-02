import pandas as pd
import networkx as nx
import os
import json
from rich import print as rprint


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

def print_edge_info(node, graph):
    colours = ["blue_violet", "yellow1", "orange_red1","chartreuse1" ]
    hit_databases = {}
    rprint(f":dna: [cyan bold]{node}[/cyan bold] [magenta bold]({graph.nodes[node]['name']})[/magenta bold]")
    source_node_data = graph.nodes[node]
    for key in source_node_data:
        if key != 'database' and key != 'name':
            rprint(f"[bright_cyan]:page_facing_up: {key}: {source_node_data[key]}[/bright_cyan]")

    # gather edge (hit) data
    for edge in graph.edges(node):
        target_node_data = graph.nodes[edge[1]]
        edge_data = graph.get_edge_data(edge[0], edge[1])
        database = edge[1].split(":")[0]
        accession = ''.join(edge[1].split(":")[1:])
        if database not in hit_databases:
            hit_databases[database] = {'colour': colours.pop(), 'hits': {}}
        hit_databases[database]['hits'][accession] = {
            'accession_data': target_node_data,
            'edge_data': edge_data
        }
    # print edge (hit) data
    for database in hit_databases:
        colour = hit_databases[database]['colour']
        rprint(f"  :file_cabinet: [{colour}]{database}")
        for accession in hit_databases[database]['hits']:
            edge_data = hit_databases[database]['hits'][accession]['edge_data']
            accession_data = hit_databases[database]['hits'][accession]['accession_data']
            if edge_data['type'] == 'RBH':
                rprint(f"    :left_right_arrow: [{colour}]{accession} ({accession_data['name']})[/{colour}]")
            else:
                rprint(f"      :right_arrow: [{colour}]{accession} ({accession_data['name']})[/{colour}]")
            for key in edge_data:
                rprint(f"        :link: [white]{key}:[/white] [grey66]{edge_data[key]}[/grey66]")
            other_data = {key:accession_data[key] for key in accession_data if key != 'database' and key != 'name'}
            for key in other_data:
                rprint(f"        :page_facing_up: [white]{key}:[/white] [grey66]{other_data[key]}[/grey66]")
    print("="*80)
    print()

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