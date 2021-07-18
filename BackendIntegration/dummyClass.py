import pickle
class dummyClass():
    def __init__(self):
        self.name = "Muhammad"
    

def setName(dumObj,name,x,que):
    print(dumObj)
    print("here")
    dumObj.name = name
    print(dumObj.name)
    x = 99
    que.put(pickle.dumps(dumObj))
    que.put(x)