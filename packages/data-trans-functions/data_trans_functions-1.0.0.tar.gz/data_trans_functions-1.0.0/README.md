# Data Trans Functions

## Description

The `data-trans-functions` package provides utility functions to perform operations on 2D matrices 
and 1D arrays. With features like 2D matrix transposition, 1D windowing, and 2D convolution, it 
simplifies common operations while ensuring type safety.

## Features

- **transpose2d**: Transposes a 2D matrix, effectively switching its axes.
- **window1d**: Generates a series of 1D sliding windows from an input array.
- **convolution2d**: Computes the 2D convolution of an input matrix using a given kernel.

## Installation

To install the package via `pip`, run:
pip install data-trans-functions

## Usage

Here are brief examples for each function:

```python
from data_trans_functions import transpose2d, window1d, convolution2d
import numpy as np

# Using transpose2d:
matrix = [[1, 2, 3], [4, 5, 6]]
print(transpose2d(matrix))  # Returns: [[1, 4], [2, 5], [3, 6]]

# Using window1d:
arr = [1, 2, 3, 4]
print(window1d(arr, 2, shift=2))  # Returns: [[1, 2], [3, 4]]

# Using convolution2d:
input_matrix = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
kernel = np.array([[1, 0], [0, -1]])
print(convolution2d(input_matrix, kernel))  # Returns: [[3, 2], [3, 2]]
```

## Recommendations

It's recommended to use these functions in combination with a type checker like mypy for safer usage.
