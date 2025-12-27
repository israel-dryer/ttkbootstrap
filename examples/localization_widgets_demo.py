"""
Demonstrates ttkbootstrap localization with MessageCatalog on common widgets.

What this shows:
- Initialize the i18n bridge (Babel/gettext + Tcl msgcat)
- Mark strings for translation via `_ = MessageCatalog.translate`
- Switch languages at runtime and refresh widget text
- Use printf-style placeholders with translate (legacy Tcl style supported)

Run:
    python examples/localization_widgets_demo.py

Tip:
    Make sure you've compiled catalogs first:
        python tools/make_i18n.py compile -d locales -D ttkbootstrap
"""
from __future__ import annotations
import ttkbootstrap as tb
from ttkbootstrap.dialogs import MessageBox
from ttkbootstrap.core.localization import MessageCatalog


def main():
    # Create the app window (auto-inits i18n via Style)
    app = tb.App(theme="flatly")

    # Style auto-initializes MessageCatalog with auto-discovery; no manual init needed.
    print('tcl locale code', MessageCatalog.locale('zh_CN'))
    print(MessageCatalog.translate('Cancel'))

    # Recommended alias so you can write _(...) around user-facing strings
    _ = MessageCatalog.translate

    # Simple function to apply current language to all dynamic strings
    def apply_language():
        app.title(_("Localization Demo"))
        lbl_hello.configure(text=_("Hello, world!"))
        lbl_hint.configure(text=_("Choose a language:"))
        btn_ok.configure(text=_("OK"))
        btn_cancel.configure(text=_("Cancel"))
        # Obvious samples
        sample_cancel.configure(text="Cancel -> " + _("Cancel"))
        sample_open.configure(text="Open -> " + _("Open"))
        # Menu labels (0-based)
        menubar.entryconfig(0, label=_("Open"))
        menubar.entryconfig(1, label=_("Close"))
        menubar.entryconfig(2, label=_("Exit"))
        # Formatting example (works with both %s and legacy %1$s styles)
        fmt_label.configure(text=MessageCatalog.translate("test with string: '%s'", entry_var.get()))
        print("Active:", MessageCatalog.locale(), "Cancel:", MessageCatalog.translate("Cancel"))

    # Menu with a few common actions using localized labels
    menubar = tb.Menu(app)
    app.configure(menu=menubar)

    def do_open():
        MessageBox.show_info(title=_("Open"), message=_("Open"))

    def do_close():
        MessageBox.show_info(title=_("Close"), message=_("Close"))

    menubar.add_command(label=_("Open"), command=do_open)
    menubar.add_command(label=_("Close"), command=do_close)
    menubar.add_command(label=_("Exit"), command=app.destroy)

    # Main content
    container = tb.Frame(app, padding=20)
    container.pack(fill="both", expand=True)

    lbl_hello = tb.Label(container, text=_("Hello, world!"))
    lbl_hello.pack(anchor="w")

    lbl_hint = tb.Label(container, text=_("Choose a language:"))
    lbl_hint.pack(anchor="w", pady=(12, 4))

    # Language selector (discover languages from compiled catalogs)
    # Available language list (keep simple for demo)
    langs = ["en", "de", "fr", "nl", "zh_CN"]
    start_lang = "nl"
    lang_var = tb.StringVar(value=start_lang)

    def on_lang_change(*_):
        MessageCatalog.locale(lang_var.get())

    lang_menu = tb.OptionMenu(container, lang_var.get(), langs, textvariable=lang_var)
    lang_var.trace("w", on_lang_change)
    lang_menu.pack(anchor="w")

    # Row of localized buttons
    btn_row = tb.Frame(container)
    btn_row.pack(fill="x", pady=(16, 0))
    btn_ok = tb.Button(btn_row, text=_("OK"), width=12, command=lambda: MessageBox.show_info(_("OK"), _("OK")))
    btn_ok.pack(side="left", padx=(0, 8))
    btn_cancel = tb.Button(
        btn_row, text=_("Cancel"), width=12, command=lambda: MessageBox.show_info(_("Cancel"), _("Cancel")))
    btn_cancel.pack(side="left")

    # Formatting example using translate with a value from an entry
    entry_var = tb.StringVar(value="string value")
    entry = tb.Entry(container, textvariable=entry_var, width=30)
    entry.pack(anchor="w", pady=(16, 4))
    fmt_label = tb.Label(container)
    fmt_label.pack(anchor="w")

    # Always-present samples for obvious change
    sample_row = tb.Frame(container)
    sample_row.pack(anchor="w", pady=(8, 0))
    sample_cancel = tb.Label(sample_row)
    sample_cancel.pack(side="left", padx=(0, 12))
    sample_open = tb.Label(sample_row)
    sample_open.pack(side="left")

    def on_entry_change(*_):
        fmt_label.configure(text=MessageCatalog.translate("test with string: '%s'", entry_var.get()))

    entry_var.trace_add("write", on_entry_change)

    # Initial text
    apply_language()

    app.geometry("520x320")
    # React to locale changes via virtual event emitted by MessageCatalog
    app.bind("<<LocaleChanged>>", lambda e: apply_language())

    app.mainloop()


if __name__ == "__main__":
    main()
