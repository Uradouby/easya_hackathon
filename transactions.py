from web3.gas_strategies.rpc import rpc_gas_price_strategy
from web3 import Web3

provider_rpc = {
    'development': 'http://localhost:9944',
    'alphanet': 'https://rpc.api.moonbase.moonbeam.network',
}

web3 = Web3(Web3.HTTPProvider('https://rpc.api.moonbase.moonbeam.network'))

account_from = {
    'private_key': '77a97728c0f31e86de31b5d1fc736bb3bc05bbc2485242b82c7624d6257606a9',
    'address': '0x22e65C87ce17bfefC65C1A8694E167539DfDA3f7',
}

address_to = '0xCa1143BFf2Ce579Fe545ec1c9933F30fBDa0e9cE'

print(
    f'Attempting to send transaction from { account_from["address"] } to { address_to }'
)

web3.eth.set_gas_price_strategy(rpc_gas_price_strategy)

tx_create = web3.eth.account.sign_transaction(
    {
        'nonce': web3.eth.get_transaction_count(account_from['address']),
        'gasPrice': web3.eth.generate_gas_price(),
        'gas': 3000000,
        'to': address_to,
        'value': web3.to_wei('1', 'ether'),
    },
    account_from['private_key'],
)

tx_hash = web3.eth.send_raw_transaction(tx_create.rawTransaction)
tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

print(f'Transaction successful with hash: { tx_receipt.transactionHash.hex() }')
