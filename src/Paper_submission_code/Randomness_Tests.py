# -*- coding: utf-8 -*-
import random
import math
import sys
import numpy as np
from .Data_Formatting import Data_formatting
#this imports the NIST tests - it may be that you need to change this line depending on the structure of your directory
#sys.path.append('randomness_testsuite-master')
from .randomness_testsuite.NewMain import string_calls
from .randomness_testsuite.RunTest_Q import *
from .randomness_testsuite.Spectral_Q import *
from .randomness_testsuite.FrequencyTest_Q import *
from .randomness_testsuite.FourbyFourBMRT import Matrix

#%%
class Randomness_Testing:
    
    @staticmethod
    def get_p_values(array, mode):
        """
        Parameter: array of the 0-1 output values for a device. Mode: see notes, chooses row/col/block tests
        Returns: An array of p-values for the NIST tests.
        Notes: The output array is in the order specified in NewMain for the NIST randomness test suite and in the Main file.
        mode 0 = row order
        mode 1 = col order
        mode 2 = block order
        
        """
        #flatten input array so we can turn it into string
        flat_array = array.flatten()
        #turn array into string
        string_format = Data_formatting.array_to_string(flat_array)
        #get and return array of p values
        if mode == 0:
            p_values = string_calls.row_test_runner(string_format)
        if mode == 1:
            p_values = string_calls.col_test_runner(string_format)
        if mode == 2:
            p_values = string_calls.block_test_runner(string_format)
        return np.array(p_values)
    
    @staticmethod
    def get_pass_fails(array, p_value, mode):
        """
        Parameter: array of the 0-1 output values for a device, a p-value, a mode
        Returns: An array of booleans, pass/fail scores for the NIST tests at the chosen p-value
        Notes: The output array depends on order, can be found in NewMain
        mode 0 = row order
        mode 1 = col order
        mode 2 = block order
        """
        #call p_value test on array scores 
        p_values = Randomness_Testing.get_p_values(array, mode)
        #compare p-value score to chosen p-value threshold
        pass_fail_array = p_values > p_value
        return pass_fail_array
    
    @staticmethod
    def p_values_serializer(arrays, mode):
        """
        Parameter: an array of arrays, each containing the scores for a device
        Returns: an array of array of p-values for the NIST tests
        Notes: This just serializes get_p_values
        mode 0 = row order
        mode 1 = col order
        mode 2 = block order
        """
        no_of_arrays = len(arrays)
        if mode == 0:
            no_of_tests = 11
        if mode == 1:
            no_of_tests = 10
        if mode == 2:
            no_of_tests = 2
        p_value_arrays = np.empty((no_of_arrays, no_of_tests), dtype=object)
        for i in range(no_of_arrays):
            test_results = Randomness_Testing.get_p_values(arrays[i], mode)
            for j in range(no_of_tests):
                p_value_arrays[i][j] = test_results[j]
        return p_value_arrays


    @staticmethod
    def pass_fails_serializer(arrays, p_value, mode):
        """
        Parameter: an array of arrays, each containing the scores for a device
        Returns: an array of arrays of booleans, pass/fail scores for the NIST tests at chosen p-value
        Notes: This just serializes get_pass_fails
        mode 0 = row order
        mode 1 = col order
        mode 2 = block order
        """
        no_of_arrays = len(arrays)
        pass_fail_arrays = np.empty(no_of_arrays, dtype = object)
        for i in range(no_of_arrays):
            pass_fail_arrays[i] = Randomness_Testing.get_pass_fails(arrays[i], p_value, mode)
        return pass_fail_arrays
    
    
    @staticmethod
    def single_BMRT_test_running(arrays):
        """
        This function runs the block BMRT test on all arrays in a dataset. Its existence as a separate function is slightly for legacy reasons.
        """
        no_of_arrays = len(arrays)
        p_value_arrays = np.empty(no_of_arrays, dtype=object)
        for i in range(no_of_arrays):
            p_value_arrays[i] = string_calls.run_test_on_string(Matrix.binary_matrix_rank_test, Data_formatting.array_to_string(arrays[i]))[0]
        return p_value_arrays
    
    @staticmethod
    def get_q_values(array):
        """
        Parameter: an array of the 0-1 output values for a device, in the appropriate order
        Returns: an array of 3 Q-values for the device outputs, in order: Frequency,DFT, Autocorrelation
        """
        flat_array = array.flatten()
        string_format = Data_formatting.array_to_string(flat_array)
        frequency_score = FrequencyTest_Q.monobit_test(string_format)
        spectral_score = SpectralTest_Q.spectral_test(string_format)
        runs_score = RunTest_Q.run_test(string_format)
        output_list = []
        output_list.append(frequency_score)
        output_list.append(spectral_score)
        output_list.append(runs_score)
        output_array = np.array(output_list)
        return output_array
        
    @staticmethod
    def q_values_serializer(arrays):
        """
        Parameter: an array of arrays, each containing the scores for a device
        Returns: an array of q-values for each array
        """
        no_of_arrays = len(arrays)
        q_values = np.empty((no_of_arrays, 3), dtype = object)
        for i in range(no_of_arrays):
            values = Randomness_Testing.get_q_values(arrays[i])
            for j in range(3):
                q_values[i][j] = values[j]
        return q_values