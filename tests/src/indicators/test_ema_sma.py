from pyta.calculations.smoothings import calculate_ema, calculate_sma

abc: list[float] = [10, 20, 30, 50, 60, 90, 100, 500, 600]


print(calculate_sma(abc, 5))
print(calculate_ema(abc, 5))