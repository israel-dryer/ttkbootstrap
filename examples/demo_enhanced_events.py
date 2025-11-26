"""Test script for enhanced event system.

This script demonstrates the enhanced event binding functionality,
showing how custom data can be passed through virtual events.
"""
import ttkbootstrap as ttk
from ttkbootstrap.events import get_cache_size


def event_handler(event):
    """Handle custom events with data."""
    print(f"Event received: {event}")
    print(f"  Event type: {event.type}")
    print(f"  Event data: {event.data}")
    print(f"  Cache size: {get_cache_size()}")
    print()


def key_handler(event):
    """Handle keyboard events (regular events)."""
    print(f"Key event: {event}")
    print(f"  Key pressed: {event.keysym}")
    print(f"  Event data: {event.data}")
    print()


# Create main window
root = ttk.Window(themename="darkly", title="Enhanced Events Test")

# Bind virtual events with handlers
root.bind('<<MyEvent>>', event_handler)
root.bind('<<AnotherEvent>>', event_handler)
root.bind('<KeyPress>', key_handler)


# Event generation functions
def generate_my_event():
    """Generate MyEvent with dictionary data."""
    root.event_generate('<<MyEvent>>', data={
        'key': 'value',
        'items': [1, 2, 3],
        'nested': {'foo': 'bar'}
    })


def generate_another_event():
    """Generate AnotherEvent with simple data."""
    root.event_generate('<<AnotherEvent>>', data={'status': 'success', 'count': 42})


def generate_complex_event():
    """Generate event with complex object data."""
    root.event_generate('<<MyEvent>>', data={
        'user': 'John Doe',
        'action': 'save',
        'timestamp': '2025-11-26',
        'metadata': {
            'version': '1.0',
            'platform': 'Windows'
        }
    })


# Create UI
frame = ttk.Frame(root, padding=20)
frame.pack(fill='both', expand=True)

ttk.Label(
    frame,
    text="Enhanced Event System Test",
    font=('Helvetica', 16, 'bold')
).pack(pady=(0, 20))

ttk.Label(
    frame,
    text="Click buttons to generate events with custom data.\nPress any key to see regular event handling.",
    justify='center'
).pack(pady=(0, 20))

ttk.Button(
    frame,
    text='Generate MyEvent',
    command=generate_my_event,
    bootstyle='success'
).pack(pady=5, fill='x')

ttk.Button(
    frame,
    text='Generate AnotherEvent',
    command=generate_another_event,
    bootstyle='info'
).pack(pady=5, fill='x')

ttk.Button(
    frame,
    text='Generate Complex Event',
    command=generate_complex_event,
    bootstyle='warning'
).pack(pady=5, fill='x')

ttk.Separator(frame, orient='horizontal').pack(pady=20, fill='x')

cache_label = ttk.Label(frame, text=f"Cache size: {get_cache_size()}")
cache_label.pack()


def update_cache_size():
    """Update cache size display."""
    cache_label.config(text=f"Cache size: {get_cache_size()}")
    root.after(100, update_cache_size)


update_cache_size()

print("Enhanced Event System Test")
print("=" * 50)
print("Press buttons to generate events.")
print("Watch the console for event details.")
print("=" * 50)
print()

root.mainloop()