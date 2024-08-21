import heapq
import time
from graph import Graph

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

def dijkstra(graph, start_vertex):
    # Initialize distances and priority queue
    distances = {vertex: float('infinity') for vertex in graph._graph}
    distances[start_vertex] = 0
    priority_queue = [(0, start_vertex)]
    
    while priority_queue:
        current_distance, current_vertex = heapq.heappop(priority_queue)
        
        # Nodes can only be visited once, so we skip any already visited nodes
        if current_distance > distances[current_vertex]:
            continue
        
        for neighbor in graph._graph[current_vertex]['neighbors']:
            distance = current_distance + 1  # Assuming unweighted graph with edge weight 1
            
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

def longest_shortest_path_from_node(graph, start_vertex):
    distances = dijkstra(graph, start_vertex)
    # Filter out infinite distances (unreachable nodes)
    finite_distances = [dist for dist in distances.values() if dist != float('infinity')]
    max_distance = max(finite_distances)
    return max_distance

if __name__ == "__main__":
    total_time = calculate_shortest_paths_and_time(page_graph, '0')
    print("Total time (in seconds) multiplied by number of nodes:", total_time)
    
    longest_path = longest_shortest_path_from_node(page_graph, '0')
    print("Longest path among all shortest paths from node '0':", longest_path)
