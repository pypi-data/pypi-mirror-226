# Data Transformation Library

## Project description
Create 3 functions that are common for transforming data used in machine learning models and publish then to `PyPi` using `poetry` dependency management tool.
#### Functions:

- __Transpose__ signature: transpose2d(input_matrix: list[list[float]]) -> list
- __Time Series Windowing__ signature: window1d(input_array: list | np.ndarray, size: int, shift: int = 1, stride: int = 1) -> list[list | np.ndarray]
- __Cross-Correlation__ signature: convolution2d(input_matrix: np.ndarray, kernel: np.ndarray, stride : int = 1) -> np.ndarray

### Objectives for this Part
- Practice using Python and Numpy.
- Practice building Python libraries.
Practice using Poetry.
- Practice publishing your packages to PyPI.
### Requirements
- Implement the three data transformation functions described in the - - Context section.
- Build a Python library containing the three functions.
- Publish the library to PyPI.
- Provide suggestions about how your analysis can be improved.


Published library `functions3` can be found [in PyPi index](https://pypi.org/project/functions3/) and installed with </br>`pip installed functions3`.</br>

After cloning this repo run these commands to test functions:</br>
`poetry install`</br>
`poetry run pytest`

