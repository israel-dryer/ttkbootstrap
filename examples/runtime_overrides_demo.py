"""
Runtime Overrides Demo

Shows how to add translations at runtime for messages that are not in
compiled catalogs yet using MessageCatalog.set and MessageCatalog.set_many.

Run:
    python examples/runtime_overrides_demo.py
"""
from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mbox

import ttkbootstrap as tb
from ttkbootstrap.localization.msgcat import MessageCatalog


def main():
    app = tb.Window(theme="flatly")
    _ = MessageCatalog.translate

    # UI
    app.title(_("Runtime Overrides Demo"))
    app.geometry("640x360")
    container = ttk.Frame(app, padding=16)
    container.pack(fill="both", expand=True)

    # Labels and buttons that will be translated using overrides
    lbl_title = ttk.Label(container, text=_("Hello, world!"))
    lbl_title.pack(anchor="w")

    lbl_hint = ttk.Label(container, text=_("Choose a language:"))
    lbl_hint.pack(anchor="w", pady=(8, 4))

    # Language selector
    langs = ["en", "de", "fr", "nl"]
    current = tk.StringVar(value="en")

    def refresh():
        app.title(_("Runtime Overrides Demo"))
        lbl_title.configure(text=_("Hello, world!"))
        lbl_hint.configure(text=_("Choose a language:"))
        btn_ok.configure(text=_("OK"))
        btn_cancel.configure(text=_("Cancel"))
        sample.configure(text=f"Cancel -> { _('Cancel') } | Open -> { _('Open') }")

    # React to MessageCatalog's virtual event
    app.bind("<<LocaleChanged>>", lambda e: refresh())

    opt = ttk.OptionMenu(container, current, current.get(), *langs,
                         command=lambda *_: MessageCatalog.locale(current.get()))
    opt.pack(anchor="w")

    # Buttons
    row = ttk.Frame(container)
    row.pack(anchor="w", pady=(12, 0))
    btn_ok = ttk.Button(row, width=16, text=_("OK"), command=lambda: mbox.showinfo(_("OK"), _("OK")))
    btn_ok.pack(side="left", padx=(0, 8))
    btn_cancel = ttk.Button(row, width=16, text=_("Cancel"), command=lambda: mbox.showinfo(_("Cancel"), _("Cancel")))
    btn_cancel.pack(side="left")

    # Sample always-visible reference
    sample = ttk.Label(container)
    sample.pack(anchor="w", pady=(10, 8))

    # Runtime overrides actions
    actions = ttk.Frame(container)
    actions.pack(anchor="w", pady=(8, 0))

    def apply_fr_overrides():
        # Add French translations for keys that may not be in .po yet
        MessageCatalog.set_many(
            "fr",
            "Runtime Overrides Demo", "Demo des remplacements a l'execution",
            "Hello, world!", "Bonjour le monde !",
            "Choose a language:", "Choisissez une langue :",
            "OK", "OK",
            "Cancel", "Annuler",
            "Open", "Ouvrir",
            "Close", "Fermer",
            "Exit", "Quitter",
        )
        if MessageCatalog.locale().lower().startswith("fr"):
            app.event_generate("<<LocaleChanged>>", when="tail")

    def apply_de_overrides():
        MessageCatalog.set_many(
            "de",
            "Runtime Overrides Demo", "Laufzeitueberschreibungen Demo",
            "Hello, world!", "Hallo Welt!",
            "Choose a language:", "Waehlen Sie eine Sprache:",
            "OK", "OK",
            "Cancel", "Abbrechen",
            "Open", "Oeffnen",
            "Close", "Schliessen",
            "Exit", "Beenden",
        )
        if MessageCatalog.locale().lower().startswith("de"):
            app.event_generate("<<LocaleChanged>>", when="tail")

    def apply_nl_overrides():
        MessageCatalog.set_many(
            "nl",
            "Runtime Overrides Demo", "Runtime-overschrijvingen Demo",
            "Hello, world!", "Hallo wereld!",
            "Choose a language:", "Kies een taal:",
            "OK", "OK",
            "Cancel", "Annuleren",
            "Open", "Openen",
            "Close", "Sluiten",
            "Exit", "Afsluiten",
        )
        if MessageCatalog.locale().lower().startswith("nl"):
            app.event_generate("<<LocaleChanged>>", when="tail")

    ttk.Button(actions, text="Apply FR overrides", command=apply_fr_overrides).pack(side="left", padx=(0, 8))
    ttk.Button(actions, text="Apply DE overrides", command=apply_de_overrides).pack(side="left", padx=(0, 8))
    ttk.Button(actions, text="Apply NL overrides", command=apply_nl_overrides).pack(side="left")

    # Initial paint
    refresh()
    app.mainloop()


if __name__ == "__main__":
    main()


