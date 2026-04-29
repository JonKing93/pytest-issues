"""
Modules that check tests issue expected exceptions and warnings
----------
Each module includes a function named check_<issue>, which is the lowest level
validator. This function simply validates that function call issues an expected
exception or warning. Each module also includes a function named
check_test_<issue>. This is a higher level function aware of pytest testing
environments. As such, this function is responsible for formatting messages
with test kwargs, and for optionally requiring message checking.
----------
Modules:
    raises      - Functions to check a test raises an expected exception
    warns       - Functions to check a test issues an expected warning
"""
