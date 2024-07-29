from math import floor as floor
from numpy import array as array
from numpy import exp as exp
from numpy import zeros as zeros
import numpy as np
from scipy.special import gammaincc as gammaincc
from scipy.special import hyp1f1 as hyp1f1


class TemplateMatching:
    #uses a default template. may want to reset or randomize this as appropriate to check for other templates
    @staticmethod
    def four_bit_overlap(binary_data:str, verbose=False, template_pattern='0000'):
        #I think we can use one test for all patterns
        #BUT
        #need an argument telling the function how overlapping the pattern is, so that you can get the correct buckets
        if template_pattern in ['0000', '1111']:
            overlap = 3
        if template_pattern in ['0101', '1010']:
            overlap = 2
        if template_pattern in ['0010', '0100', '0110', '1001', '1011', '1101']:
            overlap = 1
        if template_pattern in ['0001', '0011', '0111', '1000', '1100', '1110']:
            overlap = 0
        """
        note that this test is our adaptation of the NIST template tests, and can be understood by reading the paper. In particular, the probabilities
        given in the expected_values lists are computed directly, and don't use asymptotic arguments or any numbers from the NIST documentation.
        """

        length_of_binary = len(binary_data)
        pattern_size = len(template_pattern)
        block_size = 64
        block = floor(length_of_binary / 64)
        pattern_counts = zeros(block)
        #this should be coded s.t. the last value is the >= x value is a single bucket
        if overlap == 0:
            buckets = [[0,1,2], [3], [4], [i for i in range(5,block_size)]]
            num_buckets = len(buckets)
            expected_values = [0.188312, 0.23798, 0.26006, 0.313648]
         
        if overlap == 1:
            buckets = [[0,1,2], [3], [4], [i for i in range(5,block_size)]]
            num_buckets = len(buckets)
            expected_values = [0.237221, 0.215906, 0.216319, 0.330554]
            
        if overlap == 2:
            buckets = [[0,1,2], [3], [4], [i for i in range(5,block_size)]]
            num_buckets = len(buckets)
            expected_values = [0.275492, 0.199207, 0.18832, 0.336981]
           
        if overlap == 3:
            buckets = [[0,1,2], [3,4], [5,6], [i for i in range(7,block_size)]]
            num_buckets = len(buckets)
            expected_values = [0.388599, 0.26515, 0.176063, 0.170188]
            
        # For each block in the data
        for count in range(block):
            block_start = count * block_size
            block_end = block_start + block_size
            #if you wanted to re-add wraparounds: + binary_data[block_start:(block_start + 3)]
            block_data = binary_data[block_start:block_end] 
            # Count the number of pattern hits
            inner_count = 0
            while inner_count < block_size-pattern_size:
                sub_block = block_data[inner_count:inner_count+pattern_size]
                if sub_block == template_pattern:
                    pattern_counts[count] += 1
                    inner_count += 1
                else:
                    inner_count += 1
        
        #instantiate a frequency counter, for each bucket, add to that frequency counter all scores in that bucket
        frequency_count = zeros(num_buckets)
        for i in range(num_buckets):
            for values in buckets[i]:
                frequency_count[i] += np.count_nonzero(pattern_counts == values)
            
        
            # Calculate the theoretical mean and variance
            # Mean - µ = (M-m+1)/2m
            #mean = (block_size - pattern_size + 1) / pow(2, pattern_size)
            # Variance - σ2 = M((1/pow(2,m)) - ((2m -1)/pow(2, 2m)))
            #variance = block_size * ((1 / pow(2, pattern_size)) - (((2 * pattern_size) - 1) / (pow(2, pattern_size * 2))))

        # Calculate the xObs Squared statistic for these pattern matches
        
        xObs = 0

        for i in range(num_buckets):
            bucket_score = frequency_count[i]
            expected_score = expected_values[i] * block
            xObs += pow((bucket_score - expected_score), 2.0) / expected_score

        # Calculate and return the p value statistic
        p_value = gammaincc(((num_buckets - 1) / 2), (xObs / 2))

        # if verbose:
        #     print('Non-Overlapping Template Test DEBUG BEGIN:')
        #     print("\tLength of input:\t\t", length_of_binary)
        #     print('\tValue of Mean (µ):\t\t', mean)
        #     print('\tValue of Variance(σ):\t', variance)
        #     print('\tValue of W:\t\t\t\t', pattern_counts)
        #     print('\tValue of xObs:\t\t\t', xObs)
        #     print('\tP-Value:\t\t\t\t', p_value)
        #     print('DEBUG END.')

        return (p_value, (p_value >= 0.01))

