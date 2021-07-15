import sys
from rich import print as rprint
from chamredb.functions import graph_functions

def print_node_info(identifier, database, graph):
    colours = ["blue_violet", "yellow1", "orange_red1","chartreuse1" ]
    source_node_id, source_node_data = graph_functions.get_graph_node(identifier, database, graph)
    if not source_node_id:
        print(f"Could not find a match for {identifier} in the {database} database")
        sys.exit(1)

    rprint(f":dna: [cyan bold]{identifier}[/cyan bold] [magenta bold]({source_node_data['name']})[/magenta bold]")

    for key in source_node_data:
        if key != 'database' and key != 'name':
            rprint(f"[bright_cyan]:page_facing_up: {key}: {source_node_data[key]}[/bright_cyan]")
    
    node_targets = __node_target_info(graph,source_node_id)
    database_colours = {}
    for database in node_targets:
        database_colours[database] = colours.pop()

    # print edge (hit) data
    for database in node_targets:
        colour = database_colours[database]
        rprint(f"  :file_cabinet: [{colour}]{database}")
        # return just first match
        target_ids = list(node_targets[database])
        target_id = target_ids[0]
        edge_data = node_targets[database][target_id]['edge_data']
        target_node_data = node_targets[database][target_id]['node']
        if edge_data['type'] == 'RBH':
            rprint(f"    :left_right_arrow: [{colour}]{target_id} ({target_node_data['name']})[/{colour}]")
        else:
            rprint(f"      :right_arrow: [{colour}]{target_id} ({target_node_data['name']})[/{colour}]")
        for key in edge_data:
            rprint(f"        :link: [white]{key}:[/white] [grey66]{edge_data[key]}[/grey66]")
        other_data = {key:target_node_data[key] for key in target_node_data if key != 'database' and key != 'name'}
        for key in other_data:
            rprint(f"        :page_facing_up: [white]{key}:[/white] [grey66]{other_data[key]}[/grey66]")
    print("="*80)
    print()


def write_multiple_node_info(id_data,graph,out_filepath):
    """
    id_data: a list of dicts with keys id, database and optionally file
    """
    all_databases = set([graph.nodes[node_name]['database'] for node_name in graph.nodes])
    id_databases = set([ id_info['database'] for id_info in id_data])
    # if only one database in ids_and_databases then the header databases should not include this database
    if len(id_databases) == 1:
        header_databases = sorted(all_databases - id_databases)
    else:
        header_databases = sorted(all_databases)
    
    target_node_field_titles = ['id', 'name', 'match_type', 'match_identity', 'match_coverage', 'metadata'] 
    
    if 'file' in id_data[0]:
        multiple_samples = True
    else:
        multiple_samples = False
    
    with open(out_filepath, 'w') as out:
        header = __multiple_ids_header(header_databases, target_node_field_titles, multiple_samples)
        out.write(f'{header}\n')
        missing_ids = {}
        for id_info in id_data:
            source_id = id_info['id']
            source_database = id_info['database']
            # get a source node and it's id based on the database and an id (which could be a name)
            source_node_id, source_node = graph_functions.get_graph_node(source_id, source_database, graph)
            if not source_node_id:
                if source_database not in missing_ids:
                    missing_ids[source_database] = {}
                if source_id not in missing_ids[source_database]:
                    missing_ids[source_database][source_id] = 0
                missing_ids[source_database][source_id] += 1
                print(f"WARNING: Could not find a match for {source_id} in the {source_database} database")
                continue
            # get the name
            name = source_node['name']
            # make the metadata from the source node
            metadata_string = ','.join(__node_metadata(source_node))
            # find all target nodes for the source node
            source_node_target_info = __node_target_info(graph, source_node_id)
            # make a dict of items about the target nodes
            target_node_info = {}
            for target_database in source_node_target_info:
                best_match = __best_target_node_match(source_node_target_info[target_database])
                target_node_info[target_database] = {
                    'id': best_match['id'],
                    'name': best_match['node']['name'],
                    'match_type': best_match['edge_data']['type'],
                    'match_identity': best_match['edge_data']['identity'],
                    'match_coverage': best_match['edge_data']['coverage'],
                    'metadata': ','.join(__node_metadata(best_match['node']))
                }
            
            # write out target info
            target_node_info_list = []
            for target_database in header_databases:
                for field in target_node_field_titles:
                    if target_database == source_database or target_database not in target_node_info:
                        target_node_info_list.append('-')
                    else:
                        target_node_info_list.append(str(target_node_info[target_database][field]))
            target_node_info_string = "\t".join(target_node_info_list)
            if multiple_samples:
                source_file = id_info['file']
                out.write(f'{source_file}\t{source_id}\t{source_database}\t{name}\t{metadata_string}\t{target_node_info_string}\n')
            else:
                out.write(f'{source_id}\t{source_database}\t{name}\t{metadata_string}\t{target_node_info_string}\n')

    



# private methods
def __node_metadata(node):
    """
    return metadata for a node as a list
    """
    metadata = []
    for key in node:
        if key != 'name' and key != 'database' and key != 'alternative_id':
            metadata.append(f'{key}:{node[key]}')
    return(metadata)

def __node_target_info(graph,node_id):
    """
    Returns dictionary containing information about the edges connected to a source node and the target nodes associated with the edge.
    The dict groups the edges by database of the target node and the database are the top level keys 
    """
    node_targets = {}
    # gather edge (hit) data
    for edge in graph.edges(node_id):
        database,id,target_node,edge_data = __edge_target_info(graph,edge)
        if database not in node_targets:
            node_targets[database] = {}
        node_targets[database][id] = {
            'node': target_node,
            'edge_data': edge_data
        }
    return(node_targets)

def __best_target_node_match(node_targets):
    """
    Given a dict of target nodes (key is id) return best node based on identity and coverage
    """
    best_match_identity = 0
    best_match_coverage = 0
    best_match = None
    for target_node_id in node_targets:
        coverage = node_targets[target_node_id]['edge_data']['coverage']
        identity = node_targets[target_node_id]['edge_data']['identity']
        if  coverage >= 0.9 and coverage > best_match_coverage:
            if identity > best_match_identity:
                best_match = node_targets[target_node_id]
                best_match['id'] = target_node_id
                best_match_coverage = coverage
                best_match_identity = identity
    return(best_match)

def __edge_target_info(graph,edge):
    target_node = graph.nodes[edge[1]]
    edge_data = graph.get_edge_data(edge[0], edge[1])
    database = edge[1].split(":")[0]
    id = ''.join(edge[1].split(":")[1:])
    return(database,id,target_node,edge_data)


def __multiple_ids_header(databases, field_titles, multiple_samples):
    database_header_titles = []
    for db in sorted(databases):
        for title in field_titles:
            database_header_titles.append(f'{db}: {title}')
    if multiple_samples:
        sample_header_string = "sample\tid\tdatabase\tname\tmetadata"
    else:
        sample_header_string = "id\tdatabase\tname\tmetadata"
    database_header_title_string = '\t'.join(database_header_titles)
    header = f"{sample_header_string}\t{database_header_title_string}\n"
    return(header)

