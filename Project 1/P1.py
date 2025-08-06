import sys

MOD = 10**9 + 7

class BstSequenceCounter:
    def __init__(self, max_size, mod):
        self.mod = mod
        self.memo = {}
        
        # Pre-computes and stores a table of combination values
        self.combinations_table = self._build_combinations(max_size, mod)

    def _build_combinations(self, n, mod):
        table = [[0] * (n + 1) for _ in range(n + 1)]
        for i in range(n + 1):
            table[i][0] = 1
            table[i][i] = 1
            for j in range(1, i):
                table[i][j] = (table[i-1][j-1] + table[i-1][j]) % mod
        return table

    def count_arrangements(self, sequence):

        # Using a tuple for the sequence and memoization
        return self._count_recursive(tuple(sequence))

    def _count_recursive(self, sequence):
        if len(sequence) <= 1:
            return 1
        
        if sequence in self.memo:
            return self.memo[sequence]

        root = sequence[0]
        left_nodes = tuple(x for x in sequence if x < root)
        right_nodes = tuple(x for x in sequence if x > root)
        
        ways_for_left = self._count_recursive(left_nodes)
        ways_for_right = self._count_recursive(right_nodes)
        
        # Calculates ways to interleave the left and right sub-sequences
        num_to_place = len(sequence) - 1
        ways_to_interleave = self.combinations_table[num_to_place][len(left_nodes)]
        
        result = (ways_to_interleave * ways_for_left) % self.mod
        result = (result * ways_for_right) % self.mod
        
        self.memo[sequence] = result
        return result

def main():
    try:
        n = int(input())
        numbers = list(map(int, input().split()))
    except (IOError, ValueError):
        n = 0
        numbers = []

    if n == 0:
        print(0)
        return

    counter = BstSequenceCounter(n, MOD)
    total_ways = counter.count_arrangements(numbers)
    
    print(total_ways - 1)

if __name__ == "__main__":
    main()