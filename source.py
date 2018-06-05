# noinspection PyInterpreter
import random
import sys
import threading
import matplotlib.pyplot as plt
from matplotlib import style
from statistics import mean
style.use('ggplot')
import numpy as np
from numpy.polynomial.polynomial import polyfit
import hashlib
import tkinter
import sqlite3
import requests
from tkinter import *
from datetime import datetime
from multiprocessing import Process
import time

#Prints text in the submit_text widget to console
#Mines new block with the text in the field as the data
def mine_block():
    thread1 = myThread(1, "mining thread", 'mine')
    thread1.start()

#Quits GUI
def quit_gui():
    global top
    top.destroy()
    global exitFlag
    exitFlag = 1

def print_all_blocks():
    thread2 = myThread(2, "print values thread", 'print')
    thread2.start()

#Helper function for plotting time
def lsrl(x, y):
    m = (((mean(x)*mean(y)) - mean(x * y))/((mean(x)*mean(x))-mean(x*x)))
    b = mean(y) - m * mean(x)
    return m, b

#GETs data from NodeJS server and plots it using Matploblib
def plot_time():
    get = requests.get('http://8c3076e2.ngrok.io/times', auth = ('admin', 'supersecret'))
    data = get.json()
    print (data)
    x = []
    for i in range(0, len(data)):
        x.append(i)
    x = np.array(x)
    y = np.array(data)
    m, b = lsrl(x, y)
    regression_line = [(m*xp) + b for xp in x]
    #print (z)

    plt.scatter(x, data)
    plt.plot(x, regression_line)
    plt.xlabel('Block Number')
    plt.ylabel('Seconds')
    plt.show()

#Checks if block has been mined already
def check():
    thread3 = myThread(1, "check block thread", 'check')
    thread3.start()
#Creates a form to sign up for User ID/Password
def sign_up():
    sign_up_menu = tkinter.Tk()
    sign_up_menu.title("Sign Up")

    #Captions
    username_caption = Label(sign_up_menu, text = "Enter your username", padx= '15', pady = '5')
    username_caption.grid(row = 0, column = 0)

    password_caption = Label(sign_up_menu, text = "Enter your password", padx= '15', pady = '5')
    password_caption.grid(row = 2, column = 0)

    #
    global username, password
    username = Entry(sign_up_menu, width = '40', selectborderwidth = '15')
    username.grid(row = 0, column = 1, columnspan = 2)

    password = Entry(sign_up_menu, show = '*', width = '40', selectborderwidth = '15')
    password.grid(row = 2, column = 1, columnspan = 2)

    #Submit Button
    sign_up_button = tkinter.Button(sign_up_menu, text = "Create Account", command = create_account, font = ('Times', '12'))
    sign_up_button.grid(row = 3, column = 0, columnspan = 3, sticky=W+E+N+S)

#POSTS a new account into database
#Should check if account already exists
def create_account():
    global username, password
    print(username.get(), password.get())

    newdata = {"username": username.get(), "password": password.get()}
    try:
        post = requests.post('http://8c3076e2.ngrok.io/postaccount', json=newdata, auth=('admin', 'supersecret'))
    except requests.exceptions.RequestException as e:
        print (e)
    print(post.status_code)
    if (post.status_code == 400):
        print ("Username already exists. Please sign in")
    else:
        print("Account Created. Please Log in")
    username.delete(0, END)
    password.delete(0, END)


#Checks database if a username password key pair exists, then logs them in if it does
def login():
    global username, password, ID
    print(username.get(), password.get())
    ID = username.get()
    newdata = {"username": username.get(), "password": password.get()}
    try:
        post = requests.post('http://8c3076e2.ngrok.io/signin', json=newdata, auth=('admin', 'supersecret'))
    except requests.exceptions.RequestException as e:
        print (e)
    print(post.status_code)
    if(post.status_code == 400):
        print("Invalid user information. Please Try again")
        username.delete(0, END)
        password.delete(0, END)
    else:
        sign_up_menu.destroy()
        global top
        top = tkinter.Tk()
        top.title("Welcome to the ZerOCoin GUI")

        #Captions
        caption = Label(top, text = "Enter data for the block", font = ('Times', '12'))
        caption.grid(row = 0, columnspan = 1)

        #Text entries
        global submit_text
        submit_text = Text(top, bd = 5, height = '30' )
        submit_text.grid(row = 1, rowspan = 5)

        #Buttons
        print_blocks_button = tkinter.Button(top, text = "Print All blocks", command = print_all_blocks, font = ('Times', '12'))
        print_blocks_button.grid(row = 1, column = 1, sticky=W+E+N+S)

        submit_button = tkinter.Button(top, text = "Mine New Block", command = mine_block, font = ('Times', '12'))
        submit_button.grid(row = 2, column = 1, sticky=W+E+N+S)

        quit_button = tkinter.Button(top, text = "Exit Application", command = quit_gui, font = ('Times', '12'))
        quit_button.grid(row = 4, column = 1, sticky=W+E+N+S)

        plot_button = tkinter.Button(top, text = "Plot Times", command = plot_time, font = ('Times', '12'), width = '20')
        plot_button.grid(row = 3, column = 1, sticky=W+E+N+S)

        check_button = tkinter.Button(top, text = "Check if Block Has Been Mined", command = check, font = ('Times', '12'), width = '25')
        check_button.grid(row = 5, column = 1, sticky=W+E+N+S)

        print ("Logged in!")

        top.mainloop()
        exitFlag = 1


class Block:
    def __init__(self, data, previous_Hash, blocknum):
        self.blocknum = blocknum
        self.data = data
        self.previous_Hash = previous_Hash

    def mine_nonce(self):
        global exitFlag
        exitLoop = False
        self.nonce = 0
        total_string = str(self.blocknum) + str(self.nonce) + self.data + self.previous_Hash
        hash_value = hashlib.sha256(total_string.encode('utf-8')).hexdigest()
        print ("Mining nonce...Please wait")
        print (self.blocknum)
        while hash_value[0:7] != "0000000":
            if(exitFlag == 1):
                sys.exit()

            self.nonce += 1
            total_string = str(self.blocknum) + str(self.nonce) + self.data + self.previous_Hash
            hash_value = hashlib.sha256(total_string.encode('utf-8')).hexdigest()
            if(self.nonce % 500000 == 0):
                print (self.nonce)
        get = requests.get('http://8c3076e2.ngrok.io/interrupt', auth=('admin', 'supersecret'))
        data = get.json()
        if (data != self.blocknum):
            exitLoop = True
        if(exitLoop == False):
            self.current_Hash = hash_value
        return exitLoop

    def check_self(self):
        total_string = str(self.blocknum) + str(self.nonce) + self.data + self.previous_Hash
        hash_value = hashlib.sha256(total_string.encode('utf-8')).hexdigest()
        if hash_value != self.current_Hash:
            return False
        return True



class myThread (threading.Thread):
   def __init__(self, threadID, name, job):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.job = job

   def run(self):
      if(self.job == 'mine'):
          global submit_text, username, ID, blocknum
          print ("Starting " + self.name)
          get = requests.get('http://8c3076e2.ngrok.io', auth=('admin', 'supersecret'))
          data = get.json()
          blocknum = data['number'] + 1
          global BlockChain, iterate, mining_times
          if blocknum == data["number"] + 1:
              new_block = Block(submit_text.get(1.0, END) + str(datetime.now()) + ' Mined by ' + ID, data["curr_hash"], blocknum)
          else:
              new_block = Block(submit_text.get(1.0, END) + str(datetime.now()) + ' Mined by' + ID, BlockChain[iterate - 1].current_Hash,
                                blocknum)
          start_time = time.clock()
          duplicate = new_block.mine_nonce()
          if(duplicate == False):
              total_time = time.clock() - start_time
              print(str(total_time) + " seconds to run")
              mining_times.append(total_time)
              BlockChain.append(new_block)
              submit_text.delete(1.0, END)

              newdata = {"number": blocknum, "nonce": new_block.nonce, "data": new_block.data,
                         "prev_hash": new_block.previous_Hash, "curr_hash": new_block.current_Hash,
                         "time": total_time}
              post = requests.post('http://8c3076e2.ngrok.io/postdata', json=newdata, auth=('admin', 'supersecret'))

              print(str(blocknum) + " " + str(
                  new_block.nonce) + " " + new_block.data + " " + new_block.previous_Hash + " " + new_block.current_Hash)
              iterate += 1
              blocknum += 1
              print("Block successfully mined and added to BlockChain!")
          else:
              print ("Block has already been mined")

          print ("Exiting " + self.name)

      if(self.job == 'print'):
          get = requests.get('http://8c3076e2.ngrok.io/allblocks', auth=('admin', 'supersecret'))
          data = get.json()
          # data is a list ADT, each element of Data is a dict ADT
          for i in range(0, len(data)):
              print('Block Number:', str(data[i]['number']))
              print('Block Nonce:', str(data[i]['nonce']))
              print('Block Data:', data[i]['data'])
              print('Block Previous Hash:', data[i]['prev_hash'])
              print('Block Current Hash:', data[i]['curr_hash'])
              print('\n')

      if(self.job == 'check'):
          try:
            blocknum
          except NameError:
              print("You are not mining a block right now")
          else:
              get = requests.get('http://8c3076e2.ngrok.io/interrupt', auth=('admin', 'supersecret'))
              data = get.json()
              if(blocknum == data):
                  print ("Block has not yet been mined")
              else:
                  print ("Block has been mined")
#Main Thread/Loop
if __name__ == '__main__':
    BlockChain = []
    mining_times = []
    iterate = 0
    exitFlag = 0
    exitLoop = False

    global sign_up_menu
    sign_up_menu = tkinter.Tk()
    sign_up_menu.title("Sign Up")

    #Captions
    username_caption = Label(sign_up_menu, text = "Enter your username", padx= '15', pady = '5')
    username_caption.grid(row = 0, column = 0)

    password_caption = Label(sign_up_menu, text = "Enter your password", padx= '15', pady = '5')
    password_caption.grid(row = 2, column = 0)

    #
    global username, password
    username = Entry(sign_up_menu, width = '40', selectborderwidth = '15')
    username.grid(row = 0, column = 1, columnspan = 3)

    password = Entry(sign_up_menu, show = '*', width = '40', selectborderwidth = '15')
    password.grid(row = 2, column = 1, columnspan = 3)

    #Submit Button
    sign_up_button = tkinter.Button(sign_up_menu, text = "Create Account", command = create_account, font = ('Times', '12'))
    sign_up_button.grid(row = 3, column = 0, columnspan = 2, sticky=W+E+N+S)

    login_button = tkinter.Button(sign_up_menu, text = "Log In", command = login, font = ('Times', '12'))
    login_button.grid(row = 3, column = 2, columnspan = 2, sticky=W+E+N+S)


    sign_up_menu.mainloop()

