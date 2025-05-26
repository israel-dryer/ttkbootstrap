from ttkbootstrap.window import Window

from ttkbootstrap.widgets import (
    Badge, CheckBox,
    Button, CheckBoxToggle, RadioToggle,
    Button, CheckBoxToggle, RadioToggle, TextBox,
    IconButton, Radiobutton, Switch, Frame, Slider, Toast,

)

app = Window()

frame = Frame(app, padding=10)
frame.pack(fill="both", padx=20, pady=20, expand=True)
# IconButton(frame, icon="sun-fill", color="warning", command=lambda: app.theme_manager.use_theme("light")).pack(pady=2, padx=2)
# IconButton(frame, icon="moon-fill", color="dark", command=lambda: app.theme_manager.use_theme("dark")).pack(pady=2, padx=2)
# Button(frame, text="Disabled", color="success", state="disabled").pack(pady=2, padx=2)
# Button(frame, text="Minty", variant="outline", command=lambda: app.theme_manager.use_theme("minty")).pack(pady=2, padx=2)
# Button(frame, icon="person", text="Superhero", variant="outline", color="warning", command=lambda: app.theme_manager.use_theme("superhero")).pack(pady=2, padx=2)
# Button(frame, text="Cosmo", variant="outline", color="success", state="disabled").pack(pady=2, padx=2)
# Button(frame, text="Text", variant="text").pack(pady=2, padx=2)
# Button(frame, text="Text", color="danger", variant="text").pack(pady=2, padx=2)
# Button(frame, text="Text", color="success", variant="text", state="disabled").pack(pady=2, padx=2)
# CheckBox(frame, text="Checkbutton").pack(pady=2, padx=2)
# CheckBox(frame, text="Checkbutton", color="danger").pack(pady=2, padx=2, fill='x', expand=1)
# Switch(frame, text="Switch").pack(pady=2, padx=2)
# Switch(frame, color="success").pack(pady=2, padx=2, fill='x', expand=1)
# Radiobutton(frame, text="Radio 1", value=2).pack(pady=2, padx=2, fill='x', expand=1)
# Radiobutton(frame, text="Radio 2", value=3, color="success").pack(pady=2, padx=2, fill='x', expand=1)
# TextBox(frame).pack(padx=2, pady=2, fill='x', expand=1)
# Slider(frame, color="warning").pack(padx=2, pady=2, expand=1, fill='x')
# Slider(frame, orient="vertical", color="danger").pack(padx=2, pady=2, expand=1, fill='y')
# CheckBoxToggle(frame, text="One").pack(side="left", padx=2, pady=2)
# CheckBoxToggle(frame, text="Two", color="info").pack(side="left", padx=2, pady=2)
# CheckBoxToggle(frame, text="Three").pack(side="left", padx=2, pady=2)
# CheckBoxToggle(frame, text="disabled", state="disabled").pack(side="left", padx=2, pady=2)
# RadioToggle(frame, text="One", value="one").pack(padx=2, pady=2)
# RadioToggle(frame, text="Two", value="two").pack(side="left", padx=2, pady=2)
# RadioToggle(frame, text="Three", value="three").pack(side="left", padx=2, pady=2)

Badge(frame, text="100 Votes").pack(padx=10, pady=10)
Badge(frame, variant="pill", text="100 Votes", color="danger").pack(padx=10, pady=10)
Badge(frame, text="1", color="success", variant="circle").pack(padx=10, pady=10)

toast = Toast(app, toast_type="success", message="Something bad has happened", close_on_click=True)
app.after(500, toast.show)



app.mainloop()
