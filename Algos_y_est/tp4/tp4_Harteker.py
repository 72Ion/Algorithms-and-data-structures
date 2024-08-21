import random
import time
import heapq
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
            if not page_graph.vertex_exists(v):
                page_graph.add_vertex(str(v))
        page_graph.add_edge(str(edge[0]), str(edge[1]))


# ========================================PUNTO 1========================================
def get_connected_components(graph):
    visited = set()
    components = []

    for vertex in graph._graph.keys():
        if vertex not in visited:
            component = []
            queue = deque([vertex])
            while queue:
                v = queue.popleft()
                if v not in visited:
                    visited.add(v)
                    component.append(v)
                    for neighbor in graph.get_neighbors(v):
                        if neighbor not in visited:
                            queue.append(neighbor)
            components.append(component)
    
    return components

def size_of_largest_connected_component(graph):
    components = get_connected_components(graph)
    largest_component = max(components, key=len)
    return len(largest_component)

def number_of_connected_components(graph):
    components = get_connected_components(graph)
    return len(components)

# ========================================PUNTO 2========================================

def dijkstra(graph, start_vertex):
    distances = {vertex: float('infinity') for vertex in graph._graph}
    distances[start_vertex] = 0
    priority_queue = [(0, start_vertex)]
    
    while priority_queue:
        current_distance, current_vertex = heapq.heappop(priority_queue)
        
        if current_distance > distances[current_vertex]:
            continue
        
        for neighbor, weight in graph._graph[current_vertex]['neighbors'].items():
            distance = current_distance + (weight if weight else 1)
            
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(priority_queue, (distance, neighbor))
    
    return distances

def calculate_shortest_paths_and_time(graph, start_vertex):
    start_time = time.time()
    distances = dijkstra(graph, start_vertex)
    end_time = time.time()
    
    time_taken = end_time - start_time
    total_time = time_taken * len(graph._graph)
    
    return total_time

# ========================================PUNTO 3========================================

def count_triangles(graph):
    count = 0
    vertices = graph._graph.keys()
    for v in vertices:
        neighbors = set(graph.get_neighbors(v))
        for neighbor in neighbors:
            mutual_neighbors = neighbors.intersection(graph.get_neighbors(neighbor))
            count += len(mutual_neighbors)
    return count // 3

# ========================================PUNTO 4========================================


def longest_shortest_path_from_node(graph, start_vertex):
    distances = dijkstra(graph, start_vertex)
    finite_distances = [dist for dist in distances.values() if dist != float('infinity')]
    max_distance = max(finite_distances)
    return max_distance

def approximate_diameter_with_random_nodes(graph, sample_size=50):
    vertices = list(graph._graph.keys())
    if len(vertices) <= sample_size:
        sample_vertices = vertices
    else:
        sample_vertices = random.sample(vertices, sample_size)

    max_longest_shortest_path = 0

    for vertex in sample_vertices:
        longest_shortest_path = longest_shortest_path_from_node(graph, vertex)
        if longest_shortest_path > max_longest_shortest_path:
            max_longest_shortest_path = longest_shortest_path

    return max_longest_shortest_path

# ========================================PUNTO 5========================================

def monte_carlo_pagerank(graph, num_samples=100, num_steps=50, damping_factor=0.85):
    pagerank = {vertex: 0 for vertex in graph._graph}
    vertices = list(graph._graph.keys())
    
    for _ in range(num_samples):
        current_vertex = random.choice(vertices)
        for _ in range(num_steps):
            pagerank[current_vertex] += 1
            if random.random() < damping_factor and graph.get_neighbors(current_vertex):
                current_vertex = random.choice(graph.get_neighbors(current_vertex))
            else:
                current_vertex = random.choice(vertices)
    
    total_samples = num_samples * num_steps
    for vertex in pagerank:
        pagerank[vertex] /= total_samples
    
    return pagerank

# ========================================PUNTO 6========================================

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


# ========================================EXTRAS========================================

# ========================================PUNTO 2========================================

def clustering_coefficient(graph):

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

# ========================================PUNTO 3========================================

def approximate_betweenness_centrality(graph, sample_size=100):

    centrality = {vertex: 0 for vertex in graph._graph}
    vertices = list(graph._graph.keys())
    sample_vertices = random.sample(vertices, min(sample_size, len(vertices)))

    for s in sample_vertices:
        stack = []
        pred = {w: [] for w in graph._graph}
        sigma = dict.fromkeys(graph._graph, 0)
        sigma[s] = 1
        d = dict.fromkeys(graph._graph, -1)
        d[s] = 0
        Q = deque([s])
        while Q:   # BFS loop
            v = Q.popleft()
            stack.append(v)
            for w in graph.get_neighbors(v):
                if d[w] < 0:
                    Q.append(w)
                    d[w] = d[v] + 1
                if d[w] == d[v] + 1:
                    sigma[w] += sigma[v]
                    pred[w].append(v)
        delta = dict.fromkeys(graph._graph, 0)
        while stack:
            w = stack.pop()
            for v in pred[w]:
                delta[v] += (sigma[v] / sigma[w]) * (1 + delta[w])
            if w != s:
                centrality[w] += delta[w]
    
    scale = 1 / ((len(graph._graph) - 1) * (len(sample_vertices)))
    for v in centrality:
        centrality[v] *= scale

    return centrality


if __name__ == "__main__":

    #Punto 1

    print("Size of the largest connected component:", size_of_largest_connected_component(page_graph))
    print("Number of connected components:", number_of_connected_components(page_graph))

    # Punto 2

    total_time = calculate_shortest_paths_and_time(page_graph, '0')
    print("Total time (in seconds) multiplied by number of nodes:", total_time)

    # Punto 3

    print("Number of triangles in the graph:", count_triangles(page_graph))

    # Punto 4
    
    approximate_diameter = approximate_diameter_with_random_nodes(page_graph, sample_size=50)
    print("Approximate diameter of the graph (using 50 random nodes):", approximate_diameter)

    # Punto 5
        
    approx_pagerank = monte_carlo_pagerank(page_graph, num_samples=1000, num_steps=50, damping_factor=0.85)
    top_vertices = sorted(approx_pagerank.items(), key=lambda x: x[1], reverse=True)[:10]
    print("Top 10 vertices by PageRank:")
    for vertex, score in top_vertices:
        print(f"Vertex: {vertex}, Score: {score}")

    # Punto 6

    approx_circumference = approximate_longest_circumference(page_graph, sample_size=25)
    print("Approximate longest circumference of the graph:", approx_circumference)


    #Extras

    #Punto 2 
    clustering_coef = clustering_coefficient(page_graph)
    print(f"Clustering coefficient of the graph: {clustering_coef:.6f}")

    #Punto 3

    sample_size = 100
    centrality = approximate_betweenness_centrality(page_graph, sample_size)
    max_centrality_vertex = max(centrality, key=centrality.get)
    print(f"Vertex with the highest betweenness centrality: {max_centrality_vertex}, Betweenness Centrality: {centrality[max_centrality_vertex]:.6f}")







"""
PUNTO 1:
    Size of the largest connected component: 600493
    Number of connected components: 179851
PUNTO 2:
    Total time (in seconds) multiplied by number of nodes: 3849088.7093570232

PUNTO 3:
    Number of triangles in the graph: 9399651

PUNTO 4:
    Approximate diameter of the graph (using 50 random nodes): 38

PUNTO 5:
    Top 10 vertices by PageRank:
        Vertex: 597621, Score: 0.00104
        Vertex: 551829, Score: 0.0008
        Vertex: 504140, Score: 0.0008
        Vertex: 687325, Score: 0.0008
        Vertex: 885605, Score: 0.00078
        Vertex: 537039, Score: 0.00076
        Vertex: 32163, Score: 0.00074
        Vertex: 605856, Score: 0.00072
        Vertex: 558791, Score: 0.0007
        Vertex: 751384, Score: 0.0007

PUNTO 6:
    Approximate longest circumference of the graph: 3

EXTRAS:

PUNTO 2:
    Clustering coefficient of the graph: 1.348013

PUNTO 3:
    Vertex with the highest betweenness centrality: 560622, Betweenness Centrality: 0.055376



"""