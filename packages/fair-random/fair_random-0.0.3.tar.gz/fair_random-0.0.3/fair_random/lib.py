"""lib"""
import hashlib
import random


def get_hash(val: str) -> str:
    """get string hash"""
    return hashlib.sha256(val.encode()).hexdigest()


def get_random_seed() -> str:
    """get server seed"""
    server_seed = random.random()
    return get_hash(f"{server_seed}")
