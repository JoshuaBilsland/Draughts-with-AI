class Node:
    __data = None
    __parent = None

    def __init__(self, data, parent):
        self.__data = data
        self.__parent = parent # Node object

    def addChild(self, childData): # Add a new node object to the list of children
        self.__children(Node(childData))
    
    def getData(self): # Return data
        return self.__data

class Tree:
    __nodes = []
    
    def __init__(self, data):
        self.__nodes.appendNode(data) # Make root node

    def addChild(self, data, parent): # Add new child node
        self.__nodes.append(Node(data, parent))

    def getNodes(self): # Return the tree
        return self.__nodes 
    
    def getNodesByDepth(self): # Get nodes based on how far 'down the tree' they are
        print()


