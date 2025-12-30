import ttkbootstrap as ttk


class RadioGroupDemo(ttk.App):
    def __init__(self):
        super().__init__(title="RadioGroup Demo")
        self.geometry("900x700")
        self.pack_propagate(False)

        # --- 1. Basic RadioGroup with Signal ---
        ttk.Label(self, text="Basic RadioGroup (Label on Top)", font="-weight bold").pack(pady=(10, 5))

        size_signal = ttk.Signal("medium")

        size_group = ttk.RadioGroup(
            self,
            text="Select Size:",
            signal=size_signal,
            orient='horizontal'
        )
        size_group.add("Small", "small")
        size_group.add("Medium", "medium")
        size_group.add("Large", "large")
        size_group.pack(pady=5)

        # Live update label
        size_label = ttk.Label(self, text=f"Selected Size: {size_signal.get()}")
        size_label.pack()
        size_signal.subscribe(lambda v: size_label.configure(text=f"Selected Size: {v}"))

        # --- 2. Different Label Positions ---
        ttk.Label(self, text="Different Label Positions", font="-weight bold").pack(pady=(10, 5))

        label_frame = ttk.Frame(self)
        label_frame.pack(pady=5, fill='x', padx=20)

        # Left label
        left_group = ttk.RadioGroup(
            label_frame,
            text="Color:",
            labelanchor='w',
            value='blue',
            color='info'
        )
        left_group.add("Red", "red")
        left_group.add("Green", "green")
        left_group.add("Blue", "blue")
        left_group.pack(side='left', padx=10, pady=5)

        # Right label
        right_group = ttk.RadioGroup(
            label_frame,
            text="Theme:",
            labelanchor='e',
            value='dark',
            color='secondary'
        )
        right_group.add("Light", "light")
        right_group.add("Dark", "dark")
        right_group.pack(side='left', padx=10, pady=5)

        # --- 3. Vertical Orientation with Bottom Label ---
        ttk.Label(self, text="Vertical Orientation (Label on Bottom)", font="-weight bold").pack(pady=(10, 5))

        priority_group = ttk.RadioGroup(
            self,
            text="Select Priority Level",
            labelanchor='s',
            orient='vertical',
            value='medium',
            color='warning'
        )
        priority_group.add("Low Priority", "low")
        priority_group.add("Medium Priority", "medium")
        priority_group.add("High Priority", "high")
        priority_group.add("Critical", "critical")
        priority_group.pack(pady=5)

        # --- 4. Different Bootstyles ---
        ttk.Label(self, text="Different Bootstyles", font="-weight bold").pack(pady=(10, 5))

        style_frame = ttk.Frame(self)
        style_frame.pack(pady=5)

        # Primary style
        primary_group = ttk.RadioGroup(
            style_frame,
            text="Primary:",
            labelanchor='w',
            color='primary',
            value='opt2'
        )
        primary_group.add("Opt 1", "opt1")
        primary_group.add("Opt 2", "opt2")
        primary_group.add("Opt 3", "opt3")
        primary_group.pack(side='left', padx=10)

        # Success style
        success_group = ttk.RadioGroup(
            style_frame,
            text="Success:",
            labelanchor='w',
            color='success',
            value='yes'
        )
        success_group.add("Yes", "yes")
        success_group.add("No", "no")
        success_group.pack(side='left', padx=10)

        # Danger style
        danger_group = ttk.RadioGroup(
            style_frame,
            text="Danger:",
            labelanchor='w',
            color='danger',
            value='b'
        )
        danger_group.add("A", "a")
        danger_group.add("B", "b")
        danger_group.pack(side='left', padx=10)

        # --- 5. With Callbacks (on_changed / off_changed) ---
        ttk.Label(self, text="With Event Callbacks", font="-weight bold").pack(pady=(10, 5))

        callback_label = ttk.Label(self, text="Callback not triggered yet")
        callback_label.pack()

        def on_preference_change(value):
            callback_label.configure(text=f"Callback triggered! New value: {value}")

        preference_group = ttk.RadioGroup(
            self,
            text="Email Preference:",
            labelanchor='n',
            orient='horizontal',
            value='daily',
            color='info'
        )
        preference_group.add("Immediate", "immediate")
        preference_group.add("Daily Digest", "daily")
        preference_group.add("Weekly Summary", "weekly")
        preference_group.add("Never", "never")
        preference_group.pack(pady=5)

        # Subscribe to changes
        sub_id = preference_group.on_changed(on_preference_change)

        # --- 6. Dynamic Configuration ---
        ttk.Label(self, text="Dynamic Configuration", font="-weight bold").pack(pady=(10, 5))

        config_group = ttk.RadioGroup(
            self,
            text="Mode:",
            labelanchor='n',
            orient='horizontal',
            value='mode1'
        )
        config_group.add("Mode 1", "mode1")
        config_group.add("Mode 2", "mode2")
        config_group.add("Mode 3", "mode3")
        config_group.pack(pady=5)

        # Buttons to dynamically change configuration
        button_frame = ttk.Frame(self)
        button_frame.pack(pady=5)

        ttk.Button(
            button_frame,
            text="Switch to Vertical",
            command=lambda: config_group.configure(orient='vertical')
        ).pack(side='left', padx=5)

        ttk.Button(
            button_frame,
            text="Switch to Horizontal",
            command=lambda: config_group.configure(orient='horizontal')
        ).pack(side='left', padx=5)

        ttk.Button(
            button_frame,
            text="Change to Success Style",
            command=lambda: config_group.configure(color='success')
        ).pack(side='left', padx=5)

        ttk.Button(
            button_frame,
            text="Move Label to Left",
            command=lambda: config_group.configure(labelanchor='w')
        ).pack(side='left', padx=5)


if __name__ == "__main__":
    app = RadioGroupDemo()
    app.mainloop()