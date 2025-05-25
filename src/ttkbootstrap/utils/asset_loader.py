from PIL import Image
from PIL.Image import Resampling
from importlib.resources import files
from typing import Optional
import io

def load_asset_image(name: str, size: Optional[tuple[int, int]] = None) -> Image.Image:
    """
    Load an image asset using importlib.resources and return it as an RGBA Pillow Image.

    Args:
        package (str): The package path containing the asset (e.g. 'myapp.assets').
        name (str): The name of the image file (e.g. 'icon.png').
        size (tuple[int, int], optional): Desired size (width, height) to resize the image.

    Returns:
        Image.Image: A Pillow image in RGBA mode.

    Raises:
        FileNotFoundError: If the asset file doesn't exist.
        ValueError: If the file cannot be opened as an image.
    """
    package = 'ttkbootstrap.assets.images'
    try:
        asset_path = files(package).joinpath(name)
        with asset_path.open("rb") as f:
            img = Image.open(io.BytesIO(f.read())).convert("RGBA")
            if size:
                img = img.resize(size, Resampling.LANCZOS)
            return img
    except FileNotFoundError:
        raise FileNotFoundError(f"Asset '{name}' not found in package '{package}'")
    except Exception as e:
        raise ValueError(f"Error loading asset '{name}': {e}")
