"""Shim so style imports keep working while runtime owns tk_patch."""

from ttkbootstrap.runtime.tk_patch import install_tk_autostyle

__all__ = ["install_tk_autostyle"]
