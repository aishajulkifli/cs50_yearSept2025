import numpy as np

arr = np.array([[1, 2, 3, 4], [5, 6, 7, 8]])       # Create a NumPy array

print("Original Array:", arr)               # Print the original array
print("Every other element:", arr[::1])     # Print every other element of the array, arr[::1] means start from the beginning to the end of the array with a step of 1
print("Number of dimensions:", arr.ndim)    # Print the number of dimensions of the array
print("Shape of array:", arr.shape)         # Print the shape of the array, which representing the size of each dimension
print("Total elements:", arr.size)          # Print the total number of elements in the array
