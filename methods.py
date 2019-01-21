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
            self.map={self.start:0}
            self.frontierList=[]
            self.frontierList.append(self.start)
        elif self.type == "astar":
            self.explored = []
            startCost = self.grid.nodes[self.start].cost() + 0
            self.frontierList=[]
            self.frontierList.append(self.start)
            self.frontier=[]
            self.map={self.start:startCost}
            heapq.heappush(self.frontier,(startCost,self.start))

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

    def dfs_step(self):
        # Checking if the frontire is empty
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
             
    def bfs_step(self): 
        # Checking if the frontire is empty
        if not self.frontier:
            self.failed = True
            print("no path")
            return
        # Extract the first element from the frontier 
        current = self.frontier.pop(0)
        print("current node: ", current)
        
        # Setting the checks to proper boolean value 
        self.grid.nodes[current].checked = True
        self.grid.nodes[current].frontier = False
        self.explored.append(current)

        # Finding all the children of the current node
        children = [(current[0]+a[0], current[1]+a[1]) for a in ACTIONS]
        
        # Going through each node in the list called children, which contains all the children/puddle near the current node
        for node in children:
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
        # Checking if the frontire is empty
        if not self.frontier:
            self.failed = True
            print("no path")
            return

        current1 = heapq.heappop(self.frontier)
        print("current node: ", current1)
        # Setting the checks to proper boolean value 
        self.grid.nodes[current1[1]].checked = True
        self.grid.nodes[current1[1]].frontier = False
        self.explored.append(current1[1])
        
        if current1[1] == self.goal:
            self.finish = True
            return 
        children = [(current1[1][0]+a[0], current1[1][1]+a[1]) for a in ACTIONS]

        #Going through each node in the list called children, which contains all the children/puddle near the current node
        for node in children:
            #See what happens if you disable this check here
            if node in self.explored or node in self.frontier:
                print("explored before: ", node)
                continue
            #Checking to see if the 'node' object's coordinates are in the allowed broundry of the frid or no
            if node == self.goal:
                self.finished = True
                self.previous[node] = current1[1]
                return 
            if node[0] in range(self.grid.row_range) and node[1] in range(self.grid.col_range):
                #Checking to see if the given node is a puddle/wall(can not be part of the path)
                if self.grid.nodes[node].puddle:
                    print("puddle at: ", node)
                    continue
                else:
                    # Checking if the previous of the 'node' exists 
                    currCost = self.grid.nodes[node].cost()
                    if current1[1] in self.map:
                        newCost = currCost + self.map[current1[1]]
                    else:
                        newCost = currCost

                    # Check if this is the we are seeing this node, if not check for lesser cost in heapq
                    if node not in self.frontierList:
                        print ("node is: " + str(node))
                        heapq.heappush(self.frontier,(newCost,node))
                        self.grid.nodes[node].frontier = True
                        self.frontierList.append(node)
                        # We need to heapify in order to recreat the list as the pq
                        heapq.heapify(self.frontier)
                        self.map[node] = newCost
                        # Setting the previous of this node to current so we can connect for the path
                        self.previous[node] = current1[1]
                    else:
                        # Check each element in the frontier if the node has been prvioulsy entered in it
                        for each in self.frontier:
                                if node == each[1] and newCost < each[0]:
                                    print("\n\n Removing some elements \n\n")
                                    self.frontier.remove[each]
                                    heapq.heapify(self.frontier)
                                    heapq.heappush(self.frontier,(newCost,node))
                                    # Deleting the node from the map to insert with the smaller cost
                                    del self.map[node]
                                    self.map[node] = newCost
                        # Setting the previous of this node to current so we can connect for the path
                        self.previous[node] = current1[1]          
            else:
                print("out of range: ", node)
    
    # A Function which will help calculate the heuristic cost
    def heuristicFunc(self,node1,node2):
        dis = abs(node1[0]-node2[0]) + abs(node1[1]-node2[1])
        return dis

    def astar_step(self):
        # Check if the frontier is empty 
        if not self.frontier:
            self.failed = True
            print("no path")
            return

        # Extract first element from the priority queue
        current1 = heapq.heappop(self.frontier)
        # Setting the checks to proper boolean value 
        self.grid.nodes[current1[1]].checked = True
        self.grid.nodes[current1[1]].frontier = False
        self.explored.append(current1[1])
        
        # Check to see if the current node is the goal node 
        if current1[1] == self.goal:
            self.finish = True
            return 
        children = [(current1[1][0]+a[0], current1[1][1]+a[1]) for a in ACTIONS]

        #Going through each node in the list called children, which contains all the children/puddle near the current node
        for node in children:
            if node in self.explored or node in self.frontier:
                print("explored before: ", node)
                continue
            #Checking to see if the 'node' object's coordinates are in the allowed broundry of the frid or no
            if node == self.goal:
                self.finished = True
                self.previous[node] = current1[1]
                return 
            if node[0] in range(self.grid.row_range) and node[1] in range(self.grid.col_range):
                #Checking to see if the given node is a puddle/wall(can not be part of the path)
                if self.grid.nodes[node].puddle:
                    print("puddle at: ", node)
                    continue
                else:
                    # Getting the real cost of the node 
                    currCost = self.grid.nodes[node].cost()

                    # Checking if the previous of 'node' exist in the map
                    if current1[1] in self.map:
                        currCost = currCost + self.map[current1[1]]
                    
                    # Adding the heuristic Cost to the newCost
                    newCost = currCost + self.heuristicFunc(current1[1],node)
                    
                     # Check each element in the frontier if the node has been prvioulsy entered in it    
                    if node not in self.frontierList:
                        heapq.heappush(self.frontier,(newCost,node))
                        self.grid.nodes[node].frontier = True
                        self.frontierList.append(node)
                        # Deleting the node from the map to insert with the smaller cost
                        heapq.heapify(self.frontier)
                        self.previous[node] = current1[1]
                        self.map[node] = newCost
                    else:
                        for each in self.frontier:
                                if node == each[1] and newCost < each[0]:
                                    self.frontier.remove[each]
                                    heapq.heapify(self.frontier)
                                    heapq.heappush(self.frontier,(newCost,node))
                                    # Deleting the node from the map to insert with the smaller cost 
                                    del self.map[node]
                                    self.map[node] = newCost
                        self.previous[node] = current1[1]            
            else:
                print("out of range: ", node)
