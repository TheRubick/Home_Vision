from dummyClass import dummyClass, setName
import multiprocessing
from multiprocessing import Manager
import pickle
from integrationUtils import objectTrackerProcess

if __name__ == "__main__":
    pass    
    '''
    manager = multiprocessing.Manager()
    multiprocessing.Array(typecode_or_type=type(dummyClass),size_or_initializer=900,lock=False)
    obj = dummyClass()
    obj2 = dummyClass()
    que = multiprocessing.Queue()
    que2 = multiprocessing.Queue()
    x = None
    x2 = None
    print(obj)
    p = multiprocessing.Process(target=setName,args=(obj,"Ahmed",x,que,))
    p.start()
    
    p2 = multiprocessing.Process(target=setName,args=(obj,"Kareem",x2,que2))
    p2.start()
    
    obj = pickle.loads(que.get())
    obj2 = pickle.loads(que2.get())

    p.join()
    p2.join()
    x = que.get()
    print(x)
    print(obj.name)
    print(obj2.name)
    '''
    