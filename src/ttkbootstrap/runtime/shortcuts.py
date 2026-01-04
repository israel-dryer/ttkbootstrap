"""Cross-platform keyboard shortcut management.

This module provides a service for managing keyboard shortcuts with
automatic platform detection and modifier key translation.

Examples:
    ```python
    import ttkbootstrap as ttk

    app = ttk.App()
    shortcuts = ttk.get_shortcuts()

    # Register shortcuts
    shortcuts.register("save", "Mod+S", save_file)
    shortcuts.register("open", "Mod+O", open_file)
    shortcuts.register("quit", "Mod+Q", app.quit)

    # Bind to app window
    shortcuts.bind_to(app)

    # Menu displays shortcut text automatically
    menu.add_command(text="Save", shortcut="save", command=save_file)
    ```
"""
from __future__ import annotations

import sys
from dataclasses import dataclass, field
from typing import Callable, Any
from weakref import WeakSet

IS_MAC = sys.platform == 'darwin'
IS_WIN = sys.platform == 'win32'

# Modifier display symbols for Mac
_MAC_SYMBOLS = {
    'mod': '\u2318',      # ⌘ Command
    'command': '\u2318',  # ⌘
    'ctrl': '\u2303',     # ⌃ Control
    'control': '\u2303',  # ⌃
    'alt': '\u2325',      # ⌥ Option
    'option': '\u2325',   # ⌥
    'shift': '\u21E7',    # ⇧
}

# Modifier display names for Windows/Linux
_WIN_NAMES = {
    'mod': 'Ctrl',
    'command': 'Ctrl',
    'ctrl': 'Ctrl',
    'control': 'Ctrl',
    'alt': 'Alt',
    'option': 'Alt',
    'shift': 'Shift',
}

# Tkinter binding modifiers
_BINDING_MODIFIERS = {
    'mod': 'Command' if IS_MAC else 'Control',
    'command': 'Command',
    'ctrl': 'Control',
    'control': 'Control',
    'alt': 'Option' if IS_MAC else 'Alt',
    'option': 'Option',
    'shift': 'Shift',
}


@dataclass
class Shortcut:
    """A registered keyboard shortcut.

    Attributes:
        key: Unique identifier for lookup (e.g., "save", "file.open")
        pattern: Shortcut pattern (e.g., "Mod+S", "Shift+Alt+N")
        command: Function to execute when triggered
    """
    key: str
    pattern: str
    command: Callable

    @property
    def display(self) -> str:
        """Platform-appropriate display string for menus.

        Returns:
            On Mac: "⇧⌘S" (symbols, no separators)
            On Windows/Linux: "Ctrl+Shift+S" (names with + separators)
        """
        parts = self.pattern.split('+')
        key_part = parts[-1]
        mod_parts = [p.lower() for p in parts[:-1]]

        if IS_MAC:
            # Mac style: symbols without separators, specific order
            # Standard order: Control, Option, Shift, Command
            ordered_mods = []
            for mod in ['ctrl', 'control', 'alt', 'option', 'shift', 'mod', 'command']:
                if mod in mod_parts:
                    symbol = _MAC_SYMBOLS.get(mod, mod)
                    if symbol not in ordered_mods:
                        ordered_mods.append(symbol)
            return ''.join(ordered_mods) + key_part.upper()
        else:
            # Windows/Linux style: names with + separators
            mod_names = []
            for mod in mod_parts:
                name = _WIN_NAMES.get(mod, mod.capitalize())
                if name not in mod_names:
                    mod_names.append(name)
            return '+'.join(mod_names + [key_part.upper()])

    @property
    def binding(self) -> str:
        """Tkinter binding string.

        Returns:
            Binding string like "<Control-s>" or "<Command-Shift-s>"
        """
        parts = self.pattern.split('+')
        key_part = parts[-1].lower()
        mod_parts = [p.lower() for p in parts[:-1]]

        # Convert to Tkinter modifier names
        tk_mods = []
        for mod in mod_parts:
            tk_mod = _BINDING_MODIFIERS.get(mod, mod.capitalize())
            if tk_mod not in tk_mods:
                tk_mods.append(tk_mod)

        # Handle function keys - keep uppercase
        if key_part.upper().startswith('F') and key_part[1:].isdigit():
            key_part = key_part.upper()

        return f"<{'-'.join(tk_mods + [key_part])}>"


class Shortcuts:
    """Singleton service for managing keyboard shortcuts.

    Provides cross-platform keyboard shortcut registration and binding.
    The service automatically translates modifier keys for each platform:

    - ``Mod`` becomes ``Ctrl`` on Windows/Linux, ``Command`` on Mac
    - ``Alt`` becomes ``Alt`` on Windows/Linux, ``Option`` on Mac
    - ``Shift`` works the same on all platforms

    Examples:
        ```python
        shortcuts = get_shortcuts()

        # Register shortcuts
        shortcuts.register("save", "Mod+S", save_file)
        shortcuts.register("undo", "Mod+Z", undo)
        shortcuts.register("find", "Mod+F", find)

        # Bind all to window
        shortcuts.bind_to(app)

        # Get display string for menu
        shortcuts.display("save")  # "Ctrl+S" on Windows, "⌘S" on Mac
        ```
    """

    _instance: 'Shortcuts | None' = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._shortcuts: dict[str, Shortcut] = {}
            cls._instance._bound_windows: WeakSet = WeakSet()
            cls._instance._bindings: dict[int, list[tuple[str, str]]] = {}
        return cls._instance

    def register(self, key: str, pattern: str, command: Callable) -> Shortcut:
        """Register a keyboard shortcut.

        Args:
            key: Unique identifier (e.g., "save", "file.open")
            pattern: Shortcut pattern using symbolic modifiers:
                - ``Mod+S`` - Primary modifier + S
                - ``Mod+Shift+S`` - Primary modifier + Shift + S
                - ``Alt+F4`` - Alt + F4
                - ``F5`` - Function key alone
            command: Function to call when triggered

        Returns:
            The created Shortcut object.

        Raises:
            ValueError: If key is already registered.

        Examples:
            ```python
            shortcuts.register("save", "Mod+S", save_file)
            shortcuts.register("quit", "Mod+Q", app.quit)
            shortcuts.register("refresh", "F5", refresh)
            ```
        """
        if key in self._shortcuts:
            raise ValueError(f"Shortcut key '{key}' is already registered")

        shortcut = Shortcut(key=key, pattern=pattern, command=command)
        self._shortcuts[key] = shortcut

        # Bind to any already-bound windows
        for window in self._bound_windows:
            self._bind_shortcut(window, shortcut)

        return shortcut

    def unregister(self, key: str) -> None:
        """Remove a registered shortcut.

        Args:
            key: The shortcut key to remove.

        Raises:
            KeyError: If key is not registered.
        """
        if key not in self._shortcuts:
            raise KeyError(f"Shortcut key '{key}' is not registered")

        shortcut = self._shortcuts.pop(key)

        # Unbind from all windows
        for window in self._bound_windows:
            self._unbind_shortcut(window, shortcut)

    def get(self, key: str) -> Shortcut | None:
        """Get a shortcut by key.

        Args:
            key: The shortcut key to look up.

        Returns:
            The Shortcut object, or None if not found.
        """
        return self._shortcuts.get(key)

    def display(self, key: str) -> str:
        """Get display string for a shortcut key.

        Args:
            key: The shortcut key to look up.

        Returns:
            Platform-appropriate display string (e.g., "Ctrl+S" or "⌘S"),
            or empty string if not found.
        """
        shortcut = self._shortcuts.get(key)
        return shortcut.display if shortcut else ''

    def binding(self, key: str) -> str:
        """Get Tkinter binding string for a shortcut key.

        Args:
            key: The shortcut key to look up.

        Returns:
            Tkinter binding string (e.g., "<Control-s>"),
            or empty string if not found.
        """
        shortcut = self._shortcuts.get(key)
        return shortcut.binding if shortcut else ''

    def bind_to(self, window: Any) -> None:
        """Bind all registered shortcuts to a window.

        Args:
            window: The window (App, Toplevel, Tk) to bind shortcuts to.

        Note:
            Shortcuts registered after calling bind_to will also be
            automatically bound to this window.
        """
        if window in self._bound_windows:
            return

        self._bound_windows.add(window)
        window_id = id(window)
        self._bindings[window_id] = []

        for shortcut in self._shortcuts.values():
            self._bind_shortcut(window, shortcut)

    def unbind_from(self, window: Any) -> None:
        """Remove all shortcut bindings from a window.

        Args:
            window: The window to unbind shortcuts from.
        """
        if window not in self._bound_windows:
            return

        self._bound_windows.discard(window)
        window_id = id(window)

        # Unbind all shortcuts
        bindings = self._bindings.pop(window_id, [])
        for binding_str, func_id in bindings:
            try:
                window.unbind(binding_str, func_id)
            except Exception:
                pass

    def all(self) -> dict[str, Shortcut]:
        """Get all registered shortcuts.

        Returns:
            Dictionary mapping keys to Shortcut objects.
        """
        return dict(self._shortcuts)

    def _bind_shortcut(self, window: Any, shortcut: Shortcut) -> None:
        """Bind a single shortcut to a window."""
        window_id = id(window)
        binding_str = shortcut.binding

        def handler(event):
            shortcut.command()
            return 'break'

        try:
            func_id = window.bind(binding_str, handler, add='+')
            if window_id in self._bindings:
                self._bindings[window_id].append((binding_str, func_id))
        except Exception:
            pass

    def _unbind_shortcut(self, window: Any, shortcut: Shortcut) -> None:
        """Unbind a single shortcut from a window."""
        window_id = id(window)
        binding_str = shortcut.binding

        if window_id not in self._bindings:
            return

        # Find and remove the binding
        bindings = self._bindings[window_id]
        for i, (b_str, func_id) in enumerate(bindings):
            if b_str == binding_str:
                try:
                    window.unbind(binding_str, func_id)
                except Exception:
                    pass
                bindings.pop(i)
                break


def get_shortcuts() -> Shortcuts:
    """Get the global Shortcuts service instance.

    Returns:
        The singleton Shortcuts instance.

    Examples:
        ```python
        import ttkbootstrap as ttk

        shortcuts = ttk.get_shortcuts()
        shortcuts.register("save", "Mod+S", save_file)
        shortcuts.bind_to(app)
        ```
    """
    return Shortcuts()


__all__ = ['Shortcut', 'Shortcuts', 'get_shortcuts']