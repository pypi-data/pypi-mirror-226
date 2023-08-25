from typing import List, Union, TypeVar
import numpy as np


def transpose2d(
    input_matrix: List[List[Union[int, float]]]
) -> List[List[Union[int, float]]]:
    """
    Transposes a 2D matrix (switches axis of the 2D matrix).

    This function returns the transpose of a given 2D matrix. Each row of the
    matrix should have the same length. If not, a ValueError is raised. Matrix
    elements can be integers or floats.

    Note:
    - For safer use, use with a type checker like `mypy`.

    Parameters:
    - input_matrix (List[List[Union[int, float]]]):
      2D matrix with integers or floats.

    Returns:
    - List[List[Union[int, float]]]: Transposed matrix.

    Raises:
    - ValueError: If rows in input matrix have varying lengths.

    Example:
    >>> transpose2d([[1,2,3], [4,5,6]])
    [[1, 4], [2, 5], [3, 6]]
    """
    if not input_matrix:
        return []

    l = len(input_matrix[0])
    if any(l != len(row) for row in input_matrix):
        raise ValueError("Matrix rows must be equal length!")

    return [list(i) for i in zip(*input_matrix)]


ElementType = Union[int, float]
ArrayType = TypeVar("ArrayType", List[ElementType], np.ndarray)


def window1d(
    input_array: ArrayType, size: int, shift: int = 1, stride: int = 1
) -> ArrayType:
    """
    Generates list of 1D windows(lists) from the input array.

    This function creates a series of 1D sliding windows from the given input
    array, considering the specified size, shift, and stride. The function can
    handle both Python lists and one-dimensional numpy arrays.

    Note:
    - For safer use, it's recommended to use with a type checker like `mypy`.

    Parameters:
    - input_array (ArrayType): Input list or 1D numpy array.
    - size (int): Size of each window.
    - shift (int, optional): The shift between consecutive windows. Defaults to 1.
    - stride (int, optional): Steps between elements within a window. Defaults to 1.

    Returns:
    - ArrayType: List of windows or a 2D numpy array of windows.

    Raises:
    - ValueError: For non-positive size, shift, stride, or if input_array isn't 1D.

    Example:
    >>> window1d([1,2,3,4], 2, shift=2)
    [[1, 2], [3, 4]]
    """
    if size <= 0:
        raise ValueError("Size must be positive integer!")

    if shift <= 0:
        raise ValueError("Shift must be positive integer!")

    if stride <= 0:
        raise ValueError("Stride must be positive integer!")

    input_len = len(input_array)
    start_position = 0
    window_reach = stride * (size - 1) + 1

    if isinstance(input_array, list):
        windows = []
        while start_position + window_reach <= input_len:
            end_position = start_position + window_reach
            window = input_array[start_position:end_position:stride]
            windows.append(window)
            start_position += shift
    else:
        if input_array.ndim != 1:
            raise ValueError("Input_array must be one-dimensional array!")

        num_windows = ((input_len - window_reach) // shift) + 1
        windows = np.empty((num_windows, size), dtype=input_array.dtype)

        for window_idx in range(num_windows):
            end_position = start_position + window_reach
            windows[window_idx] = input_array[
                start_position:end_position:stride
            ]
            start_position += shift

    return windows


def convolution2d(
    input_matrix: np.ndarray, kernel: np.ndarray, stride: int = 1
) -> np.ndarray:
    """
    Performs 2D convolution on an input matrix with a given kernel.

    This function computes the 2D convolution of the input_matrix using the
    specified kernel. The stride determines the step size taken when moving
    the kernel across the input matrix (both directions).

    Note:
    - For safer use, it's recommended to use with a type checker like `mypy`.

    Parameters:
    - input_matrix (np.ndarray): Input 2D array to be convoluted.
    - kernel (np.ndarray): 2D array representing the convolution kernel.
    - stride (int, optional): Step size taken when moving the kernel. Defaults to 1.

    Returns:
    - np.ndarray: 2D array representing the result of the convolution.

    Raises:
    - ValueError: If matrices aren't 2D, for non-positive strides, or if the
      kernel dimensions exceed those of the input_matrix.

    Example:
    >>> input_matrix = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    >>> kernel = np.array([[1, 0], [0, -1]])
    >>> convolution2d(input_matrix, kernel)
    array([[  3.,   2.],
           [  3.,   2.]])
    """
    if not (input_matrix.ndim == kernel.ndim == 2):
        raise ValueError(
            "Both input_matrix and kernel must be two-dimensional arrays!"
        )

    if stride <= 0:
        raise ValueError("Stride can not be negative!")

    matrix_height, matrix_width = input_matrix.shape
    kernel_height, kernel_width = kernel.shape

    if kernel_width > matrix_width or kernel_height > matrix_height:
        raise ValueError(
            "Kernel width/height can not exceed matrix width/height!"
        )

    output_height = (matrix_height - kernel_height) // stride + 1
    output_width = (matrix_width - kernel_width) // stride + 1

    output = np.zeros((output_height, output_width))

    for y in range(output_height):
        for x in range(output_width):
            output[y, x] = np.sum(
                input_matrix[
                    y * stride : y * stride + kernel_height,
                    x * stride : x * stride + kernel_width,
                ]
                * kernel
            )

    return output
