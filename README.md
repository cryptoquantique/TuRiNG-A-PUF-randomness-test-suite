# Randomness Test Suite

This repository contains code implementing the Crypto Quantique Randomness Test Suite for 
Physically Unclonable Functions (PUF) of [link? paper name?].
The tests defined are modifications of existing test suites for RNGs (e.g. NIST 800-22) that 
better suit the output and architecture of a PUF. These improvements address the key differences 
between PUF and RNG output, i.e. the restriction on PUF output lengths vs RNG, and the possible 
spatial effects caused by a PUF array.


## To install
pip install git+ssh://git@github.com:cryptoquantique/puf-randomness-test.git --upgrade


Please see the README here for details of how to run the tests.

