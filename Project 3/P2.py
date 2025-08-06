def solve_case():
    a, b, c, d = map(int, input().split())
    text_string = input()
    
    expected_h_count = a + c + d
    expected_p_count = b + c + d
    
    if len(text_string) != expected_h_count + expected_p_count:
        print("NO")
        return
        
    actual_h_count = text_string.count('H')
    actual_p_count = text_string.count('P')
    
    if actual_h_count == expected_h_count and actual_p_count == expected_p_count:
        print("YES")
    else:
        print("NO")

def main():
    try:
        num_test_cases = int(input())
        for _ in range(num_test_cases):
            solve_case()
    except (IOError, ValueError):
        # Cases with empty or invalid input
        pass

if __name__ == "__main__":
    main()