from unittest import TestCase
import os
from chamredb.functions import utility_functions

class TestChamredb(TestCase):
    def test_multiple_id_parsing(self):
        multiple_ids_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'test_data', 'card_ids.txt')
        self.assertEqual(
            ['ARO:3001816', 'ARO:3002012', 'ARO:3001082', 'ARO:3000951', 'ARO:3001350'],
            utility_functions.parse_id_file(multiple_ids_file)
        )
