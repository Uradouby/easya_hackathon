import random
from web3.gas_strategies.rpc import rpc_gas_price_strategy

from web3 import Web3
web3 = Web3(Web3.HTTPProvider('https://rpc.api.moonbase.moonbeam.network')) # Insert your RPC URL here
account_player = {
    'private_key': '77a97728c0f31e86de31b5d1fc736bb3bc05bbc2485242b82c7624d6257606a9',
    'address': '0x22e65C87ce17bfefC65C1A8694E167539DfDA3f7',
}

account_boss = {
    'private_key': '3cd86ff4fcf0082d9ff25432382935f18f1ff10f5d63ff66985b131e71c424a9',
    'address': '0xCa1143BFf2Ce579Fe545ec1c9933F30fBDa0e9cE',
}

for i in range(0, 10):
    win = random.randint(0, 1)
    web3.eth.set_gas_price_strategy(rpc_gas_price_strategy)
    if win==1:
        print('player win')
        tx_create = web3.eth.account.sign_transaction(
            {
                'nonce': web3.eth.get_transaction_count(account_boss['address']),
                'gasPrice': web3.eth.generate_gas_price(),
                'gas': 3000000,
                'to': account_player['address'],
                'value': web3.to_wei('0.001', 'ether'),
            },
            account_boss['private_key'],
        )
        tx_hash = web3.eth.send_raw_transaction(tx_create.rawTransaction)
        tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        print(f'Transaction successful with hash: {tx_receipt.transactionHash.hex()}')
    else:
        print('boss win')
        tx_create = web3.eth.account.sign_transaction(
            {
                'nonce': web3.eth.get_transaction_count(account_player['address']),
                'gasPrice': web3.eth.generate_gas_price(),
                'gas': 3000000,
                'to': account_boss['address'],
                'value': web3.to_wei('0.001', 'ether'),
            },
            account_player['private_key'],
        )
        tx_hash = web3.eth.send_raw_transaction(tx_create.rawTransaction)
        tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        print(f'Transaction successful with hash: {tx_receipt.transactionHash.hex()}')
    balance_boss = web3.from_wei(web3.eth.get_balance(account_boss['address']), 'ether')
    balance_player = web3.from_wei(web3.eth.get_balance(account_player['address']), 'ether')

    print(f'The balance of boss is: {balance_boss} ETH')
    print(f'The balance of player is: {balance_player} ETH')
    print("--------------------------------------------------------------------")

