#!/usr/bin/python3

from pymongo import MongoClient

class XX:
	def __init__(self, ):
		self.a = {
				"1": 1,
				"2": 2, 
				"3": 3
		}

client = MongoClient()

dbtest = client['test']
model = dbtest['model']
x = XX()
info = {
		"conv1": 1
}
info2 = {
		"conv2": 2
}
model.insert_one(info)
model.replace_one(info, info2)
doc = model.find()
for i in doc:
	print(i)
model.remove(info2, 1)
model.remove(info, 2)
# print(test)
# print(client)

