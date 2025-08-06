# DSU for Kruskal
class DSU:
    def __init__(self, size):
        self.parent = list(range(size))
        self.rank = [0] * size

    def find(self, i):
        if self.parent[i] == i:
            return i
        self.parent[i] = self.find(self.parent[i])
        return self.parent[i]

    def union(self, i, j):
        root_i = self.find(i)
        root_j = self.find(j)
        if root_i != root_j:
            if self.rank[root_i] > self.rank[root_j]:
                self.parent[root_j] = root_i
            elif self.rank[root_i] < self.rank[root_j]:
                self.parent[root_i] = root_j
            else:
                self.parent[root_j] = root_i
                self.rank[root_i] += 1
            return True
        return False

# The modified Kruskal
def get_mst_info(num_nodes, all_edges, required_edges=[]):
    dsu = DSU(num_nodes)
    total_weight = 0
    edges_in_tree = 0
    
    for u, v, w in required_edges:
        if not dsu.union(u, v):
            return (float('inf'), []) 
        total_weight += w
        edges_in_tree += 1

    for u, v, w in all_edges:
        if dsu.union(u, v):
            total_weight += w
            edges_in_tree += 1

    if edges_in_tree == num_nodes - 1:
        return (total_weight, [])
    else:
        return (float('inf'), [])

def main():
    try:
        n, m = map(int, input().split())
        all_edges = []
        for _ in range(m):
            u, v, w = map(int, input().split())
            all_edges.append((u - 1, v - 1, w))
        
        num_queries = int(input())
        queries = []
        for _ in range(num_queries):
            data = list(map(int, input().split()))
            required_indices = data[1:]
            queries.append([all_edges[i - 1] for i in required_indices])

    except (IOError, ValueError):
        return

    sorted_edges = sorted(all_edges, key=lambda x: x[2])
    
    # Finds the optimal MST weight without any constraints
    original_mst_weight, _ = get_mst_info(n, sorted_edges)

    # Checks if the MST weight changes
    for required_set in queries:
        try:
            constrained_mst_weight, _ = get_mst_info(n, sorted_edges, required_set)
            if constrained_mst_weight == original_mst_weight:
                print("YES")
            else:
                print("NO")
        except:
            print("NO")

if __name__ == "__main__":
    main()