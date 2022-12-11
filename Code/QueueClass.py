class Queue:
    def __init__(self, maxSize):
        self.__maxSize = maxSize
        self.__queue = []
    
    def isFull(self):
        boolean = False
        if len(self.__queue) == self.__maxSize:
            boolean = True
        return boolean

    def isEmpty(self):
        boolean = False
        if len(self.__queue) == 0:
            boolean = True
        return boolean

    def enQueue(self, itemToEnQueue):
        if self.isFull() == False:
            self.__queue.append(itemToEnQueue)
        
    def deQueue(self):
        if self.isEmpty() == False:
            itemToReturn = self.__queue[0]
            
            # Shift items
            for item in range(len(self.__queue)-1): # Move each item one to the left (overwriting each other and deleting the front item)
                self.__queue[item] = self.__queue[item+1]
            self.__queue.pop() # Delete the right-most item since it is a duplicate of the last item (and should not exist)
        
        return itemToReturn