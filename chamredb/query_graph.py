from chamredb.functions import graph_visualisation_functions
from chamredb.functions import graph_functions
from rich import print as rprint

def query_graph_single_id(id,database,coverage_threshold,identity_threshold):
    graph = graph_functions.read_graph()
    single_id_info_text = graph_visualisation_functions.single_node_info_text(id,database,graph,coverage_threshold,identity_threshold)
    rprint(single_id_info_text)

def query_graph_multiple_ids(id_data,outfile_path,coverage_threshold,identity_threshold):
    graph = graph_functions.read_graph()
    graph_visualisation_functions.write_multiple_node_info(id_data,graph,outfile_path,coverage_threshold,identity_threshold)
        