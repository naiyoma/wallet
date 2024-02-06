import json
import unittest
import binascii
import re
from unittest.mock import Mock
from script import create_redeem_script, generate_new_address


class TestTransactionScript(unittest.TestCase):
    def test_create_redeem_script(self):
        redeem_script = create_redeem_script()
        self.assertEqual(redeem_script.serialize().hex(), "a820fde0d71fd75fe03b84db05ac3f5f7c81785ed7d7d3e8b9182e1f2fc4ac4d")
    
    def test_generate_new_address(self):
        redeem_script = create_redeem_script()
        address = generate_new_address(redeem_script)
        # Add assertion here to check if the generated address is valid
        # self.assertTrue(is_valid_address(address))
        # Replace is_valid_address with an appropriate function to check address validity

if __name__ == '__main__':
    unittest.main()