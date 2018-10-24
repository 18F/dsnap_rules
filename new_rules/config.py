from collections import namedtuple


Config = namedtuple('Config', [
    'worked_in_disaster_area_is_dnsap_eligible'
])


def get_config():
    return Config(worked_in_disaster_area_is_dnsap_eligible=True)
