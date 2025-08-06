
def is_possible(group_size, resources, required_groups, n):
    if group_size == 0:
        return True 
    
    leftover = resources[0]
    groups_formed = 0
    
    for i in range(n - 2):
        current_resource = resources[i+1]
        
        newly_formed_groups = (leftover + current_resource) // group_size
        groups_formed += newly_formed_groups
        
        # Calculates the new leftover for the next pair
        total_value_needed = newly_formed_groups * group_size
        value_taken_from_current = max(0, total_value_needed - leftover)
        leftover = current_resource - value_taken_from_current

    return groups_formed >= required_groups

def solve_case(n, k, resources):
    # Edge cases
    if n == 0:
        print(0)
        return
    if n == 1:
        group_size = resources[0] // k if k > 0 else 0
        print(group_size * k)
        return
    
    # Binary searching
    low = 0
    high = sum(resources) 
    
    while low <= high:
        mid_size = (low + high) // 2
        if mid_size == 0:
            low = 1
            continue

        if is_possible(mid_size, resources, k, n):

            # If this size works, we will try for a bigger one
            best_size = mid_size
            low = mid_size + 1
        else:
            high = mid_size - 1
            
    print(best_size * k)
    
def main():
    try:
        num_test_cases = int(input())
        for _ in range(num_test_cases):
            n, k = map(int, input().split())
            ages = list(map(int, input().split()))
            solve_case(n, k, ages)
    except (IOError, ValueError):
        pass

if __name__ == "__main__":
    main()