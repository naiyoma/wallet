import json
import unittest
import binascii
import re
from unittest.mock import Mock
from hex import parse_transactions



class TestParseTransaction(unittest.TestCase):
    def mock_transaction(self,hex_data=None):
        with open("mock_data.json", "r") as file:
            mock_data = json.load(file)["mock_transaction"]
        mock_transaction = Mock()
        mock_transaction.txid = mock_data["txid"]
        mock_transaction.locktime  = mock_data["locktime"]
        mock_transaction.version = mock_data["version"]
        mock_transaction.outputs = [
            Mock(address=output_data["address"], value=output_data["value"], output_n=output_data["output_n"],
                script=Mock(serialize=Mock(hex=output_data["hex"])))
            for output_data in mock_data["outputs"]
        ]


        return mock_transaction

    def test_parse_transactions_invalid_hex(self):
        """
        Test an invalid hex.
        """
        invalid_hex = "0000001010ccc140e766b5dbc884ea2d780c5e91e4eb7759775228b79e234900000000000000000002bd37060000000000225120245091249f4f29d30820e5f36e1e5d477dc3386144220bd6f35839e94de4b9cae81c00000000000016001416d31d7632aa17b3b316b813c0a3177f5b6150200140838a1f0f1ee607b54abf0a3f55792f6f8d09c3eb7a9fa46cd4976f2137ca2e3f4a901e314e1b827c3332d7e1865ffe1d7ff5f5d7576a9000f354487a09de44cd00000000"
        mock_transaction = self.mock_transaction()

        with self.assertRaises(Exception):
            parse_transactions(invalid_hex)


    def test_parse_transactions_valid_version(self):
        """
        Test if a version is 4 bytes.
        """
        transaction = self.mock_transaction()  
        hex_data = transaction.version
        version_bytes = binascii.unhexlify(hex_data)
        self.assertEqual(len(version_bytes), 4)


    def test_parse_transactions_is_hexadecimal(self):
        transaction = self.mock_transaction()
        hex_data = transaction.version
        pattern = r"^[0-9A-Fa-f]+$"
        is_hex = re.fullmatch(pattern, hex_data) is not None

        self.assertTrue(is_hex, "Hexadecimal format is invalid")

if __name__ == "__main__":
    unittest.main()