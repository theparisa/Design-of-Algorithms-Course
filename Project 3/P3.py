
search_start_index = 0

# Checks current arrangement
def is_arrangement_beautiful(heights, k):
    global search_start_index
    num_books = len(heights)
    
    for i in range(search_start_index, num_books - 1):
        is_valid_for_book_i = False
        for j in range(i + 1, min(i + k + 1, num_books)):
            if heights[j] < heights[i]:
                is_valid_for_book_i = True
                break
        
        if not is_valid_for_book_i:
            search_start_index = max(0, i - 1)
            return False
            
    return True

def solve_case():
    n, k = map(int, input().split())
    book_heights = list(map(int, input().split()))
    book_heights.append(0) 

    if is_arrangement_beautiful(book_heights, k):
        print("YES")
        return
    
    # tries every single swap to fix it
    for i in range(search_start_index, len(book_heights)):
        for j in range(i + 1, len(book_heights)):
            if book_heights[i] > book_heights[j]:
                book_heights[i], book_heights[j] = book_heights[j], book_heights[i]
                
                if is_arrangement_beautiful(book_heights, k):
                    print("YES")
                    return
                
                # Swaps back
                book_heights[i], book_heights[j] = book_heights[j], book_heights[i]
    
    print("NO")

if __name__ == "__main__":
    solve_case()