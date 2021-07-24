import pytest
import os
import textwrap
from chamredb.functions import graph_visualisation_functions
from chamredb.functions import graph_functions

@pytest.fixture(scope="module") 
def expected_print_node_info_output():
    return textwrap.dedent(
        """
        :dna: [cyan bold]WP_012695489.1[/cyan bold] [magenta bold](qnrB2)[/magenta bold]
        [bright_cyan]:page_facing_up: phenotype: confers resistance to subclass QUINOLONE[/bright_cyan]
          :file_cabinet: [chartreuse1]card[/chartreuse1]
            :left_right_arrow: [chartreuse1]ARO3002735 (QnrB20)[/chartreuse1]
                :link: [white]coverage:[/white] [grey66]1.0[/grey66]
                :link: [white]identity:[/white] [grey66]0.995[/grey66]
                :link: [white]type:[/white] [grey66]RBH[/grey66]
                :page_facing_up: [white]is_a:[/white] [grey66]ARO:3000419:quinolone resistance protein (qnr)[/grey66]
                :page_facing_up: [white]phenotype:[/white] [grey66]confers resistance to drug class: fluoroquinolone antibiotic[/grey66]
          :file_cabinet: [orange_red1]resfinder[/orange_red1]
            :left_right_arrow: [orange_red1]qnrB2 (qnrB2)[/orange_red1]
                :link: [white]coverage:[/white] [grey66]1.0[/grey66]
                :link: [white]identity:[/white] [grey66]1.0[/grey66]
                :link: [white]type:[/white] [grey66]RBH[/grey66]
                :page_facing_up: [white]phenotype:[/white] [grey66]confers resistance to Ciprofloxacin [/grey66]
        ================================================================================

        """
    )

@pytest.fixture(scope="module") 
def chamredb_graph():
    return graph_functions.read_graph()


def test_single_node_info_text(expected_print_node_info_output, chamredb_graph):
    assert expected_print_node_info_output == graph_visualisation_functions.single_node_info_text(
        'WP_012695489.1',
        'ncbi',
        chamredb_graph
    )

def test_write_multiple_node_info(expected_print_node_info_output, chamredb_graph):
    assert expected_print_node_info_output == graph_visualisation_functions.single_node_info_text(
        'WP_01269548',
        'ncbi',
        chamredb_graph
    )
    

