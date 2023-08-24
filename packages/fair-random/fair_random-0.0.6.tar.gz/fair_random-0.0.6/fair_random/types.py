"""types"""
from typing import Any
import binascii
import hashlib
import dataclasses
import abc
from .lib import get_hash


@dataclasses.dataclass
class Seed:
    """random seed"""

    hash: str

    @property
    def server_prove(self) -> str:
        """server prove"""
        return get_hash(self.hash)

    @property
    def byte_hash(self) -> bytes:
        """server prove"""
        return self.hash.encode()


class RandomGenerator(abc.ABC):
    """Generates random object"""

    @classmethod
    @abc.abstractmethod
    def get_value(cls, seed: Seed) -> Any:
        """Returns a random"""
        return NotImplemented

    @staticmethod
    def get_int(seed: Seed, gen_from: int, gen_to: int) -> int:
        """Returns a random integer"""
        return (
            int(binascii.hexlify(hashlib.md5(seed.byte_hash).digest()), 16)
            % (gen_to - gen_from + 1)
        ) + gen_from

    @classmethod
    def shuffle(cls, seed: Seed, original: list):
        """Shuffle list of elements"""
        new_list = []
        original_len = len(original)
        for _ in range(original_len):
            original_len -= 1
            new_list.append(original.pop(cls.get_int(seed, 0, original_len)))
        return new_list
