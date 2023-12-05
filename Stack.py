"""
Stack code from my practical work. Using it to stack the vertex in DFS
"""
import numpy as np

class DSAStack():                                       # From the pseudo code in lecture slides
    def __init__(self):
        self.defaultCapacity = 100                      
        self.stack = np.array([None]*self.defaultCapacity)      # Initialising stack with array of default capacity
        self.count = 0                                  

    def getCount(self):
        return self.count  
                                     
    def isEmpty(self):                                  
        if self.count == 0:
            return True
        else:
            return False
    
    def push(self, value):
        if self.count == self.defaultCapacity:
            raise ValueError('Not allowed. Stack limit reached. Increase the limit')
        else:
            self.stack[self.count] = value                          # Inserting the given value to the available count place
            self.count += 1                                         # Incrementing the count
            return value
            
    def pop(self):
        topValue = self.stack[self.count - 1]                       # Getting the top value 
        self.stack[self.count - 1] = None                           # Replacing with none 
        self.count -= 1                                             # decrementing the count
        return topValue
    