'''
Basic model for the algorithm visualizer.

This model includes methods to set up and run 3 different types of search algorithms: BFS, DFS, and A*.

Created on February 7th, 2023
@author: Samuel Dahlberg
'''

import math
import time
import heapq


class Model:

    # Dictionary for updating the view.
    # '1' = in queue
    # '2' = checked
    # '3' = solved path
    newChanges = {}

    def __init__(self, numRows):
        # Current list of Algorithms that the model can run
        self.algoList = ['BFS', 'A*', 'DFS']

        self.numRow = numRows

    # Returns the list of algorithms that the model can run
    def getAlgos(self):
        return self.algoList

    # Sets up all needed variables for the search algorithm.
    # Since the search is called step by step, set-up needs to be separate from the main search method
    def setSearch(self, grid, algo, start, end):

        self.st = time.process_time()

        # initializing class variables for the search algorithms. Since the algorithms are called step by step, they
        # need to be class variables. They also need to be initialized in this method, because we have a reset feature.
        self.visited = []
        self.backtrack = []
        self.queue = []
        self.done = False

        # Creating a 1D array representing the board. -1 indicates that the tile is at the start of the search, or did
        # not have a parent
        for i in range(self.numRow):
            for i in range(self.numRow):
                self.backtrack.append(-1)

        # Array to store the path weights for A*
        self.weights = []
        if algo == 'A*':
            for i in range(self.numRow):
                for i in range(self.numRow):
                    self.weights.append(1000000)

        # Getting the queue started with the initial start point
        if algo == 'A*':
            startF = self._heuristic(start, 0, end)
            self.visited.append(start)
            self.oheap = []
            heapq.heappush(self.oheap, startF)
            # self.queue.append(startF)
        else:
            self.visited.append(start)
            self.queue.append(start)

        self.algo = algo

    # Will be called throughout the search algorithm process. Each call represents one step in the search algorithm
    # This method simply calls the appropriate algorithm method
    def runSearch(self, grid, algo, start, end):
        self.newChanges = {}

        match algo:
            case 'BFS':
                self._BFS(grid, start)
            case "DFS":
                self._DFS(grid, start)
            case 'A*':
                self._AStar(grid, end)

        return self.newChanges, self.done

    # Breadth First Search: Method to complete one step of breadth first search. Will update the "newChanges" variable,
    # and the "done" variable.
    def _BFS(self, grid, start):
        # If there is anything left to search in queue, proceed
        if self.queue:
            n = self.queue.pop(0)
            self.newChanges[n] = 2
            self.visited.append(n)

            # Checking if the current tile is the end
            if grid[n] == 3:
                self.done = True
                et = time.process_time()
                res = et - self.st
                print('CPU Execution time: ', res, 'seconds')
                return self._processBacktrack(n)

            # Grabbing all neighbors, and checking if they have been searched, if not, add them to queue
            neighbors = self._checkNeighbors(n, grid)
            for neighbor in neighbors:
                if (neighbor not in self.visited) & (neighbor not in self.queue):
                    self.queue.append(neighbor)
                    self.newChanges[neighbor] = 1
                    self.backtrack[neighbor] = n

    # Depth First Search: Method to complete one step of depth first search. Will update the "newChanges" variable,
    # and the "done" variable.
    def _DFS(self, grid, start):
        # If there is anything left to search in queue, proceed
        if self.queue:
            n = self.queue.pop()
            self.newChanges[n] = 2
            self.visited.append(n)

            # Checking if the current tile is the end
            if grid[n] == 3:
                self.done = True
                et = time.process_time()
                res = et - self.st
                print('CPU Execution time: ', res, 'seconds')
                return self._processBacktrack(n)

            # Grabbing all neighbors, and checking if they have been searched, if not, add them to queue
            neighbors = self._checkNeighbors(n, grid)
            for neighbor in neighbors:
                if neighbor not in self.visited:
                    self.queue.append(neighbor)
                    self.newChanges[neighbor] = 1
                    self.backtrack[neighbor] = n

    # A* Search: Method to complete one step of A* search. Will update the "newChanges" variable,
    # and the "done" variable.
    def _AStar(self, grid, end):
        # In A*, each element in oheap will have [f, g, n]
        # f: g + euclidean distance to goal
        # g: path distance from start to this node
        # n: this node

        if self.oheap:
            # n = min(self.queue)
            n = heapq.heappop(self.oheap)
            # self.queue.remove(n)
            self.newChanges[n[2]] = 2

            if grid[n[2]] == 3:
                self.done = True
                et = time.process_time()
                res = et - self.st
                print('CPU Execution time: ', res, 'seconds')
                return self._processBacktrack(n[2])

            neighbors = self._checkNeighbors(n[2], grid)
            for neighbor in neighbors:
                temp = self._heuristic(neighbor, n[1], end)
                if temp[1] < self.weights[temp[2]]:
                    self.weights[temp[2]] = temp[1]
                    self.backtrack[temp[2]] = n[2]
                if neighbor not in self.visited:
                    self.visited.append(neighbor)
                    # self.queue.append(temp)
                    heapq.heappush(self.oheap, temp)
                    self.newChanges[neighbor] = 1

    # Method for calculating a heuristic. Has Euclidean and Manhattan distance heuristic available
    def _heuristic(self, n, g, end):
        endX = end % self.numRow
        endY = math.floor(end / self.numRow)
        nX = n % self.numRow
        nY = math.floor(n / self.numRow)
        # euclideanDistance = math.sqrt((endX - nX)**2 + (endY - nY)**2)
        manhattanDistance = abs(endX - nX) + abs(endY - nY)
        newG = g + 1
        # return [newG + euclideanDistance, newG, n]
        return [newG + manhattanDistance, newG, n]

    # Will return all neighbors of tile n.
    def _checkNeighbors(self, n, grid):
        r = self.numRow

        neighbors = []
        # Above
        if n >= r:
            if grid[n - r] == 0 or grid[n - r] == 3:
                neighbors.append(n - r)

        # Left
        if n % r != 0:
            if grid[n - 1] == 0 or grid[n - 1] == 3:
                neighbors.append(n - 1)

        # Right
        if n % r != (r - 1):
            if grid[n + 1] == 0 or grid[n + 1] == 3:
                neighbors.append(n + 1)

        # Below
        if n < ((r**2) - r):
            if grid[n + r] == 0 or grid[n + r] == 3:
                neighbors.append(n + r)

        return neighbors

    # When the end has been found, backtrack the search and return the path.
    def _processBacktrack(self, end):
        path = [end]
        self.newChanges[end] = 3
        while end != -1:
            tmp = self.backtrack[end]
            path.append(tmp)
            self.newChanges[tmp] = 3
            end = tmp
        return path
