import tkinter as tk
import uuid
import weakref
from collections import OrderedDict

# Global storage for event data with size limit
_event_data_cache = OrderedDict()
_MAX_CACHE_SIZE = 100  # Prevent unbounded growth

# Patch event_generate
_original_event_generate = tk.Misc.event_generate


def patched_event_generate(self, sequence, data=None, **kw):
    if data is not None:
        guid = str(uuid.uuid4())
        _event_data_cache[guid] = data

        # Limit cache size to prevent memory leaks
        if len(_event_data_cache) > _MAX_CACHE_SIZE:
            # Remove oldest entry
            _event_data_cache.popitem(last=False)

        kw['data'] = guid

    return _original_event_generate(self, sequence, **kw)


tk.Misc.event_generate = patched_event_generate

# Patch bind to add %d substitution and capture event name
_original_bind = tk.Misc.bind


def patched_bind(self, sequence=None, func=None, add=None):
    if func is not None and sequence is not None:
        is_virtual = sequence and sequence.startswith('<<')

        if is_virtual:
            # Use weakref to avoid circular references
            widget_ref = weakref.ref(self)

            # For virtual events, we need to capture both data_guid and event details
            def wrapper(
                    data_guid, serial, num, height, width, keycode, state, time,
                    x, y, x_root, y_root, char, keysym, keysym_num, event_type,
                    send_event, delta):
                # Create a proper event object with __str__ method
                class Event:
                    def __init__(self, widget):
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
                        self.data = None

                    def __str__(self):
                        # Extract event name from sequence (remove << and >>)
                        event_name = sequence.strip('<').strip('>')
                        parts = [f"type={event_name}"]

                        # Add key attributes
                        if self.x is not None and self.x != '??':
                            parts.append(f"x={self.x}")
                        if self.y is not None and self.y != '??':
                            parts.append(f"y={self.y}")

                        # Add data if present
                        if self.data is not None:
                            data_repr = repr(self.data)
                            max_length = 50
                            if len(data_repr) > max_length:
                                parts.append(f"data={data_repr[:max_length]}...")
                            else:
                                parts.append(f"data={data_repr}")

                        return f"<VirtualEvent {' '.join(parts)}>"

                    def __repr__(self):
                        return self.__str__()

                # Get widget from weakref
                widget = widget_ref()
                if widget is None:
                    # Widget was destroyed, clean up data if present
                    if data_guid and data_guid in _event_data_cache:
                        _event_data_cache.pop(data_guid)
                    return

                event = Event(widget)

                # Attach data and clean up cache
                if data_guid and data_guid in _event_data_cache:
                    event.data = _event_data_cache.pop(data_guid)
                else:
                    # Data might have been cleaned up already
                    event.data = None

                return func(event)

            # Register with all the substitutions
            name = self._register(wrapper)

            # Build command with all substitutions including %d for data
            cmd = f'{name} %d %# %b %h %w %k %s %t %x %y %X %Y %A %K %N %T %E %D'

            self.tk.call('bind', self._w, sequence, cmd if not add else '+' + cmd)

            return name
        else:
            # For regular events, just add data=None attribute
            def regular_wrapper(event):
                if not hasattr(event, 'data'):
                    event.data = None
                return func(event)

            return _original_bind(self, sequence, regular_wrapper, add)

    return _original_bind(self, sequence, func, add)


tk.Misc.bind = patched_bind


# Optional: Add a cleanup function to manually clear old cache entries
def cleanup_event_cache():
    """Manually clear the event data cache to prevent memory leaks."""
    _event_data_cache.clear()


# Optional: Periodic cleanup (call this from your app's mainloop if needed)
def periodic_cache_cleanup(root, interval=60000):
    """
    Periodically clean up event cache. Call once with your root window.
    interval is in milliseconds (default: 60 seconds)
    """
    if len(_event_data_cache) > 10:  # Only clean if cache is growing
        # Remove entries older than a reasonable time
        to_remove = list(_event_data_cache.keys())[:len(_event_data_cache) // 2]
        for key in to_remove:
            _event_data_cache.pop(key, None)

    root.after(interval, lambda: periodic_cache_cleanup(root, interval))


def handler(event):
    print(f"Event received: {event}")
    print(f"Event type: {event.type}")
    print(f"Event data: {event.data}")


def key_handler(event):
    print(f"Key event: {event}")
    print(f"Key pressed: {event.keysym}")
    print(f"Event data: {event.data}")


root = tk.Tk()
root.bind('<<MyEvent>>', handler)
root.bind('<<AnotherEvent>>', handler)
root.bind('<KeyPress>', key_handler)


# Optional: Enable periodic cleanup
# periodic_cache_cleanup(root)

def generate():
    root.event_generate('<<MyEvent>>', data={'key': 'value', 'items': [1, 2, 3]})


def generate2():
    root.event_generate('<<AnotherEvent>>', data={'foo': 'bar'})


tk.Button(root, text='Generate MyEvent', command=generate).pack()
tk.Button(root, text='Generate AnotherEvent', command=generate2).pack()

root.mainloop()