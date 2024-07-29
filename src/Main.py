# -*- coding: utf-8 -*-
"""
This file takes as input an array of (PUF x row values x column values) data and writes a text file summarising the number of passes of the 
appropriate tests for a pre-chosen p-value. The array must be saved in the same folder as an np array. For more detailed results, the file
"Randomness_Tests" has a method to obtain the p-values directly.
"""
import numpy as np
from Paper_submission_code.Inter_Array_FHD import *
from Paper_submission_code.Randomness_Tests import *
from Paper_submission_code.Data_Formatting import *
from Paper_submission_code.chi_sq_testing_paper import *

#%%User Input Choices
#data input file, results output file, 
data_file_name = "Paper_submission_code/example_4096_data"
results_file_name = "Paper_submission_code/4096_example_output.txt"
#block size choices b1 and b2; relatively safe to leave these as 4.
b1 = 4
b2 = 4

#%%hardcode chosen p-value parameters
p_value = 0.01

#%%Put the data you want here
file = open(data_file_name, "rb")
data = np.load(file, allow_pickle = True)

#extract some helpful parameters
number_of_devices = len(data)
row_length = len(data[0])
if len(np.shape(data)) == 3:
    col_length = len(data[0].T)
#set block size, if appropriate
    block_row_size = b1
    block_col_size = b2

#%%
#stage1: the data is a big array. run the functions that put it in the right input format
#for various definitions of "right"
row_order = Data_formatting.row_col_serializer(data)[0]
if len(np.shape(data)) == 3:
    col_order = Data_formatting.row_col_serializer(data)[1]
    block_order = Data_formatting.blocks_serializer(data, block_row_size, block_col_size, row_length, col_length)
    #if block size is left as 4, this last order is the same as the previous one.
    blocks_for_BMRT = Data_formatting.blocks_serializer(data, 4, 4, row_length, col_length)
print("Progress Update: Data organized")

#%%
#stage 2: run the tests, output results. Occasionally prints a progress update, as the functions can be slow on large datasets and are not optimized.
FHD_scores = FHD.FHD_values_serializer(data)

print("Progress Update: FHD test computed")
#%%

row_p_values = Randomness_Testing.p_values_serializer(row_order, 0)
print("Progress Update: Row Randomness Tests computed")
if len(np.shape(data)) == 3:
    col_p_values = Randomness_Testing.p_values_serializer(col_order, 1)
    print("Progress Update: Column Randomness Tests computed")
    block_p_values = Randomness_Testing.p_values_serializer(block_order, 2)
#%%
if len(np.shape(data)) == 3:
    block_BMRT_performance = Randomness_Testing.single_BMRT_test_running(blocks_for_BMRT)
    print("Progress Update: Block Randomness Tests computed")
#%%Collate pass-fail scores
FHD_pass_fails = (FHD_scores > p_value).sum()

row_pass_fails = Data_formatting.p_values_to_pass_fail(row_p_values.T, p_value)

if len(np.shape(data)) == 3:
    col_pass_fails = Data_formatting.p_values_to_pass_fail(col_p_values.T, p_value)

    block_pass_fails = Data_formatting.p_values_to_pass_fail(block_p_values.T, p_value)

    block_BMRT_score = (block_BMRT_performance > p_value).sum()

#%%compute chi-squared scores
row_chi_sq_values = many_test_scores(row_p_values.T)
if len(np.shape(data)) == 3:
    col_chi_sq_values = many_test_scores(col_p_values.T)
    block_chi_sq_values = many_test_scores(block_p_values.T)
    block_BMRT_chi_sq = test_score(block_BMRT_performance)
#%% q values for relevant tests
q_values_row = Randomness_Testing.q_values_serializer(row_order)
if len(np.shape(data)) == 3:
    q_values_col = Randomness_Testing.q_values_serializer(col_order)
q_chi_sq_values_row = many_test_scores(q_values_row.T)
if len(np.shape(data)) == 3:
    q_chi_sq_values_col = many_test_scores(q_values_col.T)
#%%

#stage 3: compile the results in an output .txt

results_file = open(results_file_name, "a")

results_file.write("There were %s devices in the dataset \n" % number_of_devices)
results_file.write("The p-value for tests was %s" % p_value)
results_file.write("\n")
#start adding things one by one. Start with Uniqueness; FHD
results_file.write("FHD Test: %s devices out of %s passed \n" % (FHD_pass_fails, number_of_devices))
results_file.write("\n")

#Randomness tests ordered correctly:
results_file.write("Randomness test pass counts (row order) at p-value %s: \n" % p_value)
results_file.write("Monobit Test: %s of %s, chi = %s \n" % (row_pass_fails[0], number_of_devices, q_chi_sq_values_row[0]))
results_file.write("Approximate Entropy: %s of %s, chi = %s \n" % (row_pass_fails[1], number_of_devices, row_chi_sq_values[1]))
results_file.write("Cumulative Sums: %s of %s, chi = %s \n" % (row_pass_fails[2], number_of_devices, row_chi_sq_values[2]))
results_file.write("Block Frequency: %s of %s, chi = %s \n" % (row_pass_fails[3], number_of_devices, row_chi_sq_values[3]))
results_file.write("Runs Test: %s of %s, chi = %s \n" % (row_pass_fails[4], number_of_devices, q_chi_sq_values_row[2]))
results_file.write("Longest Run of Ones: %s of %s, chi = %s \n" % (row_pass_fails[5], number_of_devices, row_chi_sq_values[5]))
results_file.write("DFT: %s of %s, chi = %s \n" % (row_pass_fails[6], number_of_devices, q_chi_sq_values_row[1]))
results_file.write("Template Matching (fixed template): %s of %s, chi = %s \n" % (row_pass_fails[7], number_of_devices, row_chi_sq_values[7]))
results_file.write("Binary Matrix Rank Test: %s of %s, chi = %s \n" % (row_pass_fails[8], number_of_devices, row_chi_sq_values[8]))
results_file.write("Serial: %s of %s, chi = %s \n" % (row_pass_fails[9], number_of_devices, row_chi_sq_values[9]))
results_file.write("Serial Variant: %s of %s, chi = %s \n" % (row_pass_fails[10], number_of_devices, row_chi_sq_values[10]))
results_file.write("\n")
#col order
if len(np.shape(data)) == 3:
    results_file.write("Randomness test pass counts (column order) at p-value %s: \n" % p_value)
    results_file.write("Approximate Entropy: %s of %s, chi = %s \n" % (col_pass_fails[0], number_of_devices, col_chi_sq_values[0]))
    results_file.write("Cumulative Sums: %s of %s, chi = %s \n" % (col_pass_fails[1], number_of_devices, col_chi_sq_values[1]))
    results_file.write("Block Frequency: %s of %s, chi = %s \n" % (col_pass_fails[2], number_of_devices, col_chi_sq_values[2]))
    results_file.write("Runs Test: %s of %s, chi = %s \n" % (col_pass_fails[3], number_of_devices, q_chi_sq_values_col[2]))
    results_file.write("Longest Run of Ones: %s of %s, chi = %s \n" % (col_pass_fails[4], number_of_devices, col_chi_sq_values[4]))
    results_file.write("DFT: %s of %s, chi = %s \n" % (col_pass_fails[5], number_of_devices, q_chi_sq_values_col[1]))
    results_file.write("Template Matching (fixed template): %s of %s, chi = %s \n" % (col_pass_fails[6], number_of_devices, col_chi_sq_values[6]))
    results_file.write("Binary Matrix Rank Test: %s of %s, chi = %s \n" % (col_pass_fails[7], number_of_devices, col_chi_sq_values[7]))
    results_file.write("Serial: %s of %s, chi = %s \n" % (col_pass_fails[8], number_of_devices, col_chi_sq_values[8]))
    results_file.write("Serial Variant: %s of %s, chi = %s \n" % (col_pass_fails[9], number_of_devices, col_chi_sq_values[9]))
    results_file.write("\n")
    #block order
    results_file.write("Randomness test pass counts (block order) at p-value %s: \n" % p_value)
    results_file.write("Block Frequency: %s of %s, chi = %s \n" % (block_pass_fails[0], number_of_devices, block_chi_sq_values[0]))
    results_file.write("Cumulative Sums: %s of %s, chi = %s \n" % (block_pass_fails[1], number_of_devices, block_chi_sq_values[1]))
    results_file.write("Binary Matrix Rank Test: %s of %s, chi = %s \n" % (block_BMRT_score, number_of_devices, block_BMRT_chi_sq))
results_file.write("The p-values are written as arrays by Main for more information e.g. for running tests for uniformity")
results_file.close()

print("Results saved to", results_file_name)
