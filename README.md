# Randomness Test Suite

This repository contains code implementing the Crypto Quantique [Randomness Test Suite for Physically Unclonable Functions](A_Randomness_Test_Suite_for_Physical_Unclonable_Functions 2.pdf).
The tests defined are modifications of existing test suites for RNGs (e.g. NIST 800-22) that 
better suit the output and architecture of a PUF. These improvements address the key differences 
between PUF and RNG output, i.e. the restriction on PUF output lengths vs RNG, and the possible 
spatial effects caused by a PUF array.


## To install and run the tests

Please see the documentation [here](src/README.md)


## Acknowledgement

The implementations of the tests found here are based on those found here https://github.com/stevenang/randomness_testsuite , with some minor modifications.
