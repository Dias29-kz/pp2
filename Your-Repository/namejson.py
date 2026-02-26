import json #we can add json functions 

x =  '{ "name":"Diko", "age":18, "city":"Tokyo"}' #here sets string for json


y = json.loads(x) #load string it's make dictionary list a separate consideration 

# the result is a Python dictionary we to get 18
print(y["age"])

# a Python object (dict):
x = {
  "name": "Diko",
  "age": 19,
  "city": "Tokyo"
}

y = json.dumps(x) #dumps make string and print it how have in the row

# the result is a JSON string we can to get {"name": "Diko", "age": 19, "city": "Tokyo"}
print(y)