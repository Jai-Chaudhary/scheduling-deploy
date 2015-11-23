import requests
import csv
from pprint import pprint
from pymongo import MongoClient
from time import sleep

client = MongoClient()
raw_order = client.schedule.raw_order
raw_order.drop()

csvfile = 'test.csv'
listen_url = 'http://localhost:5000/hl7json'

reader = csv.DictReader(open(csvfile))
for row in reader:
    for x in row:
        if row[x] == 'NA':
            row[x] = None
    requests.post(listen_url, json=row)
    #sleep(1)

for x in raw_order.find():
    pprint(x, indent=4)
