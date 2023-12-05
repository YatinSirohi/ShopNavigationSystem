"""
student id - 21391002
Hash tables are created to quickly get all the shops based on given category and provide real time data in case modification happens in
the shop informations.
Code reference from my Practical 7 work
"""
import numpy as np

class HashEntry:                                        # Code reference from Practical 7 work
    def __init__(self, shopNumber, category, location, rating, shopName):
        self.key = category
        self.shopNumber = shopNumber
        self.category = category
        self.location = location
        self.rating = rating
        self.shopName = shopName
        self.state = 1

class HashTable:                                     # Assignment component 5:  Design the hash table
    def __init__(self, tableSize):
        self.minsize = 10
        self.upper_load_factor = 0.7
        self.lower_load_factor = 0.2
        actualSize = self.findNextPrime(max(tableSize, self.minsize))
        self.hashArray = np.empty(actualSize, dtype=object)  # empty array of HashEntry
        self.count = 0
        
    def findNextPrime(self, startVal):
        if startVal % 2 == 0:
            primeVal = startVal - 1
        else:
            primeVal = startVal
        
        isPrime = False
        
        while not isPrime:
            primeVal += 2
            ii = 3
            isPrime = True
            rootVal = int(primeVal ** 0.5)
            
            while ii <= rootVal:
                if primeVal % ii == 0:
                    isPrime = False
                    break
                ii += 2
        
        return primeVal

    def hashFunction(self, category):               # Assignment component 5: Hash function
        hashIndex = 0
        for i in range(len(category)-1):
            hashIndex = (hashIndex*31) + ord(category[i])
        hashIndex = hashIndex % len(self.hashArray)
        # print(hashIndex)
        return hashIndex
    
    def add(self, shopNumber, category, location, rating, shopName):        # Assignment component 5: Real time updates
        # a new hash entry
        entry = HashEntry(shopNumber, category, location, rating, shopName)

        # Find the hash index and add the entry
        hashIdx = self.hashFunction(category)
        origIdx = hashIdx

        while self.hashArray[hashIdx] is not None:
            hashIdx = (hashIdx + 1) % len(self.hashArray)       # Assignment component 5: collision handling
            if hashIdx == origIdx:
                # If Hash table is full, resize it
                self.resize(self.findNextPrime(len(self.hashArray) * 2))
                hashIdx = self.hashFunction(category)  # Recompute hash index after resizing

        self.hashArray[hashIdx] = entry
        self.count += 1
        self.hashArray[hashIdx].state = 1

    def searchShopsByCategory(self, category):              # Assignment component 5: Searching by category with error handling
        shops = []
        hashIdx = self.hashFunction(category)
        origIdx = hashIdx

        while self.hashArray[hashIdx] is not None:
            if self.hashArray[hashIdx].key == category and self.hashArray[hashIdx].state != -1:
                shops.append(self.hashArray[hashIdx])
            hashIdx = (hashIdx + 1) % len(self.hashArray)   # Assignment component 5: Collision handling
            if hashIdx == origIdx:
                break

        return shops
    
    def getLoadFactor(self):
        return self.count / len(self.hashArray)         # Total elements/size of hashtable
    
    def resize(self, newSize):
        # Create a new hash array with the specified size
        new_hashArray = [None] * newSize

        # Rehash all existing elements into the new array
        for entry in self.hashArray:
            if entry is not None:
                new_hashIdx = self.hashFunction(entry.key) % newSize
                while new_hashArray[new_hashIdx] is not None:
                    new_hashIdx = (new_hashIdx + 1) % newSize
                new_hashArray[new_hashIdx] = entry

        # Update the hashArray and recompute the count
        self.hashArray = new_hashArray
        self.count = sum(1 for entry in self.hashArray if entry is not None)

    def clearHashTable(self):                       # To clear the hash table
        for category in self.hashArray:
            if category is not None and category.state != -1:
                self.removeCategory(category.key)
            
    def removeCategory(self, category):             # Helper method to clear the hashtable after getting real time data
        hashIdx = self.hashFunction(category)
        origIdx = hashIdx
        giveUp = False
        removed = False

        while not giveUp:
            if self.hashArray[hashIdx] is None:
                # If the slot is never used, the key is not in the table
                return False
            elif self.hashArray[hashIdx].key == category:
                # Mark the entry as deleted
                self.hashArray[hashIdx].state = -1
                self.count -= 1
                removed = True
            hashIdx = (hashIdx + 1) % len(self.hashArray)
            if hashIdx == origIdx:
                giveUp = True

        if self.getLoadFactor() < self.lower_load_factor:
            new_size = max(self.minsize, len(self.hashArray) // 2)
            if len(self.hashArray) != new_size:
                self.resize(new_size)

        return removed
