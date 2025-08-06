from collections import deque

def solve_problem():
    n, m, grid = read_grid_input()

    # dists[r][c][i] : stores the min distance
    dists = [[[float('inf')] * 3 for _ in range(m)] for _ in range(n)]

    # Run BFS for each landmark
    for landmark_type in range(1, 4):
        q = deque()
        visited = [[False] * m for _ in range(n)]
        
        for r in range(n):
            for c in range(m):
                if grid[r][c] == str(landmark_type):
                    q.append((r, c, 0))
                    visited[r][c] = True
        
        while q:
            row, col, dist = q.popleft()
            dists[row][col][landmark_type - 1] = dist
            
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = row + dr, col + dc
                if 0 <= nr < n and 0 <= nc < m and not visited[nr][nc] and grid[nr][nc] != '#':
                    visited[nr][nc] = True
                    q.append((nr, nc, dist + 1))
    
    # Finds the two shortest direct paths between zones
    dist_1_2 = find_dist_between_zones(1, 2, n, m, grid) - 1
    dist_2_3 = find_dist_between_zones(2, 3, n, m, grid) - 1
    dist_1_3 = find_dist_between_zones(1, 3, n, m, grid) - 1

    min_total_dist = sum(sorted([dist_1_2, dist_2_3, dist_1_3])[:2])

    # Checks paths that meet at an empty cell
    for r in range(n):
        for c in range(m):
            if grid[r][c] == '.':
                cost_via_cell = sum(dists[r][c]) - 2
                min_total_dist = min(min_total_dist, cost_via_cell)
                
    print(min_total_dist)

# Finds shortest path between any two zones
def find_dist_between_zones(type1, type2, n, m, grid):
    q = deque()
    visited = [[False] * m for _ in range(n)]
    
    for r in range(n):
        for c in range(m):
            if grid[r][c] == str(type1):
                q.append((r, c, 0))
                visited[r][c] = True
    
    while q:
        row, col, dist = q.popleft()
        if grid[row][col] == str(type2):
            return dist
            
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = row + dr, col + dc
            if 0 <= nr < n and 0 <= nc < m and not visited[nr][nc] and grid[nr][nc] != '#':
                visited[nr][nc] = True
                q.append((nr, nc, dist + 1))
    return float('inf')

def read_grid_input():
    n, m = map(int, input().split())
    grid = [input().strip() for _ in range(n)]
    return n, m, grid

if __name__ == "__main__":
    solve_problem()