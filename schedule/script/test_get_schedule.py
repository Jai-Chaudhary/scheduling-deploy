import requests

r = requests.post('http://localhost:5000/schedule', json={'time': '2012-09-27 12:30:00'})
print(r.text)
