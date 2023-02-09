import QueueClass

class TreeNode:
    def __init__(self, data):
        self.__data = data
        self.__children = []


    # Get
    def getData(self):
        return self.__data
    
    def getChildren(self):
        return self.__children


    # Other
    def addChild(self, childData):
        self.__children.append(TreeNode(childData))

    def getRootToLeafPaths(self, rootNode):
        paths = []
        queue = QueueClass.Queue(999)
        queue.enQueue((rootNode, [rootNode.getData()]))
        while queue.isEmpty() == False:
            currentNode, path = queue.deQueue()
            if len(currentNode.getChildren()) == 0:
                paths.append(path)
            else:
                for moveChildNode in currentNode.getChildren():
                    new_path = path + [moveChildNode.getData()]
                    queue.enQueue((moveChildNode, new_path))
        return paths