
problem_data = {}

def read_inputs():
    global problem_data
    n, k, cost_A, cost_B = map(int, input().split())
    
    item_locations = sorted(map(int, input().split()))
    
    problem_data = {
        "n": n,
        "k": k,
        "A": cost_A,
        "B": cost_B,
        "locations": item_locations,
        "location_idx": 0,
        "num_locations": len(item_locations)
    }

# Recursively finds the minimum cost for a given range
def find_minimum_cost(start, end):

    # The range is a single cell
    if start == end:
        items_in_cell = 0
        while (problem_data["location_idx"] < problem_data["num_locations"] and 
               problem_data["locations"][problem_data["location_idx"]] == start + 1):
            problem_data["location_idx"] += 1
            items_in_cell += 1

        if items_in_cell == 0:
            cost = problem_data["A"]
        else:
            cost = problem_data["B"] * items_in_cell
        return items_in_cell, cost
    
    mid = (start + end) // 2
    
    items_left, cost_left = find_minimum_cost(start, mid)
    items_right, cost_right = find_minimum_cost(mid + 1, end)
    
    total_items = items_left + items_right
    
    # Compares cost of handling range 
    cost_if_together = problem_data["A"]
    if total_items > 0:
        range_size = end - start + 1
        cost_if_together = problem_data["B"] * total_items * range_size
    
    cost_if_separate = cost_left + cost_right
    
    final_cost = min(cost_if_together, cost_if_separate)
    
    return total_items, final_cost

def main():
    read_inputs()
    
    total_range = 2**problem_data["n"]
    min_cost = find_minimum_cost(0, total_range - 1)[1]
    
    print(min_cost)

if __name__ == "__main__":
    main()