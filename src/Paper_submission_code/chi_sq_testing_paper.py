# -*- coding: utf-8 -*-

import numpy as np
import scipy.special as sc

def buckets(p_values):
    buckets = np.histogram(p_values, bins = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1])
    return buckets[0]
    
def x_sq_p_values(bin_counts):
    sample_size = sum(bin_counts)
    expected_bucket_size = sample_size/10
    chi_sq_sum = 0
    for bins in bin_counts:
        contribution = ((bins - expected_bucket_size)**2)/(expected_bucket_size)
        chi_sq_sum += contribution
    return chi_sq_sum

def test_score(p_values):
    bucket_values = buckets(p_values)
    chi_sq = x_sq_p_values(bucket_values)
    gammainc_value = sc.gammaincc(9/2, chi_sq/2)
    return gammainc_value

def many_test_scores(p_values_list):
    scores = []
    for tests in p_values_list:
        scores.append(test_score(tests))
    return scores
