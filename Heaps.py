"""
Code reference from my Practical 8 work. Heaps are used to sort the shops based on rating, when category is mentioned.
Student ID - 21391002
"""
import numpy as np

class DSAHeapEntry:
    def __init__(self, shopNumber, shopName, category, location, rating):
        self.rating = rating                    # Priority in this case
        self.shopNumber = shopNumber
        self.shopName = shopName
        self.category = category
        self.location = location

    def getRating(self):
        return self.rating

    def setRating(self, rating):
        self.rating = rating

    def getShopName(self):
        return self.shopName

    def getShopNumber(self):
        return self.shopNumber
    
    def getCategory(self):
        return self.category
    
    def getLocation(self):
        return self.location
    

class DSAHeap:
    def __init__(self, maxSize):
        self.heap = np.empty(maxSize, dtype=object)
        self.count = 0

    def add(self, shopNumber, shopName, category, location, rating):
        if self.count < len(self.heap):
            entry = DSAHeapEntry(shopNumber, shopName, category, location, rating)
            self.heap[self.count] = entry
            self.trickleUp(self.count)
            self.count += 1
        else:
            print("Heap is full. Cannot add more elements.")

    def remove(self):
        if self.count > 0:
            root = self.heap[0]
            self.heap[0] = self.heap[self.count - 1]
            self.count -= 1
            self.trickleDown(0)
            return root
        else:
            print("Heap is empty. Cannot remove elements.")
            return None

    def display(self):
        for i in range(self.count-1,-1,-1):
            print("SHOPNUMBER:", self.heap[i].getShopNumber(), ", SHOPNAME:", self.heap[i].getShopName(), ", CATEGORY:", self.heap[i].getCategory(), 
                  ", LOCATION:", self.heap[i].getLocation(), ", RATING:", self.heap[i].getRating())
        
    def swap(self, index1, index2):
        self.heap[index1], self.heap[index2] = self.heap[index2], self.heap[index1]

    def trickleUp(self, index):
        parentIdx = (index - 1) // 2
        while index > 0 and float(self.heap[index].getRating()) > float(self.heap[parentIdx].getRating()):
            self.swap(index, parentIdx)
            index = parentIdx
            parentIdx = (index - 1) // 2

    def trickleDown(self, index, size=None):
        if size is None:
            size = self.count

        while index < size:
            leftChildIdx = index * 2 + 1
            rightChildIdx = leftChildIdx + 1
            largeIdx = index

            if leftChildIdx < size and float(self.heap[leftChildIdx].getRating()) > float(self.heap[largeIdx].getRating()):
                largeIdx = leftChildIdx
            if rightChildIdx < size and float(self.heap[rightChildIdx].getRating()) > float(self.heap[largeIdx].getRating()):
                largeIdx = rightChildIdx

            if largeIdx != index:
                self.swap(index, largeIdx)
                index = largeIdx
            else:
                break


    def heapify(self):
        for i in range((self.count // 2) - 1, -1, -1):
            self.trickleDown(i)

    def heapSort(self):
        self.heapify()
        for i in range(self.count-1, -1, -1):
            self.swap(0, i)
            self.trickleDown(0, size=i)

    def clearHeaps(self):
        self.count = 0


# if __name__ == "__main__":
#     # maxHeap = DSAHeap(10)
#     # maxHeap.add(5, "A")
#     # maxHeap.add(10, "B")
#     # maxHeap.add(8, "C")
#     # maxHeap.add(12, "D")
#     # maxHeap.add(3, "E")

#     # print("Heap Elements:")
#     # maxHeap.display()

#     # print("Removing the highest priority element:")
#     # removedEntry = maxHeap.remove()
#     # if removedEntry is not None:
#     #     print("Priority:", removedEntry.getPriority(), ", Value:", removedEntry.getValue())

#     # print("Updated Heap Elements:")
#     # maxHeap.display()

#     # print("Heap Sorting the Elements:")
#     # maxHeap.heapSort()
#     # maxHeap.display()

#     with open('RandomNames7000.csv') as csv_file:
#         csv_reader = csv.reader(csv_file, delimiter=',')
#         heap = DSAHeap(7000)
#         count = 0
#         for row in csv_reader:
#             heap.add(row[0], row[1])
#             count += 1
#         heap.heapSort()
#         heap.display()
#         result = heap.displayList()
#         result_df = pd.DataFrame(result, columns=['id', 'Name']) # Create a DataFrame from the list
#         result_df.to_csv('heapsort.csv', index=False)
#         print('Count of total records: ',count)
            