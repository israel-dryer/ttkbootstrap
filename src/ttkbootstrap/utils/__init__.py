from . import style_utils
from . import window_utils
from .asset_loader import load_asset_image


def snake_to_lower(name: str):
    return name.replace('_', '').lower()

def keys_to_lower(d: dict):
    return {snake_to_lower(k): v for k, v in d.items()}
