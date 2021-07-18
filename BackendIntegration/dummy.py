from dummyClass import dummyClass, setName
import multiprocessing

if __name__ == "__main__":
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
    
    obj = que.get()
    obj2 = que2.get()

    p.join()
    p2.join()
    x = que.get()
    print(x)
    print(obj.name)
    print(obj2.name)