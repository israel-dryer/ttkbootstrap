"""Demo showcasing Field widgets (TextEntry, SpinnerEntry, NumberEntry, etc.)."""

from ttkbootstrap import Window
import ttkbootstrap as ttk
from ttkbootstrap.widgets.composites.textentry import TextEntry
from ttkbootstrap.widgets.composites.spinnerentry import SpinnerEntry
from ttkbootstrap.widgets.composites.numericentry import NumericEntry
from ttkbootstrap.widgets.composites.passwordentry import PasswordEntry
from ttkbootstrap.widgets.composites.dateentry import DateEntry
from ttkbootstrap.widgets.composites.timeentry import TimeEntry
from ttkbootstrap.widgets.composites.pathentry import PathEntry


def main(density='default'):
    root = Window(title="Field Widgets Demo", size=(500, 600))

    # Header
    ttk.Label(
        root,
        text="Field Widgets Demo",
        font="title",
        anchor="center"
    ).pack(fill="x", pady=(20, 10))

    # Main container
    container = ttk.Frame(root, padding=20)
    container.pack(fill="both", expand=True)

    # TextEntry
    te = TextEntry(container, label="Text Entry", value="Hello World")
    te.pack(fill="x", pady=5)

    # PasswordEntry
    pe = PasswordEntry(container, label="Password Entry")
    pe.pack(fill="x", pady=5)

    # NumericEntry
    ne = NumericEntry(container, label="Numeric Entry", value=42)
    ne.pack(fill="x", pady=5)

    # SpinnerEntry
    se = SpinnerEntry(container, label="Spinner Entry", value=50)
    se.pack(fill="x", pady=5)

    # DateEntry
    de = DateEntry(container, label="Date Entry")
    de.pack(fill="x", pady=5)

    # TimeEntry
    tie = TimeEntry(container, label="Time Entry")
    tie.pack(fill="x", pady=5)

    # PathEntry (File Entry)
    fe = PathEntry(container, label="File Entry")
    fe.pack(fill="x", pady=5)

    # Compact Density comparison section
    ttk.Separator(container).pack(fill="x", pady=15)
    ttk.Label(container, text="Compact Density Comparison", font="body[bold]").pack(pady=(0, 10))

    compact_frame = ttk.PackFrame(container, direction='horizontal', gap=8, anchor_items='s').pack()
    btn_icon_compact = ttk.Button(compact_frame, icon='gear-fill', density='compact', icon_only=True).pack()
    ne_compact = DateEntry(compact_frame, label="Date Entry", density="compact").pack()
    te_compact = TextEntry(compact_frame, label="Text Entry", value="Hello", density="compact").pack()
    btn_compact = ttk.Button(compact_frame, text="Compact Button", density="compact").pack()

    def check_compact_height():
        print('Compact Icon Button:', btn_icon_compact.winfo_height(), btn_icon_compact.winfo_width())
        print('Compact NumericEntry:', ne_compact._field.winfo_height())
        print('Compact TextEntry:', te_compact._field.winfo_height())
        print('Compact Button:', btn_compact.winfo_height())

    ttk.Button(container, text="Check Compact Heights", command=check_compact_height).pack(pady=10)

    root.mainloop()


if __name__ == "__main__":
    main()
