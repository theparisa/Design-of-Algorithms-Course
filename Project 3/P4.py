
def solve():
    n = int(input().strip())
    node_values = list(map(int, input().strip().split()))
    edges = []
    for _ in range(n - 1):
        u, v = map(int, input().strip().split())
        edges.append((u - 1, v - 1))

    # Each node stores its value, neighbors, and calculated cost
    graph = {i: {"value": node_values[i], "neighbors": [], "cost": 0} for i in range(n)}
    for u, v in edges:
        graph[u]["neighbors"].append(v)
        graph[v]["neighbors"].append(u)
    
    # The DFS starts from the node with the highest value
    root_node = node_values.index(max(node_values))
    
    calculate_costs_dfs(graph, root_node, -1)
    
    total_cost = sum(node["cost"] for node in graph.values())
    print(total_cost)

def calculate_costs_dfs(graph, current_node_idx, parent_node_idx):
    is_leaf = len(graph[current_node_idx]["neighbors"]) == 1 and parent_node_idx != -1
    if is_leaf:
        graph[current_node_idx]["cost"] = graph[current_node_idx]["value"]
        return current_node_idx

    rep_leaves_from_children = []
    for neighbor_idx in graph[current_node_idx]["neighbors"]:
        if neighbor_idx == parent_node_idx:
            continue
        rep_leaves_from_children.append(calculate_costs_dfs(graph, neighbor_idx, current_node_idx))
        
    # Finds the leaf with the highest cost
    main_path_leaf = max(rep_leaves_from_children, key=lambda idx: graph[idx]["cost"])
    
    # Propagates this node's value down
    value_to_add = max(0, graph[current_node_idx]["value"] - graph[main_path_leaf]["cost"])
    graph[main_path_leaf]["cost"] += value_to_add
    
    # The root node 's logic for a second path
    if parent_node_idx == -1 and len(rep_leaves_from_children) > 1:
        rep_leaves_from_children.sort(key=lambda idx: graph[idx]["cost"], reverse=True)
        second_path_leaf = rep_leaves_from_children[1]
        
        secondary_value_to_add = max(0, graph[current_node_idx]["value"] - graph[second_path_leaf]["cost"])
        graph[second_path_leaf]["cost"] += secondary_value_to_add
        
    return main_path_leaf

if __name__ == "__main__":
    solve()