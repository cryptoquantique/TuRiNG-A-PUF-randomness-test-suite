# -*- coding: utf-8 -*-
from math import fabs as fabs
from math import floor as floor
from math import sqrt as sqrt
from scipy.special import erfc as erfc
from scipy.special import gammaincc as gammaincc

import numpy as np

class FHD:
    
    @staticmethod
    def inter_array_FHD(array_1, array_2):
        """
        Parameters: array_1, array_2. Two binary arrays of matching length representing strings to have FHD compared.
        Returns: the Fractional (normalized) hamming distance between array_1 and array_2
        Notes: the function will flatten the arrays, so the format shouldn't matter - they can be input as m x n or mn x 1, for example
        """
        #flatten the arrays so that they have the same format
        flat_array_1 = array_1.flatten()
        flat_array_2 = array_2.flatten()
        
        #compute length of input data, needed for normalizing. check both arrays have same length.
        input_length = len(flat_array_1)
        if len(flat_array_2) != input_length:
            print("Length Mistmatch")
            return "Test Failed"
        
        #XOR the strings to get number of mismatched bits
        difference_array = np.bitwise_xor(flat_array_1, flat_array_2)
        
        #compute the HD and then the FHD
        hamming_distance = np.sum(difference_array)
        fractional_hd = hamming_distance/input_length
        
        #return FHD
        return fractional_hd
    
    def inter_array_FHD_test(devices, tested_index = 0):
        """
        Parameters
        ----------
        devices : Array
            Array of read values for eachd evice.
        tested_index : Integer, optional
            DESCRIPTION. The index of the device to be tested. Default is the first device in devices.

        Returns
        -------
        p-value for the inter array FHD test for the indexed device 

        """
        no_of_devices = len(devices)
        device_length = len(devices[0].flatten())
        #makes a list of FHD scores for tested device against other devices
        FHD_scores = []
        for i in range(no_of_devices):
            if i != tested_index:
                FHD_scores.append(FHD.inter_array_FHD(devices[tested_index], devices[i]))
        #compute chi^2 statistic:
        chi_squared_sum = 0
        for FHD_score in FHD_scores:
            square_value = (FHD_score - 0.5)**2
            chi_squared_sum += square_value
        chi_squared_value = (4*device_length*chi_squared_sum)
        #get p value using the incomplete gamma function
        p_value = gammaincc((no_of_devices - 1)/2, chi_squared_value/2)
        return p_value
        
    
    @staticmethod
    def FHD_values_serializer(devices):
        """
        Parameters
        ----------
        devices : Array
            Array of read values for each device.
        Returns
        -------
        array of FHD scores for the devices under test. 
        """
        no_of_arrays = len(devices)
        FHD_value_arrays = np.empty(no_of_arrays, dtype=object)
        for i in range(no_of_arrays):
            FHD_value_arrays[i] = FHD.inter_array_FHD_test(devices, tested_index = i)
        return FHD_value_arrays
                