"""
Code reference from my Practical 5 work. Linked list is used to store shop information in a graph
Student ID - 21391002
"""
class DSAListNode():                            # List node class
    def __init__(self, value = None):
        self.value = value
        self.next = None
        self.prev = None               
    def getValue(self):
        return self.value
    def setValue(self, value):
        self.value = value
    def getNext(self):
        return self.next
    def setNext(self, newNext):
        self.next = newNext
    def getPrev(self):                  
        return self.prev
    def setPrev(self, newPrev):         
        self.prev = newPrev
        
class DSALinkedList():
    def __init__(self):
        self.head = None            # Singly linked list with only head value
    
    def isEmpty(self):
        return self.head is None

    def insertFirst(self, newValue):
        newNd = DSAListNode(newValue)
        if self.isEmpty():
            self.head = newNd
            return newValue
        else:
            newNd.setNext(self.head)
            self.head = newNd
            return newValue
       
    def insertLast(self, newValue):
        newNd = DSAListNode(newValue)
        if self.isEmpty():
            self.head = newNd
            return newValue
        else:
            currNd = self.head
            while currNd.getNext() != None:
                currNd = currNd.getNext()
            currNd.setNext(newNd)
            return newValue

    def peekFirst(self):
        if self.isEmpty():
            print('Empty')
        else:
            nodeValue = self.head.getValue()
            return nodeValue

    def peekLast(self):
        if self.isEmpty():
            print('Empty')
        else:
            currNd = self.head
            while currNd.getNext() != None:
                currNd = currNd.getNext()
            nodeValue = currNd.getValue()
            return nodeValue
        
    def removeFirst(self):
        if self.isEmpty():
            print('Empty')
        else:
            nodeValue = self.head.getValue()
            self.head = self.head.getNext()
            return nodeValue
    
    def removeLast(self):
        if self.isEmpty():
            print('Empty')
        elif self.head.getNext() == None:
            nodeValue = self.head.getValue()
            self.head = None
            return nodeValue
        else:
            prevNd = None
            currNd = self.head
            while currNd.getNext() != None:
                prevNd = currNd
                currNd = currNd.getNext()
            prevNd.setNext(None)
            nodeValue = currNd.getValue()
            return nodeValue