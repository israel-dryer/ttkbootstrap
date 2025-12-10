"""Backwards compatibility layer - constants moved to ttkbootstrap.constants.

.. deprecated::
    Import from `ttkbootstrap.constants` instead of `ttkbootstrap.core.constants`.

This module re-exports all constants from the root-level constants module
for backwards compatibility with existing code.

Example:
    ```python
    # New (preferred)
    from ttkbootstrap.constants import *

    # Old (still works but deprecated)
    from ttkbootstrap.core.constants import *
    ```
"""

# Re-export everything from root constants module
from ttkbootstrap.constants import *  # noqa: F401, F403