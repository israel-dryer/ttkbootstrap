import ttkbootstrap as ttk

from ttkbootstrap.widgets.mixins.validation_mixin import ValidationMixin


class ValidatedEntry(ValidationMixin, ttk.Entry):

    def __init__(self, master=None, *args, **kwargs):
        super().__init__(master=None, *args, **kwargs)


root = ttk.Window()

ValidatedEntry(root).pack()

entry = ValidatedEntry(root)
entry.pack()
entry.add_validation_rule('required')
entry.on_validated(lambda e: print(e, entry.value()))
entry.on_invalid(lambda e: print(e, entry.value()))
entry.on_valid(lambda e: print(e, entry.value()))


root.mainloop()
