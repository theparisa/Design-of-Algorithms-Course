from collections import deque

class Edge:
    def __init__(self, to_node, capacity):
        self.to = to_node
        self.capacity = capacity
        self.flow = 0
        self.reverse_edge = None

def add_edge_pair(u_node, v_node, capacity):
    fwd_edge = Edge(v_node, capacity)
    bwd_edge = Edge(u_node, 0)
    fwd_edge.reverse_edge = bwd_edge
    bwd_edge.reverse_edge = fwd_edge
    u_node.edge.append(fwd_edge)
    v_node.edge.append(bwd_edge)
    return fwd_edge

# Max-flow 
class DinicSolver:
    def __init__(self, nodes, source, sink):
        self.all_nodes = nodes + [source, sink]
        self.source = source
        self.sink = sink

    def bfs_build_levels(self):
        self.levels = {node: -1 for node in self.all_nodes}
        self.levels[self.source] = 0
        q = deque([self.source])
        while q:
            u = q.popleft()
            for edge in u.edge:
                if edge.capacity > edge.flow and self.levels[edge.to] < 0:
                    self.levels[edge.to] = self.levels[u] + 1
                    q.append(edge.to)
        return self.levels[self.sink] != -1

    def dfs_send_flow(self, u, pushed, iter_state):
        if pushed == 0 or u == self.sink: return pushed
        while iter_state[u] < len(u.edge):
            edge = u.edge[iter_state[u]]
            if self.levels[edge.to] == self.levels[u] + 1:
                flow_sent = self.dfs_send_flow(edge.to, min(pushed, edge.capacity - edge.flow), iter_state)
                if flow_sent > 0:
                    edge.flow += flow_sent
                    edge.reverse_edge.flow -= flow_sent
                    return flow_sent
            iter_state[u] += 1
        return 0

    def run(self):
        max_flow = 0
        while self.bfs_build_levels():
            iter_state = {node: 0 for node in self.all_nodes}
            while True:
                pushed = self.dfs_send_flow(self.source, float('inf'), iter_state)
                if pushed == 0: break
                max_flow += pushed
        return max_flow

def solve_case():
    try:
        n, m = map(int, input().split())
        matrix = [list(input().split()) for _ in range(n)]
    except (IOError, ValueError):
        return

    # Nodes for a bipartite graph: (n rows, m columns)
    row_nodes = [type('Node', (), {'edge':[]}) for _ in range(n)]
    col_nodes = [type('Node', (), {'edge':[]}) for _ in range(m)]
    source = type('Node', (), {'edge':[]})()
    sink = type('Node', (), {'edge':[]})()
    
    frac_matrix = [[0] * m for _ in range(n)]
    
    # Calculates how many numbers in each row need to be rounded
    total_row_demand = 0
    for r in range(n):
        row_frac_sum = 0
        for c in range(m):
            frac_val = int(matrix[r][c].split('.')[1])
            if matrix[r][c].startswith('-'): frac_val *= -1
            frac_matrix[r][c] = frac_val
            row_frac_sum += frac_val
        
        if row_frac_sum % 1000 != 0:
            print("NO")
            return
        row_up_rounds = row_frac_sum // 1000
        add_edge_pair(source, row_nodes[r], row_up_rounds)
        total_row_demand += row_up_rounds

    # Calculates how many numbers in each column need to be rounded
    total_col_demand = 0
    for c in range(m):
        col_frac_sum = sum(frac_matrix[r][c] for r in range(n))
        if col_frac_sum % 1000 != 0:
            print("NO")
            return
        col_up_rounds = col_frac_sum // 1000
        add_edge_pair(col_nodes[c], sink, col_up_rounds)
        total_col_demand += col_up_rounds
        
    if total_row_demand != total_col_demand:
        print("NO")
        return
    
    cell_edges = [[add_edge_pair(row_nodes[r], col_nodes[c], 1) for c in range(m)] for r in range(n)]
    
    solver = DinicSolver(row_nodes + col_nodes, source, sink)
    max_flow = solver.run()
    
    if max_flow != total_row_demand:
        print("NO")
        return
        
    print("YES")
    for r in range(n):
        print(*(int(edge.flow) for edge in cell_edges[r]))

def main():
    try:
        num_test_cases = int(input())
        for _ in range(num_test_cases):
            solve_case()
    except (IOError, ValueError):
        pass

if __name__ == "__main__":
    main()