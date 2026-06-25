"""Lifecycle/leak regression tests (2.0 Workstream B).

Widgets that schedule `after()` loops, add variable traces, or subscribe to
the `Publisher` must release those resources when they are reconfigured or
destroyed. Otherwise a destroyed widget keeps firing callbacks (raising
`TclError`) or is kept alive by an external variable's trace.

Runnable headlessly with pytest.
"""
import ttkbootstrap as ttk
from ttkbootstrap.internal.publisher import Publisher
from ttkbootstrap.widgets.floodgauge import Floodgauge
from ttkbootstrap.widgets.meter import Meter


# --------------------------------------------------------------------------- #
# Floodgauge (canvas)
# --------------------------------------------------------------------------- #
def test_floodgauge_external_var_trace_released_on_destroy(root):
    """Destroying a Floodgauge detaches traces from an external variable."""
    var = ttk.IntVar(master=root, value=0)
    fg = Floodgauge(root, variable=var)
    root.update_idletasks()
    assert len(var.trace_info()) == 1

    fg.destroy()
    assert len(var.trace_info()) == 0


def test_floodgauge_configure_variable_no_trace_accumulation(root):
    """Swapping the variable via configure removes the old trace."""
    fg = Floodgauge(root)
    v1 = ttk.IntVar(master=root)
    fg.configure(variable=v1)
    assert len(v1.trace_info()) == 1

    v2 = ttk.IntVar(master=root)
    fg.configure(variable=v2)
    assert len(v1.trace_info()) == 0  # old trace gone
    assert len(v2.trace_info()) == 1  # new var traced exactly once


def test_floodgauge_destroy_cancels_animation(root):
    """A running animation loop is cancelled on destroy."""
    fg = Floodgauge(root, mode="indeterminate")
    fg.pack()
    root.update_idletasks()
    fg.start()
    assert fg._after_id is not None

    fg.destroy()
    assert fg._after_id is None
    root.update()  # a stale after-callback would raise here


# --------------------------------------------------------------------------- #
# Meter
# --------------------------------------------------------------------------- #
def test_meter_interactive_toggle_no_bind_accumulation(root):
    """Toggling interactive mode does not accumulate indicator bindings."""
    m = Meter(root, interactive=True)
    root.update_idletasks()
    assert len(m._bindids) == 2

    # Re-asserting interactive must not add a second pair of bindings.
    m.configure(interactive=True)
    assert len(m._bindids) == 2

    m.configure(interactive=False)
    assert len(m._bindids) == 0


def test_meter_value_trace_released_on_destroy(root):
    """Destroying a meter detaches its value-variable trace."""
    m = Meter(root, amountused=10)
    root.update_idletasks()
    var = m.amountusedvar
    assert len(var.trace_info()) == 1

    m.destroy()
    assert len(var.trace_info()) == 0


# --------------------------------------------------------------------------- #
# Combobox popdown subscription
# --------------------------------------------------------------------------- #
def test_combobox_unsubscribes_on_destroy(root):
    """A combobox releases its Publisher popdown subscription on destroy."""
    base = Publisher.subscriber_count()
    cb = ttk.Combobox(root, values=["a", "b"])
    cb.pack()
    root.update_idletasks()
    assert Publisher.subscriber_count() > base

    cb.destroy()
    root.update_idletasks()
    assert Publisher.subscriber_count() == base