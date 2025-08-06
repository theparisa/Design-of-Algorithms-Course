
lower_bound = 0
upper_bound = 0
valid_subarray_count = 0

def main():
    global valid_subarray_count, lower_bound, upper_bound
    
    initial_numbers, lower_b, upper_b = read_inputs()
    lower_bound = lower_b
    upper_bound = upper_b
    
    prefix_sums = calculate_prefix_sums(initial_numbers)
    
    # Counts subarrays starting from the beginning
    for p_sum in prefix_sums:
        if lower_bound <= p_sum <= upper_bound:
            valid_subarray_count += 1
            
    # Counts all other subarrays using a divide-and-conquer method
    count_valid_subarrays(prefix_sums)
    print(valid_subarray_count)

# Modified merge
def count_valid_subarrays(arr):
    if len(arr) > 1:
        mid = len(arr) // 2
        left_half = arr[:mid]
        right_half = arr[mid:]
        
        count_valid_subarrays(left_half)
        count_valid_subarrays(right_half)
        
        count_crossing_pairs(left_half, right_half)
        
        merge(arr, left_half, right_half)

def count_crossing_pairs(left, right):
    global valid_subarray_count
    
    excluded_count = 0
    j = 0
    for i_val in left:
        while j < len(right) and right[j] - i_val < lower_bound:
            j += 1
        excluded_count += j
    
    j = len(right) - 1
    for i_val in reversed(left):
        while j >= 0 and right[j] - i_val > upper_bound:
            j -= 1
        excluded_count += len(right) - 1 - j
    
    total_pairs = len(left) * len(right)
    valid_pairs = total_pairs - excluded_count
    valid_subarray_count += valid_pairs
        
def merge(arr, left, right):
    i = j = k = 0
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            arr[k] = left[i]
            i += 1
        else:
            arr[k] = right[j]
            j += 1
        k += 1
        
    while i < len(left):
        arr[k] = left[i]
        i += 1
        k += 1
        
    while j < len(right):
        arr[k] = right[j]
        j += 1
        k += 1
        
# Converts to prefix sums
def calculate_prefix_sums(arr):
    if not arr:
        return []
    for i in range(1, len(arr)):
        arr[i] += arr[i-1]
    return arr

def read_inputs():
    arr = list(map(int, input().split()))
    lower, upper = map(int, input().split())
    return arr, lower, upper

if __name__ == "__main__":
    main()