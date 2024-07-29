# -*- coding: utf-8 -*-
import random
import math
import numpy as np

from .ApproximateEntropy import *
from .CumulativeSum import *
from .FrequencyTest import *
from .FourbyFourBMRT import *
from .RunTest import *
from .Serial import *
from .Spectral import *
from .TemplateMatching_4bit import *
from .RunTest_Q import *
from .Spectral_Q import *
from .FrequencyTest_Q import *



row_order_test_pairs_list = [FrequencyTest.monobit_test, ApproximateEntropy.approximate_entropy_test, CumulativeSums.cumulative_sums_test, FrequencyTest.block_frequency,
                         RunTest.run_test, RunTest.longest_one_block_test, SpectralTest.spectral_test, TemplateMatching.four_bit_overlap, Matrix.binary_matrix_rank_test]

col_order_test_pairs_list = [ApproximateEntropy.approximate_entropy_test, CumulativeSums.cumulative_sums_test, FrequencyTest.block_frequency,
                         RunTest.run_test, RunTest.longest_one_block_test, SpectralTest.spectral_test, TemplateMatching.four_bit_overlap, Matrix.binary_matrix_rank_test]

block_order_test_pairs_list = [FrequencyTest.block_frequency, CumulativeSums.cumulative_sums_test]

"""
below, when things are called "pairs" it refers to the behaviour of the test; some tests from the original repository we use return
output in the format (p_value, boolean), whereas others return something more complex. the code handles these tests differently.
"""
#define a test runner that runs a test on a string given the test call and returns the output tuple.
#all tests below just run the appropriate tests on the appropriate set and output a list of p_values.
class string_calls:
    
    #define a function that takes as input a function call and a string and outputs the function run on that string.
    @staticmethod
    def run_test_on_string(test_call, string):
        return test_call(string)
    
    @staticmethod
    def row_short_string_pair_test_runner(string):
        output_p_values = []
        for test in row_order_test_pairs_list:
            test_tuple = string_calls.run_test_on_string(test, string)
            test_p_value = test_tuple[0]
            output_p_values.append(test_p_value)
        return output_p_values
    
    @staticmethod    
    def col_short_string_pair_test_runner(string):
        output_p_values = []
        for test in col_order_test_pairs_list:
            test_tuple = string_calls.run_test_on_string(test, string)
            test_p_value = test_tuple[0]
            output_p_values.append(test_p_value)
        return output_p_values
    
    @staticmethod    
    def block_short_string_pair_test_runner(string):
        output_p_values = []
        for test in block_order_test_pairs_list:
            test_tuple = string_calls.run_test_on_string(test, string)
            test_p_value = test_tuple[0]
            output_p_values.append(test_p_value)
        return output_p_values

    @staticmethod
    #same for serial test
    def serial_test_runner(string):
        test_p_values = []
        test_outputs = Serial.serial_test(string)
        for tuples in test_outputs:
            test_p_values.append(tuples[0])
        return test_p_values
 
    @staticmethod
    def row_test_runner(string):
        test_p_values = []
        pairs = string_calls.row_short_string_pair_test_runner(string)
        for pair in pairs:
            test_p_values.append(pair)
        serial = string_calls.serial_test_runner(string)
        for value in serial:
            test_p_values.append(value)
        return test_p_values

    @staticmethod
    def col_test_runner(string):
        test_p_values = []
        pairs = string_calls.col_short_string_pair_test_runner(string)
        for pair in pairs:
            test_p_values.append(pair)
        #random_excursions = random_excursions_runner(string)
        #for value in random_excursions:
        #    test_p_values.append(value)
        serial = string_calls.serial_test_runner(string)
        for value in serial:
            test_p_values.append(value)
        return test_p_values

    @staticmethod
    def block_test_runner(string):
        test_p_values = []
        pairs = string_calls.block_short_string_pair_test_runner(string)
        for pair in pairs:
            test_p_values.append(pair)
        return test_p_values
