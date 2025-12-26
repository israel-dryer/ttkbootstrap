import ttkbootstrap as ttk
from ttkbootstrap import SelectBox


app = ttk.Window(theme="darkly")

languages = [
    'Python', 'JavaScript', 'TypeScript', 'Java', 'C#', 'C++', 'C',
    'Go', 'Rust', 'Ruby', 'PHP', 'Swift', 'Kotlin', 'Scala', 'R',
    'MATLAB', 'Perl', 'Haskell', 'Lua', 'Dart', 'Elixir', 'Clojure',
    'F#', 'Erlang', 'Julia', 'Groovy', 'COBOL', 'Fortran', 'Assembly'
]

# Standard readonly selectbox with keyboard navigation
sb1 = SelectBox(app, "Python", label="Standard (readonly)", items=languages)
sb1.pack(padx=10, pady=10)
sb1.on_changed(lambda x: print("Standard:", x))

# Searchable selectbox
sb2 = SelectBox(app, "JavaScript", label="With search", items=languages, search_enabled=True)
sb2.pack(padx=10, pady=10)
sb2.on_changed(lambda x: print("Search:", x))

app.mainloop()
