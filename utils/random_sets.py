import numpy as np


def generate_k_numbers_with_total_sum_m(k, m):
    if k < m:
        raise Exception(f"{k} should be bigger than {m}")
    elif k == m:
        return np.ones(k)

    numbers = np.random.uniform(0, 1, k)
    numbers[numbers >= 0.5] = 1
    attempts = 0
    while numbers.sum() <= m:
        numbers = np.random.uniform(0, 1, k)
        numbers[numbers >= 0.5] = 1
        attempts += 1
        if attempts == 100:
            numbers = np.ones(k)
    return numbers
