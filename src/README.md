# PUF Testing Suite

Clone the repository and run the Main.py script
> python Main.py

In addition the test suite can be installed as a Python package via pip:
pip install git+ssh://git@github.com:cryptoquantique/puf-randomness-test.git --upgrade

The modules used in Main can then be imported to your own application.

## Input Data Format
The Main file runs the test suite on data saved as an numpy array in n x a x b format, where
n = number of PUFs
a = row length of the PUF
b = column length of the PUF
If the PUF does not have a row/column layout, the suite should work on n x m arrays, for m = output length.

## Required User Input
User input variables are found towards the top of Main.py in the code block marked "User Input Choices"
The user must specify:
* the data file containing the data by changing the variable data_file_name
* the results file where the results will be saved by changing the variable results_file_name
Additionally, if the PUF is arranged in rows and columns, the user must specify:
* the row block length b1
* the column block length b2
Note that a sensible default value for b1 and b2 is 4.

## Results File and Output
Main outputs a .txt file summarizing the results, giving a pass/fail count at the selected p-value (in each order).
Each test is also given a chi-squared test for uniformity score on the p-values.
If the results file already exists, the new results will be appended to the previous file rather than overwriting it.

Main also writes several objects that may be of interest to variables. For example:
* row_p_values and col_p_values are arrays of p-values per test/device.
* Similarly, row_chi_sq_values provides the chi-sq value per test.

## File Arrangement
The files are arranged so that the top folder holds the files running the tests, as well as some formatting files that make the implementation compatible with the test files.
The tests themselves are contained in the randomness_testsuite subfolder.

## Acknowledgement
The implementations of the tests found here are based on those found here https://github.com/stevenang/randomness_testsuite , with some minor modifications.
