
import unittest

from unittest.mock import Mock
from blockconstructor import Mempool, sort_mempool_transactions, create_block


class TestBlockConstructor(unittest.TestCase):

    def test_sort_mempool_transactions(self):

        """
        Check if the transactions are sorted correctly based on fee rate
        """
        mempool_data = {
            'txid1': Mempool('2e3da8fbc1eaca8ed9b7c2db9e6545d8ccac3c67deadee95db050e41c1eedfc0', 452,1620), #0.27901234
            'txid2': Mempool('79c51c9d4124c5cbb37a85263748dcf44e182dff83561fa3087f0e9e43f41c33', 682,1136), #0.60035211
            'txid3': Mempool('b0ef627c8dc2a706475d33d7712209ec779f7a8302aaeab86c64cf00316a3df8', 285,1132)  #0.25176678
        }
        sorted_transactions = sort_mempool_transactions(mempool_data)
        # import pdb; pdb.set_trace()
        # Highest fee rate(#0.27901234)
        assert sorted_transactions[0].txid == '79c51c9d4124c5cbb37a85263748dcf44e182dff83561fa3087f0e9e43f41c33' 
        # Middle fee rate(#0.60035211)
        assert sorted_transactions[1].txid == '2e3da8fbc1eaca8ed9b7c2db9e6545d8ccac3c67deadee95db050e41c1eedfc0'  
        # Lowest fee rate(#0.25176678)
        assert sorted_transactions[2].txid == 'b0ef627c8dc2a706475d33d7712209ec779f7a8302aaeab86c64cf00316a3df8' 
    
    def test_create_block_with_invalid_weight(self):
        """
        Check that the total weight of transactions in a block must not exceed 4,000,000 weight
        """
        mempool_data = {
            'txid1': Mempool('2e3da8fbc1eaca8ed9b7c2db9e6545d8ccac3c67deadee95db050e41c1eedfc0', 10, 50000000),
            'txid2': Mempool('b0ef627c8dc2a706475d33d7712209ec779f7a8302aaeab86c64cf00316a3df8', 20, 5000000),
            'txid3': Mempool('79c51c9d4124c5cbb37a85263748dcf44e182dff83561fa3087f0e9e43f41c33', 30, 50000000)
        }
        block_transactions = create_block(mempool_data)
        assert block_transactions is None

if __name__ == "__main__":
    unittest.main()