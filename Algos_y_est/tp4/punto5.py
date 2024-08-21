import random
from graph import Graph

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
    
    # Normalize pagerank values
    total_samples = num_samples * num_steps
    for vertex in pagerank:
        pagerank[vertex] /= total_samples
    
    return pagerank

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

# Apply Monte Carlo PageRank approximation
approx_pagerank = monte_carlo_pagerank(page_graph, num_samples=1000, num_steps=50, damping_factor=0.85)

# Print the top 10 vertices by PageRank
top_vertices = sorted(approx_pagerank.items(), key=lambda x: x[1], reverse=True)[:10]
print("Top 10 vertices by PageRank:")
for vertex, score in top_vertices:
    print(f"Vertex: {vertex}, Score: {score}")
