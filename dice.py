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
dice_tpl = '''\
    ┌───┐ , ┌───┐, ┌───┐, ┌───┐, ┌───┐, ┌───┐
	│   │ , │ ● │, │●  │, │● ●│, │● ●│, │● ●│
    │ ● │ , │   │, │ ● │, │   │, │ ● │, │● ●│
    │   │ , │ ● │, │  ●│, │● ●│, │● ●│, │● ●│
    └───┘ , └───┘, └───┘, └───┘, └───┘, └───┘'''

def play_game():
    dice_lines = dice_tpl.split('\n')
    for m in range(5):
        dice_lines[m] = dice_lines[m].split(',')
    dice = ['', '', '', '', '', '']
    for n in range(6):
        dice[n] = dice_lines[0][n] + '\n' + dice_lines[1][n] + '\n' + dice_lines[2][n] + '\n' + dice_lines[3][n] + '\n' + \
                  dice_lines[4][n]
    print('''\n-----Welcome to guessing the dices------
            The rules are as follows：
            roll 3 dices, if the total number of dices are bigger than 10, its big, other case its small\n ''')

    amount = float(input('How many DEV you want to gamble?'))

    use = int(input("Please guess the result 1(big) or 0(small):"))
    a1 = random.randint(1, 6)
    a2 = random.randint(1, 6)
    a3 = random.randint(1, 6)
    print("\n First dice", a1)
    print("Second dice", a2)
    print("Third dice", a3)
    print(dice[a1 - 1])
    print(dice[a2 - 1])
    print(dice[a3 - 1])
    sum = a1 + a2 + a3
    if sum < 10:
        flag = 0
        print("The outcome is small\n")
    else:
        flag = 1
        print("The outcome is big\n")

    web3.eth.set_gas_price_strategy(rpc_gas_price_strategy)

    if use == flag:
        print('you are right.')
        tx_create = web3.eth.account.sign_transaction(
            {
                'nonce': web3.eth.get_transaction_count(account_boss['address']),
                'gasPrice': web3.eth.generate_gas_price(),
                'gas': 3000000,
                'to': account_player['address'],
                'value': web3.to_wei(amount, 'ether'),
            },
            account_boss['private_key'],
        )
        tx_hash = web3.eth.send_raw_transaction(tx_create.rawTransaction)
        tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        print(f'Transaction successful with hash: {tx_receipt.transactionHash.hex()}')
    else:
        print('you are wrong.')
        tx_create = web3.eth.account.sign_transaction(
            {
                'nonce': web3.eth.get_transaction_count(account_player['address']),
                'gasPrice': web3.eth.generate_gas_price(),
                'gas': 3000000,
                'to': account_boss['address'],
                'value': web3.to_wei(amount, 'ether'),
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


if __name__ == '__main__':
    while(True):
        play_game()