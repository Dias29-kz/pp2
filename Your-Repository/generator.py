#Here we have function generation
#function for from one to six, and yield is function generators it's return only one value 
# but function keeps it's place
def numbers():
    for i in range(1, 6):
        yield i

for n in numbers():
    print(n)