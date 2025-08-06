def solve_max_coins(balloon_values):
    num_balloons = len(balloon_values)
    
    dp_table = [[0] * num_balloons for _ in range(num_balloons)]
    
    # Iterates by the length of the balloon array
    for length in range(1, num_balloons + 1):
        for start_idx in range(num_balloons - length + 1):
            end_idx = start_idx + length - 1
            
            for k_idx in range(start_idx, end_idx + 1):
                
                left_part_coins = 0
                if k_idx != start_idx:
                    left_part_coins = dp_table[start_idx][k_idx - 1]
                
                right_part_coins = 0
                if k_idx != end_idx:
                    right_part_coins = dp_table[k_idx + 1][end_idx]
                
                left_boundary = 1
                if start_idx > 0:
                    left_boundary = balloon_values[start_idx - 1]
                
                right_boundary = 1
                if end_idx < num_balloons - 1:
                    right_boundary = balloon_values[end_idx + 1]
                
                current_score = left_part_coins + \
                                (left_boundary * balloon_values[k_idx] * right_boundary) + \
                                right_part_coins
                
                # Updates the table if this path gives more coins
                if current_score > dp_table[start_idx][end_idx]:
                    dp_table[start_idx][end_idx] = current_score
    
    return dp_table[0][num_balloons - 1]

def main():
    num_balloons = int(input())
    values = list(map(int, input().split()))
    
    max_score = solve_max_coins(values)
    print(max_score)

if __name__ == "__main__":
    main()