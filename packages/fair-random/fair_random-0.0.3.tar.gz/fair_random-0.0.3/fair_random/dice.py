"""dice"""
from .types import RandomGenerator, Seed


class Dice(RandomGenerator):
    """dice"""

    @classmethod
    def get_value(cls, seed: Seed) -> int:
        return cls.get_int(seed, 1, 6)
