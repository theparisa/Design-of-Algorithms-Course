
# Large number for modulo operations
MOD = 100000000

def count_arrangements(num_a, num_b, max_run_a, max_run_b):

    dp_table = [[[[0] * (max_run_b + 1) for _ in range(max_run_a + 1)] 
                for _ in range(num_b + 1)] for _ in range(num_a + 1)]

    # Base case
    dp_table[0][0][0][0] = 1

    for i in range(num_a + 1):
        for j in range(num_b + 1):
            for k in range(max_run_a + 1):
                for l in range(max_run_b + 1):
                    if dp_table[i][j][k][l] == 0:
                        continue
                    
                    current_ways = dp_table[i][j][k][l]

                    # Adds of type A
                    if i < num_a and k < max_run_a:
                        dp_table[i + 1][j][k + 1][0] = (dp_table[i + 1][j][k + 1][0] + current_ways) % MOD
                    
                    #  Add of type B
                    if j < num_b and l < max_run_b:
                        dp_table[i][j + 1][0][l + 1] = (dp_table[i][j + 1][0][l + 1] + current_ways) % MOD

    # Sums up
    total_ways = 0
    for k in range(max_run_a + 1):
        for l in range(max_run_b + 1):
            total_ways = (total_ways + dp_table[num_a][num_b][k][l]) % MOD

    return total_ways

def main():
    n, m, v, c = map(int, input().split())
    result = count_arrangements(n, m, v, c)
    print(result)

if __name__ == "__main__":
    main()