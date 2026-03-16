## --------------------------------------------------
## Computational Thinking Assignment 1
## Tristan Walmsley - 21269280
## --------------------------------------------------

# Importing Libraries

import time                     # For performance timing
import tracemalloc              # For memory tracking
import random                   # For generating random test data
import math                     # For distance calculations
import heapq                    # For priority queue in Dijkstra's algorithm
import matplotlib.pyplot as plt # For plotting results
import pandas as pd             # For data manipulation
import os                       # For file path handling


# --------------------------------------------------
# Sorting & Searching Algorithms
# --------------------------------------------------

def bubbleSort(array):
    """
    Performs a bubble sort on a given Array. The
    function compares adjacent elements & swaps them if
    they are in the wrong order. Each iteration pushes
    the largest unsorted value to the end of the array.
    """

    n = len(array) #Get array length

    #Outer Loop through the array of elements
    for i in range(n - 1):

        #Inner loop that compares each pair of adjacent elements
        for j in range(n - i - 1):

            #Check if the next item is smaller and swap them
            if array[j] > array[j+1]:
                array[j], array[j+1] = array[j+1], array[j]
    
    #Return the sorted array
    return array

def mergeSort(array):
    '''
    Performs a recursive merge sort on a given array.
    The function splits the array into two halves
    repeatedly, sorts each half, & then merges them
    back together in a sorted order.
    '''

    n = len(array) #Get array length

    if n > 1:
        #Find the middle point
        midpoint = n // 2

        #Split the array into a left & right half
        leftArray  = array[0:midpoint]
        rightArray = array[midpoint:]

        # Recursively sort both halves
        sortedLeftArray  = mergeSort(leftArray)
        sortedRightArray = mergeSort(rightArray)

        #Merge the sorted halves together
        return merge(sortedLeftArray, sortedRightArray)
    
    else: #Base case - a list of 1 element is already sorted
        return array

def merge(leftArray, rightArray):
    '''
    Merges two sorted arrays into a single sorted array.
    Compares elements from each array & combines them.
    '''

    resultArray = []
    i = j = 0

    #Compares elements from both arrays & merges in order
    while i < len(leftArray) and j < len(rightArray):
        if leftArray[i] < rightArray[j]:
            resultArray.append(leftArray[i])
            i += 1
        else:
            resultArray.append(rightArray[j])
            j += 1
    
    #Add any remaining elements from either array
    resultArray.extend(leftArray[i:])
    resultArray.extend(rightArray[j:])

    return resultArray

def hashSearch(hashTable, key):
    '''
    Searches for a key in a hash table & returns its value.
    Since the time complexity is O(1), lookups are instant.
    '''

    if key in hashTable:
        return hashTable[key]
    return None

def binarySearch(array, targetValue):
    '''
    Performs a binary search on a sorted array to locate a
    target value. The array is repeatedly divided in half
    until the target value is found or the search range
    is empty.
    '''
    
    #Define starting and endpoints of the search range
    lowPoint = 0
    highPoint = len(array) - 1

    #Search as long as the search range is valid
    while lowPoint <= highPoint:
        #Calculate the midpoint
        midpoint = (lowPoint + highPoint) // 2
        
        #Check if the middle element matches the target value
        if array[midpoint] == targetValue:
            return midpoint
        
        # If the middle element is smaller, ignore the left half
        elif array[midpoint] < targetValue:
            lowPoint = midpoint + 1
        
        #If the middle element is larger, ignore the right half
        else:
            highPoint = midpoint - 1

    #Return None if the value is not found
    return None


# --------------------------------------------------
# Route Optimisation Algorithms
# --------------------------------------------------

def calculateDistance(pointA, pointB):
    '''
    Calculates the distance between two points A and B.
    Each point is represented as a tuple (x, y).
    '''
    # Distance Formula: sqrt((x2 - x1)^2 + (y2 - y1)^2)
    return math.sqrt((pointA["X"] - pointB["X"]) ** 2 + (pointA["Y"] - pointB["Y"]) ** 2)

def createGraph(dataframe, nodeData):
    '''
    Creates a graph representation from a dataframe.
    Each node represents the data, and edges represent distances between nodes.
    nodeData is the column name used to identify nodes in the dataframe.
    '''
    
    # Initialize an empty graph
    graph = {}

    # Iterate through each row in the dataframe
    for i, rowA in dataframe.iterrows():
        # nodeData is the column name to use as the node identifier
        # Initialize the node in the graph
        graph[rowA[nodeData]] = {}

        # Iterate through each row again to calculate distances
        for j, rowB in dataframe.iterrows():

            # Continue if it's the same node
            if rowA[nodeData] == rowB[nodeData]:
                continue
            else:
                # Calculate the distance between the two nodes
                distance = calculateDistance(rowA, rowB)

                # Add the edge to the graph
                graph[rowA[nodeData]][rowB[nodeData]] = distance

    return graph

def dijkstasRouteOptimisation(graph, startNode, goalNode):
    '''
    Implements Dijkstra's algorithm to find the shortest path
    from startNode to goalNode in the given graph.
    '''

    # Initialise testing variables
    operations = 0

    # Create a priority queue to store tuples of (cost, node)
    priorityQueue = [(0, startNode)]

    # Create a dictionary to store the shortest distance to each node
    # Initialize all distances to infinity
    distances = {node: float("inf") for node in graph}
    distances[startNode] = 0 # Distance to start node is 0

    # Create a dictionary to store the previous node
    previousNodes = {node: None for node in graph}

    # Main loop
    while priorityQueue:
        # Get the next node in the priority queue
        currentDistance, currentNode = heapq.heappop(priorityQueue)
        operations += 1

        # Check if we reached the goal node
        if currentNode == goalNode:
            break

        # Explore neighbors
        for neighbour, weight in graph[currentNode].items():
            operations += 1
            newDistance = currentDistance + weight

            # If a shorter path to the neighbor is found
            if newDistance < distances[neighbour]:
                # Update the distance and previous node
                distances[neighbour] = newDistance
                previousNodes[neighbour] = currentNode

                # Add the neighbor to the priority queue
                heapq.heappush(priorityQueue, (newDistance, neighbour))
    
    # Reconstruct the shortest path
    path = []
    currentNode = goalNode
    
    # Backtrack from goal to start using previousNodes
    while currentNode is not None:
        path.append(currentNode)
        currentNode = previousNodes[currentNode]
    
    path.reverse() # Reverse the path to get it from start to goal

    return path, distances[goalNode], operations

def heuristic(currentNode, goalNode, dataframe, nodeData):
    '''
    Heuristic function for A* algorithm.
    Estimates the cost from currentNode to goalNode.
    Uses distance as the heuristic.
    nodeData is the column name used to identify nodes in the dataframe.
    '''

    # Retrieve the coordinates of the current and goal nodes
    # iloc[0] gets the first row of the dataframe
    current = dataframe[dataframe[nodeData] == currentNode].iloc[0]
    goal    = dataframe[dataframe[nodeData] == goalNode].iloc[0]

    return calculateDistance(current, goal)

def aStarRouteOptimisation(graph, startNode, goalNode, dataframe, nodeData):
    '''
    Implements the A* algorithm to find the shortest path
    from startNode to goalNode in the given graph.
    nodeData is the column name used to identify nodes in the dataframe.
    '''

    # Initialise testing variables
    operations = 0

    # Create a priority queue to store tuples of (cost, node)
    priorityQueue = [(0, startNode)]

    # Create a dictionary to store the cost from start to each node
    # Initialize all distances to infinity
    gCosts = {node: float("inf") for node in graph}
    gCosts[startNode] = 0 # Cost to start node is 0

    # Create a dictionary to store the previous node
    previousNodes = {node: None for node in graph}

    # Main loop
    while priorityQueue:
        # Get the next node in the priority queue
        currentCost, currentNode = heapq.heappop(priorityQueue)
        operations += 1

        # Check if we reached the goal node
        if currentNode == goalNode:
            break

        # Explore neighbors
        for neighbour, weight in graph[currentNode].items():
            operations += 1

            # The tentative g cost is the cost from start to the neighbor
            tentativeGCost = gCosts[currentNode] + weight

            # If a shorter path to the neighbor is found
            if tentativeGCost < gCosts[neighbour]:
                # Update the g cost
                gCosts[neighbour] = tentativeGCost

                # Calculate the f cost (g + h)
                fCost = tentativeGCost + heuristic(neighbour, goalNode, dataframe, nodeData)
                
                # Update the previous node
                previousNodes[neighbour] = currentNode

                # Add the neighbor to the priority queue
                heapq.heappush(priorityQueue, (fCost, neighbour))

    # Reconstruct the shortest path
    path = []
    currentNode = goalNode

    # Backtrack from goal to start using previousNodes
    while currentNode is not None:
        path.append(currentNode)
        currentNode = previousNodes[currentNode]
    
    path.reverse() # Reverse the path to get it from start to goal

    return path, gCosts[goalNode], operations

# --------------------------------------------------
# Operation Counting Functions
# --------------------------------------------------

def countBubbleSortOperations(array):
    '''
    Counts the number of comparisons performed
    by the bubble sort algorithm.
    '''

    n = len(array)
    comparisons = 0

    for i in range(n - 1):
        for j in range(n - i - 1):
            comparisons += 1
            if array[j] > array[j + 1]:
                array[j], array[j + 1] = array[j + 1], array[j]

    return comparisons

def countMergeSortOperations(array):
    '''
    Counts the number of comparisons performed
    by the merge sort algorithm.
    '''

    if len(array) <= 1:
        return 0

    midpoint = len(array) // 2
    leftArray = array[:midpoint]
    rightArray = array[midpoint:]

    leftComparisons = countMergeSortOperations(leftArray)
    rightComparisons = countMergeSortOperations(rightArray)
    mergeComparisons = mergeAndCount(leftArray, rightArray)

    return leftComparisons + rightComparisons + mergeComparisons

def mergeAndCount(leftArray, rightArray):
    '''
    Merges two sorted arrays and counts the
    number of comparisons made during the merge.
    '''

    i = j = 0
    comparisons = 0

    while i < len(leftArray) and j < len(rightArray):
        comparisons += 1
        if leftArray[i] < rightArray[j]:
            i += 1
        else:
            j += 1

    return comparisons

def countBinarySearchOperations(array, targetValue):
    '''
    Counts the number of comparisons performed
    by the binary search algorithm.
    '''

    lowPoint = 0
    highPoint = len(array) - 1
    comparisons = 0

    while lowPoint <= highPoint:
        midpoint = (lowPoint + highPoint) // 2
        comparisons += 1

        if array[midpoint] == targetValue:
            return comparisons
        elif array[midpoint] < targetValue:
            lowPoint = midpoint + 1
        else:
            highPoint = midpoint - 1

    return comparisons

def countHashSearchOperations(hashTable, key):
    '''
    Counts the number of operations performed
    by the hash search algorithm.
    '''

    return 1 if key in hashTable else 0


# --------------------------------------------------
# Performance Measuring Functions
# --------------------------------------------------

def measurePerformance(function, *arguments):
    '''
    Measures the execution time and memory usage of a function.
    Returns the result, execution time, & memory used.
    '''

    # Start tracking memory
    tracemalloc.start()
    
    # Record start time
    startTime = time.perf_counter()
    
    # Execute the function
    result = function(*arguments)
    
    # Record end time
    endTime = time.perf_counter()
    
    # Get current and peak memory usage
    currentMemory, peakMemory = tracemalloc.get_traced_memory()
    
    # Stop tracking memory
    tracemalloc.stop()
    
    # Calculate execution time (in ms)
    executionTime = (endTime - startTime) * 1000
    memoryKb = peakMemory / 1024  # Convert to KB
    
    return result, executionTime, peakMemory / 1024 # Return result, time in ms, memory in KB

def displaySortingResults(algorithmName, execTime, memoryUsed, operations):
    '''
    Displays the results of a sorting algorithm.
    '''
    # Not printing the sorted array to reduce output size for large arrays
    print("-----")
    print(f"{algorithmName} Sort:")
    print(f"Time (2dp) = {execTime:.2f} ms, Memory = {memoryUsed:.2f} KB, Operations = {operations}")
    print("-----")

def displaySearchResults(algorithmName, searchResult, execTime, memoryUsed, searchKey, operations):
    '''
    Displays the results of a search algorithm.
    '''

    print("-----")
    print(f"{algorithmName} Search for {searchKey}: Result = {searchResult}")
    print(f"Time (4dp) = {execTime:.4f} ms, Memory = {memoryUsed:.4f} KB, Operations = {operations}")
    print("-----")

def displayRouteOptimisationResults(algorithmName, path, distance, operations):
    '''
    Displays the results of a route optimisation algorithm.
    '''

    print("-----")
    print(f"{algorithmName} Route Optimisation:")
    print(f"Path: {' -> '.join(map(str, path))}")
    print(f"Total Distance: {distance:.2f}, Operations: {operations}")
    print("-----")

def generateRandomRequests(numRequests):
    '''
    Generates a list of random priority values
    for testing purposes.
    '''

    priorities = [1, 2, 3] # 1: Low, 2: Medium, 3: High

    # Generate random priorities for the specified number of requests
    return [random.choice(priorities) for i in range(numRequests)]


# --------------------------------------------------
# Plotting Functions
# --------------------------------------------------

def plotResultsBarChart(size, resultsTable, title, ylabel, color, alpha, rotation):
    '''
    Plots a bar chart for the given results table.
    '''

    plt.figure(figsize=(10, 5))
    plt.bar(resultsTable.keys(), [resultsTable[alg][ylabel] for alg in resultsTable], color=color, alpha=alpha)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.xticks(rotation=rotation)
    plt.show()


def plotCampusMap(locationsDataframe, title, ylabel, xlabel):
    """
    Plots the unoptimised campus map and returns the matplotlib axes 
    so other functions can draw on the same map.
    """
    
    # Create the plot
    fig, ax = plt.subplots(figsize=(8, 6))

    # Get unique buildings
    buildings = locationsDataframe["Building"].unique()

    # Colour-coded building groups
    for building in buildings:
        # Filter locations for the current building
        subset = locationsDataframe[locationsDataframe["Building"] == building]
        # Plot the locations
        ax.scatter(subset["X"], subset["Y"], label=building)
        # Label each location
        for i, row in subset.iterrows():
            ax.text(row["X"], row["Y"], row["Name"], fontsize=8)

    # Set titles and labels
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.legend(title="Building") # Key

    return ax

def plotOptimisedRoute(locationsDataframe, path, title):
    # Plot the campus map first
    ax = plotCampusMap(locationsDataframe, title, "Y Coordinate", "X Coordinate")

    # Extract coordinates for the path
    xs, ys = [], []
    for loc_id in path:
        row = locationsDataframe[locationsDataframe["LocationID"] == loc_id].iloc[0]
        xs.append(row["X"])
        ys.append(row["Y"])

    # Draw route on the SAME axes
    ax.plot(xs, ys, linestyle="--", linewidth=2, marker="o", markersize=7, color="black")

    # Label the route nodes (optional)
    for i, loc_id in enumerate(path):
        ax.text(xs[i] + 0.5, ys[i] + 0.5, loc_id, fontsize=9)

    plt.show()

# --------------------------------------------------
# Algorithm Testing - Setup
# --------------------------------------------------

# Get the directory of this file
directory = os.path.dirname(os.path.abspath(__file__))
staffFilePath = directory + "\\datasets\\staff.csv.xlsx"

staffDataframe = pd.read_excel(directory + '/datasets/staff.csv.xlsx')
requestsDataframe = pd.read_excel(directory + '/datasets/requests.csv.xlsx')
locationsDataframe = pd.read_excel(directory + '/datasets/locations.csv.xlsx')

# Convert priority to number values and add as new column
priorityMapping = {'Low': 1, 'Medium': 2, 'High': 3}
requestsDataframe['PriorityValue'] = requestsDataframe['Priority'].map(priorityMapping)

# Get a list of priority values
priorityValuesList = requestsDataframe['PriorityValue'].tolist()

# Convert staff IDs to a hash table / dictionary
records = staffDataframe.to_dict(orient = 'records')
index = staffDataframe['StaffID'].to_list()
staffHashTable = pd.Series(data = records, index = index).to_dict()

# --------------------------------------------------
# Algorithm Testing - Searching & Sorting on Priorities
# --------------------------------------------------

unsortedPriorities = priorityValuesList.copy()

# Test Bubble Sort
bubbleSortedPriorities, bubbleTime, bubbleMemory = measurePerformance(bubbleSort, unsortedPriorities)
bubbleSortOperations = countBubbleSortOperations(unsortedPriorities.copy())
displaySortingResults("Bubble Sort (Priorities)", bubbleTime, bubbleMemory, bubbleSortOperations)

# Test Merge Sort
mergeSortedPriorities, mergeTime, mergeMemory = measurePerformance(mergeSort, unsortedPriorities)
print(mergeSortedPriorities)
mergeSortOperations = countMergeSortOperations(unsortedPriorities.copy())
displaySortingResults("Merge Sort (Priorities)", mergeTime, mergeMemory, mergeSortOperations)

# Test Hash Search
randomStaffID = random.choice(list(staffHashTable.keys())) # Select a random StaffID from the hash table keys
hashResult, hashTime, hashMemory = measurePerformance(hashSearch, staffHashTable, randomStaffID)
hashSearchOperations = countHashSearchOperations(staffHashTable, randomStaffID)
displaySearchResults("Hash", hashResult, hashTime, hashMemory, randomStaffID, hashSearchOperations)

# Test Binary Search
# Convert staff IDs like S001 to 1
staffIDList = [int(id[1:]) for id in staffDataframe['StaffID']]
sortedStaffIDs = mergeSort(staffIDList.copy())
print(sortedStaffIDs)

# Pick a random staff ID to search
targetStaff = random.choice(sortedStaffIDs)

# Perform the binary search
binaryResult, binaryTime, binaryMemory = measurePerformance(binarySearch, sortedStaffIDs, targetStaff)
binarySearchOperations = countBinarySearchOperations(sortedStaffIDs, targetStaff)
displaySearchResults("Binary", staffIDList[binaryResult], binaryTime, binaryMemory, targetStaff, binarySearchOperations)

# Collate the results for plotting
resultsTable = {
    "Bubble Sort": {
        "Time (ms)": bubbleTime,
        "Memory (KB)": bubbleMemory,
        "Operations": bubbleSortOperations
    },
    "Merge Sort": {
        "Time (ms)": mergeTime,
        "Memory (KB)": mergeMemory,
        "Operations": mergeSortOperations
    },
    "Hash Search": {
        "Time (ms)": hashTime,
        "Memory (KB)": hashMemory,
        "Operations": hashSearchOperations
    },
    "Binary Search": {
        "Time (ms)": binaryTime,
        "Memory (KB)": binaryMemory,
        "Operations": binarySearchOperations
    }
}


# --------------------------------------------------
# Algorithm Testing - Searching & Sorting on Random Requests
# --------------------------------------------------

# Generate & test random requests
randomRequests = generateRandomRequests(500)

# Test Bubble Sort with random requests
bubbleSortedRequests, bubbleTime, bubbleMemory = measurePerformance(bubbleSort, randomRequests.copy())
bubbleSortRandomOperations = countBubbleSortOperations(randomRequests.copy())
displaySortingResults("Bubble Sort (500 Random Requests)", bubbleTime, bubbleMemory, bubbleSortRandomOperations)

# Test Merge Sort with random requests
mergeSortedRequests, mergeTime, mergeMemory = measurePerformance(mergeSort, randomRequests.copy())
mergeSortRandomOperations = countMergeSortOperations(randomRequests.copy())
displaySortingResults("Merge Sort (500 Random Requests)", mergeTime, mergeMemory, mergeSortRandomOperations)

# Add staff IDs to the hash table for testing
for i in range(1, 300):
    staffHashTable[i] = {"StaffID": "S" + str(i).zfill(3), "Name": f"Staff Member {i}"}

# Test Hash Search with random requests
randomStaffID = random.choice(list(staffHashTable.keys())) # Select a random StaffID from the hash table keys
hashResult, hashTime, hashMemory = measurePerformance(hashSearch, staffHashTable, randomStaffID)
hashSearchRandomOperations = countHashSearchOperations(staffHashTable, randomStaffID)
displaySearchResults("Hash (500 Random Requests)", hashResult, hashTime, hashMemory, randomStaffID, hashSearchRandomOperations)

# Add 300 staff IDs to the staff id list for testing
staffIDList = [int(id[1:]) for id in staffDataframe['StaffID']]
for i in range(1, 300):
    if i not in staffIDList:
        staffIDList.append(i)

# Sort the staff IDs for binary search
sortedStaffIDs = mergeSort(staffIDList.copy())

# Test Binary Search with random requests
targetStaff = random.choice(sortedStaffIDs)
binaryResult, binaryTime, binaryMemory = measurePerformance(binarySearch, sortedStaffIDs, targetStaff)
binarySearchRandomOperations = countBinarySearchOperations(sortedStaffIDs, targetStaff)
displaySearchResults("Binary (500 Random Requests)", staffIDList[binaryResult], binaryTime, binaryMemory, targetStaff, binarySearchRandomOperations)

# Collate the results for plotting
randomResultsTable = {
    "Bubble Sort": {
        "Time (ms)": bubbleTime,
        "Memory (KB)": bubbleMemory,
        "Operations": bubbleSortRandomOperations
    },
    "Merge Sort": {
        "Time (ms)": mergeTime,
        "Memory (KB)": mergeMemory,
        "Operations": mergeSortRandomOperations
    },
    "Hash Search": {
        "Time (ms)": hashTime,
        "Memory (KB)": hashMemory,
        "Operations": hashSearchRandomOperations
    },
    "Binary Search": {
        "Time (ms)": binaryTime,
        "Memory (KB)": binaryMemory,
        "Operations": binarySearchRandomOperations
    }
}


# --------------------------------------------------
# Algorithm Testing - Route Optimisation
# --------------------------------------------------

# Pick random start and goal locations
startLocation = random.choice(locationsDataframe['LocationID'].tolist())

goalLocation = startLocation
while goalLocation == startLocation:
    goalLocation = random.choice(locationsDataframe['LocationID'].tolist())

# Create the graph from the locations dataframe
campusGraph = createGraph(locationsDataframe, "LocationID")

# Test Dijkstra's Algorithm
dijkstraResult, dijkstraTime, dijkstraMemory = measurePerformance(dijkstasRouteOptimisation, campusGraph, startLocation, goalLocation)
displayRouteOptimisationResults("Dijkstra's", dijkstraResult[0], dijkstraResult[1], dijkstraResult[2])

# Test A* Algorithm
aStarResult, aStarTime, aStarMemory = measurePerformance(aStarRouteOptimisation, campusGraph, startLocation, goalLocation, locationsDataframe, "LocationID")
displayRouteOptimisationResults("A*", aStarResult[0], aStarResult[1], aStarResult[2])

# Collate the results for plotting
routeResultsTable = {
    "Dijkstra's": {
        "Time (ms)": dijkstraTime,
        "Memory (KB)": dijkstraMemory,
        "Operations": dijkstraResult[2],
        "Distance": dijkstraResult[1]
    },
    "A*": {
        "Time (ms)": aStarTime,
        "Memory (KB)": aStarMemory,
        "Operations": aStarResult[2],
        "Distance": aStarResult[1]
    }
}


# --------------------------------------------------
# Algorithm Testing - Plotting Results
# --------------------------------------------------

# Plot the results on priorities - sorting and searching algorithms
plotResultsBarChart((10, 5), resultsTable, 
                    "Priorities - Sorting & Searching - Timing Performance", "Time (ms)", "blue", 0.7, 45)
plotResultsBarChart((10, 5), resultsTable, 
                    "Priorities - Sorting & Searching - Memory Performance", "Memory (KB)", "green", 0.7, 45)
plotResultsBarChart((10, 5), resultsTable, 
                    "Priorities - Sorting & Searching - No. Operations Performance", "Operations", "orange", 0.7, 45)

# Plot the results on random requests - sorting and searching algorithms
plotResultsBarChart((10, 5), randomResultsTable, 
                    "Random Requests - Sorting & Searching - Timing Performance", "Time (ms)", "blue", 0.7, 45)
plotResultsBarChart((10, 5), randomResultsTable, 
                    "Random Requests Sorting & Searching - Memory Performance", "Memory (KB)", "green", 0.7, 45)
plotResultsBarChart((10, 5), randomResultsTable, 
                    "Random Requests Sorting & Searching - No. Operations Performance", "Operations", "orange", 0.7, 45)

# Plot the results on route optimisation algorithms
plotResultsBarChart((10, 5), routeResultsTable, 
                    "Route Optimisation - Timing Performance", "Time (ms)", "blue", 0.7, 45)
plotResultsBarChart((10, 5), routeResultsTable, 
                    "Route Optimisation - Memory Performance", "Memory (KB)", "green", 0.7, 45)
plotResultsBarChart((10, 5), routeResultsTable,
                    "Route Optimisation - No. Operations Performance", "Operations", "orange", 0.7, 45)
plotResultsBarChart((10, 5), routeResultsTable,
                    "Route Optimisation - Distance Performance", "Distance", "red", 0.7, 45)

# Plot the optimised routes on the campus map
plotOptimisedRoute(locationsDataframe, dijkstraResult[0], "Optimised Route (Dijkstra)")
plotOptimisedRoute(locationsDataframe, aStarResult[0], "Optimised Route (A*)")
