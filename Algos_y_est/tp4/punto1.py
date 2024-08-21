import random
import time
import heapq
from graph import Graph
from collections import defaultdict, deque

def clustering_coefficient(graph):
    """
    Calculate the clustering coefficient of the graph.
    """
    triangles = 0
    triplets = 0

    for vertex in graph._graph.keys():
        neighbors = graph.get_neighbors(vertex)
        if len(neighbors) < 2:
            continue

        for i in range(len(neighbors)):
            for j in range(i + 1, len(neighbors)):
                triplets += 1
                if graph.edge_exists(neighbors[i], neighbors[j]):
                    triangles += 1

    if triplets == 0:
        return 0.0
    return (3 * triangles) / triplets

if __name__ == "__main__":
    page_graph = Graph()

    with open('web-Google.txt', 'r') as file:
        for l in file:
            if "# FromNodeId	ToNodeId" in l:
                break
        for l in file:
            if not l:
                break
            edge = tuple(int(v.replace("\n", "").replace("\t", "")) for v in l.split("\t"))
            for v in edge:
                if not page_graph.vertex_exists(v):
                    page_graph.add_vertex(str(v))
            page_graph.add_edge(str(edge[0]), str(edge[1]))

    clustering_coef = clustering_coefficient(page_graph)
    print(f"Clustering coefficient of the graph: {clustering_coef:.6f}")
