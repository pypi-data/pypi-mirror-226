# primenumbersrangepackage

Description.

The package primenumbersrangepackage is used to:

    - Set a minimum number
    - Set a maximum number
    - Find prime numbers in that range

# Installation

Use the package manager [pip](https://pypi.org/project/primenumbersrangepackage/0.0.1/) to install primenumbers

"""bash

pip install primenumbersrangepackage

"""

# Usage

from primenumbersrangepackage import minimum, maximum, find_prime_numbers

minimum_number = minimum()

maximum_number = maximum(minimum_number)

find_prime_numbers(minimum_number, maximum_number)

# Author
Lucas Venicius Alves Santos