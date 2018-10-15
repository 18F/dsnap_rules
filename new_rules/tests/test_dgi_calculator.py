import pytest

from new_rules.dsnap.dgi_calculator import DisasterGrossIncomeCalculator


def test_constructor():
    with pytest.raises(ValueError):
        DisasterGrossIncomeCalculator([
                40,
                20,
                30,
            ],
            8)


def test_limit_calculations():
    calculator = DisasterGrossIncomeCalculator([
            10,
            20,
            30,
        ],
        8)
    assert calculator.get_limit(1) == 10
    assert calculator.get_limit(2) == 20
    assert calculator.get_limit(3) == 30
    assert calculator.get_limit(5) == 30 + 2 * 8
