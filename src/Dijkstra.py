# Implementation of Dijkstra's shortest paths algorithm 
#
# Main functions:
#     1) dij() --> Returns shortest distances
#     2) dij_paths() --> Returns shortest paths
#
# Graph representation:
#     Use dict datastructure to represent Graph:
#         nodes == keys
#         [(Edge to, Weight)] == Value
#     Example:
#         1 --> 2 (weight of 5)
#         represented as (1: [(2, 5)])
import heapq
import collections


class NoPathError(Exception):
    '''Exception for when there is no path from source to node'''
    pass

#add node s with distance 0 and all other nodes with distance infinity
#while loop: add node v with the smallest distance of the nodes that are "one step" away
#now consider all nodes "one step" from v and see if there are smaller distance, if yes then update with decrease key and add that to the priority queue
#returns the shortest distance from a single source to the specified node t if there is one, or all the shortest paths
def dij(adjacentList, s, t=None):
    '''Calculates shortest distances for each node from a source
    Arguments:
        adjacentList -- dict containing (node: (edge, weight)) pairs
                        represents the directed graph
        s -- int representing the source node to start with
        t -- int representing the target node to find shortest dist to
    Returns:
        dict with shortest distances for all nodes or shortest distance
        to target if target param is given
    Raises:
        NoPathError -- if there is no path to target node   
    '''
    infinity = float('inf')    
    PQ = []
    visited = {}
    visited[s] = 0 #the source is visited
    nodes = {x:x for x in adjacentList}
    prev = {x:x for x in adjacentList} #list of previous nodes vistied, to keep the shortest path
    distances = {x:infinity for x in adjacentList}
    distances[s] = 0
    item = [s, distances[s]]#the distance from the source is 0
    #the priority queue has a format of the (node name, distance from source)
    heapq.heappush(PQ, item)#like the pseudo-code: push (s,0) into PQ

    for n in nodes: 
        item = [n, infinity]
        heapq.heappush(PQ, item)#like the pseudo-code: insert each node with distance infinity

  
    while(PQ):
        v = heapq.heappop(PQ) #like the pseudo-code: extractmin from the priority queue
        vNode = v[0]
        vDist = v[1]
        for u in adjacentList[vNode]: #nested for loop
            uNode = u[0]
            uvDist = u[1]

            if uNode not in visited or uvDist < visited[uNode]:
                visited[uNode] = uvDist
                if distances[uNode] > distances[vNode] + uvDist: #like the pseudo-code: decreasekey part
                    distances[uNode] = distances[vNode] + uvDist #update the distance if necesary
                    item = [uNode, distances[uNode]]
                    heapq.heappush(PQ, item)#push the updated value onto the priority queue
                    prev[uNode] = vNode #updating previous list

    if t is not None: #there is a destination node given 
        if distances[t] == infinity: #no path to t 
            raise NoPathError()
        else:
            return distances[t]#return the shortest distance to the destination node
    
    return distances #if no specific destination node is given return the shortest distances to all nodes from the source node

#gives the shortest path, very similar to above code  
def dij_paths(adjacentList, s, t=None): 
    '''Constructs shortest paths for every node in graph based on 
    shortest distances unless a target node is specified
    Arguments:
        adjacentList -- dict containing (node: (edge, weight)) pair 
                        representing the directed graph
        s -- int representing the source node to start with
        t -- int representing the target node to find shortest path to
    Return:
        dict with the shortest paths for each node in graph if target 
        is None, else list with shortest path from src to target node
    Raises:
        NoPathError -- if there is no path to target node  
    '''
    infinity = float('inf')    
    PQ = []
    visited = {}
    visited[s] = 0 #the source is visited
    nodes = {x:x for x in adjacentList}
    prev = {x:x for x in adjacentList} #list of previous nodes vistied, to keep the shortest path
    distances = { x:infinity for x in adjacentList}
    distances[s] = 0
    item = [s, distances[s]]
    heapq.heappush(PQ, item)

    for n in nodes: 
        item = [n, infinity]
        heapq.heappush(PQ, item) 

    

    while(PQ):
        v = heapq.heappop(PQ)
        vNode = v[0]
        vDist = v[1]
        
        for u in adjacentList[vNode]: 
            uNode = u[0]
            uvDist = u[1]

            if uNode not in visited or uvDist < visited[uNode]:
                visited[uNode] = uvDist
                if distances[uNode] > distances[vNode] + uvDist: 
                    distances[uNode] = distances[vNode] + uvDist 
                    item = [uNode, distances[uNode]]
                    heapq.heappush(PQ, item)
                    prev[uNode] = vNode #once you have pushed the node u onto the priority queue not that the previous node was v so you can return the path

    if t is not None:
        return shortest_path(s, t, prev)
    
    # Construct shortest path route
    shortest_paths = {node: [] for node in adjacentList}

    for node in shortest_paths:
        try:
            shortest_paths[node] = shortest_path(s, node, prev)
        except NoPathError:
            pass
    
    return shortest_paths

def shortest_path(s, t, prev):
    '''Construct the shortest path from source to target node with
    given list of previous nodes
    Arguments:
        s -- int representing the source node
        t -- int representing the target node
        prev -- dict with (node: previous node) pairs for each node
    Return:
        list containing the path from source to target node
    Raises:
        NoPathError -- if there is no path to target node  
    '''
    # Collections.deque() used for O(1) insertion @ front of list
    path = collections.deque()

    path.append(t)
    prev_node = prev[t]

    if prev_node == t and t != 0:
        raise NoPathError()

    if prev_node == 0 and t != 0:
        path.appendleft(prev_node)
        return list(path)
    elif t != 0:
        curr_node = t
        while prev_node != s:
            if prev_node == curr_node:
                raise NoPathError()
            
            path.appendleft(prev_node)
            curr_node = prev_node
            prev_node = prev[prev_node]
            
        path.appendleft(s)
        
    return list(path)
        
def main():
     
    adj = {'a': [('b', 9), ('c', 6), ('e', 13)],
         'b': [('a', 9), ('f', 10)],
         'c': [('a', 6), ('e', 8), ('f', 18), ('d', 30)],
         'd': [('c', 30), ('e', 20), ('f', 6), ('h', 16), ('g', 11)],
         'e': [('a', 13), ('h', 25), ('c', 8), ('d', 20)],
         'f': [('b', 10), ('c', 18), ('d', 6),  ('g', 6), ('h', 19)],
         'g': [('d', 11), ('f', 6), ('h', 6)],
         'h': [('e', 25), ('f', 19), ('d', 16),  ('g', 6)]}

 
    dij_paths(adj, 'a', 'h')

if __name__ == "__main__":
    main()
