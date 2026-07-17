"""Screenshot scenes for docs/widgets/text.rst."""

import ttkbootstrap as ttk


def hero():
    app = ttk.App(title="Text")
    frm = ttk.Frame(app, padding=10).pack()

    text = ttk.Text(frm, width=40, height=6)
    text.pack()

    text.insert("end", "Meeting notes\n\n")
    text.insert("end", "Review the draft with the team, then\n")
    text.insert("end", "send the final version to print by\n")
    text.insert("end", "Friday.\n")

    colors = ttk.Style.get_instance().colors
    text.tag_configure("hl", background=colors.warning,
                       foreground=colors.get_foreground("warning"))
    text.tag_add("hl", "5.0", "5.6")  # highlight "Friday"

    app.mainloop()


SCENES = {
    "hero": hero,
}
