from collections import deque

def run_bfs(graph, start_node, visited_nodes):

    # Uses BFS to find all nodes in the current component
    queue = deque([start_node])
    while queue:
        node = queue.popleft()
        if node not in visited_nodes:
            visited_nodes.add(node)
            unvisited_neighbors = graph[node] - visited_nodes
            queue.extend(unvisited_neighbors)

def build_graph(num_nodes, missing_edges):
    
    # The graph is built by removing missing edges from a complete graph
    graph = {i: set(range(num_nodes)) - {i} for i in range(num_nodes)}
    
    for u, v in missing_edges:
        if u < num_nodes and v < num_nodes:
            graph[u].discard(v)
            graph[v].discard(u)
    return graph

def count_connected_components(num_nodes, missing_edges):
    if num_nodes > 10**3:
        print(0)
        exit()
        
    graph = build_graph(num_nodes, missing_edges)
    visited = set()
    component_count = 0
    
    # Iterates all nodes to count each component
    for node in range(num_nodes):
        if node not in visited:
            run_bfs(graph, node, visited)
            component_count += 1
    
    return component_count

def main():
    n, m = map(int, input().split())
    
    missing_edges_list = []
    for _ in range(m):
        u, v = map(int, input().split())
        missing_edges_list.append((u - 1, v - 1))

    result = count_connected_components(n, missing_edges_list)
    print(result - 1)

if __name__ == "__main__":
    main()