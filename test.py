import requests

get = requests.get('http://localhost:8080/')
print(get.json())

#newdata = {"data1": "haha!"}
#post = requests.post('http://localhost:8080/postdata', json = newdata)
#print(post.text)