import ttkbootstrap as ttk
from ttkbootstrap.widgets.toast import ToastNotification
from ttkbootstrap.constants import *

def show_basic_toast():
    ToastNotification(
        title="Basic Toast",
        message="This toast will disappear after 3 seconds.",
        duration=3000,
    ).show_toast()

def show_alert_toast():
    ToastNotification(
        title="Alert Toast",
        message="This toast rings the display bell and must be clicked to close.",
        alert=True,
    ).show_toast()

def show_custom_toast():
    ToastNotification(
        title="Custom Toast",
        message="This uses a custom color and icon!",
        color="danger",
        icon="🔥",
        duration=4000,
    ).show_toast()

def show_top_left_toast():
    ToastNotification(
        title="Top Left Toast",
        message="Positioned top-left of the screen.",
        position=(20, 20, "nw"),
        icon="🔔",
        color="info",
        duration=5000,
    ).show_toast()

app = ttk.Window("Toast Notification Demo", size=(400, 300), themename="cosmo")

ttk.Label(app, text="Click a button to show a toast:").pack(pady=10)

ttk.Button(app, text="Basic Toast", command=show_basic_toast).pack(fill=X, padx=10, pady=5)
ttk.Button(app, text="Alert Toast", command=show_alert_toast).pack(fill=X, padx=10, pady=5)
ttk.Button(app, text="Custom Icon & Color", command=show_custom_toast).pack(fill=X, padx=10, pady=5)
ttk.Button(app, text="Top-Left Positioned", command=show_top_left_toast).pack(fill=X, padx=10, pady=5)

app.mainloop()
