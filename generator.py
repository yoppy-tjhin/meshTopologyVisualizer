import json
import BitArray2D
from BitArray2D import godel

mesh_topo = """[
    {
        "nodeId" : 2147321738,
        "subs" : [
            {
                "nodeId" : 2147319559,
                "subs" : [
                ]
            }
        ]
    },
    {
        "nodeId" : 2142436481,
        "subs" : [
            {
                "nodeId" : 2787708646,
                "subs" : [
                ]
            }
        ]
    }
]"""

data = json.loads(mesh_topo)


def countdown(n):
    print ("Counting down from", n)
    while n > 0:
        print ("beefore yield")
        yield n
        print("after yield")
        n -= 1

def recursive_iter(obj):
    if isinstance(obj, dict):
        for item in obj.values():
            yield from recursive_iter(item)
    #elif any(isinstance(obj, t) for t in (list, tuple)):
    elif isinstance(obj, list):
        for item in obj:
            yield from recursive_iter(item)
    else:
        yield obj
        #pass

for item in recursive_iter(data):
    print (item)
    #pass

###############
def generator2():
    for i in range(10):
        yield i

def generator3():
    for j in range(10, 20):
        yield j

def generator():
    for i in generator2():
        yield i
    for j in generator3():
        yield j

def generator_yield():
    yield from generator2()
    yield from generator3()