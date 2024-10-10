# -*- coding: utf-8 -*-
import numpy as np
from scipy.stats import bernoulli

class Data_formatting:
    
    @staticmethod
    def array_to_string(array):
        """
        Parameter: 1d Array of binary data to be input into NIST randomness tests, which require string format
        Returns: The data in string format
        Notes: The function turns the array to a list then a string - if you call str(array), once the array is too long, you get an output
        that looks like 110...010, e.g. of length 9 and losing all the middle data. This function appears to work now, but  it is plausible that it is buggy in some unknown way.
        """
        return ''.join(map(str, array))
    
    
    @staticmethod
    def row_col_orders(array):
        """
        Parameter: array in m x n format to be split into row and column order for testing
        Returns: A pair (row_order, col_order) of 1d arrays, with the data in row and column order
        Notes: It may be helpful to check that the array input is already in the right order
        """
        row_order = array.flatten()
        col_order = (array.T).flatten()
        return row_order, col_order
    
    @staticmethod
    def row_col_serializer(arrays):
        """
        Parameters: An array of PUF-data arrays
        Returns: A tuple of arrays (row_orders, col_orders) of row/column output order per device
        Notes: only takes a single input array for each device
        """
        no_of_arrays = len(arrays)
        row_arrays = np.empty(no_of_arrays, dtype=object)
        col_arrays = np.empty(no_of_arrays, dtype = object)
        for i in range(no_of_arrays):
            row_arrays[i] = Data_formatting.row_col_orders(arrays[i])[0]
            col_arrays[i] = Data_formatting.row_col_orders(arrays[i])[1]
        return row_arrays, col_arrays
    
    
    @staticmethod
    def make_blocks(data, row_length, col_length, puf_row_length, puf_col_length):
        """
        Parameters
        ----------
        data : array
            Read data for the PUF under test, stored in row order.
        row_length : integer
            length of row of the block.
        col_length : integer
            length of column of the block
        puf_row_length : integer
            length of PUF rows
        puf_col_length : integer
            length of PUF cols
        Returns
        -------
        A single long array of PUF data read in block order

        """
        #count number of blocks for the given block size
        number_of_row_blocks = int(np.floor(puf_row_length/row_length))
        number_of_col_blocks = int(np.floor(puf_col_length/col_length))
        global_block_list = []
        rows_block_list = []
        #split into blocks of rows, then split those row blocks into rectangular blocks
        for i in range(number_of_col_blocks):
            block_row_start = col_length*i
            block = data[block_row_start:(block_row_start + col_length)]
            rows_block_list.append(block)
        #here is where we split the row blocks into the end blocks
        for i in range(len(rows_block_list)):
            for j in range(number_of_row_blocks):
                block_col_start = row_length*j
                block_ij = (rows_block_list[i]).T[block_col_start:(block_col_start + row_length)]                
                global_block_list.append(block_ij.T)
        
        block_array = np.array(global_block_list)
        reordered_output = block_array.flatten()
        return reordered_output
    
    @staticmethod
    def blocks_serializer(arrays, row_length, col_length, puf_row_length, puf_col_length):
        """
        This just serializes the above function for an array of many input PUFs to be reformatted to block order
        """
        no_of_arrays = len(arrays)
        block_orders = np.empty(no_of_arrays, dtype=object)
        for i in range(no_of_arrays):
            block_orders[i] = Data_formatting.make_blocks(arrays[i], row_length, col_length, puf_row_length, puf_col_length)
        return block_orders

    @staticmethod
    def p_values_to_pass_fail(p_values, p_value):
        """
        Parameters
        ----------
        p_values : array
            An array of all p_values for all test (e.g. per test, a set of p-values, stored in test x device format).
        p_value : float
            a p_value

        Returns
        -------
        An array of length equal to the number of tests (length of p_values) of number of passes of each type.

        """
        number_of_tests = len(p_values)
        test_pass_fail_scores = []
        for i in range(number_of_tests):
            test_i_passes = (p_values[i] > p_value).sum()
            test_pass_fail_scores.append(test_i_passes)
        test_scores = np.array(test_pass_fail_scores)
        return test_scores