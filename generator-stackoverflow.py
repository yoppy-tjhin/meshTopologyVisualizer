import json
import BitArray2D
from BitArray2D import godel

my_json_data = """[
    1,
    {
        "2": 3,
        "4": [
            "5",
            "6",
            "7"
        ]
    },
    8,
    9
]"""


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

x_len = 11
y_len = 11

init_node = [ int(x_len/2), int(y_len/2) ]    #[ node position ]
init_direction = [0,1]          # direction vector
node_map = BitArray2D.BitArray2D(rows=x_len, columns=y_len)
node_map[int(x_len/2), int(y_len/2)] = 1
relation_list = []

def find_empty_position(neighbourNodeId, current_node, direction, node_map, relation_list):

    all_dir = [ [1,0], [0,1], [-1,0], [0,-1] ]          # define NEWS direction

    new_node = [current_node[0]+direction[0], current_node[1]+direction[1] ]
    all_dir.remove(direction)
    # if available, take it
    if not node_map[ godel (new_node[0], new_node[1]) ]:

        node_map[new_node] = 1                          # update node_map. new_node occupied
        relation_list.append( [current_node[:], new_node[:]] )
        current_node[:] = new_node                  # update current_node
                                                        # direction unchanged
        pass
        #pass # got new node. update node_map, etc.. RETURN

    # else, try other directions
    else:
        for dir in all_dir:
            new_node = [current_node[0]+dir[0], current_node[1]+dir[1]]
            # Got a empty spot. Take it
            if not node_map[ godel( new_node[0], new_node[1])]:

                node_map[new_node] = 1              # update node_map. new_node occupied
                relation_list.append([current_node[:], new_node[:]])
                current_node[:] = new_node          # update current_node
                direction[:] = dir                  # update direction
                break
                pass # got new node. update node_map, etc, RETURN



def recursive_iter(obj, current_node_pos, direction, node_map, relation_list):
    if isinstance(obj, dict):
        #for item in obj:
        neighbourNodeId = obj["nodeId"]      # direct neighbour of the current_node
        find_empty_position(neighbourNodeId, current_node_pos, direction, node_map, relation_list)

        print (neighbourNodeId)    #find empty position in node_mapping, update current_node
        yield from recursive_iter( obj["subs"], current_node_pos[:], direction, node_map, relation_list)
    elif isinstance(obj, list):
        for item in obj:
            yield from recursive_iter(item, current_node_pos[:], direction, node_map, relation_list)
    else:
        yield obj
        #print (obj)
        #pass

#recursive_iter(data)
for item in recursive_iter(data, init_node, init_direction, node_map, relation_list):
    print (relation_list)
    pass


#modify real mesh json. [] are omitted
mesh_dict = """
    {
        "nodeId" : 2147321738,
        "subs" : [
            {
                "nodeId" : 2147319559,
                "subs" : [
                ]
            }
        ]
    }
    """

# data = json.loads(my_json_data)
# for item in recursive_iter(data):
#     print(item)

#data = json.loads(mesh_topo)


