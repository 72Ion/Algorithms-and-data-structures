import random
import time
import heapq
from graph import Graph
from collections import defaultdict, deque

# def load_graph_from_file(file_path):
#     graph = Graph()
#     with open(file_path, 'r') as file:
#         for l in file:
#             if "# FromNodeId\tToNodeId" in l:
#                 break
#         for l in file:
#             if not l.strip():
#                 continue
#             edge = tuple(int(v) for v in l.split())
#             for v in edge:
#                 if not graph.vertex_exists(str(v)):
#                     graph.add_vertex(str(v))
#             graph.add_edge(str(edge[0]), str(edge[1]))
#     return graph


def load_graph_from_file(file_path):
    graph = {}
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith('#'):
                continue
            from_node, to_node = line.split()
            if from_node not in graph:
                graph[from_node] = []
            if to_node not in graph:
                graph[to_node] = []
            graph[from_node].append(to_node)
    return graph


# def dijkstra(graph, start_vertex):
#     distances = {vertex: float('inf') for vertex in graph._graph}
#     previous_vertices = {vertex: None for vertex in graph._graph}
#     distances[start_vertex] = 0
#     priority_queue = [(0, start_vertex)]

#     while priority_queue:
#         current_distance, current_vertex = heapq.heappop(priority_queue)

#         if current_distance > distances[current_vertex]:
#             continue

#         for neighbor in graph.get_neighbors(current_vertex):
#             distance = current_distance + 1  # assuming all edges have weight 1
#             if distance < distances[neighbor]:
#                 distances[neighbor] = distance
#                 previous_vertices[neighbor] = current_vertex
#                 heapq.heappush(priority_queue, (distance, neighbor))

#     return distances, previous_vertices

# def get_connected_components(graph):  ## Will explore components based on the BFS.
#     visited = set()
#     components = []

#     for vertex in graph._graph.keys():
#         if vertex not in visited:
#             component = []
#             queue = deque([vertex])
#             while queue:
#                 v = queue.popleft()
#                 if v not in visited:
#                     visited.add(v)
#                     component.append(v)
#                     for neighbor in graph.get_neighbors(v):
#                         if neighbor not in visited:
#                             queue.append(neighbor)
#             components.append(component)
    
#     return components

# def size_of_largest_connected_component(graph):
#     components = get_connected_components(graph)
#     largest_component = max(components, key=len)
#     return len(largest_component)

# def number_of_connected_components(graph):
#     components = get_connected_components(graph)
#     return len(components)


def dijkstra(graph, start_vertex):
    distances = {vertex: float('inf') for vertex in graph}
    previous_vertices = {vertex: None for vertex in graph}
    distances[start_vertex] = 0
    priority_queue = [(0, start_vertex)]

    while priority_queue:
        current_distance, current_vertex = heapq.heappop(priority_queue)

        if current_distance > distances[current_vertex]:
            continue

        for neighbor in graph[current_vertex]:
            distance = current_distance + 1  # assuming all edges have weight 1
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous_vertices[neighbor] = current_vertex
                heapq.heappush(priority_queue, (distance, neighbor))

    return distances, previous_vertices

def get_connected_components(graph):
    visited = set()
    components = []

    for vertex in graph.keys():
        if vertex not in visited:
            component = []
            queue = deque([vertex])
            while queue:
                v = queue.popleft()
                if v not in visited:
                    visited.add(v)
                    component.append(v)
                    for neighbor in graph[v]:
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




#PUNTO 2

########################################################################################################
def bfs_shortest_paths(graph, start_vertex):
    distances = {vertex: float('inf') for vertex in graph}
    distances[start_vertex] = 0
    queue = deque([start_vertex])
    
    while queue:
        current_vertex = queue.popleft()
        for neighbor in graph[current_vertex]:
            if distances[neighbor] == float('inf'):
                distances[neighbor] = distances[current_vertex] + 1
                queue.append(neighbor)
    
    return distances

def landmark_shortest_paths_estimate(graph, num_landmarks=10):
    vertices = list(graph.keys())
    landmarks = random.sample(vertices, num_landmarks)
    
    start_time = time.time()
    landmark_distances = {}
    for landmark in landmarks:
        landmark_distances[landmark] = bfs_shortest_paths(graph, landmark)
    end_time = time.time()
    
    preprocessing_time = end_time - start_time
    
    def estimate_distance(vertex1, vertex2):
        min_distance = float('inf')
        for landmark in landmarks:
            dist_v1_l = landmark_distances[landmark].get(vertex1, float('inf'))
            dist_v2_l = landmark_distances[landmark].get(vertex2, float('inf'))
            min_distance = min(min_distance, dist_v1_l + dist_v2_l)
        return min_distance
    
    return estimate_distance, preprocessing_time


if __name__ == "__main__":
    # graph = load_graph_from_file('web-Google.txt')
    # print("Size of the largest connected component:", size_of_largest_connected_component(graph))
    # print("Number of connected components:", number_of_connected_components(graph))

    graph = load_graph_from_file('web-Google.txt')
    print("Size of the largest connected component:", size_of_largest_connected_component(graph))
    print("Number of connected components:", number_of_connected_components(graph))
    

    estimate_distance, preprocessing_time = landmark_shortest_paths_estimate(graph, num_landmarks=10)
    
    print(f"Preprocessing time: {preprocessing_time:.2f} seconds")
    
    # Example of estimating distance between two nodes
    vertex1, vertex2 = '0', '11342'
    estimated_distance = estimate_distance(vertex1, vertex2)
    print(f"Estimated shortest path between {vertex1} and {vertex2}: {estimated_distance}")
    
    # Estimating total time for the full dataset based on the sample
    estimated_full_preprocessing_time = preprocessing_time
    print(f"Estimated preprocessing time for the full dataset: {estimated_full_preprocessing_time:.2f} seconds")
    print(f"Order of Preprocessing: O(k*(|V|+|E|)), Query time complexity: O(k)")