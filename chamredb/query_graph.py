from chamredb.functions import graph_visualisation_functions
from chamredb.functions import graph_functions
from rich import print as rprint

def query_graph_single_id(id,database,coverage_threshold,identity_threshold):
    """
    query_graph_single_id query the graph with AMR metadata with a single id from one database

    Args:
        id (string): the identifier used in the database
        database (string): database name
        coverage_threshold (float): coverage threshold below which a match will not be reported
        identity_threshold (float): identity threshold below which a match will not be reported

    """
    graph = graph_functions.read_graph()
    single_id_info_text = graph_visualisation_functions.single_node_info_text(id,database,graph,coverage_threshold,identity_threshold)
    rprint(single_id_info_text)

def query_graph_multiple_ids(id_data,outfile_path,coverage_threshold,identity_threshold):
    """
    query_graph_multiple_ids query the graph with AMR metdata with a list of identifiers from one or more databases

    Args:
        id_data (list):  id_data: a list of dicts with keys id, database and optionally file
        out_filepath (string): path to the outfile that will contain the id matches
        coverage_threshold (float): The covergae value below which a match will not be reported
        identity_threshold (float): The identity value below which a match will not be reported
    """
    graph = graph_functions.read_graph()
    graph_visualisation_functions.write_multiple_node_info(id_data,graph,outfile_path,coverage_threshold,identity_threshold)
        