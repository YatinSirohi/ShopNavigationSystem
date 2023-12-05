"""
Student ID - 21391002
Graph consists of all the shop information and allow user to perform several operations like add shop, delete shop, add path and many more
Code reference from my Practical 6 work
"""
from LinkedList import DSALinkedList            # Importing Linkedlist to store shop objects. This linked list is my work from practicals
import csv                                      # Importing csv to read shops from csv file                 
import pandas as pd                             # To display the shop details in a nice dataframe
import numpy as np
import queueCode                                # Importing queueCode from my practicals for BFS
import Stack                                    # Importing Stack.DSAStack() from my practicals for DFS

class ShopsGraphNode:                           # Code reference from Practical 6 work
    def __init__(self, shopNumber, category, location, rating, shopName=None):  # Assignment component 1: Graph representation
        self.shopNumber = shopNumber                    # Should be unique. Considered as label of vertex.
        self.shopName = shopName
        self.category = category
        self.location = location
        self.rating = rating
        self.adjacency_list = DSALinkedList()       # Assignment component 1: Storing adjacency list
        self.visited = False                        # Used in DFS and BFS

    def addPathInAdjacencyList(self, vertex):
        curr_node = self.adjacency_list.head
        paths = []
        while curr_node is not None:
            item = curr_node.getValue()
            paths.append(item)
            curr_node = curr_node.getNext()
        if vertex not in paths:
            self.adjacency_list.insertLast(vertex)

    def getAdjacentShop(self):
        return self.adjacency_list

class ShopsGraph:
    def __init__(self):
        self.vertices = DSALinkedList()             # Using linked list that I created in practicals , to store shop information
        self.vertex_shopNumbers = {}

    def addShop(self, shopNumber, category, location, rating, shopName):       # Assignment component 2: adding a shop node
        if not self.hasShop(shopNumber):                                       # Other exceptions handeled while taking user input
            new_vertex = ShopsGraphNode(shopNumber, category, location, rating, shopName)
            self.vertices.insertLast(new_vertex)
            self.vertex_shopNumbers[shopNumber] = new_vertex
    
    def updateShop(self, shopNumber, newCategory, newLocation, newRating, newShopName):     # Assignment component 2: Updating shop info
        if self.hasShop(shopNumber):
            existing_shop = self.vertex_shopNumbers[shopNumber] # Getting exisiting shop details
            # Updating the shop's information
            existing_shop.category = newCategory
            existing_shop.location = newLocation
            existing_shop.rating = newRating
            existing_shop.shopName = newShopName
        else:
            print('\nShop number does not exist. Please enter valid shop number')

    def allShops(self):             # To get all the shops available with all the details
        all_shops = np.array([], dtype=object)
        curr_vertex = self.vertices.head
        while curr_vertex is not None:                      # Getting all the information of the shops
            shopNumber = curr_vertex.getValue().shopNumber
            shopName = curr_vertex.getValue().shopName
            category = curr_vertex.getValue().category
            location = curr_vertex.getValue().location
            rating = curr_vertex.getValue().rating
            all_shops = np.append(all_shops, [shopNumber,shopName,category,location,rating])       # Adding the informations in the list
            curr_vertex = curr_vertex.getNext()
        all_shops = all_shops.reshape(-1, 5)                # Reshaping to fit in pandas dataframe to show as cleaner output
        df = pd.DataFrame(all_shops, columns=['SHOPNUMBER', 'SHOPNAME', 'CATEGORY', 'LOCATION', 'RATING'])
        print(df)               # showing the shops in pandas dataframe
        return df

    def addPath(self, shopNumber1, shopNumber2):                            # Assignment component 3: Add edge
        if self.hasShop(shopNumber1) and self.hasShop(shopNumber2):
            if shopNumber1 != shopNumber2:  # To Avoid adding self-loop edges
                vertex1 = self.vertex_shopNumbers[shopNumber1]
                vertex2 = self.vertex_shopNumbers[shopNumber2]

                vertex1.addPathInAdjacencyList(vertex2)
                vertex2.addPathInAdjacencyList(vertex1)
            else:
                print('\nCannot add path between same shop. Please select different shop numbers')
        else:
            print('\nPath not added. Shop numbers not available')

    def hasShop(self, shopNumber):
        return shopNumber in self.vertex_shopNumbers

    def getShopCount(self):
        return self.vertices.getCount()

    def getPathCount(self):
        return self.vertices.getCount()

    def getShop(self, shopNumber):
        if self.hasShop(shopNumber):
            return self.vertex_shopNumbers[shopNumber].shopName
        else:
            return None

    def getAdjacentShop(self, shopNumber):
        adjacent_vertices = []
        if self.hasShop(shopNumber):
            vertex_node = self.vertex_shopNumbers[shopNumber]
            adjacent_list = vertex_node.getAdjacentShop()
            curr_node = adjacent_list.head
            while curr_node is not None:
                adjacent_vertices.append(curr_node.getValue().shopNumber)
                curr_node = curr_node.getNext()
        return adjacent_vertices

    def isAdjacent(self, shopNumber1, shopNumber2):
        if self.hasShop(shopNumber1) and self.hasShop(shopNumber2):
            adjacent_vertices = self.getAdjacentShop(shopNumber1)
            return shopNumber2 in adjacent_vertices
            
    def deleteShop(self, shopNumber):                   # Assignment component 2: deleting a shop node
        if self.hasShop(shopNumber):
            self.deleteShopPaths(shopNumber)            # Helper method to delete the paths of deleted shop with other shops
            # Remove the vertex from the vertices linked list
            curr_vertex = self.vertices.head
            prev_vertex = None

            while curr_vertex is not None:
                if curr_vertex.getValue().shopNumber == shopNumber:
                    if prev_vertex is None:
                        self.vertices.head = curr_vertex.getNext()
                    else:
                        prev_vertex.setNext(curr_vertex.getNext())
                    break
                prev_vertex = curr_vertex
                curr_vertex = curr_vertex.getNext()

            # Remove the vertex from the vertex_shopNumbers dictionary
            del self.vertex_shopNumbers[shopNumber]
                
            print('Shop details have been deleted')
        else:
            print('Shop number does not exist')         # Assignment component 2: Error and exception handling

    def deleteShopPaths(self, shopNumber):      # Helper method to delete paths of the shop from the other shops, when shop is being deleted
        if self.hasShop(shopNumber):
            # Get the vertex corresponding to the shopNumber
            shop_vertex = self.vertex_shopNumbers[shopNumber]

            # Iterate through all other shops to remove paths to the shop being deleted
            for other_shopNumber, other_vertex in self.vertex_shopNumbers.items():
                if other_shopNumber != shopNumber:
                    # Remove the edge from other_vertex to shop_vertex
                    self.removeEdge(other_vertex, shop_vertex)
 
    def deletePaths(self, shopNumber1, shopNumber2):                  # Assignment component 3: delete edge
        if self.hasShop(shopNumber1) and self.hasShop(shopNumber2):
            vertex1 = self.vertex_shopNumbers[shopNumber1]
            vertex2 = self.vertex_shopNumbers[shopNumber2]

            # Check if shopNumber2 is in the adjacency list of shopNumber1
            if self.isAdjacent(shopNumber1, shopNumber2):
                # Remove the edge between shopNumber1 and shopNumber2
                self.removeEdge(vertex1, vertex2)
                print('\nPath between Shop',shopNumber1,'and Shop',shopNumber2,'has been deleted')
            else:
                print('\nNo path exists between Shop',shopNumber1,'and Shop',shopNumber2)
        else:
            print('One or both shop numbers do not exist')

    def removeEdge(self, vertex1, vertex2):                 # Helper method to delete paths
        # Remove the edge between vertex1 and vertex2
        curr_node = vertex1.adjacency_list.head
        prev_node = None

        while curr_node is not None:
            if curr_node.getValue() == vertex2:
                if prev_node is None:
                    vertex1.adjacency_list.head = curr_node.getNext()
                else:
                    prev_node.setNext(curr_node.getNext())
                break
            prev_node = curr_node
            curr_node = curr_node.getNext()
        # Similarly, remove the edge between vertex2 and vertex1
        curr_node = vertex2.adjacency_list.head
        prev_node = None

        while curr_node is not None:
            if curr_node.getValue() == vertex1:
                if prev_node is None:
                    vertex2.adjacency_list.head = curr_node.getNext()
                else:
                    prev_node.setNext(curr_node.getNext())
                break
            prev_node = curr_node
            curr_node = curr_node.getNext()

    def displayAsList(self):                                            # Assignment component 1: Showing adjacent shops as a list
        curr_vertex = self.vertices.head
        while curr_vertex is not None:
            shopNumber = curr_vertex.getValue().shopNumber
            adjacent_vertices = self.getAdjacentShop(shopNumber)
            # list of vertices with the shopNumber at the front
            formatted_adjacent = [shopNumber]+['-->'] + [adjacentShop for adjacentShop in adjacent_vertices if adjacentShop != shopNumber]
            # Convert the list to a comma-separated string
            formatted_adjacent_str = [', '.join(formatted_adjacent)]

            print(formatted_adjacent_str)
            curr_vertex = curr_vertex.getNext()

    def DepthFirstSearch(self, start_label, stop_label):        # Assignment component 4: Implement DFS correctly
    # Creating a stack
        stack = Stack.DSAStack()
        # List to store the visited vertices in the order they are visited so can be returned as output
        dfs_order = []

        if self.hasShop(start_label) and self.hasShop(stop_label):      # Assignment component 4: Input validation
            start_vertex = self.vertex_shopNumbers[start_label]
            stop_vertex = self.vertex_shopNumbers[stop_label]
            stack.push(start_vertex)
            while not stack.isEmpty():
                current_vertex = stack.pop()
                if current_vertex is not None and not current_vertex.visited:
                    # Marking the current vertex as visited
                    current_vertex.visited = True
                    # Adding the current vertex to the visited_order list
                    dfs_order.append([current_vertex.shopNumber, current_vertex.shopName])
                    if current_vertex.shopNumber == stop_label:
                        break
                    # Geting the adjacent vertices of the current vertex
                    adjacent_vertices = self.getAdjacentShop(current_vertex.shopNumber)
                    adjacent_vertices.sort()  # Sort alphabetically
                    # Pushing the sorted adjacent vertices onto the stack in reverse order
                    for adjacent_label in reversed(adjacent_vertices):
                        adjacent_vertex = self.vertex_shopNumbers[adjacent_label]
                        # If the adjacent vertex is not visited, append it to the stack
                        if not adjacent_vertex.visited:
                            stack.push(adjacent_vertex)
        # Reset the 'visited' flag for all vertices after DFS
            self.resetVisited()
            if ([start_vertex.shopNumber, start_vertex.shopName]) in dfs_order and ([stop_vertex.shopNumber, stop_vertex.shopName]) in dfs_order:
                return dfs_order
            else:
                print('\nNo path between source and destination shops for DFS')                           # Assignment component 4: Error handling
        else:
            print("Source or destination shops are not available for DFS. Please check and try again")  # Assignment component 4: Error handling

    def breadthFirstSearch(self, start_label, stop_label=None):         # Assignment component 4: Implement BFS correctly
        # queue for BFS
        Q = queueCode.DSAQueue()
        # Clear the 'visited' flag for all vertices
        self.resetVisited()
        # Check if the start_label is a valid vertex
        if self.hasShop(start_label) and self.hasShop(stop_label):      # Assignment component 4: Input validation
            # Get the start_vertex and mark it as visited
            start_vertex = self.vertex_shopNumbers[start_label]
            stop_vertex = self.vertex_shopNumbers[stop_label]
            start_vertex.visited = True
            # Enqueue the start_vertex into the BFS queue
            Q.enqueue(start_vertex)
            bfs_order = []
            # Perform BFS
            while not Q.isEmpty():
                # Dequeue a vertex from the BFS queue
                current_vertex = Q.dequeue()
                bfs_order.append([current_vertex.shopNumber, current_vertex.shopName])
                # If the stop_label is reached, stop the BFS
                if stop_label is not None and current_vertex.shopNumber == stop_label:
                    break
                # Get the adjacent vertices of the current vertex
                adjacent_vertices = self.getAdjacentShop(current_vertex.shopNumber)
                adjacent_vertices.sort()

                for adjacent_label in adjacent_vertices:
                    adjacent_vertex = self.vertex_shopNumbers[adjacent_label]
                    # If the adjacent vertex is not visited, mark it as visited
                    # and enqueue it into the BFS queue
                    if not adjacent_vertex.visited:
                        adjacent_vertex.visited = True
                        Q.enqueue(adjacent_vertex)
        # Reset the 'visited' flag for all vertices after BFS
            self.resetVisited()
            if ([start_vertex.shopNumber, start_vertex.shopName]) in bfs_order and ([stop_vertex.shopNumber, stop_vertex.shopName]) in bfs_order:
                return bfs_order
            else:
                print('\nNo path between source and destination shops for BFS')                               # Assignment component 4: Error handling
        else:
            print('\nSource or destination shops are not available for BFS. Please check and try again')    # Assignment component 4: Error handling
                
    def resetVisited(self):
        for label in self.vertex_shopNumbers:
            self.vertex_shopNumbers[label].visited = False

    def compareBfsDfs(self, start_label, stop_label):               # Assignment component 4: comparing BFS and DFS
        bfs = self.breadthFirstSearch(start_label, stop_label)
        dfs = self.DepthFirstSearch(start_label, stop_label)
        if bfs is not None:
            print('\nBFS path: ',bfs)
        if dfs is not None:
            print('\nDFS path: ',dfs)
        try:
            if len(bfs) > len(dfs):
                print('\nDFS is the shortest path between shop',start_label,'and shop',stop_label)
            elif len(dfs) > len(bfs):
                print('\nBFS is the shortest path between shop',start_label,'and shop',stop_label)
            else:
                print('\nBoth the paths have same distance')
        except:
            print('Could not complete comparison')

    def addPathsFromCsv(self):                      # code reference - Csv documentation - https://docs.python.org/3/library/csv.html 
        try:
            with open('paths.csv', 'r', newline='', encoding='utf-16') as pathsFile:
                csvreader = csv.reader(pathsFile)
                for row in csvreader:
                    if len(row) == 2:
                        shopNumber1 = row[0]
                        shopNumber2 = row[1]
                        if self.hasShop(shopNumber1) and self.hasShop(shopNumber2):
                            self.addPath(shopNumber1, shopNumber2)
                        else:
                            print('Shop numbers',shopNumber1,'and/or',shopNumber2,'do not exist, skipping path creation between them.')
        except Exception as e:
            print(f"An error occurred while adding paths from CSV: {str(e)}")

    def addShopsFromCsv(self):                  # code reference - Csv documentation - https://docs.python.org/3/library/csv.html 
        with open('shops.csv', 'r') as file:
            reader = csv.reader(file)
            rows = []
            for row in reader:
                rows.append(row)

            for j in rows:
                shopNumber = j[0]
                shopName = j[1]
                category = j[2]
                location = j[3]
                rating =  j[4]
                self.addShop(shopNumber, category, location, rating, shopName)
            print('\nSome shops are already added. You can add more shops from the interactive menu or from the csv file.\n')
            self.allShops()