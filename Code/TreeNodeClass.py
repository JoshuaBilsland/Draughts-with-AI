import QueueClass

class TreeNode:
    def __init__(self, data):
        self.__data = data
        self.__children = []


    # Get Methods
    def getData(self):
        return self.__data
    
    def getChildren(self):
        return self.__children


    # Other Methods

    # Add a child node to the list of child nodes
    def addChild(self, childData):
        self.__children.append(TreeNode(childData))


    # Return 2D list of every possible way of going from the root node (only down) to a leaf node
    # (Used by the AI/minimax to work out all possible combinations of moves in a given turn)
    def getAllRootToLeafPaths(self, rootNode):
        paths = []
        queue = QueueClass.Queue(999)
        queue.enQueue((rootNode, [rootNode.getData()]))

        while queue.isEmpty() == False:
            currentNode, path = queue.deQueue()
            if len(currentNode.getChildren()) == 0: # Leaf node found (0 child nodes)
                paths.append(path)
            else:
                # For each child node, enqueue the path and node and go back to loop start to check if those nodes are a leaf node
                for moveChildNode in currentNode.getChildren():
                    newPath = path + [moveChildNode.getData()]
                    queue.enQueue((moveChildNode, newPath))
        
        return paths