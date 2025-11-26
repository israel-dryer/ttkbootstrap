"""Enhanced event system for ttkbootstrap.

This module patches the standard tkinter event system to enable passing custom
data with virtual events. This provides a more powerful and flexible event
handling mechanism than the default tkinter implementation.

Features:
    - Pass custom Python objects as data with virtual events
    - Automatic memory management with LRU cache to prevent leaks
    - Consistent Event objects for both regular and virtual events
    - All standard event attributes preserved (x, y, widget, etc.)
    - Backwards compatible with existing tkinter code

Example:
    ```python
    import tkinter as tk
    import ttkbootstrap as ttk

    root = ttk.Window()

    def handler(event):
        print(f"Received: {event.data}")

    root.bind('<<CustomEvent>>', handler)
    root.event_generate('<<CustomEvent>>', data={'key': 'value', 'items': [1, 2, 3]})

    root.mainloop()
    ```

Note:
    This module automatically patches tkinter when imported. The patches are
    applied globally and affect all tkinter widgets in the application.
"""

import tkinter as tk
import uuid
import weakref
from collections import OrderedDict
from typing import Any, Callable, Optional, Union


# Global storage for event data with LRU cache behavior
_event_data_cache: OrderedDict[str, Any] = OrderedDict()
_MAX_CACHE_SIZE = 100  # Prevent unbounded growth

# Store original tkinter methods before patching
_original_event_generate: Callable = tk.Misc.event_generate
_original_bind: Callable = tk.Misc.bind


def _patched_event_generate(
    self: tk.Misc,
    sequence: str,
    data: Optional[Any] = None,
    **kw
) -> None:
    """Enhanced event_generate that supports custom data parameter.

    This patched version of tkinter's event_generate method allows passing
    arbitrary Python objects as event data. The data is stored in a cache
    with a unique identifier that is passed through the event system.

    Args:
        self: The widget instance (automatically provided)
        sequence: Virtual event name (e.g., '<<MyEvent>>')
        data: Optional custom data to attach to the event. Can be any Python object.
        **kw: Additional keyword arguments passed to the original event_generate

    Example:
        ```python
        widget.event_generate('<<Save>>', data={'filename': 'doc.txt', 'author': 'John'})
        ```

    Note:
        The cache uses LRU eviction to prevent memory leaks. Old entries are
        automatically removed when the cache exceeds _MAX_CACHE_SIZE.
    """
    if data is not None:
        # Generate unique identifier for this data
        guid = str(uuid.uuid4())
        _event_data_cache[guid] = data

        # Limit cache size using LRU eviction
        if len(_event_data_cache) > _MAX_CACHE_SIZE:
            # Remove oldest entry (FIFO from OrderedDict)
            _event_data_cache.popitem(last=False)

        # Pass GUID through tkinter's event system
        kw['data'] = guid

    return _original_event_generate(self, sequence, **kw)


def _patched_bind(
    self: tk.Misc,
    sequence: Optional[str] = None,
    func: Optional[Callable] = None,
    add: Optional[Union[bool, str]] = None
) -> Optional[str]:
    """Enhanced bind that supports data attribute on all events.

    This patched version of tkinter's bind method ensures that:
    1. Virtual events (<<EventName>>) receive custom data if provided
    2. All event objects have a 'data' attribute (None for regular events)
    3. Virtual events get properly formatted Event objects with __str__

    Args:
        self: The widget instance (automatically provided)
        sequence: Event sequence (e.g., '<Button-1>', '<<MyEvent>>')
        func: Callback function to handle the event
        add: If True/'+', add binding without removing existing ones

    Returns:
        Tkinter function name string if binding was created, None otherwise

    Example:
        ```python
        def handler(event):
            print(f"Event: {event}, Data: {event.data}")

        widget.bind('<<CustomEvent>>', handler)
        ```
    """
    if func is not None and sequence is not None:
        is_virtual = sequence and sequence.startswith('<<')

        if is_virtual:
            # Create wrapper for virtual events to handle data retrieval
            widget_ref = weakref.ref(self)  # Avoid circular references

            def wrapper(
                data_guid, serial, num, height, width, keycode, state, time,
                x, y, x_root, y_root, char, keysym, keysym_num, event_type,
                send_event, delta
            ):
                """Internal wrapper that constructs Event objects for virtual events.

                This function is called by tkinter's event system with all the
                standard event substitution values plus our custom data GUID.
                """

                class VirtualEvent:
                    """Event object for virtual events with enhanced functionality.

                    This class mimics tkinter's Event class but adds:
                    - Custom data attribute from event_generate
                    - Proper __str__ representation showing event details
                    - All standard tkinter event attributes
                    """

                    def __init__(self, widget: tk.Misc) -> None:
                        """Initialize event with standard tkinter attributes.

                        Args:
                            widget: The widget that received the event
                        """
                        self.serial = serial
                        self.num = num
                        self.height = height
                        self.width = width
                        self.keycode = keycode
                        self.state = state
                        self.time = time
                        self.x = x
                        self.y = y
                        self.x_root = x_root
                        self.y_root = y_root
                        self.char = char
                        self.keysym = keysym
                        self.keysym_num = keysym_num
                        self.type = event_type
                        self.send_event = send_event
                        self.delta = delta
                        self.widget = widget
                        self.data: Optional[Any] = None

                    def __str__(self) -> str:
                        """Return human-readable event representation.

                        Returns:
                            Formatted string like: <VirtualEvent type=MyEvent x=10 y=20 data={'key': 'value'}>
                        """
                        # Extract event name from sequence (remove << and >>)
                        event_name = sequence.strip('<').strip('>')
                        parts = [f"type={event_name}"]

                        # Add position if available
                        if self.x is not None and self.x != '??':
                            parts.append(f"x={self.x}")
                        if self.y is not None and self.y != '??':
                            parts.append(f"y={self.y}")

                        # Add data if present (truncate if too long)
                        if self.data is not None:
                            data_repr = repr(self.data)
                            max_length = 50
                            if len(data_repr) > max_length:
                                parts.append(f"data={data_repr[:max_length]}...")
                            else:
                                parts.append(f"data={data_repr}")

                        return f"<VirtualEvent {' '.join(parts)}>"

                    def __repr__(self) -> str:
                        """Return repr string (same as __str__)."""
                        return self.__str__()

                # Retrieve widget from weakref
                widget = widget_ref()
                if widget is None:
                    # Widget was destroyed, clean up cache entry if present
                    if data_guid and data_guid in _event_data_cache:
                        _event_data_cache.pop(data_guid)
                    return

                # Create event object
                event = VirtualEvent(widget)

                # Attach custom data and remove from cache
                if data_guid and data_guid in _event_data_cache:
                    event.data = _event_data_cache.pop(data_guid)
                else:
                    # Data might have been evicted from cache already
                    event.data = None

                return func(event)

            # Register wrapper function with tkinter
            name = self._register(wrapper)

            # Build command with all substitutions including %d for data GUID
            # Substitution codes: https://tcl.tk/man/tcl8.6/TkCmd/bind.htm
            cmd = f'{name} %d %# %b %h %w %k %s %t %x %y %X %Y %A %K %N %T %E %D'

            # Bind to widget
            self.tk.call('bind', self._w, sequence, cmd if not add else '+' + cmd)

            return name
        else:
            # For regular events, wrap to add data=None attribute
            def regular_wrapper(event):
                """Wrapper for regular events to add consistent data attribute."""
                if not hasattr(event, 'data'):
                    event.data = None
                return func(event)

            return _original_bind(self, sequence, regular_wrapper, add)

    # No function or sequence provided, pass through to original
    return _original_bind(self, sequence, func, add)


def cleanup_event_cache() -> None:
    """Manually clear the entire event data cache.

    This function removes all cached event data. It's useful for:
    - Forcing memory cleanup in long-running applications
    - Resetting state during testing
    - Manual intervention when cache grows unexpectedly

    Note:
        Normally cache cleanup is automatic via LRU eviction. Manual cleanup
        should rarely be needed in production code.

    Example:
        ```python
        from ttkbootstrap.events import cleanup_event_cache

        # After processing many events
        cleanup_event_cache()
        ```
    """
    _event_data_cache.clear()


def enable_periodic_cache_cleanup(
    root: tk.Misc,
    interval: int = 60000,
    threshold: int = 10
) -> None:
    """Enable automatic periodic cleanup of the event cache.

    This function sets up a recurring timer that checks the cache size
    and performs cleanup when it exceeds a threshold. This helps prevent
    cache growth in long-running applications that generate many events.

    Args:
        root: Root window or any widget (needed for .after() scheduling)
        interval: Cleanup check interval in milliseconds (default: 60000 = 1 minute)
        threshold: Only clean if cache has more than this many entries (default: 10)

    Example:
        ```python
        import ttkbootstrap as ttk
        from ttkbootstrap.events import enable_periodic_cache_cleanup

        root = ttk.Window()
        enable_periodic_cache_cleanup(root, interval=30000)  # Check every 30 seconds
        root.mainloop()
        ```

    Note:
        This is optional. The LRU cache already prevents unbounded growth.
        Periodic cleanup is only needed for applications that generate
        thousands of events and want more aggressive memory management.
    """
    def cleanup_task():
        """Internal task that performs conditional cache cleanup."""
        if len(_event_data_cache) > threshold:
            # Remove half of the oldest entries
            to_remove = list(_event_data_cache.keys())[:len(_event_data_cache) // 2]
            for key in to_remove:
                _event_data_cache.pop(key, None)

        # Schedule next cleanup
        root.after(interval, cleanup_task)

    # Start the cleanup cycle
    cleanup_task()


def get_cache_size() -> int:
    """Get the current number of entries in the event data cache.

    This is primarily useful for debugging and monitoring cache behavior.

    Returns:
        Number of cached event data objects

    Example:
        ```python
        from ttkbootstrap.events import get_cache_size

        print(f"Current cache size: {get_cache_size()}")
        ```
    """
    return len(_event_data_cache)


def install_enhanced_events() -> None:
    """Install the enhanced event system by patching tkinter methods.

    This function applies monkey patches to tkinter's Misc class,
    replacing event_generate and bind with enhanced versions that
    support passing custom data through virtual events.

    The patches are applied globally and affect all tkinter widgets
    in the application. This function is called automatically when
    ttkbootstrap is imported.

    Note:
        You should not need to call this manually unless you've explicitly
        uninstalled the patches and need to reinstall them.

    Example:
        ```python
        from ttkbootstrap.events import install_enhanced_events

        # Reinstall if needed
        install_enhanced_events()
        ```
    """
    tk.Misc.event_generate = _patched_event_generate
    tk.Misc.bind = _patched_bind


def uninstall_enhanced_events() -> None:
    """Restore original tkinter event methods.

    This function removes the patches and restores tkinter to its
    original behavior. Useful for testing or if conflicts arise.

    Warning:
        After calling this, event_generate will no longer accept
        the 'data' parameter, and existing bindings may not work
        as expected.

    Example:
        ```python
        from ttkbootstrap.events import uninstall_enhanced_events

        # Restore original tkinter behavior
        uninstall_enhanced_events()
        ```
    """
    tk.Misc.event_generate = _original_event_generate
    tk.Misc.bind = _original_bind
    cleanup_event_cache()


__all__ = [
    'cleanup_event_cache',
    'enable_periodic_cache_cleanup',
    'get_cache_size',
    'install_enhanced_events',
    'uninstall_enhanced_events',
]