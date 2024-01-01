import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
import os
from main import get_branch_prompt

class TestGetBranchPrompt(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Setup: Create a mock file with known content
        cls.test_file_name = "test_prompt"
        cls.expected_content = "Sample content for testing"
        cls.test_file_path = f"./prompts/{cls.test_file_name}.pt"
        with open(cls.test_file_path, "w") as f:
            f.write(cls.expected_content)

    @classmethod
    def tearDownClass(cls):
        # Cleanup: Remove the mock file
        os.remove(cls.test_file_path)

    def test_get_branch_prompt(self):
        # Test: Call the function and assert the returned content
        result = get_branch_prompt(self.test_file_name)
        self.assertEqual(result, self.expected_content)

if __name__ == '__main__':
    unittest.main()


