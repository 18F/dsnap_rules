def get_dgi_calculator(state_or_territory, region_category=None):
    """
    Get the appropriate Disaster Gross Income Calculator for the state
    or territory.
    """
    if state_or_territory == "AK":
        if region_category == "URBAN":
            return AK_URBAN_DGICalculator
        elif region_category == "RURAL1":
            return AK_RURAL1_DGICalculator
        elif region_category == "RURAL2":
            return AK_RURAL2_DGICalculator
        else:
            raise Exception("Calculator not found")
    elif state_or_territory == "HI":
        return HI_DGICalculator
    elif state_or_territory == "GU":
        return GU_DGICalculator
    elif state_or_territory == "VI":
        return VI_DGICalculator
    else:
        return DEFAULT_DGICalculator


class DisasterGrossIncomeCalculator:
    def __init__(self, limits, overflow_rate):
        self.limits = limits
        self.overflow_rate = overflow_rate

    def get_limit(self, size_of_household):
        if size_of_household <= len(self.limits):
            return self.limits[size_of_household - 1]
        else:
            return self.limits[-1] + (
                (size_of_household - len(self.limits)) * self.overflow_rate)


DEFAULT_DGICalculator = DisasterGrossIncomeCalculator([
        1728,
        2088,
        2448,
        2818,
        3208,
        3598,
        3958,
        4318,
    ],
    360)

AK_URBAN_DGICalculator = DisasterGrossIncomeCalculator([
        2427,
        2877,
        3327,
        3777,
        4227,
        4688,
        5138,
        5588,
    ],
    450)

AK_RURAL1_DGICalculator = DisasterGrossIncomeCalculator([
        2427,
        2877,
        3327,
        3777,
        4227,
        4688,
        5138,
        5588,
    ],
    450)

AK_RURAL2_DGICalculator = DisasterGrossIncomeCalculator([
        2427,
        2877,
        3327,
        3777,
        4227,
        4688,
        5138,
        5588,
    ],
    450)


HI_DGICalculator = DisasterGrossIncomeCalculator([
        2139,
        2553,
        2967,
        3381,
        3797,
        4247,
        4661,
        5075,
    ],
    415)

GU_DGICalculator = DisasterGrossIncomeCalculator([
        1990,
        2350,
        2710,
        3087,
        3507,
        3926,
        4286,
        4646,
    ],
    360)

VI_DGICalculator = DisasterGrossIncomeCalculator([
        1592,
        1952,
        2312,
        2701,
        3091,
        3481,
        3841,
        4201,
    ],
    360)
