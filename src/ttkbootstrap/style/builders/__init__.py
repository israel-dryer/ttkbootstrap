"""Style builder functions for ttkbootstrap widgets.

This package contains individual builder functions organized by widget type.
Each builder is registered with the BootstyleBuilder registry using decorators.

Builder modules are automatically imported to trigger registration.
"""

from __future__ import annotations

from . import button, checkbutton, frame, label, progressbar, radiobutton

# Import all builder modules to trigger registration

__all__ = [
    'button',
    'frame',
    'label',
    'radiobutton',
    'checkbutton',
    'progressbar',
]
