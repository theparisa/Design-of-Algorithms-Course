def solve_problem():
    num_strings = int(input())
    reversal_costs = list(map(int, input().split()))
    strings = [input() for _ in range(num_strings)]
    
    reversed_strings = [s[::-1] for s in strings]
    infinity = float('inf')
    
    # The DP table 
    min_costs = [[infinity] * 2 for _ in range(num_strings)]
    
    # Base cases 
    min_costs[0][0] = 0
    min_costs[0][1] = reversal_costs[0]

    #  DP loop 
    for i in range(1, num_strings):
        # Checks the four possible ways to extend the sorted sequence
        
        if strings[i] >= strings[i-1]:
            min_costs[i][0] = min_costs[i-1][0]
            
        if reversed_strings[i] >= strings[i-1]:
            min_costs[i][1] = min_costs[i-1][0] + reversal_costs[i]
            
        if strings[i] >= reversed_strings[i-1]:
            min_costs[i][0] = min(min_costs[i][0], min_costs[i-1][1])
            
        if reversed_strings[i] >= reversed_strings[i-1]:
            min_costs[i][1] = min(min_costs[i][1], min_costs[i-1][1] + reversal_costs[i])

    final_result = min(min_costs[num_strings - 1])

    if final_result == infinity:
        print(-1)
    else:
        print(final_result)

if __name__ == "__main__":
    solve_problem()