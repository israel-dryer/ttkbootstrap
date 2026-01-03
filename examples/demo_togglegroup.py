import ttkbootstrap as ttk

class ToggleGroupDemo(ttk.App):
    def __init__(self):
        super().__init__(title="ToggleGroup Demo")
        self.geometry("800x600")
        self.pack_propagate(False)

        # --- 1. Single Mode (RadioToggle) with Icons and Signal ---
        ttk.Label(self, text="Single Mode (View Selector)", font="-weight bold").pack(pady=(10, 5))
        
        view_signal = ttk.Signal("grid")
        
        single_group = ttk.ToggleGroup(
            self,
            mode='single',
            signal=view_signal
        )
        single_group.add(text="Grid", value="grid", icon='grid-fill', icon_only=True)
        single_group.add(text="List", value="list", icon='list', icon_only=True)
        single_group.pack(pady=5)

        # Live update label for single mode
        single_label = ttk.Label(self, text=f"Selected View: {view_signal.get()}")
        single_label.pack()
        view_signal.subscribe(lambda v: single_label.configure(text=f"Selected View: {v}"))

        # --- 2. Multi Mode (CheckToggle) with Signal ---
        ttk.Label(self, text="Multi Mode (Filters)", font="-weight bold").pack(pady=(10, 5))

        filter_signal = ttk.Signal({'on_sale'})

        multi_group = ttk.ToggleGroup(
            self,
            mode='multi',
            signal=filter_signal,
            accent='success'
        )
        multi_group.add(text="In Stock", value="in_stock")
        multi_group.add(text="On Sale", value="on_sale")
        multi_group.add(text="Backorder", value="backorder")
        multi_group.pack(pady=1)

        # Live update label for multi mode
        multi_label = ttk.Label(self, text=f"Selected Filters: {filter_signal.get()}")
        multi_label.pack()
        filter_signal.subscribe(lambda v: multi_label.configure(text=f"Selected Filters: {v}"))

        # --- 3. Different Bootstyles ---
        ttk.Label(self, text="Different Bootstyles", font="-weight bold").pack(pady=(10, 5))

        style_frame = ttk.Frame(self)
        style_frame.pack(pady=5)

        # Outline style
        outline_group = ttk.ToggleGroup(style_frame, variant='outline', value='b')
        outline_group.add("A", "a")
        outline_group.add("B", "b")
        outline_group.pack(side='left', padx=10)

        # Ghost style
        ghost_group = ttk.ToggleGroup(style_frame, variant='ghost', accent='success', value='y')
        ghost_group.add("X", "x")
        ghost_group.add("Y", "y")
        ghost_group.pack(side='left', padx=10)

        # --- 4. Different Orientations ---
        ttk.Label(self, text="Vertical Orientation", font="-weight bold").pack(pady=(10, 5))

        vertical_group = ttk.ToggleGroup(
            self,
            mode='multi',
            orient='vertical',
            accent='danger',
            value={'red'}
        )
        vertical_group.add("Red", "red")
        vertical_group.add("Green", "green")
        vertical_group.add("Blue", "blue")
        vertical_group.pack(pady=5)


if __name__ == "__main__":
    app = ToggleGroupDemo()
    app.mainloop()
