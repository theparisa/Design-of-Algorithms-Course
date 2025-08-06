import sys
sys.setrecursionlimit(2000)

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
            else:
                self.parent[root_i] = root_j
                if self.rank[root_i] == self.rank[root_j]:
                    self.rank[root_j] += 1
            return True
        return False

def solve_small_n(n, edges):
    edge_objects = [type('Edge', (), {'u': u, 'v': v, 'w': w, 'idx': i}) for i, (u, v, w) in enumerate(edges)]
    edge_objects.sort(key=lambda e: e.w)
    
    # Runs Kruskal's
    dsu = DSU(n)
    mst_edges = []
    mst_weight = 0
    adj_list = [[] for _ in range(n)]
    for e in edge_objects:
        if dsu.union(e.u, e.v):
            mst_edges.append(e)
            mst_weight += e.w
            adj_list[e.u].append((e.v, e.w))
            adj_list[e.v].append((e.u, e.w))

    answers = ["none"] * len(edges)
    
    for e in edge_objects:
        # (node, parent, max_edge_on_path)
        q = [(e.u, -1, -1)]
        visited = {e.u}
        max_w = -1
        
        # Find max edge on path from u to v in the MST
        head = 0
        while head < len(q):
            curr, p, path_max = q[head]
            head += 1
            if curr == e.v:
                max_w = path_max
                break
            for neighbor, weight in adj_list[curr]:
                if neighbor != p:
                    visited.add(neighbor)
                    q.append((neighbor, curr, max(path_max, weight)))
        
        if e.w == max_w:
            answers[e.idx] = "at least one"

    for e in mst_edges:
        temp_dsu = DSU(n)
        temp_weight = 0
        num_edges = 0
        for other_e in edge_objects:
            if e.idx != other_e.idx:
                if temp_dsu.union(other_e.u, other_e.v):
                    temp_weight += other_e.w
                    num_edges += 1
        
        if num_edges < n - 1 or temp_weight > mst_weight:
            answers[e.idx] = "any"

    return answers

def solve_large_n(n, edges):
    sorted_edges = sorted([(w, u, v, i) for i, (u, v, w) in enumerate(edges)])
    status = ["none"] * len(edges)

    # Finds the MST and mark its edges
    dsu = DSU(n)
    mst_edges = []
    for w, u, v, idx in sorted_edges:
        if dsu.union(u, v):
            mst_edges.append((u, v, w, idx))
            status[idx] = "any"
            
    adj = [[] for _ in range(n)]
    for u, v, w, idx in mst_edges:
        adj[u].append((v, w, idx))
        adj[v].append((u, w, idx))

    LOG_N = n.bit_length()
    parent = [[-1] * LOG_N for _ in range(n)]
    max_w = [[0] * LOG_N for _ in range(n)]
    depth = [-1] * n
    
     # (node, parent, depth, weight_from_parent)
    q = [(0, -1, 0, 0)]
    depth[0] = 0
    head = 0
    while head < len(q):
        u, p, d, w = q[head]
        head += 1
        parent[u][0] = p
        max_w[u][0] = w
        for v_node, v_w, _ in adj[u]:
            if v_node != p:
                depth[v_node] = d + 1
                q.append((v_node, u, d + 1, v_w))

    for j in range(1, LOG_N):
        for i in range(n):
            if parent[i][j-1] != -1:
                p = parent[i][j-1]
                parent[i][j] = parent[p][j-1]
                max_w[i][j] = max(max_w[i][j-1], max_w[p][j-1])
    
    for w, u, v, idx in sorted_edges:
        if status[idx] == "none":
            # Find heaviest edge on path between u and v in MST
            path_max_w = 0
            u_node, v_node = u, v
            if depth[u_node] < depth[v_node]: u_node, v_node = v_node, u_node
            
            for j in range(LOG_N - 1, -1, -1):
                if depth[u_node] - (1 << j) >= depth[v_node]:
                    path_max_w = max(path_max_w, max_w[u_node][j])
                    u_node = parent[u_node][j]

            if u_node != v_node:
                for j in range(LOG_N - 1, -1, -1):
                    if parent[u_node][j] != -1 and parent[u_node][j] != parent[v_node][j]:
                        path_max_w = max(path_max_w, max_w[u_node][j], max_w[v_node][j])
                        u_node, v_node = parent[u_node][j], parent[v_node][j]
                path_max_w = max(path_max_w, max_w[u_node][0], max_w[v_node][0])
            
            if w == path_max_w:
                status[idx] = "at least one"
                # Downgrade any edges that could be replaced
                q_lca = [(u, v)]
                visited_lca = set()
                while q_lca:
                    curr_u, curr_v = q_lca.pop(0)
                    if (curr_u, curr_v) in visited_lca: continue
                    visited_lca.add((curr_u, curr_v))
                    
                    for neighbor, neighbor_w, neighbor_idx in adj[curr_u] + adj[curr_v]:
                         if status[neighbor_idx] == "any" and neighbor_w == w:
                              status[neighbor_idx] = "at least one"

    return status

def main():
    try:
        n, m = map(int, input().split())
        edges = [tuple(map(int, input().split())) for _ in range(m)]
        if n < 500:
            results = solve_small_n(n, [(u-1, v-1, w) for u, v, w in edges])
        else:
            results = solve_large_n(n, [(u, v, w) for u, v, w in edges])
        print("\n".join(results))
    except (IOError, ValueError):
        pass

if __name__ == "__main__":
    main()