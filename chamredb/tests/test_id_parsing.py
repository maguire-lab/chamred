import pytest
import os
from chamredb.functions import utility_functions

@pytest.fixture(scope="module") 
def expected_harmonizarion_parsing_output():
    return(
            [
                {'file': 'G18002568', 'id': 'NG_047244.1', 'database': 'ncbi'},
                {'file': 'G18002568', 'id': 'NG_054648.1', 'database': 'ncbi'},
                {'file': 'G18002569', 'id': 'NG_049444.1', 'database': 'ncbi'},
                {'file': 'G18002569', 'id': 'NG_051852.1', 'database': 'ncbi'},
                {'file': 'G18002570', 'id': 'NG_047282.1', 'database': 'ncbi'},
                {'file': 'G18002570', 'id': 'NG_049326.1', 'database': 'ncbi'},
                {'file': 'G18002570', 'id': 'NG_049798.1', 'database': 'ncbi'},
                {'file': 'G18002570', 'id': 'NG_048161.1', 'database': 'ncbi'},
                {'file': 'G18002571', 'id': 'NG_047244.1', 'database': 'ncbi'},
                {'file': 'G18002571', 'id': 'NG_050145.1', 'database': 'ncbi'}
            ]
    )


def test_multiple_id_parsing():
    multiple_ids_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'test_data', 'card_ids.txt')
    assert ['ARO:3001816', 'ARO:3002012', 'ARO:3001082', 'ARO:3000951', 'ARO:3001350'] == utility_functions.parse_id_file(multiple_ids_file)


def test_harmonizarion_parsing(expected_harmonizarion_parsing_output):
    hamronization_json_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'test_data', 'ncbi_summary.json')
    assert expected_harmonizarion_parsing_output == utility_functions.parse_hamronization_json_file(hamronization_json_file)
