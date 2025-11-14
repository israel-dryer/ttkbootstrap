from collections.abc import Sequence
from tkinter import PhotoImage
from typing import Any, Optional, Tuple, Union


class Element:
    """
    A style layout element for use in ttk-style widget construction.

    Represents a named element within a widget layout. Each element can have
    layout options (like `expand`, `side`, `sticky`, etc.) and nested children.

    Attributes:
        name (str): The name of this element (e.g., "Label.border").
        parent (Optional[Element]): The parent element, if any.
        _children (list[Element]): The list of child elements.
        _options (dict): Layout configuration options for this element.
    """

    def __init__(
            self,
            name: str,
            *,
            expand: Optional[int] = None,
            side: Optional[str] = None,
            sticky: Optional[str] = None,
            border: Optional[int] = None,
    ):
        """
        Initialize a new layout Element.

        Args:
            name: The name of the element.
            expand: Whether the element should expand to fill its parcel.
            side: The side of the cavity to place the element.
            sticky: How to align the element within its parcel (e.g., "nsew").
            border: Border margin applied to the element.
        """
        self.name = name
        self.parent: Optional[Element] = None
        self._children: list[Element] = []
        self._options: dict[str, Any] = {
            "expand": expand,
            "side": side,
            "sticky": sticky,
            "border": border,
        }

    def add_parent(self, parent: "Element") -> None:
        """
        Set the parent element and register this element as its child.

        Args:
            parent: The parent Element to attach to.
        """
        self.parent = parent
        parent._children.append(self)

    def children(self, layout: Sequence["Element"]):
        """
        Add children to this layout

        Args:
            layout: A list of Elements or nested lists/tuples representing the hierarchy.
        """

        def assign_parents(elements: Sequence[Any], parent: Optional[Element] = None):
            for i, item in enumerate(elements):
                if isinstance(item, Element) and parent:
                    item.add_parent(parent)
                elif isinstance(item, (list, tuple)):
                    assign_parents(item, elements[i - 1] if i > 0 else None)

        assign_parents(layout, self)
        return self

    def spec(self):
        """
        Recursively build a Python layout spec compatible with ttk.Style().layout().

        Returns:
            Tuple[str, dict]: A (name, options) pair for use in a layout tree.
        """
        options = {k: v for k, v in self._options.items() if v is not None}

        if self._children:
            options["children"] = [child.spec() for child in self._children]

        if options:
            return self.name, options
        else:
            return self.name, {"sticky": ""}


class ElementImage:
    """
    An image-based element for styling ttk widgets.

    Attributes:
        _name (str): Name of the image element.
        _image (str | PhotoImage): The default image.
        _image_specs (list): List of state-specific overrides.
        _options (dict): Element rendering options like width, padding, sticky, etc.
    """

    def __init__(
            self,
            name: str,
            image: Union[PhotoImage, str],
            *,
            border: Optional[Union[int, Tuple[int, int]]] = None,
            height: Optional[int] = None,
            width: Optional[int] = None,
            padding: Optional[Union[int, Tuple[int, ...]]] = None,
            sticky: Optional[str] = None,
    ):
        """
        Initialize a new image element.

        Args:
            name: The name of the element (e.g., "Button.border").
            image: The default image object or image name.
            border: Border definition for tiling/stretching (e.g., 2 or (2,2)).
            height: Minimum height of the element.
            width: Minimum width of the element.
            padding: Interior padding within the element.
            sticky: Alignment within the layout parcel (e.g., "nsew").
        """
        self._name = name
        self._image = image
        self._image_specs: list[tuple[str, Union[str, PhotoImage]]] = []
        self._options: dict[str, Any] = {
            "border": border,
            "height": height,
            "width": width,
            "padding": padding,
            "sticky": sticky,
        }

    @property
    def name(self) -> str:
        """
        Return the name of the element.

        Returns:
            str: Element name.
        """
        return self._name

    def add_spec(self, state: str, image: Union[str, PhotoImage]) -> None:
        """
        Add a state-specific image override.

        Args:
            state: Widget state (e.g., "disabled", "active").
            image: ManagedImage instance or registered image name.
        """
        self._image_specs.append((state, str(image)))

    def build(self):
        args: list[Any] = [str(self._image)]
        for state, image in self._image_specs:
            args.append(tuple([state, str(image)]))
        options = {k: v for k, v in self._options.items() if v is not None}
        return self.name, args, options

    def state_specs(self, specs: list[Tuple[str, Union[str, PhotoImage]]]):
        for spec in specs:
            self.add_spec(*spec)
        return self

    def __str__(self) -> str:
        return self.name
