import threading
import time
import hashlib

exitFlag = 0
multiplier = 0

class myThread (threading.Thread):
   def __init__(self, threadID, name, interval):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.interval = interval
   def run(self):
      print ("Starting " + self.name)
      #while (exitFlag != 1):
      mine_nonce(self.name, self.interval)
      print ("Exiting " + self.name)

def mine_nonce(threadName, interval):
    global multiplier, exitFlag, start_time
    x = multiplier * interval
    lower_interval = x
    upper_interval = (multiplier + 1) * interval
    multiplier += 1
    while (x < upper_interval):
        if(exitFlag == 1):
            return
        hash_value = hashlib.sha256((threadName + str(x)).encode('utf-8')).hexdigest()
        if(hash_value[0:7] == "0000000"):
            exitFlag = 1
            print ("Correct hash is ", hash_value, x)
        print (threadName, "Hashing values between " + str(lower_interval) + " to " + str(upper_interval), hash_value)
        x += 1
    final_time = time.clock() - start_time
    print(final_time)



# Create new threads
thread1 = myThread(1, "thread1", 10000000)
thread2 = myThread(2, "thread2", 10000000)
thread3 = myThread(3, "thread3", 10000000)

# Start new Threads
start_time = time.clock()
thread1.start()
thread2.start()
thread3.start()

print ("Exiting Main Thread")