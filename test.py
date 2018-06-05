import threading
import time
import hashlib
import requests

password = '33'
for x in range (0, 100000):
    password = hashlib.sha256(password.encode('utf-8')).hexdigest()
print(password)

newdata = {"username": '1', "password": '1'}
try:
    post = requests.post('http://8c3076e2.ngrok.io/signin', json=newdata, auth=('admin', 'supersecret'))
except requests.exceptions.RequestException as e:
    print (e)
print(post.status_code)
if (post.status_code == 400):
    print ("Invalid information")
else:
    print("Logged in")
