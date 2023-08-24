from typing import List, Union

import numpy as np
import numpy.typing as npt


def _array_number(input_array: Union[List[float], npt.NDArray], size: int,
                  shift: int = 1, stride: int = 1) -> int:
    """Function to return number of arrays of dataset for window1d function

    Parameters:
    input_array: a list or 1D Numpy array of real numbers
    size: a positive integer that determines the size (length) of the window
    shift: a positive integer that determines the shift (step size) between different windows
    stride: a positive integer that determines the stride (step size) within each window

    Returns:
        int: number of arrays
    """
    step_size = (size - 1) * stride + 1
    return (len(input_array) - step_size) // shift + 1


def transpose2d(input_matrix: List[List[float]]) -> List[List[float]]:
    """
    Returns an array with axes transposed.

    Parameters:
    input_matrix: 2d array

    Returns:
    list of real numbers
    """
    return [
        [input_matrix[j][i] for j in range(len(input_matrix))]
        for i in range(len(input_matrix[0]))
        ]


def window1d(input_array: Union[List[float], npt.NDArray], size: int, shift: int = 1,
             stride: int = 1) -> Union[list, npt.NDArray]:
    """
    Returns a dataset of "windows". Each "window" is a dataset that
    contains a subset of elements of the input dataset.

    Parameters:
    input_array: a list or 1D Numpy array of real numbers
    size: a positive integer that determines the size (length) of the window
    shift: a positive integer that determines the shift (step size) between different windows
    stride: a positive integer that determines the stride (step size) within each window

    Returns:
    list of lists or 1D Numpy arrays of real numbers
    """
    for arg_name, arg in {'size': size, 'shift': shift, 'stride': stride}.items():
        if not isinstance(arg, int) or arg < 1:
            raise ValueError(f'{arg_name} should be a positive integer')

    array_num = _array_number(input_array, size, shift, stride)
    return [[input_array[num * shift + i*stride] for i in range(size)] for num in range(array_num)]


def convolution2d(input_matrix: npt.NDArray, kernel: npt.NDArray, stride: int = 1) -> npt.NDArray:
    """
    Compute 2D cross-correlation.

    Parameters:
    input_matrix: 2d Numpy array of real numbers
    kernel: 2D Numpy array of real numbers
    stride: an integer that is greater than 0

    Returns:
    2D Numpy array of real numbers
    """
    if not isinstance(stride, int) or stride < 1:
        raise ValueError('stride should be a integer greater than 0')

    h, w = kernel.shape
    output = np.zeros((round((input_matrix.shape[0] - h + stride)/stride),
                       round((input_matrix.shape[1] - w + stride)/stride)))
    for i in range(output.shape[0]):
        st_i = i * stride
        for j in range(output.shape[1]):
            st_j = j * stride
            output[i, j] = (input_matrix[st_i:st_i + h, st_j:st_j + w] * kernel).sum()
    return output
