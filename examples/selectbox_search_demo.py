import ttkbootstrap as ttk
from ttkbootstrap.constants import *

# Sample data for testing
countries = [
    "Afghanistan", "Albania", "Algeria", "Andorra", "Angola",
    "Argentina", "Armenia", "Australia", "Austria", "Azerbaijan",
    "Bahamas", "Bahrain", "Bangladesh", "Barbados", "Belarus",
    "Belgium", "Belize", "Benin", "Bhutan", "Bolivia",
    "Brazil", "Brunei", "Bulgaria", "Burkina Faso", "Burundi",
    "Cambodia", "Cameroon", "Canada", "Chad", "Chile",
    "China", "Colombia", "Comoros", "Congo", "Costa Rica",
    "Croatia", "Cuba", "Cyprus", "Czech Republic", "Denmark",
    "Djibouti", "Dominica", "Dominican Republic", "Ecuador", "Egypt",
    "El Salvador", "Equatorial Guinea", "Eritrea", "Estonia", "Ethiopia",
    "Fiji", "Finland", "France", "Gabon", "Gambia",
    "Georgia", "Germany", "Ghana", "Greece", "Grenada",
    "Guatemala", "Guinea", "Guyana", "Haiti", "Honduras",
    "Hungary", "Iceland", "India", "Indonesia", "Iran",
    "Iraq", "Ireland", "Israel", "Italy", "Jamaica",
    "Japan", "Jordan", "Kazakhstan", "Kenya", "Kiribati"
]

def on_changed(event):
    """Handle selection changes."""
    print(f"Selection changed: {event.data}")

root = ttk.Window(theme="superhero")
root.title("SelectBox Search Demo")
root.geometry("500x600")

ttk.Label(root, text="SelectBox Search Feature Demo", font=("Helvetica", 16, "bold")).pack(pady=10)

# Example 1: Search enabled with custom values allowed
frame1 = ttk.LabelFrame(root, text="Search + Custom Values Allowed", padding=10)
frame1.pack(fill=X, padx=20, pady=10)

ttk.Label(frame1, text="Type to filter, keep custom value:").pack(anchor=W)
sb1 = ttk.SelectBox(
    frame1,
    value="Brazil",
    items=countries,
    enable_search=True,
    allow_custom_values=True,
    accent="info"
)
sb1.pack(fill=X, pady=5)
sb1.entry_widget.bind('<<Changed>>', on_changed)

# Example 2: Search enabled without custom values (selects first filtered item)
frame2 = ttk.LabelFrame(root, text="Search + Must Select from List", padding=10)
frame2.pack(fill=X, padx=20, pady=10)

ttk.Label(frame2, text="Type to filter, selects first filtered item:").pack(anchor=W)
sb2 = ttk.SelectBox(
    frame2,
    value="Canada",
    items=countries,
    enable_search=True,
    allow_custom_values=False,
    accent="success"
)
sb2.pack(fill=X, pady=5)
sb2.entry_widget.bind('<<Changed>>', on_changed)

# Example 3: Standard readonly selectbox (no search)
frame3 = ttk.LabelFrame(root, text="Standard SelectBox (No Search)", padding=10)
frame3.pack(fill=X, padx=20, pady=10)

ttk.Label(frame3, text="Click to select, no filtering:").pack(anchor=W)
sb3 = ttk.SelectBox(
    frame3,
    value="Japan",
    items=countries,
    enable_search=False,
    allow_custom_values=False,
    accent="primary"
)
sb3.pack(fill=X, pady=5)
sb3.entry_widget.bind('<<Changed>>', on_changed)

# Example 4: Search with limited items
frame4 = ttk.LabelFrame(root, text="Search with Short List", padding=10)
frame4.pack(fill=X, padx=20, pady=10)

colors = ["Red", "Orange", "Yellow", "Green", "Blue", "Indigo", "Violet"]
ttk.Label(frame4, text="Search through colors:").pack(anchor=W)
sb4 = ttk.SelectBox(
    frame4,
    value="Blue",
    items=colors,
    enable_search=True,
    allow_custom_values=False,
    accent="warning"
)
sb4.pack(fill=X, pady=5)
sb4.entry_widget.bind('<<Changed>>', on_changed)

# Instructions
instructions = ttk.LabelFrame(root, text="Instructions", padding=10)
instructions.pack(fill=X, padx=20, pady=10)
ttk.Label(instructions, text="• With enable_search=True, type in the field to filter the dropdown list").pack(anchor=W)
ttk.Label(instructions, text="• With allow_custom_values=True, any typed value is kept").pack(anchor=W)
ttk.Label(instructions, text="• With allow_custom_values=False, first filtered item is selected when popup closes").pack(anchor=W)

root.mainloop()
