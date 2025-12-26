"""
ttkbootstrap v2 Demo

A showcase of ttkbootstrap's modern widgets, layout system, and theming.
"""
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.core.signals import Signal


class WidgetShowcase:
    """Main demo application showcasing ttkbootstrap v2 features."""

    def __init__(self, master):
        self.master = master
        self.style = ttk.get_style()

        # Signals for reactive UI
        self.progress_value = Signal[int](45)
        self.slider_value = Signal[float](65.0)
        self.text_input = Signal[str]("")

        self._build_ui()

    def _build_ui(self):
        """Build the main UI layout."""
        # Main container with padding
        main = ttk.Frame(self.master, padding=20)
        main.pack(fill=BOTH, expand=YES)

        # Header section
        self._build_header(main)

        # Content area with left/right panels
        content = ttk.Frame(main)
        content.pack(fill=BOTH, expand=YES, pady=(15, 0))

        # Left panel - widgets showcase
        left = ttk.Frame(content)
        left.pack(side=LEFT, fill=BOTH, expand=YES, padx=(0, 10))

        # Right panel - more widgets
        right = ttk.Frame(content)
        right.pack(side=RIGHT, fill=BOTH, expand=YES, padx=(10, 0))

        # Build sections
        self._build_buttons_section(left)
        self._build_inputs_section(left)
        self._build_selection_section(left)

        self._build_progress_section(right)
        self._build_data_section(right)
        self._build_text_section(right)

    def _build_header(self, parent):
        """Build the header with theme selector."""
        header = ttk.Frame(parent)
        header.pack(fill=X)

        # Title and subtitle
        title_frame = ttk.Frame(header)
        title_frame.pack(side=LEFT)

        ttk.Label(
            title_frame,
            text="ttkbootstrap",
            font="heading-xl[bold]",
        ).pack(anchor=W)

        ttk.Label(
            title_frame,
            text="Modern UI framework for Python",
            font="body",
            bootstyle="secondary",
        ).pack(anchor=W)

        # Theme selector
        theme_frame = ttk.Frame(header)
        theme_frame.pack(side=RIGHT)

        ttk.Label(theme_frame, text="Theme:", font="label").pack(side=LEFT, padx=(0, 8))

        theme_names = self._get_theme_names()
        self.theme_combo = ttk.Combobox(
            theme_frame,
            values=theme_names,
            width=15,
            state="readonly",
        )
        self.theme_combo.pack(side=LEFT)
        self.theme_combo.set(self.style.current_theme)
        self.theme_combo.bind("<<ComboboxSelected>>", self._on_theme_change)

        # Separator
        ttk.Separator(parent).pack(fill=X, pady=15)

    def _get_theme_names(self):
        """Get list of available themes."""
        themes = [s['name'] for s in self.style.theme_provider.list_themes()]
        # Add light/dark shortcuts
        if 'light' not in themes:
            themes.append('light')
        if 'dark' not in themes:
            themes.append('dark')
        return sorted(themes)

    def _on_theme_change(self, event):
        """Handle theme selection change."""
        theme = self.theme_combo.get()
        self.style.theme_use(theme)
        self.theme_combo.selection_clear()

    def _build_buttons_section(self, parent):
        """Build buttons showcase section."""
        group = ttk.LabelFrame(parent, text="Buttons", padding=15)
        group.pack(fill=X, pady=(0, 10))

        # Color variants row
        colors_frame = ttk.Frame(group)
        colors_frame.pack(fill=X, pady=(0, 10))

        colors = ['primary', 'secondary', 'success', 'info', 'warning', 'danger']
        for color in colors:
            btn = ttk.Button(colors_frame, text=color.title(), bootstyle=color)
            btn.pack(side=LEFT, padx=2, expand=YES, fill=X)

        # Style variants row
        styles_frame = ttk.Frame(group)
        styles_frame.pack(fill=X)

        ttk.Button(styles_frame, text="Solid", bootstyle="primary").pack(
            side=LEFT, padx=2, expand=YES, fill=X
        )
        ttk.Button(styles_frame, text="Outline", bootstyle="primary-outline").pack(
            side=LEFT, padx=2, expand=YES, fill=X
        )
        ttk.Button(styles_frame, text="Link", bootstyle="link").pack(
            side=LEFT, padx=2, expand=YES, fill=X
        )
        ttk.MenuButton(
            styles_frame, text="Menu", bootstyle="secondary"
        ).pack(side=LEFT, padx=2, expand=YES, fill=X)

    def _build_inputs_section(self, parent):
        """Build input widgets section."""
        group = ttk.LabelFrame(parent, text="Input Widgets", padding=15)
        group.pack(fill=X, pady=(0, 10))

        # Entry
        entry_frame = ttk.Frame(group)
        entry_frame.pack(fill=X, pady=(0, 8))
        ttk.Label(entry_frame, text="Entry:", width=10).pack(side=LEFT)
        ttk.Entry(entry_frame, textsignal=self.text_input).pack(
            side=LEFT, fill=X, expand=YES
        )

        # Password
        pass_frame = ttk.Frame(group)
        pass_frame.pack(fill=X, pady=(0, 8))
        ttk.Label(pass_frame, text="Password:", width=10).pack(side=LEFT)
        password = ttk.Entry(pass_frame, show="\u2022")
        password.pack(side=LEFT, fill=X, expand=YES)
        password.insert(0, "secret123")

        # Spinbox
        spin_frame = ttk.Frame(group)
        spin_frame.pack(fill=X, pady=(0, 8))
        ttk.Label(spin_frame, text="Spinbox:", width=10).pack(side=LEFT)
        spinbox = ttk.Spinbox(spin_frame, from_=0, to=100, width=10)
        spinbox.pack(side=LEFT)
        spinbox.set(42)

        # SelectBox
        ttk.SelectBox(
            group,
            label="SelectBox:",
            items=["Option A", "Option B", "Option C", "Option D"],
            value="Option A",
            font="body",
        ).pack(fill=X)

    def _build_selection_section(self, parent):
        """Build selection widgets section."""
        group = ttk.LabelFrame(parent, text="Selection", padding=15)
        group.pack(fill=X, pady=(0, 10))

        # Checkbuttons row
        check_frame = ttk.Frame(group)
        check_frame.pack(fill=X, pady=(0, 10))

        cb1 = ttk.CheckButton(check_frame, text="Selected", bootstyle="success")
        cb1.pack(side=LEFT, padx=(0, 15))
        cb1.invoke()

        cb2 = ttk.CheckButton(check_frame, text="Unselected")
        cb2.pack(side=LEFT, padx=(0, 15))

        cb3 = ttk.CheckButton(check_frame, text="Disabled", state=DISABLED)
        cb3.pack(side=LEFT)

        # Radiobuttons row
        radio_frame = ttk.Frame(group)
        radio_frame.pack(fill=X, pady=(0, 10))

        radio_var = ttk.IntVar(value=1)
        ttk.RadioButton(
            radio_frame, text="First", value=1, variable=radio_var
        ).pack(side=LEFT, padx=(0, 15))
        ttk.RadioButton(
            radio_frame, text="Second", value=2, variable=radio_var
        ).pack(side=LEFT, padx=(0, 15))
        ttk.RadioButton(
            radio_frame, text="Third", value=3, variable=radio_var, state=DISABLED
        ).pack(side=LEFT)

        # Toggle buttons row
        toggle_frame = ttk.Frame(group)
        toggle_frame.pack(fill=X)

        t1 = ttk.CheckButton(
            toggle_frame, text="Primary Toggle", bootstyle="primary-toggle"
        )
        t1.pack(side=LEFT, padx=(0, 10))
        t1.invoke()

        t2 = ttk.CheckButton(
            toggle_frame, text="Success Toggle", bootstyle="success-toggle"
        )
        t2.pack(side=LEFT, padx=(0, 10))

        t3 = ttk.CheckButton(
            toggle_frame, text="Info Toggle", bootstyle="info-toggle"
        )
        t3.pack(side=LEFT)

    def _build_progress_section(self, parent):
        """Build progress indicators section."""
        group = ttk.LabelFrame(parent, text="Progress & Meters", padding=15)
        group.pack(fill=X, pady=(0, 10))

        # Scale with signal
        scale_frame = ttk.Frame(group)
        scale_frame.pack(fill=X, pady=(0, 10))
        ttk.Label(scale_frame, text="Scale:").pack(side=LEFT)
        ttk.Scale(
            scale_frame, from_=0, to=100, signal=self.slider_value
        ).pack(side=LEFT, fill=X, expand=YES, padx=10)

        # Progress bars
        ttk.Progressbar(
            group, signal=self.slider_value, maximum=100
        ).pack(fill=X, pady=(0, 8))

        ttk.Progressbar(
            group, value=75, maximum=100, bootstyle="success-striped"
        ).pack(fill=X, pady=(0, 8))

        # Meter widget
        meter_frame = ttk.Frame(group)
        meter_frame.pack(fill=X, pady=(0, 5))

        meter = ttk.Meter(
            meter_frame,
            metersize=120,
            amountused=45,
            amounttotal=100,
            subtext="CPU Usage",
            bootstyle="info",
            interactive=True,
        )
        meter.pack(side=LEFT, padx=(0, 20))

        meter2 = ttk.Meter(
            meter_frame,
            metersize=120,
            amountused=78,
            amounttotal=100,
            subtext="Memory",
            bootstyle="warning",
            interactive=True,
        )
        meter2.pack(side=LEFT)

    def _build_data_section(self, parent):
        """Build data display section."""
        group = ttk.LabelFrame(parent, text="Data Display", padding=15)
        group.pack(fill=X, pady=(0, 10))

        # Treeview/Table
        columns = ("name", "status", "progress")
        tree = ttk.TreeView(group, columns=columns, show="headings", height=5)

        tree.heading("name", text="Task Name")
        tree.heading("status", text="Status")
        tree.heading("progress", text="Progress")

        tree.column("name", width=150)
        tree.column("status", width=80, anchor=CENTER)
        tree.column("progress", width=80, anchor=CENTER)

        # Sample data
        data = [
            ("Database Migration", "Complete", "100%"),
            ("API Integration", "In Progress", "65%"),
            ("UI Redesign", "In Progress", "40%"),
            ("Testing Suite", "Pending", "0%"),
            ("Documentation", "In Progress", "80%"),
        ]
        for item in data:
            tree.insert("", END, values=item)

        tree.pack(fill=X)
        tree.selection_set(tree.get_children()[0])

    def _build_text_section(self, parent):
        """Build text and notebook section."""
        group = ttk.LabelFrame(parent, text="Notebook & Text", padding=15)
        group.pack(fill=BOTH, expand=YES)

        # Notebook
        notebook = ttk.Notebook(group)
        notebook.pack(fill=BOTH, expand=YES)

        # Tab 1 - Text widget
        text_frame = ttk.Frame(notebook, padding=10)
        notebook.add(text_frame, text="Text Editor")

        text = ttk.ScrolledText(text_frame, height=6, autohide=True)
        text.pack(fill=BOTH, expand=YES)
        text.insert(END, "ttkbootstrap v2 provides:\n\n")
        text.insert(END, "\u2022 Modern themed widgets\n")
        text.insert(END, "\u2022 Semantic color tokens\n")
        text.insert(END, "\u2022 Typography system\n")
        text.insert(END, "\u2022 Reactive signals\n")
        text.insert(END, "\u2022 Layout containers\n")

        # Tab 2 - Date picker
        date_frame = ttk.Frame(notebook, padding=10)
        notebook.add(date_frame, text="Date Picker")

        ttk.DateEntry(date_frame).pack(anchor=NW)

        # Tab 3 - Scrollbars demo
        scroll_frame = ttk.Frame(notebook, padding=10)
        notebook.add(scroll_frame, text="Scrollbars")

        sb1 = ttk.Scrollbar(scroll_frame, orient=HORIZONTAL)
        sb1.set(0.2, 0.6)
        sb1.pack(fill=X, pady=(0, 8))

        sb2 = ttk.Scrollbar(scroll_frame, orient=HORIZONTAL, bootstyle="danger")
        sb2.set(0.4, 0.8)
        sb2.pack(fill=X, pady=(0, 8))

        sb3 = ttk.Scrollbar(scroll_frame, orient=HORIZONTAL, bootstyle="success")
        sb3.set(0.1, 0.5)
        sb3.pack(fill=X)


def setup_demo(master):
    """Setup the demo widgets - legacy compatibility."""
    showcase = WidgetShowcase(master)
    return showcase.master.winfo_children()[0]


def run_demo():
    """Run the ttkbootstrap demo application."""
    app = ttk.App(title="ttkbootstrap Demo", size=(900, 700))
    WidgetShowcase(app)
    app.place_center()
    app.mainloop()
