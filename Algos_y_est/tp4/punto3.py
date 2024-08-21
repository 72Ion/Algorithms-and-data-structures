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

def count_triangles(graph):
    count = 0
    vertices = graph._graph.keys()
    for v in vertices:
        neighbors = set(graph.get_neighbors(v))
        for neighbor in neighbors:
            mutual_neighbors = neighbors.intersection(graph.get_neighbors(neighbor))
            count += len(mutual_neighbors)
    # Each triangle is counted three times, so divide by 3
    return count // 3

print("Number of triangles in the graph:", count_triangles(page_graph))
