"""Debug script to verify ButtonGroup density handling."""
import ttkbootstrap as ttk


class DebugApp(ttk.App):
    def __init__(self):
        super().__init__(title="ButtonGroup Density Debug")
        self.geometry("600x400")

        # Row 1: Default density
        ttk.Label(self, text="Default density:").pack(pady=(10, 2))
        default_group = ttk.ButtonGroup(self, accent='primary', density='default')
        default_group.add("Save")
        default_group.add("Open")
        dropdown = default_group.add(
            widget_type=ttk.DropdownButton,
            icon="caret-down-fill",
            compound="center"
        )
        default_group.pack(pady=5)

        # Row 2: Compact density
        ttk.Label(self, text="Compact density:").pack(pady=(10, 2))
        compact_group = ttk.ButtonGroup(self, accent='primary', density='compact')
        compact_group.add("Save")
        compact_group.add("Open")
        dropdown2 = compact_group.add(
            widget_type=ttk.DropdownButton,
            icon="caret-down-fill",
            compound="center"
        )
        compact_group.pack(pady=5)

        # Debug: Print style info for each button
        ttk.Label(self, text="Debug info (check console):").pack(pady=(20, 5))

        print("\n=== Default density buttons ===")
        for i, widget in enumerate(default_group.items()):
            print(f"Widget {i}: {type(widget).__name__}")
            print(f"  Style: {widget.cget('style')}")
            print(f"  _style_options: {getattr(widget, '_style_options', 'N/A')}")
            print(f"  _density: {getattr(widget, '_density', 'N/A')}")

        print("\n=== Compact density buttons ===")
        for i, widget in enumerate(compact_group.items()):
            print(f"Widget {i}: {type(widget).__name__}")
            print(f"  Style: {widget.cget('style')}")
            print(f"  _style_options: {getattr(widget, '_style_options', 'N/A')}")
            print(f"  _density: {getattr(widget, '_density', 'N/A')}")


if __name__ == "__main__":
    app = DebugApp()
    app.mainloop()
