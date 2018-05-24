import random
import hashlib

blocknum = 0;

class Block:
    def __init__(self, data, previous_Hash, blocknum):
        self.blocknum = blocknum;
        self.data = data;
        self.previous_Hash = previous_Hash

    def mine_Nonce(self):
        self.nonce = 0;
        total_string = str(self.blocknum) + str(self.nonce) + self.data + self.previous_Hash;
        hash_value = hashlib.sha256(total_string.encode('utf-8')).hexdigest()
        while (hash_value[0:5] != "12345"):
            self.nonce += 1
            total_string = str(self.blocknum) + str(self.nonce) + self.data + self.previous_Hash;
            hash_value = hashlib.sha256(total_string.encode('utf-8')).hexdigest()
            if(self.nonce % 100000 == 0):
                print(self.nonce)
        self.current_Hash = hash_value




Block1 = Block("abcd", "0000000000000000000000000000000000000000000000000000000000000000", blocknum)
Block1.mine_Nonce()
blocknum += 1

Block2 = Block("PogChamp", Block1.current_Hash, blocknum)
Block2.mine_Nonce()
blocknum += 1

Block3 = Block("OmegaLul", Block2.current_Hash, blocknum)
Block3.mine_Nonce()
blocknum += 1

print(Block1.blocknum, Block1.nonce, Block1.data, Block1.previous_Hash, Block1.current_Hash)
print(Block2.blocknum, Block2.nonce, Block2.data, Block2.previous_Hash, Block2.current_Hash)
print(Block3.blocknum, Block3.nonce, Block3.data, Block3.previous_Hash, Block3.current_Hash)



