import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from unittest.mock import patch
from main import branch

class TestBranchFunction(unittest.TestCase):

    @patch('main.get_branch_prompt')
    @patch('main.evolve')
    def test_branch(self, mock_evolve, mock_get_branch_prompt):
        # Setup the mock responses
        test_name = "test_name"
        test_seed_text = "test_seed"
        mock_prompt = "mock_prompt"
        mock_response = "mock_response"
        
        mock_get_branch_prompt.return_value = mock_prompt
        mock_evolve.return_value = mock_response

        # Call the function and assert the response
        response = branch(test_seed_text, test_name)
        self.assertEqual(response, mock_response)

        # Verify that the mocks were called with the correct arguments
        mock_get_branch_prompt.assert_called_once_with(test_name)
        mock_evolve.assert_called_once_with(test_seed_text, mock_prompt)

if __name__ == '__main__':
    unittest.main()

