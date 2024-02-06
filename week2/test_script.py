import os
import unittest
import binascii
import re
from unittest.mock import Mock
from script import create_redeem_script, generate_new_address, create_send_transaction

class TestTransactionScript(unittest.TestCase):
    def test_create_redeem_script(self):
        """
        Test a valid pre-image and assert the output
        """
        pre_image = "427472757374204275696c64657273"
        redeem_script = create_redeem_script()
        self.assertEqual(redeem_script.serialize().hex(), "a82016e05614526c1ebd3a170a430a1906a6484fdd203ab7ce6690a54938f5c44d7d87")
    
    def test_create_redeem_script_with_invalid_preimage(self):
        """
        Test for an invalid pre-image
        """
        invalid_preimage = bytes()
        with self.assertRaises(TypeError):
            create_redeem_script(invalid_preimage)

    def test_generate_new_address(self):
        """
        Test that the redeem script generated a P2SH address
        """
        redeem_script = create_redeem_script()
        address = generate_new_address(redeem_script)
        self.assertTrue(address.startswith('3'))

    def test_valid_transaction(self):
        """
        Test for valid transaction data.
        """
        addr = "35f5XD9JYH294zA9gtvMaHxpqNQapdVWGp"
        private_key = os.urandom(32).hex()
        transaction = create_send_transaction(addr)
        self.assertIsNotNone(transaction)
        transaction_object, key_object = transaction
        self.assertTrue(transaction_object.verify())
        self.assertEqual(transaction_object.outputs[0].value, 10) 


if __name__ == '__main__':
    unittest.main()