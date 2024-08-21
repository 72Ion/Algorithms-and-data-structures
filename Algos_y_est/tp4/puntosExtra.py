import random
import time
import heapq
import matplotlib.pyplot as plt
from graph import Graph
from collections import defaultdict, deque
from concurrent.futures import ThreadPoolExecutor, as_completed

page_graph = Graph()

with open('web-Google.txt', 'r') as file:
    for l in file:
        if "# FromNodeId\tToNodeId" in l:
            break
    for l in file:
        if not l:
            break
        edge = tuple(int(v.replace("\n", "").replace("\t", "")) for v in l.split("\t"))
        for v in edge:
            if not page_graph.vertex_exists(v):
                page_graph.add_vertex(str(v))
        page_graph.add_edge(str(edge[0]), str(edge[1]))

def approximate_count_polygons(graph, k, sample_size=100):
    """
    Approximate the number of polygons with k sides in the graph using sampling.
    """
    if k < 3:
        return 0

    vertices = list(graph._graph.keys())
    count = 0

    def dfs(v, start, depth, visited):
        nonlocal count
        visited.add(v)
        for neighbor in graph.get_neighbors(v):
            if neighbor == start and depth == k:
                count += 1
            if neighbor not in visited and depth < k:
                dfs(neighbor, start, depth + 1, visited)
        visited.remove(v)

    sampled_vertices = random.sample(vertices, min(sample_size, len(vertices)))
    for vertex in sampled_vertices:
        dfs(vertex, vertex, 1, set())

    total_vertices = len(vertices)
    return (count // (2 * k)) * (total_vertices / sample_size)

def parallel_approximate_count_polygons(graph, k, sample_size=100, num_threads=4):
    vertices = list(graph._graph.keys())
    sample_size = min(sample_size, len(vertices))

    def worker(sample):
        count = 0

        def dfs(v, start, depth, visited):
            nonlocal count
            visited.add(v)
            for neighbor in graph.get_neighbors(v):
                if neighbor == start and depth == k:
                    count += 1
                if neighbor not in visited and depth < k:
                    dfs(neighbor, start, depth + 1, visited)
            visited.remove(v)

        for vertex in sample:
            dfs(vertex, vertex, 1, set())

        return count

    sampled_vertices = random.sample(vertices, sample_size)
    samples = [sampled_vertices[i::num_threads] for i in range(num_threads)]

    total_count = 0
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [executor.submit(worker, sample) for sample in samples]
        for future in as_completed(futures):
            total_count += future.result()

    total_vertices = len(vertices)
    return (total_count // (2 * k)) * (total_vertices / sample_size)

def plot_polygon_counts(graph, max_k=5, sample_size=50):
    """
    Plot the number of polygons by the number of sides using approximations.
    """
    ks = list(range(3, max_k + 1))
    counts = [parallel_approximate_count_polygons(graph, k, sample_size) for k in ks]

    plt.figure(figsize=(10, 6))
    plt.plot(ks, counts, marker='o')
    plt.xlabel('Number of sides (k)')
    plt.ylabel('Number of polygons')
    plt.title('Number of polygons by the number of sides (Approximated)')
    plt.grid(True)
    plt.show()

# Example usage
if __name__ == "__main__":
    # Plot the number of polygons for k from 3 to 10, with estimates for 11 to 15
    plot_polygon_counts(page_graph, max_k=10, sample_size=100)
