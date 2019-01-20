from __future__ import print_function
#Use priority queues from Python libraries, don't waste time implementing your own
#from heapq import *

import heapq
import pdb

ACTIONS = [(0,-1),(-1,0),(0,1),(1,0)]

class Agent:
    def __init__(self, grid, start, goal, type):
        self.grid = grid
        self.previous = {}
        self.explored = []
        self.start = start 
        self.grid.nodes[start].start = True
        self.goal = goal
        self.grid.nodes[goal].goal = True
        self.new_plan(type)
    def new_plan(self, type):
        self.finished = False
        self.failed = False
        self.type = type
        if self.type == "dfs" :
            self.frontier = [self.start]
            self.explored = []
        elif self.type == "bfs":
            self.frontier = [self.start]
            self.explored = []
        elif self.type == "ucs":
            self.frontier = []
            heapq.heappush(self.frontier,(0,self.start))
            self.explored = []
            self.map={}
        elif self.type == "astar":
            pass
    def show_result(self):
        current = self.goal
        while not current == self.start:
            current = self.previous[current]
            self.grid.nodes[current].in_path = True #This turns the color of the node to red
    def make_step(self):
        if self.type == "dfs":
            self.dfs_step()
        elif self.type == "bfs":
            self.bfs_step()
        elif self.type == "ucs":
            self.ucs_step()
        elif self.type == "astar":
            self.astar_step()      

        """
        Question: Where are we calling this function recursively? Or where it is being called in the first place? Becaues here we are only going through the given node's children and once we are done we return true or false and we do not go to the entire frontire at all. 
        """           
    def dfs_step(self):
        #...
        if not self.frontier:
            self.failed = True
            print("no path")
            return
        current = self.frontier.pop()
        print("current node: ", current)
        #...
        self.grid.nodes[current].checked = True
        self.grid.nodes[current].frontier = False
        self.explored.append(current)
        children = [(current[0]+a[0], current[1]+a[1]) for a in ACTIONS]
        #Going through each node in the list called children, which contains all the children/puddle near the current node
        for node in children:
            #See what happens if you disable this check here
            if node in self.explored or node in self.frontier:
                print("explored before: ", node)
                continue
            #Checking to see if the 'node' object's coordinates are in the allowed broundry of the frid or no
            if node[0] in range(self.grid.row_range) and node[1] in range(self.grid.col_range):
                #Checking to see if the given node is a puddle/wall(can not be part of the path)
                if self.grid.nodes[node].puddle:
                    print("puddle at: ", node)
                else:
                    #Setting the previous node if the 'node' we are working is an actualy allowed coordinate in the grid(node)
                    self.previous[node] = current
                    # Checking to see if we found our destination/goal node that we are looking for
                    if node == self.goal:
                        self.finished = True
                        return
                    else:
                        # Adding the current 'node' to the frontier if it not the goal node we are looking for, so we can run dfs on it later on
                        self.frontier.append(node)
                        # Setting the frontire of the given 'node' to true, to indicate it is non-empty
                        self.grid.nodes[node].frontier = True
            else:
                print("out of range: ", node)
        """
        Question: For the bfs, How do we make sure that the list is beging used as a queue and not as a stack. 
        """          
    def bfs_step(self):
        if not self.frontier:
            self.failed = True
            print("no path")
            return
        current = self.frontier.pop(0)
        print("current node: ", current)
        #...
        self.grid.nodes[current].checked = True
        self.grid.nodes[current].frontier = False
        self.explored.append(current)
        children = [(current[0]+a[0], current[1]+a[1]) for a in ACTIONS]
        #Going through each node in the list called children, which contains all the children/puddle near the current node
        for node in children:
            #See what happens if you disable this check here
            if node in self.explored or node in self.frontier:
                print("explored before: ", node)
                continue
            #Checking to see if the 'node' object's coordinates are in the allowed broundry of the frid or no
            if node[0] in range(self.grid.row_range) and node[1] in range(self.grid.col_range):
                #Checking to see if the given node is a puddle/wall(can not be part of the path)
                if self.grid.nodes[node].puddle:
                    print("puddle at: ", node)
                else:
                    #Setting the previous node if the 'node' we are working is an actualy allowed coordinate in the grid(node)
                    self.previous[node] = current
                    # Checking to see if we found our destination/goal node that we are looking for
                    if node == self.goal:
                        self.finished = True
                        return
                    else:
                        # Adding the current 'node' to the frontier if it not the goal node we are looking for, so we can run dfs on it later on
                        self.frontier.append(node)
                        # Setting the frontire of the given 'node' to true, to indicate it is non-empty
                        self.grid.nodes[node].frontier = True
            else:
                print("out of range: ", node)
    
    
    
    def ucs_step(self):
        #[Hint] you can get the cost of a node by node.cost()
        if not self.frontier:
            self.failed = True
            print("no path")
            return
        current = heapq.heappop(self.frontier)
        print("current node: ", current)
        #...
        self.grid.nodes[current[1]].checked = True
        self.grid.nodes[current[1]].frontier = False
        self.explored.append(current[1])
        # Adding the cost of the current Node
        self.map[current[1]] = self.grid.nodes[current[1]].cost()

        children = [(current[1][0]+a[0], current[1][1]+a[1]) for a in ACTIONS]
        #Going through each node in the list called children, which contains all the children/puddle near the current node
        for node in children:
            #See what happens if you disable this check here
            if node in self.explored and node in self.frontier:
                print("explored before: ", node)
                continue
            #Checking to see if the 'node' object's coordinates are in the allowed broundry of the frid or no
            if node[0] in range(self.grid.row_range) and node[1] in range(self.grid.col_range):
                #Checking to see if the given node is a puddle/wall(can not be part of the path)
                if self.grid.nodes[node].puddle:
                    print("puddle at: ", node)
                else:
                    #Setting the previous node if the 'node' we are working is an actualy allowed coordinate in the grid(node)
                    currentCost = self.grid.nodes[node].cost()
                    newCost = currentCost + self.map[current[1]]
                    print("Old cost is: " + str(currentCost) + " newCost is: " + str(newCost))
                    self.previous[node] = current[1]
                    # Checking to see if we found our destination/goal node that we are looking for
                    if node == self.goal:
                        self.finished = True
                        return
                    else:
                        # Adding the current 'node' to the frontier if it not the goal node we are looking for, so we can run dfs on it later on

                        # Checking if the node is in the frontire or no
                        if node not in self.frontier:
                            print ("node is: " + str(node))
                            heapq.heappush(self.frontier,(newCost,node))
                        else:
                            for each in self.frontier:
                                if node == each[1] and each[0] > newCost:
                                    #remove the old node and add the new one
                                    self.frontier.remove(node)
                                    heapify(self.frontier)
                                    heapq.heappush(self.frontier,(newCost,node))
                       
                        # Setting the frontire of the given 'node' to true, to indicate it is non-empty
                        self.grid.nodes[node].frontier = True
            else:
                print("out of range: ", node)
    



    def astar_step(self):
        #[Hint] you need to declare a heuristic function for Astar
        pass
