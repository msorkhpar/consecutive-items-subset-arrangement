import os
from fractions import Fraction

import numpy as np


def generate_k_numbers_with_total_sum_m(k, m):
    if k < m:
        raise Exception(f"{k} should be bigger than {m}")
    elif k == m:
        return np.ones(k)

    choices = [float(Fraction(num)) if '/' in num else float(num) for num in os.getenv('VALUE_CHOICES', '').split(',')
               if
               num]
    if choices:
        numbers = np.random.choice(choices, size=k)
    else:
        numbers = np.random.uniform(0, 1, k)
        numbers[numbers >= 1/3] = 1

    attempts = 0
    while numbers.sum() <= m:
        if choices:
            numbers = np.random.choice(choices, size=k)
        else:
            numbers = np.random.uniform(0, 1, k)
            numbers[numbers >= 1/3] = 1

        attempts += 1
        if attempts == 500:
            numbers = np.ones(k)
    return numbers
