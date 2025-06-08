import pytest
from pyta.calculations.smoothings import calculate_sma as py_sma, calculate_ema as py_ema
from pyta.smoothing_cpp import calculate_sma as cpp_sma, calculate_ema as cpp_ema

BACKENDS = [
    ("Python", py_sma, py_ema),
    ("C++", cpp_sma, cpp_ema),
]

@pytest.mark.parametrize("backend,sma,ema", BACKENDS)
def test_sma_valid(backend, sma, ema):
    """SMA với đầu vào hợp lệ"""
    assert sma([1, 2, 3, 4, 5], 3) == 2.0

@pytest.mark.parametrize("backend,sma,ema", BACKENDS)
def test_sma_exact(backend, sma, ema):
    """SMA với đúng số lượng phần tử"""
    assert sma([10, 20, 30], 3) == 20.0

@pytest.mark.parametrize("backend,sma,ema", BACKENDS)
def test_sma_insufficient(backend, sma, ema):
    """SMA với dữ liệu không đủ"""
    assert sma([1, 2], 3) == None

@pytest.mark.parametrize("backend,sma,ema", BACKENDS)
def test_ema_with_padding(backend, sma, ema):
    """EMA có pad=True"""
    prices = [10, 11, 12, 13, 14]
    period = 3
    result = ema(prices, period, pad=True)
    assert len(result) == len(prices)

@pytest.mark.parametrize("backend,sma,ema", BACKENDS)
def test_ema_without_padding(backend, sma, ema):
    """EMA không pad"""
    prices = [10, 11, 12, 13, 14]
    period = 3
    result = ema(prices, period, pad=False)
    assert len(result) == len(prices) - period + 1

@pytest.mark.parametrize("backend,sma,ema", BACKENDS)
def test_ema_insufficient_data(backend, sma, ema):
    """EMA với dữ liệu không đủ"""
    assert ema([1, 2], 3) == []

@pytest.mark.parametrize("backend,sma,ema", BACKENDS)
def test_ema_computation_accuracy(backend, sma, ema):
    """Kiểm tra công thức EMA chuẩn"""
    prices = [10, 20, 30, 40, 50]
    period = 3
    alpha = 2 / (period + 1)
    sma_val = round((10 + 20 + 30) / 3, 3)
    ema1 = round(alpha * 40 + (1 - alpha) * sma_val, 3)
    ema2 = round(alpha * 50 + (1 - alpha) * ema1, 3)

    result = ema(prices, period, pad=False)
    assert round(result[0], 3) == sma_val
    assert round(result[1], 3) == ema1
    assert round(result[2], 3) == ema2

@pytest.mark.parametrize("backend,sma,ema", BACKENDS)
def test_ema_constant_values(backend, sma, ema):
    """EMA với giá trị không đổi"""
    prices = [100.0] * 10
    result = ema(prices, 5, pad=False)
    for value in result:
        assert round(value, 3) == 100.0

@pytest.mark.parametrize("backend,sma,ema", BACKENDS)
def test_ema_negative_values(backend, sma, ema):
    """EMA với giá trị âm"""
    prices = [-1, -2, -3, -4, -5]
    result = ema(prices, 2, pad=False)
    assert all(isinstance(x, float) for x in result)
