"""initialize"""
from typing import List, Dict
from .types import Seed
from .lib import get_random_seed, get_hash
from .majiang import Majiang
from .dice import Dice


def get_server_seed() -> Seed:
    """get server seed"""
    server_seed = Seed(hash=get_random_seed())
    return server_seed


def get_client_seed(client_input: str) -> Seed:
    """get client seed"""
    return Seed(hash=get_hash(client_input))


def get_final_seed(server_seed: Seed, client_seeds: List[Seed]) -> Seed:
    """get client seed"""
    client_seeds = sorted(client_seeds, key=lambda seed: seed.hash)
    return Seed(
        hash=get_hash(
            f"{server_seed.hash}_{get_hash('_'.join(map(lambda seed: seed.hash, client_seeds)))}"
        )
    )
