from tkinter import TclError
from typing import List, TYPE_CHECKING, Tuple

if TYPE_CHECKING:
    from PIL import PhotoImage


class Element:
    """A widget element layout for a style"""

    def __init__(
            self, name=None, expand=None, side=None, sticky=None,
            border=None):
        """
        Create a widget element layout for a style.

        The name of the top level element should be the ttkstyle.

        Parameters
        ----------
        name : str, optional
            The name of the element (ttkstyle if topmost element).

        expand : bool, optional
            Specifies that the allocated parcel is the entire cavity.

        side : str, optional
            The side of the cavity to place the element.

        sticky : str, optional
            The parcel position and size inside the allocated parcel.

        """
        self._children = list()
        self.name = name
        self.parent = None
        self.settings = dict()
        self.settings.update(
            expand=expand,
            side=side,
            sticky=sticky,
            border=border
        )

    @property
    def tk(self):
        """The tcl/tk interpreter object"""
        from ttkbootstrap.style.theme_manager import get_theme_manager
        return get_theme_manager().ttk.master

    @property
    def root(self) -> str:
        """The root element"""
        if self.parent is None:
            return self.name
        else:
            return self.parent

    @property
    def children(self) -> List['Element']:
        """A list of children of this element"""
        return self._children

    def add_parent(self, parent: 'Element'):
        """Set the parent of this element"""
        self.parent = parent
        parent.children.append(self)

    def layout(self, layout):
        """Build the widget layout from a list of layout objects.

        Parameters
        ----------
        layout : List[Element]
            The element layout
        """

        def assign_parents(obj_layout, parent=None):
            for i, obj in enumerate(obj_layout):
                if isinstance(obj, Element):
                    if parent is not None:
                        obj.add_parent(parent)
                elif isinstance(obj, (list, tuple)):
                    assign_parents(obj, obj_layout[i - 1])

        assign_parents([self, layout])
        script = 'ttk::style layout ' + self.to_script(self)
        self.tk.eval(script)

    def to_script(self, root):
        """Return this element as a tcl/tk script

        When generating the top-level script, pass in the style name.

        Parameters
        ----------
        root : Element
            The root element layout object.

        Returns
        -------
        str
            A string representing the tcl/tk script for this element.
        """
        tcl_args = []

        tcl_args.append(self.name)

        for k, v in self.settings.items():
            if k not in ('name', 'parent', 'style') and v is not None:
                v = '{}' if v == '' else v
                tcl_args.extend(['-' + k, str(v).lower()])

        if self.children:
            if self != root:
                tcl_args.append('-children {')
            else:
                tcl_args.append('{')
            for child in self.children:
                tcl_args.append(child.to_script(root))
            tcl_args.append('}')

        script = ' '.join(tcl_args)
        return script


class ElementImage:
    """A new image element in the current theme"""

    def __init__(
            self, name, image, border=None, height=None, padding=None,
            sticky=None, width=None):
        """Create a new image element in the current theme.

        State specific images can be added with the `add_spec` method.

        If the element's allocated parcel is larger than the image, the image
        will be placed in the parcel based on the sticky settings. If the image
        needs to stretch horizontally, subregions of the image are replicated
        to fill the parcel based on the border setting. The border divides the
        image into 9 regions of 4 corners, edges, and center.

        Parameters
        ----------
        name : str
            The name of the new element.

        image : PhotoImage | str
            The default element image.

        border : int | Tuple[int, int]
            The border around the element.

        height : int
            The minimum height of the element.

        padding : PADDING
            The element's interior padding.

        sticky : str
            How the image is placed within the final parcel.

        width : int
            The minimum width of the element.
        """
        self._settings = dict()
        self._settings.update(
            name=name,
            image=image,
            border=border,
            height=height,
            padding=padding,
            sticky=sticky,
            width=width
        )
        self._image_spec = list()

    @property
    def name(self):
        """The name of this element"""
        return self._settings.get('name')

    def conf_get(self, option):
        """Get the value of option

        Parameters
        ----------
        option : str
            The configuration option to query.

        Returns
        -------
        Any
            The value of option.
        """
        return self._settings.get(option)

    def conf_get_all(self):
        """Get all configurations for this element"""
        return self._settings

    def conf_set(self, **kw):
        """Update the element image definition.

        Parameters
        ----------
        **kw : Dict[str, Any]
                Configurations to update

        Raises
        ------
        Exception
            If not key-value pairs are provided.
        """
        if kw is None:
            raise Exception('At least one key-value pair required')
        self._settings.update(**kw)

    def add_spec(self, state, image):
        """Add an image spec to the element image.

        Image specs are evaluated in order. More than one state spec can be
        specified for `state`. For example, "disabled active"

        Parameters
        ----------
        state : str
            The state specification, e.g. "disabled" or "active".

        image : PhotoImage | str
            The image to display when the element is in this state. May
            be the image object or image name.
        """
        self._image_spec.append([state, str(image)])

    def to_script(self) -> str:
        """Return a list of tcl/tk args"""
        state_specs = []
        options = []
        default_image = self._settings.pop('image')
        for state, img in self._image_spec:
            state_specs.extend(['{' + state + '}', img])
        for option, value in self._settings.items():
            if option not in ['name'] and value is not None:
                if isinstance(value, (list, tuple)):
                    value = ' '.join(map(str, value))
                options.extend(['-' + option, '{' + str(value) + '}'])
        tcl_args = ['ttk::style', 'element', 'create', self.name]
        tcl_args.extend(['image', '[list', str(default_image), *state_specs, ']'])
        tcl_args.extend(options)
        script = ' '.join(tcl_args)
        return script

    def build(self):
        """Build the element in tcl/tk"""
        from ttkbootstrap.style.theme_manager import get_theme_manager
        tk = get_theme_manager().ttk.tk
        try:
            tk.eval(self.to_script())
        except TclError:
            pass  # already created

    def __str__(self):
        return self.name
