"""Deprecated location for ttkbootstrap's internal publisher.

The publisher is internal plumbing and has moved to
`ttkbootstrap.internal.publisher`. This shim re-exports it for backward
compatibility and will be removed in 3.0.
"""
import warnings

warnings.warn(
    "ttkbootstrap.publisher is internal and has moved to "
    "ttkbootstrap.internal.publisher; this shim will be removed in 3.0.",
    DeprecationWarning,
    stacklevel=2,
)

from ttkbootstrap.internal.publisher import Channel, Subscriber, Publisher  # noqa: F401,E402