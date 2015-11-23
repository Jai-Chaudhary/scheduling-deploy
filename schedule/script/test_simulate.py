import requests

r = requests.post('http://localhost:6000/simulate', json={'time': '2012-09-27 12:30:00'})
print(r.text)
