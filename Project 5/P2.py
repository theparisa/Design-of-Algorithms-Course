
class Node:
    def __init__(self, name):
        self.name = name
        self.out_edges = []
        self.in_edges = []

# Max-flow using the Ford-Fulkerson method
class MaxFlowSolver:
    def __init__(self, nodes, edges):
        self.nodes = nodes
        self.source = nodes[0]
        self.sink = nodes[-1]
        
        self.capacities = {}
        self.flows = {}
        
        for u, v in edges:
            self.capacities[(u, v)] = 1
            self.flows[(u, v)] = 0
            self.flows[(v, u)] = 0
    
    def _find_path_dfs(self, u, path_flow):
        self.visited_on_path[u] = True
        self.path_bottleneck[u] = path_flow
        
        if u == self.sink:
            return
            
        # Forward edges with remaining capacity
        for _, v in u.out_edges:
            edge = (u, v)
            if not self.visited_on_path[v] and self.capacities[edge] > self.flows[edge]:
                self.parent_map[v] = u
                self._find_path_dfs(v, min(path_flow, self.capacities[edge] - self.flows[edge]))

        # Backward edges with positive flow
        for v, _ in u.in_edges:
            edge = (v, u)
            if not self.visited_on_path[v] and self.flows[edge] > 0:
                self.parent_map[v] = u
                self._find_path_dfs(v, min(path_flow, self.flows[edge]))

    def run(self):

        # Finds paths in the residual graph
        while True:
            self.visited_on_path = {node: False for node in self.nodes}
            self.parent_map = {}
            self.path_bottleneck = {node: 0 for node in self.nodes}
            
            self._find_path_dfs(self.source, float('inf'))
            
            if not self.visited_on_path[self.sink]:
                break 
            
            # Augment flow along the path found by DFS
            path_capacity = self.path_bottleneck[self.sink]
            v = self.sink
            while v != self.source:
                u = self.parent_map[v]
                self.flows[(u, v)] += path_capacity
                self.flows[(v, u)] -= path_capacity
                v = u

    def reconstruct_paths(self):

        total_flow = int(sum(self.flows.get((self.source, v), 0) for _, v in self.source.out_edges))
        print(total_flow)
        
        for _ in range(total_flow):
            path = []
            curr = self.source
            while curr != self.sink:
                path.append(curr)
                for _, next_node in curr.out_edges:
                    edge = (curr, next_node)
                    if self.flows.get(edge, 0) > 0:
                        self.flows[edge] -= 1
                        curr = next_node
                        break
            path.append(self.sink)
            
            print(len(path))
            print(' '.join(str(node.name + 1) for node in path))

def main():
    n, m = map(int, input().split())
    nodes = [Node(i) for i in range(n)]
    edges = []
    for _ in range(m):
        u, v = map(int, input().split())
        u_node, v_node = nodes[u - 1], nodes[v - 1]
        edges.append((u_node, v_node))
        u_node.out_edges.append((u_node, v_node))
        v_node.in_edges.append((u_node, v_node))

    solver = MaxFlowSolver(nodes, edges)
    solver.run()
    solver.reconstruct_paths()

if __name__ == "__main__":
    main()