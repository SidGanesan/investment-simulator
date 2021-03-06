from investment_simulator.tax import income_tax, nz_tax_brackets


def test_tax_0_calculation():
    result = income_tax(nz_tax_brackets())(income=0)
    assert result == 0  # income - tax


def test_tax_45000_calculation():
    result = income_tax(nz_tax_brackets())(income=45_000)
    assert result == 6895.0  # income - tax


def test_tax_100000_calculation():
    result = income_tax(nz_tax_brackets())(income=100_000)
    assert result == 23_920  # income - tax
