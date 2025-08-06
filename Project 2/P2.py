
def calculate_win_probability(board_size, win_threshold, max_roll):

    # dp_array[i] : the probability of landing on square i
    num_squares = board_size + 1
    dp_array = [0.0] * num_squares

    dp_array[0] = 1.0

    for current_square in range(1, num_squares):

        for roll_value in range(1, max_roll + 1):
            prev_square = current_square - roll_value
            
            if prev_square < 0:
                break 
                
            if prev_square >= win_threshold:
                continue

            dp_array[current_square] += dp_array[prev_square] / max_roll
            

    total_win_chance = sum(dp_array[win_threshold:])
    return total_win_chance

def main():
    n, m, k = map(int, input().split())
    
    win_probability = calculate_win_probability(n, m, k)
    
    print(f"{win_probability:.6f}")

if __name__ == "__main__":
    main()