"""
Surfaces Demo

Demonstrates the semantic surface tokens with automatic tinting:
- chrome: UI shell (sidebars, toolbars, navigation)
- content: Main content area background
- card: Elevated content (cards, panels)
- overlay: Floating elements (menus, dialogs)
- input: Form control backgrounds

Each surface has matching foreground tokens (on_chrome, on_content, etc.)
that provide correct text contrast automatically.
"""

import ttkbootstrap as ttk
from ttkbootstrap.style.theme_provider import use_theme
from ttkbootstrap.style.style import set_theme


def create_surface_swatch(parent, surface_name: str, description: str):
    """Create a labeled swatch showing a surface and its foreground."""
    frame = ttk.Frame(parent, surface=surface_name, padding=15)
    frame.pack(fill='x', pady=4)

    # Get the actual color values for display
    theme = use_theme()
    bg_color = theme.colors.get(surface_name, '?')
    fg_color = theme.colors.get(f'on_{surface_name}', '?')

    # Primary text
    ttk.Label(
        frame,
        text=surface_name,
        font='heading-md'
    ).pack(anchor='w')

    # Secondary text with description
    ttk.Label(
        frame,
        text=description,
        font='body-sm'
    ).pack(anchor='w', pady=(2, 8))

    # Color values
    info = ttk.Frame(frame, surface=surface_name)
    info.pack(fill='x')

    ttk.Label(
        info,
        text=f'bg: {bg_color}',
        font='mono-sm'
    ).pack(side='left')

    ttk.Label(
        info,
        text=f'fg: {fg_color}',
        font='mono-sm'
    ).pack(side='right')

    return frame


def create_stroke_swatch(parent, stroke_name: str):
    """Create a swatch showing a stroke/border color."""
    theme = use_theme()
    color = theme.colors.get(stroke_name, '#888888')

    frame = ttk.Frame(parent, padding=(15, 10))
    frame.pack(fill='x', pady=2)

    # Color bar
    bar = ttk.Frame(frame, height=4)
    bar.pack(fill='x', pady=(0, 8))
    bar.configure(style=f'{stroke_name}.TFrame')

    # Create a dynamic style for the color bar
    style = ttk.Style()
    style.configure(f'{stroke_name}.TFrame', background=color)

    # Label
    ttk.Label(frame, text=f'{stroke_name}: {color}', font='mono-sm').pack(anchor='w')

    return frame


def main():
    root = ttk.App(theme="rose-dark", title="Surfaces Demo", size=(900, 750))

    # Main container with content surface
    main = ttk.Frame(root, surface='content', padding=20)
    main.pack(fill='both', expand=True)

    # Header
    ttk.Label(main, text='Surface Tokens', font='heading-xl').pack(anchor='w', pady=(0, 5))
    ttk.Label(
        main,
        text='Semantic backgrounds with automatic tinting derived from theme',
        font='body-sm'
    ).pack(anchor='w', pady=(0, 20))

    # Create columns
    columns = ttk.Frame(main, surface='content')
    columns.pack(fill='both', expand=True)

    # Left column - Surfaces
    left = ttk.Frame(columns, surface='content')
    left.pack(side='left', fill='both', expand=True, padx=(0, 10))

    ttk.Label(left, text='Surfaces', font='heading-md').pack(anchor='w', pady=(0, 10))

    create_surface_swatch(left, 'chrome', 'Sidebars, toolbars, navigation')
    create_surface_swatch(left, 'content', 'Main content area')
    create_surface_swatch(left, 'card', 'Cards, panels, elevated content')
    create_surface_swatch(left, 'overlay', 'Menus, dialogs, tooltips')
    create_surface_swatch(left, 'input', 'Form control backgrounds')

    # Right column - Strokes
    right = ttk.Frame(columns, surface='content')
    right.pack(side='left', fill='both', expand=True, padx=(10, 0))

    ttk.Label(right, text='Strokes', font='heading-md').pack(anchor='w', pady=(0, 10))

    create_stroke_swatch(right, 'stroke')
    create_stroke_swatch(right, 'stroke_subtle')

    # Example card
    ttk.Label(right, text='Example Card', font='heading-md').pack(anchor='w', pady=(30, 10))

    card = ttk.Card(right)
    card.pack(fill='x')

    ttk.Label(card, text='Card Title', font='heading-sm').pack(anchor='w')
    ttk.Label(
        card,
        text='This card uses surface="card" and automatically gets the correct tinted background and foreground colors.',
        wraplength=300
    ).pack(anchor='w', pady=(5, 10))
    ttk.Button(card, text='Action').pack(anchor='w')

    # Theme switcher
    theme_frame = ttk.Frame(main, surface='content', padding=(0, 20, 0, 0))
    theme_frame.pack(fill='x', side='bottom')

    ttk.Label(theme_frame, text='Theme:').pack(side='left', padx=(0, 10))

    themes = ['rose-dark', 'rose-light', 'classic-dark', 'classic-light',
              'forest-dark', 'forest-light', 'ocean-dark', 'ocean-light']

    def switch_theme(name):
        set_theme(name)
        # Refresh the window to show new colors
        root.after(100, lambda: refresh_display())

    def refresh_display():
        # Update color value labels
        theme = use_theme()
        for child in main.winfo_children():
            pass  # Labels update automatically on theme change

    for theme in themes:
        btn = ttk.Button(
            theme_frame,
            text=theme,
            command=lambda t=theme: switch_theme(t),
        )
        btn.pack(side='left', padx=2)

    root.mainloop()


if __name__ == '__main__':
    main()
