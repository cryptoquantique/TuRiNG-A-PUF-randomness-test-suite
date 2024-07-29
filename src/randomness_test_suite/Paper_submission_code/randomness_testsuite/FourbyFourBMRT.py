# -*- coding: utf-8 -*-

from .BinaryMatrix import BinaryMatrix as bm
from math import exp as exp
from math import floor as floor
from numpy import zeros as zeros

class Matrix:

    @staticmethod
    def binary_matrix_rank_test(binary_data:str, verbose=False, rows_in_matrix = 4, columns_in_matrix = 4):
        """
        Note: the default parameters of pi assume that we're working with 4x4 matrices. If number of rows/columns are changed, these must be recomputed
        """
        shape = (rows_in_matrix, columns_in_matrix)
        length_of_binary_data = len(binary_data)
        if length_of_binary_data < 704:
            print("Too few blocks, test may be inaccurate")
        block_size = int(rows_in_matrix * columns_in_matrix)
        number_of_block = floor(length_of_binary_data / block_size)
        block_start = 0
        block_end = block_size

        if number_of_block > 0:
            max_ranks = [0, 0, 0]

            for im in range(number_of_block):
                block_data = binary_data[block_start:block_end]
                block = zeros(len(block_data))

                for count in range(len(block_data)):
                    if block_data[count] == '1':
                        block[count] = 1.0

                matrix = block.reshape(shape)
                ranker = bm(matrix, rows_in_matrix, columns_in_matrix)
                rank = ranker.compute_rank()

                if rank == rows_in_matrix:
                    max_ranks[0] += 1
                elif rank == (rows_in_matrix - 1):
                    max_ranks[1] += 1
                else:
                    max_ranks[2] += 1

                block_start += block_size
                block_end += block_size

            pi = [0.308, 0.577, 0.115]
            #hidden: how to compute pi for block size =/= 4 x 4.
            # for x in range(1, 50):
            #     pi[0] *= 1 - (1.0 / (2 ** x))
            # pi[1] = 2 * pi[0]
            # pi[2] = 1 - pi[0] - pi[1]

            xObs = 0.0
            for i in range(len(pi)):
                xObs += pow((max_ranks[i] - pi[i] * number_of_block), 2.0) / (pi[i] * number_of_block)

            p_value = exp(-xObs / 2)

            if verbose:
                print('Binary Matrix Rank Test DEBUG BEGIN:')
                print("\tLength of input:\t", length_of_binary_data)
                print("\tSize of Row:\t\t", rows_in_matrix)
                print("\tSize of Column:\t\t", columns_in_matrix)
                print('\tValue of N:\t\t\t', number_of_block)
                print('\tValue of Pi:\t\t', pi)
                print('\tValue of xObs:\t\t', xObs)
                print('\tP-Value:\t\t\t', p_value)
                print('DEBUG END.')

            return (p_value, (p_value >= 0.01))
        else:
            return (-1.0, False)
        
        