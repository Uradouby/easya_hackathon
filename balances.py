# 1. Add import
from web3 import Web3

# 1. Add the Web3 provider logic here:
provider_rpc = {
    'development': 'http://127.0.0.1:9944',
    'alphanet': 'https://rpc.api.moonbase.moonbeam.network',
}

#web3 = Web3(Web3.HTTPProvider(provider_rpc['development']))  # Change to correct network
web3 = Web3(Web3.HTTPProvider('https://rpc.api.moonbase.moonbeam.network'))
# 2. Create address variables
address_from = '0x22e65C87ce17bfefC65C1A8694E167539DfDA3f7'
address_to = '0xCa1143BFf2Ce579Fe545ec1c9933F30fBDa0e9cE'

# 3. Fetch balance data
balance_from = web3.from_wei(web3.eth.get_balance(address_from), 'ether')
balance_to = web3.from_wei(web3.eth.get_balance(address_to), 'ether')

print(f'The balance of { address_from } is: { balance_from } ETH')
print(f'The balance of { address_to } is: { balance_to } ETH')
