from collections import deque

class Edge:
    def __init__(self, to_node, capacity):
        self.to = to_node
        self.capacity = capacity
        self.flow = 0
        self.reverse_edge = None

def add_edge_pair(u_node, v_node, capacity):
    forward_edge = Edge(v_node, capacity)
    backward_edge = Edge(u_node, 0)
    forward_edge.reverse_edge = backward_edge
    backward_edge.reverse_edge = forward_edge
    u_node.edge.append(forward_edge)
    v_node.edge.append(backward_edge)

# Max-flow problem
class DinicSolver:
    def __init__(self, nodes, source, sink):
        self.nodes = nodes + [source, sink]
        self.source = source
        self.sink = sink
        self.level_graph = {}

    def bfs_build_levels(self):

        # BFS to build a level graph from the source
        for node in self.nodes: self.level_graph[node] = -1
        self.level_graph[self.source] = 0
        q = deque([self.source])
        while q:
            u = q.popleft()
            for edge in u.edge:
                if edge.capacity > edge.flow and self.level_graph[edge.to] < 0:
                    self.level_graph[edge.to] = self.level_graph[u] + 1
                    q.append(edge.to)
        return self.level_graph[self.sink] != -1

    def dfs_send_flow(self, u, pushed, iter_state):
        
        # DFS to push flow with paths in the graph
        if pushed == 0 or u == self.sink:
            return pushed
        
        while iter_state[u] < len(u.edge):
            edge = u.edge[iter_state[u]]
            if self.level_graph[edge.to] == self.level_graph[u] + 1:
                flow_to_send = min(pushed, edge.capacity - edge.flow)
                sent = self.dfs_send_flow(edge.to, flow_to_send, iter_state)
                if sent > 0:
                    edge.flow += sent
                    edge.reverse_edge.flow -= sent
                    return sent
            iter_state[u] += 1
        return 0

    def run(self):
        max_flow = 0
        while self.bfs_build_levels():
            iter_state = {node: 0 for node in self.nodes}
            while True:
                pushed = self.dfs_send_flow(self.source, float('inf'), iter_state)
                if pushed == 0:
                    break
                max_flow += pushed
        return max_flow

def build_flow_network(n, grid):
    # Builds a bipartite graph for the grid problem
    nodes = [type('Node', (), {'edge':[]})() for _ in range(n*n)]
    source = type('Node', (), {'edge':[]})()
    sink = type('Node', (), {'edge':[]})()
    
    for r in range(n):
        for c in range(n):
            node_idx = r * n + c
            is_left_partition = (r + c) % 2 == 0
            
            available_spots = 0
            for dr, dc in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
                gr, gc = 2*r+1 + dr, 2*c+1 + dc
                if 0 <= gr < 2*n+1 and 0 <= gc < 2*n+1 and grid[gr][gc] == '.':
                    available_spots += 1
            
            if is_left_partition:
                add_edge_pair(source, nodes[node_idx], available_spots)
            else:
                add_edge_pair(nodes[node_idx], sink, available_spots)

    for r in range(n):
        for c in range(n):
            if (r + c) % 2 == 0: 
                for dr, dc in [(0, 1), (1, 0)]:
                    nr, nc = r + dr, c + dc
                    if nr < n and nc < n:
                        gr, gc = 2*r+1 + dr, 2*c+1 + dc
                        if grid[gr][gc] == '.':
                            add_edge_pair(nodes[r*n+c], nodes[nr*n+nc], 1)
                            
    return nodes, source, sink

def main():
    n_val = int(input().strip())
    grid_map = [input().strip() for _ in range(2 * n_val + 1)]

    # The total number of squares to cut
    total_spots = sum(row.count('.') for row in grid_map) // 2
    
    nodes, source, sink = build_flow_network(n_val, grid_map)
    solver = DinicSolver(nodes, source, sink)
    min_cut = solver.run()
    
    print(total_spots - min_cut)

if __name__ == "__main__":
    main()