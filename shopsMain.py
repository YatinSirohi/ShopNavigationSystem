"""
Student id - 21391002
DSA Final assignemtn - Shop finding and navigation system
This is a main file that needs to be executed to run the program. This .py file imports necessary modules and libraries to work together
as a complete program.
"""
import ShopsGraph
import shopsHashTable
import pandas as pd
import Heaps

def menu():
    print("\nShop Finding and Navigation system Menu:")
    print("(a) Add a new Shop")
    print("(b) Delete the existing Shop")
    print("(c) Add Path between the shops")
    print("(d) Delete Path between the shops")
    print("(e) Display shops as List")
    print("(f) Add path between shops from the csv file")
    print("(g) Breadth First Search")
    print("(h) Depth First Search")
    print("(i) Print all the available shops")
    print("(j) Update the Shop information")
    print("(k) Compare BFS and DFS and find shortest path")
    print("(l) Get shops based on category (From hash tables)")
    print("(m) Sort shops based on category (From maxHeaps)")
    print("(q) Quit")

def main():
    graph = ShopsGraph.ShopsGraph()             # graph object from ShopsGraph
    hashtable = shopsHashTable.HashTable(100)    # Hash table object from shopsHashTable
    heaps = Heaps.DSAHeap(100)
    graph.addShopsFromCsv()                     # Adding some shops already to start with. More shops can be added from CSV file as well

    while True:
        menu()
        choice = input("Choose an option: ").lower()

        if choice == 'a':
            shopNumber = input("Enter shop Number (Must be unique): ")
            shopName = input("Enter shop Name: ")
            category = input("Enter shop category: ")
            location = input("Enter shop location: ")
            try:
                user_rating = float(input("Enter shop rating (From 1 to 5): "))
                rating = round(user_rating, 1)
                if rating >= 0 and rating <= 5:
                    if not graph.hasShop(shopNumber):
                        graph.addShop(shopNumber, category, location, rating, shopName)
                        print('\nShop added. List of current shops -')
                        graph.allShops()
                    else:
                        print('\nShop not added. Shop number must be unique. Please try again.')
                else:
                    print('\nShop not added. Rating should be between 1 to 5. Please try again.')  # Assignment component 2: Error and exception handling
            except:
                print('\nShop not added. Rating should only be a float. Please try again.')   # Assignment component 2: Error and exception handling

        elif choice == 'b':
            print('\nAvailable shops are- ')
            graph.allShops()
            shopNumber = input("Enter Shop Number to delete: ")
            graph.deleteShop(shopNumber)

        elif choice == 'c':
            print('Available shops are- ')
            graph.allShops()
            shopNumber1 = input("Enter shopNumber 1: ")
            shopNumber2 = input("Enter shopNumber 2: ")
            graph.addPath(shopNumber1, shopNumber2)

        elif choice == 'd':
            print('Available shops are- ')
            graph.allShops()
            print('List of shops with connected paths')
            graph.displayAsList()
            shopNumber1 = input("Enter Shop Number of 1st shop: ")
            shopNumber2 = input("Enter Shop Number of 2nd shop: ")
            graph.deletePaths(shopNumber1, shopNumber2)

        elif choice == 'e':
            print('\nList of shops connected with paths-')
            graph.displayAsList()

        elif choice == 'f':
            graph.addPathsFromCsv()

        elif choice == 'g':
            start_label = input("\nEnter starting Shop number for BFS: ")
            stop_label = input("Enter destination shop number for BFS: ")
            bfs_order = graph.breadthFirstSearch(start_label, stop_label)
            if bfs_order != None:
                print("Breadth First Search Order to reach the destination from the source shop:", bfs_order)

        elif choice == 'h':
            start_label = input("\nEnter starting Shop number for DFS: ")
            stop_label = input("Enter destination shop number for DFS: ")
            dfs_order = graph.DepthFirstSearch(start_label, stop_label)
            if dfs_order is not None:
                print("Depth First Search Order to reach the destination from the source shop:", dfs_order)

        elif choice == 'i':
            print('\nList of all the shops-\n')
            graph.allShops()

        elif choice == 'j':
            shopNumber = input("Enter shop Number you want to update: ")
            newShopName = input("Enter new shop Name: ")
            newCategory = input("Enter new shop category: ")
            newLocation = input("Enter new shop location: ")
            try:
                newRating = float(input("Enter new shop rating: "))
                if newRating >= 0 and newRating <= 5:
                    graph.updateShop(shopNumber, newCategory, newLocation, newRating, newShopName)
                else:
                    print('\nRating should be between 1 to 5')
            except:
                print('\nShop not added. Rating should only be a float. Please try again.')
        
        elif choice == 'k':
            start_label = input("\nEnter starting Shop number for comparison: ")
            stop_label = input("Enter destination shop number for comparison: ")
            graph.compareBfsDfs(start_label, stop_label)

        elif choice == 'l':
            curr_vertex = graph.vertices.head
            while curr_vertex is not None:
                shopNumber = curr_vertex.getValue().shopNumber
                shopName = curr_vertex.getValue().shopName
                category = curr_vertex.getValue().category
                location = curr_vertex.getValue().location
                rating = curr_vertex.getValue().rating

                hashtable.add(shopNumber, category, location, rating, shopName)
                curr_vertex = curr_vertex.getNext()
            print('\nAvailable shops and categrory')
            c= graph.allShops()[['CATEGORY']]
            print(c.drop_duplicates())
            category = input("\nEnter a category to search: ")
            # Get shops of the specified category
            shops = hashtable.searchShopsByCategory(category)
            shopsList = []
            # Display the shops
            if shops:
                print(f"\nShops in the {category} category:")
                for shop in shops:
                    shopsList.append([shop.shopNumber,shop.shopName,shop.location,shop.rating])

                df = pd.DataFrame(shopsList, columns=['SHOPNUMBER','SHOPNAME', 'LOCATION', 'RATING'])
                print(df)
                hashtable.clearHashTable()                                      # To get the real time data in case shop is deleted
            else:
                print(f"\nNo shops found in the {category} category.")    # Assignment component 5 - exception handling 

        elif choice == 'm':
            curr_vertex = graph.vertices.head
            while curr_vertex is not None:
                shopNumber = curr_vertex.getValue().shopNumber
                shopName = curr_vertex.getValue().shopName
                category = curr_vertex.getValue().category
                location = curr_vertex.getValue().location
                rating = curr_vertex.getValue().rating

                hashtable.add(shopNumber, category, location, rating, shopName)
                curr_vertex = curr_vertex.getNext()
            print('\nAvailable shops and categrory')
            c= graph.allShops()[['CATEGORY']]
            print(c.drop_duplicates())
            category = input("\nEnter a category to get sorted shops based on rating: ")
            # Get shops of the specified category
            shops = hashtable.searchShopsByCategory(category)
            if shops:
                for shop in shops:
                    heaps.add(shop.shopNumber,shop.shopName,shop.category, shop.location, shop.rating)
                heaps.heapSort()                                        # Assignment component 6: Sorting by ratings using a max-heap
                print('\nList of shops sorted (in descending order) based on rating, using maxHeap:')
                heaps.display()                                         # Assignment component 6: Extracting and displaying sorted shops
                hashtable.clearHashTable()
                heaps.clearHeaps()
            else:
                print(f"\nNo shops found in the {category} category.")

        elif choice == 'q':
            print("\nThank you for visiting!\n")
            break
        
        else:
            print("Invalid selection. Please select a valid option from the menu.")
    

if __name__ == "__main__":
    main()