def get_calculator(disaster, region_category=None):
    """
    Get the appropriate Income and Allotment Calculator for the state
    or territory.
    """
    if disaster.uses_DSED:
        return DSED_Calculator

    if disaster.state == "AK":
        if region_category == "URBAN":
            return AK_URBAN_Calculator
        elif region_category == "RURAL1":
            return AK_RURAL1_Calculator
        elif region_category == "RURAL2":
            return AK_RURAL2_Calculator
        else:
            raise Exception("Calculator not found")
    elif disaster.state == "HI":
        return HI_Calculator
    elif disaster.state == "GU":
        return GU_Calculator
    elif disaster.state == "VI":
        return VI_Calculator
    else:
        return DEFAULT_Calculator


class IncomeAndAllotmentCalculator:
    def __init__(self, limits_and_allotments, incremental_limit,
                 incremental_allotment):
        self.limits, self.allotments = zip(*limits_and_allotments)

        if any(x > y for x, y in zip(self.limits, self.limits[1:])):
            raise ValueError("Limits must be in ascending order")
        if any(x > y for x, y in zip(self.allotments, self.allotments[1:])):
            raise ValueError("Allotments must be in ascending order")

        self.incremental_limit = incremental_limit
        self.incremental_allotment = incremental_allotment

    def get_limit(self, size_of_household):
        if size_of_household <= len(self.limits):
            return self.limits[size_of_household - 1]
        else:
            return self.limits[-1] + (
                (size_of_household - len(self.limits))
                * self.incremental_limit)

    def get_allotment(self, size_of_household):
        if size_of_household <= len(self.allotments):
            return self.allotments[size_of_household - 1]
        else:
            return self.allotments[-1] + (
                (size_of_household - len(self.allotments))
                * self.incremental_allotment)


DEFAULT_Calculator = IncomeAndAllotmentCalculator([
        (1728, 192),
        (2088, 353),
        (2448, 505),
        (2818, 642),
        (3208, 762),
        (3598, 914),
        (3958, 1011),
        (4318, 1155),
    ],
    360, 144)

AK_URBAN_Calculator = IncomeAndAllotmentCalculator([
        (2427, 232),
        (2877, 425),
        (3327, 609),
        (3777, 773),
        (4227, 918),
        (4688, 1102),
        (5138, 1218),
        (5588, 1392),
    ],
    450, 174)

AK_RURAL1_Calculator = IncomeAndAllotmentCalculator([
        (2427, 295),
        (2877, 542),
        (3327, 776),
        (3777, 986),
        (4227, 1171),
        (4688, 1405),
        (5138, 1553),
        (5588, 1775),
    ],
    450, 222)

AK_RURAL2_Calculator = IncomeAndAllotmentCalculator([
        (2427, 360),
        (2877, 660),
        (3327, 945),
        (3777, 1200),
        (4227, 1425),
        (4688, 1711),
        (5138, 1891),
        (5588, 2161),
    ],
    450, 270)


HI_Calculator = IncomeAndAllotmentCalculator([
        (2139, 358),
        (2553, 656),
        (2967, 940),
        (3381, 1193),
        (3797, 1417),
        (4247, 1701),
        (4661, 1880),
        (5075, 2148),
    ],
    415, 269)

GU_Calculator = IncomeAndAllotmentCalculator([
        (1990, 283),
        (2350, 520),
        (2710, 745),
        (3087, 946),
        (3507, 1123),
        (3926, 1348),
        (4286, 1490),
        (4646, 1703),
    ],
    360, 213)

VI_Calculator = IncomeAndAllotmentCalculator([
        (1592, 247),
        (1952, 454),
        (2312, 650),
        (2701, 825),
        (3091, 980),
        (3481, 1176),
        (3841, 1300),
        (4201, 1485),
    ],
    360, 186)

DSED_Calculator = IncomeAndAllotmentCalculator([
        (2518, 192),
        (3281, 353),
        (3773, 505),
        (4448, 642),
        (4904, 762),
        (5481, 914),
        (5900, 1011),
        (6319, 1155),
    ],
    419, 144)
