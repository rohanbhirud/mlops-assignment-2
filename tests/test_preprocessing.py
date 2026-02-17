from preprocess_dataset import split_counts

def test_split_counts_exact():
    n = 100
    train, val, test = split_counts(n, 0.8, 0.1, 0.1)
    assert train == 80
    assert val == 10
    assert test == 10
    assert train + val + test == n

def test_split_counts_rounding():
    n = 10
    # 0.8 * 10 = 8
    # 0.1 * 10 = 1
    # Test gets remainder: 10 - 8 - 1 = 1
    train, val, test = split_counts(n, 0.8, 0.1, 0.1)
    assert train == 8
    assert val == 1
    assert test == 1
