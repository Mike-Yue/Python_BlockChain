# noinspection PyInterpreter
import random
import hashlib
import tkinter
from tkinter import *
blocknum = 0
BlockChain = []


#Prints text in the submit_text widget to console
def print_text_field():
    print(submit_text.get(1.0, END))
    global blocknum, BlockChain
    if blocknum == 0:
        new_block = Block(submit_text.get(1.0, END), "0000000000000000000000000000000000000000000000000000000000000000", blocknum)
    else:
        new_block = Block(submit_text.get(1.0, END), BlockChain[0].current_Hash, blocknum)
    new_block.mine_nonce()
    BlockChain.append(new_block)
    print (new_block.blocknum, new_block.nonce, new_block.data, new_block.previous_Hash, new_block.current_Hash)
    blocknum += 1

class Block:
    def __init__(self, data, previous_Hash, blocknum):
        self.blocknum = blocknum
        self.data = data
        self.previous_Hash = previous_Hash

    def mine_nonce(self):
        self.nonce = 0
        total_string = str(self.blocknum) + str(self.nonce) + self.data + self.previous_Hash
        hash_value = hashlib.sha256(total_string.encode('utf-8')).hexdigest()
        while hash_value[0:5] != "12345":
            self.nonce += 1
            total_string = str(self.blocknum) + str(self.nonce) + self.data + self.previous_Hash
            hash_value = hashlib.sha256(total_string.encode('utf-8')).hexdigest()
            if self.nonce % 100000 == 0:
                print(self.nonce)
        self.current_Hash = hash_value

    def check_self(self):
        total_string = str(self.blocknum) + str(self.nonce) + self.data + self.previous_Hash
        hash_value = hashlib.sha256(total_string.encode('utf-8')).hexdigest()
        if hash_value != self.current_Hash:
            return False
        return True





top = tkinter.Tk()
root = Tk()
caption = Label(top, text = "Enter data for the block")
caption.pack()
submit_text = Text(top, bd = 5)
submit_text.pack(side = RIGHT)
submit_button = tkinter.Button(top, text = "submit", command = print_text_field)
submit_button.pack(side = LEFT)
top.mainloop()



