import json
import BitArray2D
from BitArray2D import godel

class NodeMapping(object):

    mesh_topo = """[
    {
        "nodeId" : 2147321731,
        "subs" : [
            {
                "nodeId" : 2147319552,
                "subs" : [
                ]
            }
        ]
    },
    {
        "nodeId" : 2142436483,
        "subs" : [
            {
                "nodeId" : 2787708644,
                "subs" : [
                ]
            }
        ]
    }
]"""
    def __init__(self):
        data = json.loads(mesh_topo)

x_map_size = 11
y_map_size = 11

init_node = [int(x_map_size / 2), int(y_map_size / 2)]                  # initial node position

init_direction = [0,1]                                                  # initial direction vector
node_map = BitArray2D.BitArray2D(rows=x_map_size, columns=y_map_size)   # create 2D bit array of node map
node_map[int(x_map_size / 2), int(y_map_size / 2)] = 1                  # initialize the center node
relation_list = []                                                      # list holding all relations

def find_empty_position(neighbourNodeId, current_node, direction, node_map, relation_list):
    found = 0                                                                   # indication that an empty is found
    all_dir = [ [1,0], [0,1], [-1,0], [0,-1] ]                                  # define North, East, West, South direction vectors
    new_node = [current_node[0]+direction[0], current_node[1]+direction[1] ]    # try a new spot according to the preferred direction
    all_dir.remove(direction)                                                   # remove the used direction

    # if available, take it
    if not node_map[ godel (new_node[0], new_node[1]) ]:

        node_map[new_node] = 1                                                  # update node_map. the new_node is now taken
        relation_list.append( [current_node[:], new_node[:]] )                  # put the relation in the list
        current_node[:] = new_node                                              # update current_node
                                                                                # direction unchanged
        found = 1
        #pass
        #pass # got new node. update node_map, etc.. RETURN

    # otherwise, try other directions
    else:
        # try every other direction until find an empty one
        for dir in all_dir:
            new_node = [current_node[0]+dir[0], current_node[1]+dir[1]]         # try a new spot

            # Got a empty spot. Take it
            if not node_map[ godel( new_node[0], new_node[1])]:
                node_map[new_node] = 1                                          # update node_map. the new_node is now taken
                relation_list.append([current_node[:], new_node[:]])            # put the relation in the list
                current_node[:] = new_node                                      # update current_node
                direction[:] = dir                                              # update the preferred direction
                found = 1
                break
                #pass # got new node. update node_map, etc, RETURN

    # TODO: Cannot find an empty spot
    # if (found == 0):
    pass

def recursive_node_mapping(obj, current_node_pos, direction, node_map, relation_list):

    # if the object is a dictionary, then it contains its one nodeId, and its one subconnection list
    if isinstance(obj, dict):
        # direct neighbour of the current_node
        neighbourNodeId = obj["nodeId"]
        # find empty position in node_mapping, update current_node, update direction, update relation_list
        find_empty_position(neighbourNodeId, current_node_pos, direction, node_map, relation_list)
        print (neighbourNodeId)

        # go into the node's subconnections
        for item in obj["subs"]:
            recursive_node_mapping(item, current_node_pos[:], direction, node_map, relation_list)

    # if the object is a list, then it is a list of dictionaries
    elif isinstance(obj, list):
        for item in obj:
            recursive_node_mapping(item, current_node_pos[:], direction, node_map, relation_list)
    # else:
    #     return obj
        #print (obj)
        #pass

#recursive_iter(data)
# UNCOMMENT below to test the function separately
recursive_node_mapping(data, init_node, init_direction, node_map, relation_list)
#print (relation_list)
print (node_map)

# data = json.loads(my_json_data)
# for item in recursive_iter(data):
#     print(item)

#data = json.loads(mesh_topo)


