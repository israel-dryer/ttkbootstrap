import ttkbootstrap as ttk
from ttkbootstrap import SelectBox


app = ttk.Window(theme="darkly")

languages = [
    'Python', 'JavaScript', 'TypeScript', 'Java', 'C#', 'C++', 'C',
    'Go', 'Rust', 'Ruby', 'PHP', 'Swift', 'Kotlin', 'Scala', 'R',
    'MATLAB', 'Perl', 'Haskell', 'Lua', 'Dart', 'Elixir', 'Clojure',
    'F#', 'Erlang', 'Julia', 'Groovy', 'COBOL', 'Fortran', 'Assembly'
]

sb = SelectBox(app, "Python", label="Choose your language", allow_custom_values=True, items=languages)
sb.pack(padx=10, pady=10)
sb.on_changed(lambda x: print(x))

app.mainloop()
