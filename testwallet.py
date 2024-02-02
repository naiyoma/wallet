from bitcoinrpc.authproxy import AuthServiceProxy


rpc_user = "123456"  
rpc_password = "123456" 
rpc_url = "http://127.0.0.1:8332"



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
wallet_connection = AuthServiceProxy(f"http://{rpc_user}:{rpc_password}@127.0.0.1:18332", timeout=290)

wallet_name = "testwallet80"
new_wallet = wallet_connection.createwallet(wallet_name)

wallet_address = wallet_connection.getnewaddress("GenerateAddress",user_address())
print("-")
print("Wallet Address: ", wallet_address)

#Retrive wallet spendable balance
wallet_balance = wallet_connection.getbalance()
print("-------------------------------------------------------------------------------")
print("Wallet Balance:",wallet_balance)
print("-\n")

#generate blocks
blocks = wallet_connection.generatetoaddress(101, wallet_address)
print("-------------------------------------------------------------------------------")
print("Generating Blocks")
print("-\n")

#new balance 
new_balance = wallet_connection.getbalance()
print("-")
print("New wallet Balance:",new_balance)
print("-")

wallet_connection.settxfee(0.00001)
send_transaction = wallet_connection.sendtoaddress(wallet_address, 0.01, "test send")
print("-")
print("Transaction Id:",send_transaction)
print("-\n")
