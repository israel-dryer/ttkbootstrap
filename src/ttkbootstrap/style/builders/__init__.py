"""Style builder functions for ttkbootstrap widgets.

This package contains individual builder functions organized by widget type.
Each builder is registered with the BootstyleBuilder registry using decorators.

Builder modules are automatically imported to trigger registration.
"""

from __future__ import annotations

# Import all builder modules to trigger registration
# As new builder modules are created, add them here
from . import button  # noqa: F401
from . import frame
from . import label
from . import radiobutton
from . import checkbutton

__all__ = [
    'button',
    'frame',
    'label',
    'radiobutton',
    'checkbutton'
]
