# App

::: ttkbootstrap.runtime.app.App
    options:
        inherited_members:
            # Window manager pass-throughs
            - show
            - title
            - geometry
            - state
            - attributes
            - iconify
            - deiconify
            - withdraw
            - resizable
            - minsize
            - maxsize
            - transient
            - protocol
            - overrideredirect
            # Convenience wrappers
            - on_close
            - hide
            - minimize
            - maximize
            - set_topmost
            - set_fullscreen
            - set_alpha
            # Positioning utilities
            - place_center
            - place_center_on
            - place_at
            - place_anchor
            - place_dropdown
            - place_cursor
            # Sizing utilities
            - set_default_size
            - apply_size_constraints
            # Introspection
            - winfo_width
            - winfo_height
            - winfo_reqwidth
            - winfo_reqheight
            - winfo_rootx
            - winfo_rooty
            - winfo_screenwidth
            - winfo_screenheight
            - winfo_pointerx
            - winfo_pointery
            - winfo_pointerxy
