import numpy as np
from .graph import Graph

# this function checks if there is any partially directed cycle starting from a particular vertex
#
# src - the vertex from which we arrived at current vertex
# current - current vertex
# path - sequence of visited vertices till current vertex
# graph - object of Graph that stores out graph
# visited - set containing number of visited vertices
# returns - True/False, and a list of vertices that forms a partially directed cycle if any
def check_partial_cycle(src, current, path, graph:Graph, visited:set):
    
    # first we check if the current vertex is already visited in our path
    # if so, then there is a partially directed cycle and hence this can not be a chain graph
    # we return false and return that path as well
    if current in path:
        path = path[path.index(current):]
        path.append(current)
        return True, path
    
    # if the current vertex is not in the path,
    # add current vertex to path and mark it as visited
    path.append(current)
    visited.add(current)

    # now we iterate all the children and neighbors to check if there is a partially directed cycle
    childrenAndNeighbor = list(graph.get_children(current)) + graph.get_neighbors(current)
    for vertex in childrenAndNeighbor:
        if vertex != src:
            result, cyclePath = check_partial_cycle(src=current, current=vertex, path=path, graph=graph, visited=visited)
            if result == True:
                return result, cyclePath
    
    # if there is no cycle, we return False and an empty list
    path.pop()
    return False, []

# this function determines if the given graph is a chain graph or not
#
# adjacency_matrix - this is an adjacency matrix of a graph
# returns - True/False, and a list of vertices that forms a partially directed cycle if any
def is_chain_graph(adjacency_matrix):

    visited = set()
    graph = Graph(adjacency_matrix)

    # we start DFS-like search from every vertex to find a partially directed cycle
    # we avoid starting from already visited vertex
    num_nodes = graph.adjacency_matrix.shape[0]
    for i in range(num_nodes):
        if i not in visited:
            isCyclic, cyclePath = check_partial_cycle(src = -1, current = i, path = [], graph = graph, visited = visited)
            if isCyclic == True:
                return False, cyclePath

    return True, []