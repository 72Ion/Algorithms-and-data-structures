import random
from collections import deque
from graph import Graph
from punto1 import get_connected_components

def bfs_longest_cycle(graph, start_vertex):
    visited = {vertex: False for vertex in graph._graph}
    distance = {vertex: float('inf') for vertex in graph._graph}
    parent = {vertex: None for vertex in graph._graph}

    queue = deque([start_vertex])
    visited[start_vertex] = True
    distance[start_vertex] = 0
    longest_cycle_length = 0

    while queue:
        current = queue.popleft()

        for neighbor in graph.get_neighbors(current):
            print("This is the neighbor:", neighbor)
            if not visited[neighbor]:
                visited[neighbor] = True
                distance[neighbor] = distance[current] + 1
                parent[neighbor] = current
                queue.append(neighbor)
            elif parent[current] != neighbor and parent[neighbor] != current:
                cycle_length = distance[current] + distance[neighbor] + 1
                if cycle_length > longest_cycle_length:
                    longest_cycle_length = cycle_length

    return longest_cycle_length

def approximate_longest_circumference(graph, sample_size=150):
    components = get_connected_components(graph)
    if len(components) <= sample_size:
        sample_components = components
    else:
        sample_components = random.sample(components, sample_size)

    max_cycle_length = 0

    for component in sample_components:
        subgraph = Graph()
        for vertex in component:
            subgraph.add_vertex(vertex)
        for vertex in component:
            for neighbor in graph.get_neighbors(vertex):
                if neighbor in component:
                    subgraph.add_edge(vertex, neighbor)
        
        for vertex in component:
            cycle_length = bfs_longest_cycle(subgraph, vertex)
            if cycle_length > max_cycle_length:
                max_cycle_length = cycle_length

    return max_cycle_length

# Initialize the graph
page_graph = Graph()

# Read the graph data
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

# Approximate the longest circumference of the graph
approx_circumference = approximate_longest_circumference(page_graph, sample_size=25)
print("Approximate longest circumference of the graph:", approx_circumference)
