# noinspection PyInterpreter
import random
import matplotlib.pyplot as plt
import hashlib
import tkinter
import sqlite3
import requests
from tkinter import *
from datetime import datetime
import time


#Prints text in the submit_text widget to console
#Mines new block with the text in the field as the data
def mine_block():
    get = requests.get('http://8c3076e2.ngrok.io', auth = ('admin', 'supersecret'))
    data = get.json()
    blocknum = data['number'] + 1
    global BlockChain, iterate, mining_times
    if blocknum == data["number"] + 1:
        new_block = Block(submit_text.get(1.0, END) + str(datetime.now()), data["curr_hash"], blocknum)
    else:
        new_block = Block(submit_text.get(1.0, END) + str(datetime.now()), BlockChain[iterate - 1].current_Hash, blocknum)
    start_time = time.clock()
    new_block.mine_nonce()
    total_time = time.clock() - start_time
    print(str(total_time) + "seconds to run")
    mining_times.append(total_time)
    BlockChain.append(new_block)
    submit_text.delete(1.0, END)

    newdata = {"number": blocknum, "nonce": new_block.nonce, "data": new_block.data, "prev_hash": new_block.previous_Hash, "curr_hash": new_block.current_Hash,
               "time": total_time}
    post = requests.post('http://8c3076e2.ngrok.io/postdata', json = newdata, auth = ('admin', 'supersecret'))

    print (str(blocknum) + " " + str(new_block.nonce) + " " + new_block.data + " " + new_block.previous_Hash + " " + new_block.current_Hash)
    iterate += 1
    blocknum += 1
    print ("Block successfully mined and added to BlockChain!")

#Quits GUI
def quit_gui():
    top.destroy()

def print_all_blocks():
    space = " "
    get = requests.get('http://8c3076e2.ngrok.io/allblocks', auth = ('admin', 'supersecret'))
    data = get.json()
    # data is a list ADT, each element of Data is a dict ADT
    for i in range(0, len(data)):
        print(str(data[i]['number']) + space + str(data[i]['nonce']) + space + data[i]['data'] + space + data[i]['prev_hash'] + space + data[i]['curr_hash'])

#GETs data from NodeJS server and plots it using Matploblib
def plot_time():
    get = requests.get('http://8c3076e2.ngrok.io/times', auth = ('admin', 'supersecret'))
    data = get.json()
    plt.plot(data)
    plt.show()

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
        while hash_value[0:7] != "0000000":
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


BlockChain = []
mining_times = []
iterate = 0

top = tkinter.Tk()

#Captions
caption = Label(top, text = "Enter data for the block")
caption.grid(row = 0, columnspan = 2)

#Text entries
submit_text = Text(top, bd = 5)
submit_text.grid(row = 1, rowspan = 4)

#Buttons
print_blocks_button = tkinter.Button(top, text = "Print all blocks", command = print_all_blocks)
print_blocks_button.grid(row = 1, column = 1)

submit_button = tkinter.Button(top, text = "Mine New Block", command = mine_block)
submit_button.grid(row = 2, column = 1)

quit_button = tkinter.Button(top, text = "Exit Application", command = quit_gui)
quit_button.grid(row = 4, column = 1)

plot_button = tkinter.Button(top, text = "Plot Times", command = plot_time)
plot_button.grid(row = 3, column = 1)

top.mainloop()