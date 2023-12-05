""""
Queue code from my practicals work. Using it in BFS, to put the vertices in queue 
"""
import numpy as np

class DSAQueue():                                  # From the pseudo code in the slides
    def __init__(self):
        self.defaultCapacity = 100
        self.queue = np.array([None]*self.defaultCapacity)
        self.count = 0
        self.head = 0
        self.tail = 0

    def getCount(self):
        return self.count

    def isEmpty(self):
        if self.count == 0:
            return True
        else:
            return False

    def isFull(self):
        if len(self.queue) == self.defaultCapacity:
            return True
        else:
            return False

    def peek(self):
        if self.count == 0:
            print('Queue is empty')
        else:
            return self.queue[self.head]

    def enqueue(self, value):
            self.queue[self.tail] = value                   # Inserting value in the tail
            self.tail += 1                                  # Incrementing the tail count
            self.count += 1
            return value

    def dequeue(self):
        if self.count == 0:
            print('Queue is empty')
        else:
            headValue = self.queue[self.head]           # Getting the value from the head
            self.queue[self.head] = None                # Replacing with None
            self.head += 1                              # Incrementing head to the next value
            if self.head == self.tail:                  # In case queue becomes empty
                self.head = 0
                self.tail = 0
            self.count -= 1                             # Decrementing the count after dequeue operation

            return headValue
