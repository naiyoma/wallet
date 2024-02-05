from pprint import pprint
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
from hex import parse_transactions


def user_address():
    """
    Get user address type.
    """
    while True:
        address_type = input("Select address type (legacy, p2sh-segwit, bech32): ").lower()
        if address_type in ["legacy", "p2sh-segwit", "bech32"]:
            return address_type
        else:
            print("Invalid address type. Please choose from legacy, p2sh-segwit, or bech32.")


# rpc_user and rpc_password are set in the bitcoin.conf file
rpc_user = "123456"  
rpc_password = "123456" 
rpc_url = "http://127.0.0.1:8332"

rpc_connection = AuthServiceProxy(f"http://{rpc_user}:{rpc_password}@127.0.0.1:18332", timeout=290)

#retrieve the blockcount of your node
block_count = rpc_connection.getblockcount()
print("-------------------------------------------------------------------------")
print("Block Count: ", block_count)
print("-------------------------------------------------------------------------")

#retrieve block details
#1.get blockcount using block count
#2.use the blockhash to get the block details.
blockhash = rpc_connection.getblockhash(block_count)

block = rpc_connection.getblock(blockhash)

print("---------------------------------------------------------------")
print("BLOCK Hash: ", blockhash)
print("-------------")
print("Number of Transaction.: ", block["nTx"])
print("Block Confirmations...: ", block["confirmations"])
print("Merkle Root..: ", block['merkleroot'])
print("Block Size...: ", block['size'])
print("Block Weight.: ", block['weight'])
print("Nonce........: ", block['nonce'])
print("Difficulty...: ", block['difficulty'])
print("---------------------------------------------------------------")

# import pdb; pdb.set_trace()
# Create a wallet named "testwallet15"
wallet_name = "testwallet80"
new_wallet = rpc_connection.createwallet(wallet_name)

# Specify the wallet file in the URI path for subsequent RPC calls
wallet_connection = AuthServiceProxy(f"http://{rpc_user}:{rpc_password}@127.0.0.1:18332/wallet/{wallet_name}", timeout=170)


# Retrieve a new address from the newly created wallet.
wallet_address = wallet_connection.getnewaddress("GenerateAddress",user_address())
wallet_info = wallet_connection.getwalletinfo()
print("-")
print("Wallet Address: ", wallet_address)
print("-\n")
print("-\n")
print("Wallet Info:")
print("-----------")
pprint(wallet_info)
print("-\n")

#Retrive wallet spendable balance
wallet_balance = wallet_connection.getbalance()

print("-------------------------------------------------------------------------------")
print("Wallet Balance:",wallet_balance)
print("-\n")

#generate blocks
# import pdb; pdb.set_trace()
blocks = wallet_connection.generatetoaddress(101, wallet_address)
print("-------------------------------------------------------------------------------")
print("Generating Blocks")
print("-----------------------------------------------------------------------------")

#new balance 
new_balance = wallet_connection.getbalance()

print("------------------------------------------------------------------------------")
print("New wallet Balance:",new_balance)
print("------------------------------------------------------------------------------")

#get the block count blocks in your node
new_block_count = wallet_connection.getblockcount()
print("-----------------------------------------------------------------------")
print("New Block Count:", new_block_count)
print("-----------------------------------------------------------------------")

#Create a Transaction
#1.Use the generated adress above as the sender
#2.Generate a send to Address which is the receive address
#3.set transaction fees (this is not necessary, i only use it to mitigate the fallback-fee error)
#4.Fetch the UTXO associated with that transaction.
wallet_connection.settxfee(0.00001)
send_transaction = wallet_connection.sendtoaddress(wallet_address, 0.01, "donation" "sean's outpost")
print("-----------------------------------------------------------------------------")
print("Transaction Id:",send_transaction)
print("------------------------------------------------------------------------------")


raw_transaction_details = wallet_connection.getrawtransaction(send_transaction, True)
print("--------------------------------------------------------------------")
# parse_transactions(raw_transaction_details)
pprint(raw_transaction_details)
print("----------------------------------------------------------------------")






#get transaction id for the input refrence
# tx_id = raw_transaction_details["vin"][0]['txid']
# new_transaction = wallet_connection.getrawtransaction(tx_id, True)
# print("---------------------------------------------------------------------------")
# pprint(new_transaction)
# transaction = wallet_connection.gettransaction(send_transaction)
# print("------------------------Transaction Details-----------------------------------")
# print("-------------------")
# print("Address:",transaction["details"][0]["address"])
# print("category:",transaction["details"][0]["category"])
# print("amount:",transaction["details"][0]["amount"])
# print("fee:",transaction["details"][0]["fee"])
# print("-------------------")

