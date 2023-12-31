from backend.blockchain.block import Block
from backend.util.qrng import generate_random_number

class Blockchain:
    """
    Blockchain: a public ledger of transactions 
    Implemented as a list of blocks - data sets of transactions 
    """

    def __init__(self):
        self.chain = [Block.genesis()]

    def add_block(self, data):
        self.chain.append(Block.mine_block(self.chain[-1], data))

    def __repr__(self):
        return f'Blockchain: {self.chain}'


def main():
    blockchain = Blockchain()
    blockchain.add_block('adithi -> utkarsh = 10 Rs,')
    blockchain.add_block('rashi -> sujeet = 20 Rs, ')

    print(blockchain)
    print(f'block.py __name__: {__name__}')

    

if __name__ == '__main__':
    main()