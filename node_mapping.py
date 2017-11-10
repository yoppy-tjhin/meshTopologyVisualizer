import json, time
import BitArray2D
from BitArray2D import godel
from read_serial import Serial

class NodeMapping:

    meshTopo = """[
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
    # TODO: more parameters init may be needed
    def __init__(self, xMapSize=15, yMapSize=15):
        #self.data = json.loads(NodeMapping.meshTopo)
        self.xMapSize = xMapSize
        self.yMapSize = yMapSize

        self.initNode = [int(self.xMapSize / 2), int(self.yMapSize / 2)]                   # initial node position
        self.initDirection = [0, 1]                                                        # initial direction vector
        self.nodeMap = BitArray2D.BitArray2D(rows=self.xMapSize, columns=self.yMapSize)    # create 2D bit array of node map
        self.nodeMap[int(self.xMapSize / 2), int(self.yMapSize / 2)] = 1                   # initialize the starting node position at the window CENTER
        self.relationList = []                                                             # list holding all relations

    # """
    # Initializing serial port.
    # :return: serialObj
    # """
    # def init_serial(self, comPort=None, baudRate=115200):
    #     serialObj = Serial(comPort, baudRate)
    #     return serialObj

    def find_empty_position(self, neighbourNodeId, currentNode, direction, nodeMap, relationList):
        found = 0                                                                       # indication that an empty is found
        allDir = [[1, 0], [0, 1], [-1, 0], [0, -1]]                                     # define North, East, West, South direction vectors
        newNode = [currentNode[0] + direction[0], currentNode[1] + direction[1]]        # try a new spot according to the preferred direction
        allDir.remove(direction)                                                        # remove the used direction

        # if available, take it
        if not nodeMap[ godel (newNode[0], newNode[1])]:

            nodeMap[newNode] = 1                                        # update node_map. the new_node is now taken
            relationList.append([currentNode[:], newNode[:]])           # put the relation in the list
            currentNode[:] = newNode                                    # update current_node
                                                                        # direction unchanged
            found = 1
            #pass

        # otherwise, try other directions
        else:
            # try every other direction until find an empty one
            for dir in allDir:
                newNode = [currentNode[0] + dir[0], currentNode[1] + dir[1]]         # try a new spot

                # Got a empty spot. Take it
                if not nodeMap[ godel(newNode[0], newNode[1])]:
                    nodeMap[newNode] = 1                                          # update node_map. the new_node is now taken
                    relationList.append([currentNode[:], newNode[:]])            # put the relation in the list
                    currentNode[:] = newNode                                      # update current_node
                    direction[:] = dir                                              # update the preferred direction
                    found = 1
                    break

        # TODO: Cannot find an empty spot
        # if (found == 0):
        pass

    def recursive_node_mapping(self, obj, current_node_pos, direction, node_map, relation_list):

        # if the object is a dictionary, then it contains its one nodeId, and its one subconnection list
        if isinstance(obj, dict):
            # direct neighbour of the current_node
            neighbourNodeId = obj["nodeId"]
            # find empty position in node_mapping, update current_node, update direction, update relation_list
            self.find_empty_position(neighbourNodeId, current_node_pos, direction, node_map, relation_list)
            print (neighbourNodeId)

            # go into the node's subconnections
            for item in obj["subs"]:
                self.recursive_node_mapping(item, current_node_pos[:], direction, node_map, relation_list)

        # if the object is a list, then it is a list of dictionaries
        elif isinstance(obj, list):
            for item in obj:
                self.recursive_node_mapping(item, current_node_pos[:], direction, node_map, relation_list)
        # else:
        #     return obj
            #print (obj)



# UNCOMMENT below to test the function separately
#recursive_node_mapping(data, init_node, init_direction, node_map, relation_list)
#print (relation_list)
#print (node_map)

# data = json.loads(my_json_data)
# for item in recursive_iter(data):
#     print(item)

#data = json.loads(mesh_topo)

meshTopo = """[
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
data = json.loads(NodeMapping.meshTopo)
x_map_size = 11
y_map_size = 11

init_node = [int(x_map_size / 2), int(y_map_size / 2)]                   # initial node position
init_direction = [0,1]                                                             # initial direction vector
node_map = BitArray2D.BitArray2D(rows=x_map_size, columns=y_map_size)    # create 2D bit array of node map
node_map[int(x_map_size / 2), int(y_map_size / 2)] = 1                             # initialize the center node
relation_list = []

# nodeMapping = NodeMapping()
# serialObj = nodeMapping.init_serial()
# while True:
#     jsonString = serialObj.read_json_string()
#     if jsonString != None:
#         print (jsonString)
#         break
#     time.sleep(0.5)
#
# #nodeMapping.recursive_node_mapping(data, init_node, init_direction, node_map, relation_list)
# jsonString = json.loads(jsonString)
#
# nodeMapping.recursive_node_mapping(jsonString, init_node, init_direction, node_map, relation_list)
# print (relation_list)
# print (node_map)




