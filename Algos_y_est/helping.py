# Function to perform selection sort on a list of tuples based on the first element
def selection_sort(arr):
    n = len(arr)
    for i in range(n-1):
        min_idx = i
        for j in range(i+1, n):
            if arr[j][0] <= arr[min_idx][0]:
                min_idx = j
        # Swap the minimum element with the first element of the unsorted part
        arr[i], arr[min_idx] = arr[min_idx], arr[i]

# Function to print the list of tuples
def print_list(arr):
    for tup in arr:
        print(tup, end=" ")
    print()

# Example list of tuples
arr = [(64, 3), (34, 2), (25, 1), (64, 5), (22, 4), (11, 6), (90, 7)]

print("Original list of tuples:")
print_list(arr)

# Perform selection sort based on the first element of the tuples
selection_sort(arr)

print("Sorted list of tuples:")
print_list(arr)
