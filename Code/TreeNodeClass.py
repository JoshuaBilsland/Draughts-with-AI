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