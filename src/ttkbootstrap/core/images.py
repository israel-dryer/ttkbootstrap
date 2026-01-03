"""Image loading and caching utilities for ttkbootstrap.

This module provides a unified image service for loading, caching, and managing
Tk-compatible PhotoImage objects. It uses Pillow as the backend to support a wide
variety of image formats beyond what Tk natively supports.

The primary interface is the `Image` class, which provides class methods for
loading images from various sources while automatically caching them to avoid
repeated decoding and to prevent garbage collection issues with Tk images.

Examples:
    Basic usage with file paths::

        from ttkbootstrap import Image

        # Load an image from disk (cached automatically)
        photo = Image.open("icons/save.png")
        button = Button(app, image=photo)

    Loading from bytes (e.g., embedded resources)::

        photo = Image.from_bytes(icon_data)

    Creating transparent spacer images::

        spacer = Image.transparent(16, 16)
"""

from __future__ import annotations

import hashlib
import io
from dataclasses import dataclass
from pathlib import Path
from typing import Hashable

from PIL import Image as PILImage
from PIL.ImageTk import PhotoImage as PILPhotoImage


@dataclass(frozen=True)
class ImageCacheInfo:
    """Information about the current state of an image cache.

    Attributes:
        items: The number of images currently stored in the cache.
    """

    items: int


class Image:
    """Platform image service for loading and caching PhotoImage objects.

    This class provides a centralized service for working with images in
    ttkbootstrap applications. It handles:

    - Loading images from files, bytes, or PIL Image objects
    - Automatic caching to avoid repeated decoding
    - Keeping strong references to prevent Tk garbage collection issues
    - Support for many image formats via Pillow (PNG, JPEG, GIF, BMP, etc.)

    All methods are class methods, so no instantiation is required.

    Examples:
        ```python
            # From a file path
            icon = Image.open("path/to/icon.png")

            # From raw bytes
            icon = Image.from_bytes(embedded_data)

            # From a PIL Image object
            pil_img = PILImage.open("photo.jpg").resize((100, 100))
            icon = Image.from_pil(pil_img)

            # Create a transparent spacer
            spacer = Image.transparent(32, 32)
        ```

    Note:
        Images are cached by default using automatically generated keys based
        on the source (file path, content hash, or object id). You can provide
        a custom `key` parameter to control caching behavior.
    """

    _cache: dict[Hashable, PILPhotoImage] = {}

    # =========================================================================
    # Cache Management
    # =========================================================================

    @classmethod
    def get_cached(cls, key: Hashable) -> PILPhotoImage | None:
        """Retrieve a cached PhotoImage by its key.

        Args:
            key: The cache key to look up.

        Returns:
            The cached PhotoImage if found, or None if not in cache.
        """
        return cls._cache.get(key)

    @classmethod
    def set_cached(cls, key: Hashable, img: PILPhotoImage) -> PILPhotoImage:
        """Store a PhotoImage in the cache.

        Args:
            key: The cache key to store the image under.
            img: The PhotoImage to cache.

        Returns:
            The same PhotoImage that was passed in (for chaining).
        """
        cls._cache[key] = img
        return img

    @classmethod
    def clear_cache(cls) -> None:
        """Clear all cached images.

        This removes all images from the cache. Use with caution, as any
        widgets still referencing these images may display incorrectly.
        """
        cls._cache.clear()

    @classmethod
    def cache_info(cls) -> ImageCacheInfo:
        """Get information about the current cache state.

        Returns:
            An ImageCacheInfo object containing cache statistics.

        Examples:
            >>> info = Image.cache_info()
            >>> print(f"Cached images: {info.items}")
        """
        return ImageCacheInfo(items=len(cls._cache))

    # =========================================================================
    # Image Constructors
    # =========================================================================

    @classmethod
    def open(cls, path: str | Path, *, key: Hashable | None = None) -> PILPhotoImage:
        """Load an image from a file path.

        Opens an image file using Pillow and converts it to a Tk-compatible
        PhotoImage. The result is cached to avoid repeated disk reads and
        decoding for the same file.

        Args:
            path: Path to the image file. Supports ~ expansion and relative paths.
            key: Optional custom cache key. If not provided, the absolute file
                path is used as the cache key.

        Returns:
            A Tk-compatible PhotoImage that can be used with widgets.

        Examples:
            >>> photo = Image.open("assets/logo.png")
            >>> label = Label(app, image=photo)

            >>> # With custom cache key for versioning
            >>> photo = Image.open("icon.png", key=("icon", "v2"))
        """
        p = Path(path).expanduser().resolve()
        cache_key = key if key is not None else ("file", str(p))
        cached = cls.get_cached(cache_key)
        if cached is not None:
            return cached

        pil = PILImage.open(p)
        photo = PILPhotoImage(image=pil)
        return cls.set_cached(cache_key, photo)

    @classmethod
    def from_pil(cls, image: PILImage.Image, *, key: Hashable | None = None) -> PILPhotoImage:
        """Convert a PIL Image to a Tk PhotoImage.

        Wraps an existing PIL Image object in a Tk-compatible PhotoImage.
        This is useful when you need to perform image manipulation (resizing,
        filtering, etc.) before displaying the image.

        Args:
            image: A PIL Image object to convert.
            key: Optional custom cache key. If not provided, the object id
                of the PIL Image is used (note: this means the same PIL Image
                object will be cached, but copies won't hit the cache).

        Returns:
            A Tk-compatible PhotoImage that can be used with widgets.

        Examples:
            >>> from PIL import Image as PILImage
            >>> pil_img = PILImage.open("photo.jpg")
            >>> pil_img = pil_img.resize((100, 100))
            >>> photo = Image.from_pil(pil_img)
        """
        cache_key = key if key is not None else ("pil", id(image))
        cached = cls.get_cached(cache_key)
        if cached is not None:
            return cached

        photo = PILPhotoImage(image=image)
        return cls.set_cached(cache_key, photo)

    @classmethod
    def from_bytes(cls, data: bytes, *, key: Hashable | None = None) -> PILPhotoImage:
        """Create a PhotoImage from raw image bytes.

        Decodes image data from bytes using Pillow and converts it to a
        Tk-compatible PhotoImage. This is useful for embedded resources,
        downloaded images, or any other source of raw image data.

        Args:
            data: Raw image bytes in any format supported by Pillow
                (PNG, JPEG, GIF, BMP, etc.).
            key: Optional custom cache key. If not provided, an MD5 hash
                of the bytes is used as the cache key.

        Returns:
            A Tk-compatible PhotoImage that can be used with widgets.

        Examples:
            >>> # Load from embedded resource
            >>> with open("icon.png", "rb") as f:
            ...     icon_data = f.read()
            >>> photo = Image.from_bytes(icon_data)

            >>> # With custom cache key
            >>> photo = Image.from_bytes(data, key="my-icon")
        """
        digest = hashlib.md5(data).hexdigest()
        cache_key = key if key is not None else ("bytes", digest)
        cached = cls.get_cached(cache_key)
        if cached is not None:
            return cached

        pil = PILImage.open(io.BytesIO(data))
        photo = PILPhotoImage(image=pil)
        return cls.set_cached(cache_key, photo)

    @classmethod
    def transparent(cls, width: int, height: int, *, key: Hashable | None = None) -> PILPhotoImage:
        """Create a transparent spacer image.

        Creates a fully transparent RGBA image of the specified dimensions.
        This is useful for creating spacing in layouts or as a placeholder
        image.

        Args:
            width: Width of the image in pixels.
            height: Height of the image in pixels.
            key: Optional custom cache key. If not provided, a tuple of
                ("transparent", width, height) is used.

        Returns:
            A transparent Tk-compatible PhotoImage.

        Examples:
            >>> # Create a 16x16 transparent spacer
            >>> spacer = Image.transparent(16, 16)
            >>> label = Label(app, image=spacer)

            >>> # Use as compound image padding
            >>> button = Button(app, image=spacer, compound="left")
        """
        cache_key = key if key is not None else ("transparent", width, height)
        cached = cls.get_cached(cache_key)
        if cached is not None:
            return cached

        pil = PILImage.new("RGBA", (width, height), (255, 255, 255, 0))
        photo = PILPhotoImage(image=pil)
        return cls.set_cached(cache_key, photo)
