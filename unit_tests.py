import pandas as pd 
import unittest
from unittest.mock import patch
from unittest import TestCase
from country_trivia import select_country

class Test(TestCase):
    
    @patch('country_trivia.get_input', return_value='japan')
    def test_select_country(self, input):
        s = select_country()
        print(s)
        self.assertEqual(s[0], 'japan')
        pd.testing.assert_frame_equal(s[1], pd.DataFrame.from_dict({"currency":["Japanese yen"],"capital":["Tokyo"],"region":["Asia"]}))