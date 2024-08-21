import heapq
import time
import random
from graph import Graph
from collections import defaultdict, deque

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
            if not page_graph.vertex_exists(str(v)):
                page_graph.add_vertex(str(v))
        page_graph.add_edge(str(edge[0]), str(edge[1]))

def approximate_betweenness_centrality(graph, sample_size=100):
    """
    Approximate the betweenness centrality for each vertex in the graph using sampling.
    """
    centrality = {vertex: 0 for vertex in graph._graph}
    vertices = list(graph._graph.keys())
    sample_vertices = random.sample(vertices, min(sample_size, len(vertices)))

    for s in sample_vertices:
        stack = []
        pred = {w: [] for w in graph._graph}
        sigma = dict.fromkeys(graph._graph, 0)   # sigma[v]=number of shortest paths from s to v
        sigma[s] = 1
        d = dict.fromkeys(graph._graph, -1)     # d[v]=distance from s to v
        d[s] = 0
        Q = deque([s])
        while Q:   # BFS loop
            v = Q.popleft()
            stack.append(v)
            for w in graph.get_neighbors(v):
                if d[w] < 0:   # w found for the first time?
                    Q.append(w)
                    d[w] = d[v] + 1
                if d[w] == d[v] + 1:   # shortest path to w via v?
                    sigma[w] += sigma[v]
                    pred[w].append(v)
        delta = dict.fromkeys(graph._graph, 0)   # delta[v]=dependency of s-paths on v
        while stack:
            w = stack.pop()
            for v in pred[w]:
                delta[v] += (sigma[v] / sigma[w]) * (1 + delta[w])
            if w != s:
                centrality[w] += delta[w]
    
    # Normalize the centrality values
    scale = 1 / ((len(graph._graph) - 1) * (len(sample_vertices)))
    for v in centrality:
        centrality[v] *= scale

    return centrality

if __name__ == "__main__":
    sample_size = 100  # You can adjust the sample size based on the desired accuracy and computation time
    centrality = approximate_betweenness_centrality(page_graph, sample_size)
    max_centrality_vertex = max(centrality, key=centrality.get)
    print(f"Vertex with the highest betweenness centrality: {max_centrality_vertex}, Betweenness Centrality: {centrality[max_centrality_vertex]:.6f}")
