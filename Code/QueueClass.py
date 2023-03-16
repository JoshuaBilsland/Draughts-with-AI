class Queue:
    def __init__(self, maxSize):
        self.__maxSize = maxSize
        self.__queue = []

    # Other Methods

    # Check if the queue is full 
    def isFull(self):
        boolean = False
        if len(self.__queue) == self.__maxSize:
            boolean = True

        return boolean


    # Check if the queue is empty
    def isEmpty(self):
        boolean = False
        if len(self.__queue) == 0:
            boolean = True

        return boolean


    # Check if the queue is full
    def enQueue(self, itemToEnQueue):
        if self.isFull() == False:
            self.__queue.append(itemToEnQueue)
        

    # Using the shift method, remove the item at the front of the queue and return it   
    def deQueue(self):
        if self.isEmpty() == False:
            itemToReturn = self.__queue[0]
            
            # Shift items (Queue uses the 'shift' method)
            for item in range(len(self.__queue)-1): # Move each item one to the left (overwriting each other and deleting the front item)
                self.__queue[item] = self.__queue[item+1]
            self.__queue.pop() # Delete the right-most item since it is a duplicate of the last item (and should not exist)
        
        return itemToReturn