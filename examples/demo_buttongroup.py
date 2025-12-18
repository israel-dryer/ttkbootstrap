import ttkbootstrap as ttk
from tkinter import messagebox, Menu

from ttkbootstrap import ContextMenu, ContextMenuItem


class ButtonGroupDemo(ttk.App):
    def __init__(self):
        super().__init__(title="ButtonGroup Demo")
        self.geometry("800x800")
        self.pack_propagate(False)

        # --- 1. Basic Horizontal ButtonGroup ---
        ttk.Label(self, text="Basic Horizontal ButtonGroup", font="-weight bold").pack(pady=(10, 5))

        file_ops = ttk.ButtonGroup(self, bootstyle='primary')
        file_ops.add("New", command=lambda: self.show_action("New"))
        file_ops.add("Open", command=lambda: self.show_action("Open"))
        file_ops.add("Save", command=lambda: self.show_action("Save"))
        file_ops.add("Save As", command=lambda: self.show_action("Save As"))
        file_ops.pack(pady=5)

        # --- 2. Vertical ButtonGroup ---
        ttk.Label(self, text="Vertical ButtonGroup", font="-weight bold").pack(pady=(10, 5))

        edit_ops = ttk.ButtonGroup(self, orient='vertical', bootstyle='success')
        edit_ops.add("Cut", command=lambda: self.show_action("Cut"))
        edit_ops.add("Copy", command=lambda: self.show_action("Copy"))
        edit_ops.add("Paste", command=lambda: self.show_action("Paste"))
        edit_ops.add("Delete", command=lambda: self.show_action("Delete"))
        edit_ops.pack(pady=5)

        # --- 3. Different Bootstyles ---
        ttk.Label(self, text="Different Bootstyles", font="-weight bold").pack(pady=(10, 5))

        style_frame = ttk.Frame(self)
        style_frame.pack(pady=5)

        # Primary
        primary = ttk.ButtonGroup(style_frame, bootstyle='primary')
        primary.add("Btn 1")
        primary.add("Btn 2")
        primary.add("Btn 3")
        primary.pack(side='left', padx=5)

        # Info
        info = ttk.ButtonGroup(style_frame, bootstyle='info-outline')
        info.add("Btn 1")
        info.add("Btn 2")
        info.add("Btn 3")
        info.pack(side='left', padx=5)

        # Danger
        danger = ttk.ButtonGroup(style_frame, bootstyle='primary-ghost')
        danger.add("Btn 1")
        danger.add("Btn 2")
        danger.add("Btn 3")
        danger.pack(side='left', padx=5)

        # --- 4. Mixed Widget Types (with DropdownButton) ---
        ttk.Label(self, text="Mixed Widget Types - Toolbar Example", font="-weight bold").pack(pady=(10, 5))

        toolbar = ttk.ButtonGroup(self, bootstyle='secondary')
        toolbar.add("New", command=lambda: self.show_action("New File"))
        toolbar.add("Open", command=lambda: self.show_action("Open File"))
        toolbar.add("Save", command=lambda: self.show_action("Save File"))

        # Add a DropdownButton for export options
        dropdown = toolbar.add(
            "Export",
            widget_type=ttk.DropdownButton,
            key="export_menu",
            icon="caret-down-fill",
            compound="right"
        )

        # Create menu for the DropdownButton
        export_menu = Menu(dropdown, tearoff=False)
        export_menu.add_command(label="Export as PDF", command=lambda: self.show_action("Export as PDF"))
        export_menu.add_command(label="Export as HTML", command=lambda: self.show_action("Export as HTML"))
        export_menu.add_command(label="Export as CSV", command=lambda: self.show_action("Export as CSV"))
        export_menu.add_separator()
        export_menu.add_command(label="Export All", command=lambda: self.show_action("Export All"))
        dropdown.configure(menu=export_menu)

        toolbar.pack(pady=5)

        # --- 5. Split Button Pattern ---
        ttk.Label(self, text="Split Button Pattern", font="-weight bold").pack(pady=(10, 5))

        split_button_frame = ttk.Frame(self)
        split_button_frame.pack(pady=5)

        # Split button for "Save" action
        save_split = ttk.ButtonGroup(split_button_frame, bootstyle='primary')
        save_split.add("Save", command=lambda: self.show_action("Save (default action)"))

        # Add icon-only dropdown for save options
        save_dropdown = save_split.add(
            widget_type=ttk.DropdownButton,
            key="save_options",
            icon="caret-down-fill",
            padding=0,
            compound="center"
        )

        # Create menu for save options
        save_menu = Menu(save_dropdown, tearoff=False)
        save_menu.add_command(label="Save", command=lambda: self.show_action("Save"))
        save_menu.add_command(label="Save As...", command=lambda: self.show_action("Save As"))
        save_menu.add_command(label="Save All", command=lambda: self.show_action("Save All"))
        save_menu.add_separator()
        save_menu.add_command(label="Save Copy...", command=lambda: self.show_action("Save Copy"))
        save_dropdown.configure(menu=save_menu)

        save_split.pack(side='left', padx=5)

        # Split button for "Run" action with success style
        run_split = ttk.ButtonGroup(split_button_frame, bootstyle='success')
        run_split.add("Run", command=lambda: self.show_action("Run (default)"))

        run_dropdown = run_split.add(
            widget_type=ttk.DropdownButton,
            key="run_options",
            icon="caret-down-fill",
            popdown_options={"anchor": "ne", "attach": "se", "offset": (0, 2)},
            items=[ContextMenuItem('command', text='Run'), ContextMenuItem('command', text='Run with Debugger'), ContextMenuItem('command', text='Run Tests')],
            padding=0,
            compound="center"
        )

        run_split.pack(side='left', padx=5)

        # --- 6. With Custom Keys ---
        ttk.Label(self, text="With Custom Keys (Disable/Enable Example)", font="-weight bold").pack(pady=(10, 5))

        keyed_group = ttk.ButtonGroup(self, bootstyle='secondary')
        keyed_group.add("Action 1", key="action1", command=lambda: self.show_action("Action 1"))
        keyed_group.add("Action 2", key="action2", command=lambda: self.show_action("Action 2"))
        keyed_group.add("Action 3", key="action3", command=lambda: self.show_action("Action 3"))
        keyed_group.pack(pady=5)

        # Control buttons
        control_frame = ttk.Frame(self)
        control_frame.pack(pady=5)

        ttk.Button(
            control_frame,
            text="Disable Action 2",
            command=lambda: keyed_group.configure_widget("action2", state='disabled')
        ).pack(side='left', padx=5)

        ttk.Button(
            control_frame,
            text="Enable Action 2",
            command=lambda: keyed_group.configure_widget("action2", state='normal')
        ).pack(side='left', padx=5)

        # --- 7. Dynamic Configuration ---
        ttk.Label(self, text="Dynamic Configuration", font="-weight bold").pack(pady=(10, 5))

        dynamic_group = ttk.ButtonGroup(self, bootstyle='warning')
        dynamic_group.add("Option A")
        dynamic_group.add("Option B")
        dynamic_group.add("Option C")
        dynamic_group.pack(pady=5)

        config_frame = ttk.Frame(self)
        config_frame.pack(pady=5)

        ttk.Button(
            config_frame,
            text="Switch to Vertical",
            command=lambda: dynamic_group.configure(orient='vertical')
        ).pack(side='left', padx=5)

        ttk.Button(
            config_frame,
            text="Switch to Horizontal",
            command=lambda: dynamic_group.configure(orient='horizontal')
        ).pack(side='left', padx=5)

        ttk.Button(
            config_frame,
            text="Change to Success Style",
            command=lambda: dynamic_group.configure(bootstyle='success')
        ).pack(side='left', padx=5)

        ttk.Button(
            config_frame,
            text="Disable All",
            command=lambda: dynamic_group.configure(state='disabled')
        ).pack(side='left', padx=5)

        ttk.Button(
            config_frame,
            text="Enable All",
            command=lambda: dynamic_group.configure(state='normal')
        ).pack(side='left', padx=5)

        # --- 8. Add/Remove Widgets Dynamically ---
        ttk.Label(self, text="Dynamic Add/Remove", font="-weight bold").pack(pady=(10, 5))

        self.dynamic_add_group = ttk.ButtonGroup(self, bootstyle='dark')
        self.dynamic_add_group.add("Button 1", key="btn1")
        self.dynamic_add_group.add("Button 2", key="btn2")
        self.dynamic_add_group.pack(pady=5)

        self.button_counter = 3

        add_remove_frame = ttk.Frame(self)
        add_remove_frame.pack(pady=5)

        ttk.Button(
            add_remove_frame,
            text="Add Button",
            command=self.add_button
        ).pack(side='left', padx=5)

        ttk.Button(
            add_remove_frame,
            text="Remove Last Button",
            command=self.remove_last_button
        ).pack(side='left', padx=5)

        ttk.Button(
            add_remove_frame,
            text="Clear All",
            command=lambda: self.dynamic_add_group.clear()
        ).pack(side='left', padx=5)

        # --- 9. Information Display ---
        ttk.Label(self, text="Widget Info", font="-weight bold").pack(pady=(10, 5))

        info_group = ttk.ButtonGroup(self, bootstyle='info')
        info_group.add("Alpha", key="a")
        info_group.add("Beta", key="b")
        info_group.add("Gamma", key="c")
        info_group.pack(pady=5)

        info_label = ttk.Label(
            self,
            text=f"Widget count: {len(info_group)}, Keys: {info_group.keys()}"
        )
        info_label.pack(pady=5)

        ttk.Button(
            self,
            text="Check 'b' in group",
            command=lambda: messagebox.showinfo("Check", f"'b' in group: {'b' in info_group}")
        ).pack(pady=5)

    def show_action(self, action):
        """Display which action was clicked."""
        messagebox.showinfo("Action", f"You clicked: {action}")

    def add_button(self):
        """Add a new button to the dynamic group."""
        key = f"btn{self.button_counter}"
        button_num = self.button_counter  # Capture value, not reference
        self.dynamic_add_group.add(
            f"Button {button_num}",
            key=key,
            command=lambda num=button_num: self.show_action(f"Button {num}")
        )
        self.button_counter += 1

    def remove_last_button(self):
        """Remove the last button from the dynamic group."""
        keys = self.dynamic_add_group.keys()
        if keys:
            last_key = keys[-1]
            self.dynamic_add_group.remove(last_key)


if __name__ == "__main__":
    app = ButtonGroupDemo()
    app.mainloop()