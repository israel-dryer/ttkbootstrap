"""Demo showcasing Entry, Combobox, Spinbox, and Field widgets with density options."""

from ttkbootstrap import Window
import ttkbootstrap as ttk
from ttkbootstrap.widgets.composites.textentry import TextEntry
from ttkbootstrap.widgets.composites.spinnerentry import SpinnerEntry


def main():
    root = Window(title="Entry Density Demo", size=(600, 600))

    # Header
    ttk.Label(
        root,
        text="Entry Widget Density Comparison",
        font="title",
        anchor="center"
    ).pack(fill="x", pady=(20, 10))

    # Main container
    container = ttk.Frame(root, padding=20)
    container.pack(fill="both", expand=True)

    # Configure grid columns
    container.columnconfigure(0, weight=1)
    container.columnconfigure(1, weight=1)
    container.columnconfigure(2, weight=1)

    # Column headers
    ttk.Label(container, text="Widget", font="body[bold]").grid(row=0, column=0, pady=(0, 10))
    ttk.Label(container, text="Default", font="body[bold]").grid(row=0, column=1, pady=(0, 10))
    ttk.Label(container, text="Compact", font="body[bold]").grid(row=0, column=2, pady=(0, 10))

    # Entry row
    ttk.Label(container, text="Entry").grid(row=1, column=0, sticky="w", pady=5)

    e1 = ttk.Entry(container)
    e1.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
    e1.insert(0, "Default")

    e2 = ttk.Entry(container, density="compact")
    e2.grid(row=1, column=2, padx=5, pady=5, sticky="ew")
    e2.insert(0, "Compact")

    # Combobox row
    ttk.Label(container, text="Combobox").grid(row=2, column=0, sticky="w", pady=5)

    options = ["Option 1", "Option 2", "Option 3"]

    c1 = ttk.Combobox(container, values=options)
    c1.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
    c1.set("Default")

    c2 = ttk.Combobox(container, values=options, density="compact")
    c2.grid(row=2, column=2, padx=5, pady=5, sticky="ew")
    c2.set("Compact")

    # Spinbox row
    ttk.Label(container, text="Spinbox").grid(row=3, column=0, sticky="w", pady=5)

    s1 = ttk.Spinbox(container, from_=0, to=100)
    s1.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

    s2 = ttk.Spinbox(container, from_=0, to=100, density="compact")
    s2.grid(row=3, column=2, padx=5, pady=5, sticky="ew")

    # Field widgets section
    ttk.Separator(container).grid(row=4, column=0, columnspan=3, sticky="ew", pady=15)

    ttk.Label(container, text="Field Widgets", font="body[bold]").grid(
        row=5, column=0, columnspan=3, pady=(0, 10)
    )

    # TextEntry row
    ttk.Label(container, text="TextEntry").grid(row=6, column=0, sticky="w", pady=5)

    te1 = TextEntry(container, label="Name", value="Default")
    te1.grid(row=6, column=1, padx=5, pady=5, sticky="ew")

    te2 = TextEntry(container, label="Name", value="Compact")
    te2.grid(row=6, column=2, padx=5, pady=5, sticky="ew")

    # SpinnerEntry row
    ttk.Label(container, text="SpinnerEntry").grid(row=7, column=0, sticky="w", pady=5)

    se1 = SpinnerEntry(container, label="Amount", value=50)
    se1.grid(row=7, column=1, padx=5, pady=5, sticky="ew")

    se2 = SpinnerEntry(container, label="Amount", value=50)
    se2.grid(row=7, column=2, padx=5, pady=5, sticky="ew")

    # Disabled state section
    ttk.Separator(container).grid(row=8, column=0, columnspan=3, sticky="ew", pady=15)

    ttk.Label(container, text="Disabled State", font="body[bold]").grid(
        row=9, column=0, columnspan=3, pady=(0, 10)
    )

    # Disabled Entry row
    ttk.Label(container, text="Entry").grid(row=10, column=0, sticky="w", pady=5)

    e3 = ttk.Entry(container, state="disabled")
    e3.grid(row=10, column=1, padx=5, pady=5, sticky="ew")

    e4 = ttk.Entry(container, density="compact", state="disabled")
    e4.grid(row=10, column=2, padx=5, pady=5, sticky="ew")

    # Disabled Combobox row
    ttk.Label(container, text="Combobox").grid(row=11, column=0, sticky="w", pady=5)

    c3 = ttk.Combobox(container, values=options, state="disabled")
    c3.grid(row=11, column=1, padx=5, pady=5, sticky="ew")
    c3.set("Disabled")

    c4 = ttk.Combobox(container, values=options, density="compact", state="disabled")
    c4.grid(row=11, column=2, padx=5, pady=5, sticky="ew")
    c4.set("Disabled")

    # Disabled Spinbox row
    ttk.Label(container, text="Spinbox").grid(row=12, column=0, sticky="w", pady=5)

    s3 = ttk.Spinbox(container, from_=0, to=100, state="disabled")
    s3.grid(row=12, column=1, padx=5, pady=5, sticky="ew")

    s4 = ttk.Spinbox(container, from_=0, to=100, density="compact", state="disabled")
    s4.grid(row=12, column=2, padx=5, pady=5, sticky="ew")



    root.mainloop()


if __name__ == "__main__":
    main()
