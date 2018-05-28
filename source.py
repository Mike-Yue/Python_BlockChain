# noinspection PyInterpreter
import random
import hashlib
import tkinter
import sqlite3
import requests
from tkinter import *
from datetime import datetime


#Prints text in the submit_text widget to console
#Mines new block with the text in the field as the data
def print_text_field():
    print(submit_text.get(1.0, END))
    global BlockChain, blocknum, iterate
    if blocknum == data["number"] + 1:
        new_block = Block(submit_text.get(1.0, END) + str(datetime.now()), data["curr_hash"], blocknum)
    else:
        new_block = Block(submit_text.get(1.0, END) + str(datetime.now()), BlockChain[iterate - 1].current_Hash, blocknum)
    new_block.mine_nonce()
    BlockChain.append(new_block)
    print (new_block.blocknum, new_block.nonce, new_block.data, new_block.previous_Hash, new_block.current_Hash)
    blocknum += 1
    iterate += 1
    submit_text.delete(1.0, END)

#Quits GUI
def quit_gui():
    top.destroy()

def print_all_blocks():
    length = len(BlockChain)
    for i in range(0, length):
        print(BlockChain[i].blocknum, BlockChain[i].nonce, BlockChain[i].data, BlockChain[i].previous_Hash,
              BlockChain[i].current_Hash)

class Block:
    def __init__(self, data, previous_Hash, blocknum):
        self.blocknum = blocknum
        self.data = data
        self.previous_Hash = previous_Hash

    def mine_nonce(self):
        self.nonce = 0
        total_string = str(self.blocknum) + str(self.nonce) + self.data + self.previous_Hash
        hash_value = hashlib.sha256(total_string.encode('utf-8')).hexdigest()
        print ("Mining nonce...Please wait")
        while hash_value[0:3] != "000":
            self.nonce += 1
            total_string = str(self.blocknum) + str(self.nonce) + self.data + self.previous_Hash
            hash_value = hashlib.sha256(total_string.encode('utf-8')).hexdigest()

        self.current_Hash = hash_value

    def check_self(self):
        total_string = str(self.blocknum) + str(self.nonce) + self.data + self.previous_Hash
        hash_value = hashlib.sha256(total_string.encode('utf-8')).hexdigest()
        if hash_value != self.current_Hash:
            return False
        return True

get = requests.get('http://localhost:8080/')
data = get.json()
blocknum = data['number'] + 1
BlockChain = []
iterate = 0
print(blocknum)


top = tkinter.Tk()

#Captions
caption = Label(top, text = "Enter data for the block")
caption.grid(row = 0, columnspan = 2)

#Text entries
submit_text = Text(top, bd = 5)
submit_text.grid(row = 1, rowspan = 3)

#Buttons
print_blocks_button = tkinter.Button(top, text = "Print all blocks", command = print_all_blocks)
print_blocks_button.grid(row = 1, column = 1)
submit_button = tkinter.Button(top, text = "Mine New Block", command = print_text_field)
submit_button.grid(row = 2, column = 1)
quit_button = tkinter.Button(top, text = "Exit Application", command = quit_gui)
quit_button.grid(row = 3, column = 1)
top.mainloop()