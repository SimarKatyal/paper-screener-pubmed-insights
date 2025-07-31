from paper_screener.core import is_non_academic

def test_affiliation_filter():
    assert is_non_academic("Pfizer Inc.")
    assert not is_non_academic("Harvard University")