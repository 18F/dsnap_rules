import pytest

from dsnap_rules.dgi_calculator import DisasterGrossIncomeCalculator


def test_non_ascending_limits():
    with pytest.raises(ValueError):
        DisasterGrossIncomeCalculator([
                (40, 4),
                (20, 6),
                (30, 8)
            ],
            8, 6)


def test_non_ascending_allotments():
    with pytest.raises(ValueError):
        DisasterGrossIncomeCalculator([
                (10, 4),
                (20, 3),
                (30, 8)
            ],
            8, 6)


def test_limit_calculations():
    calculator = DisasterGrossIncomeCalculator([
            (10, 4),
            (20, 6),
            (30, 8),
        ],
        8, 6)
    assert calculator.get_limit(1) == 10
    assert calculator.get_limit(2) == 20
    assert calculator.get_limit(3) == 30
    assert calculator.get_limit(5) == 30 + 2 * 8


def test_allotment_calculations():
    calculator = DisasterGrossIncomeCalculator([
            (10, 4),
            (20, 6),
            (30, 8),
        ],
        8, 6)
    assert calculator.get_allotment(1) == 4
    assert calculator.get_allotment(2) == 6
    assert calculator.get_allotment(3) == 8
    assert calculator.get_allotment(5) == 8 + 2 * 6
