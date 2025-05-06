"""
This module holds all predefined Bootstrap styles that are used within this library
"""
from enum import Enum


class Theme(Enum):
    """
    Predefined ttkbootstrap themes

    @see `ttkbootsrap documentation - Themes <https://ttkbootstrap.readthedocs.io/en/latest/themes/>`__
    """
    COSMO = 'cosmo'
    FLATLY = 'flatly'
    LITERA = 'litera'
    MINTY = 'minty'
    LUMEN = 'lumen'
    SANDSTONE = 'sandstone'
    YETI = 'yeti'
    PULSE = 'pulse'
    UNITED = 'united'
    MORPH = 'morph'
    JOURNAL = 'journal'
    DARKLY = 'darkly'
    SUPERHERO = 'superhero'
    SOLAR = 'solar'
    CYBORG = 'cyborg'
    VAPOR = 'vapor'
    SIMPLEX = 'simplex'
    CERCULEAN = 'cerculean'

    @property
    def value(self) -> str:
        return super().value


class BootstrapStyle(Enum):
    """
    Predefined ttkbootstrap styles

    @see `ttkbootsrap documentation - Style guide <https://ttkbootstrap.readthedocs.io/en/latest/styleguide/>`__
    """
    DANGER = 'danger'
    DARK = 'dark'
    DEFAULT = ''
    INFO = 'info'
    LIGHT = 'light'
    PRIMARY = 'primary'
    SECONDARY = 'secondary'
    SUCCESS = 'success'
    WARNING = 'warning'

    @property
    def value(self) -> str:
        return super().value


class ParentBootstrapStyle:
    """
    Parent class for specific bootstrap styles that implements the default styles

    @see `ttkbootsrap documentation - Style guide <https://ttkbootstrap.readthedocs.io/en/latest/styleguide/>`__
    """

    @classmethod
    def default(cls, bootstrap_style: BootstrapStyle = BootstrapStyle.DEFAULT) -> str:
        """ Default style """
        return bootstrap_style.value


class Button(ParentBootstrapStyle):
    """
    This is a pure static class (meaning just class methods) with predefined ttkbootstrap styles for buttons

    @see `ttkbootsrap documentation - Style guide <https://ttkbootstrap.readthedocs.io/en/latest/styleguide/button/>`__
    """
    @classmethod
    def outline_button(cls, bootstrap_style: BootstrapStyle = BootstrapStyle.DEFAULT) -> str:
        return f'{bootstrap_style.value}-outline' if bootstrap_style is not BootstrapStyle.DEFAULT else 'outline'

    @classmethod
    def link_button(cls, bootstrap_style: BootstrapStyle = BootstrapStyle.DEFAULT) -> str:
        return f'{bootstrap_style.value}-link' if bootstrap_style is not BootstrapStyle.DEFAULT else 'link'


class Checkbutton(ParentBootstrapStyle):
    """
    This is a pure static class (meaning just class methods) with predefined ttkbootstrap styles for check buttons

    @see `ttkbootsrap documentation - Style guide <https://ttkbootstrap.readthedocs.io/en/latest/styleguide/checkbutton/>`__
    """
    @classmethod
    def tool_button(cls, bootstrap_style: BootstrapStyle = BootstrapStyle.DEFAULT) -> str:
        return f'{bootstrap_style.value}-toolbutton' if bootstrap_style is not BootstrapStyle.DEFAULT else 'toolbutton'

    @classmethod
    def outline_tool_button(cls, bootstrap_style: BootstrapStyle = BootstrapStyle.DEFAULT) -> str:
        return f'{bootstrap_style.value}-outline-toolbutton' if bootstrap_style is not BootstrapStyle.DEFAULT else 'outline-toolbutton'

    @classmethod
    def round_toggle_button(cls, bootstrap_style: BootstrapStyle = BootstrapStyle.DEFAULT) -> str:
        return f'{bootstrap_style.value}-round-toggle' if bootstrap_style is not BootstrapStyle.DEFAULT else 'round-toggle'

    @classmethod
    def square_toggle_button(cls, bootstrap_style: BootstrapStyle = BootstrapStyle.DEFAULT) -> str:
        return f'{bootstrap_style.value}-square-toggle' if bootstrap_style is not BootstrapStyle.DEFAULT else 'square-toggle'


class Combobox(ParentBootstrapStyle):
    """
    This is a pure static class (meaning just class methods) with predefined ttkbootstrap styles for buttons

    @see `ttkbootsrap documentation - Style guide <https://ttkbootstrap.readthedocs.io/en/latest/styleguide/combobox/>`__
    """
    pass


class DateEntry(ParentBootstrapStyle):
    """
    This is a pure static class (meaning just class methods) with predefined ttkbootstrap styles for date entries

    @see `ttkbootsrap documentation - Style guide <https://ttkbootstrap.readthedocs.io/en/latest/styleguide/dateentry/>`__
    """
    pass


class DatePickerPopup(ParentBootstrapStyle):
    """
    This is a pure static class (meaning just class methods) with predefined ttkbootstrap styles for date entries

    @see `ttkbootsrap documentation - Style guide <https://ttkbootstrap.readthedocs.io/en/latest/styleguide/datepickerpopup/>`__
    """
    pass


class Entry(ParentBootstrapStyle):
    """
    This is a pure static class (meaning just class methods) with predefined ttkbootstrap styles for date entries

    @see `ttkbootsrap documentation - Style guide <https://ttkbootstrap.readthedocs.io/en/latest/styleguide/entry/>`__
    """
    pass


class FloodGauge(ParentBootstrapStyle):
    """
    This is a pure static class (meaning just class methods) with predefined ttkbootstrap styles for flood gouges

    @see `ttkbootsrap documentation - Style guide <https://ttkbootstrap.readthedocs.io/en/latest/styleguide/floodgauge/>`__
    """
    pass


class Frame(ParentBootstrapStyle):
    """
    This is a pure static class (meaning just class methods) with predefined ttkbootstrap styles for frames

    @see `ttkbootsrap documentation - Style guide <https://ttkbootstrap.readthedocs.io/en/latest/styleguide/frame/>`__
    """
    pass


class Label(ParentBootstrapStyle):
    """
    This is a pure static class (meaning just class methods) with predefined ttkbootstrap styles for labels

    @see `ttkbootsrap documentation - Style guide <https://ttkbootstrap.readthedocs.io/en/latest/styleguide/label/>`__
    """
    @classmethod
    def inverse_label(cls, bootstrap_style: BootstrapStyle = BootstrapStyle.DEFAULT) -> str:
        return f'inverse-{bootstrap_style.value}' if bootstrap_style is not BootstrapStyle.DEFAULT else 'inverse'


class Labelframe(ParentBootstrapStyle):
    """
    This is a pure static class (meaning just class methods) with predefined ttkbootstrap styles for label frames

    @see `ttkbootsrap documentation - Style guide <https://ttkbootstrap.readthedocs.io/en/latest/styleguide/labelframe/>`__
    """
    pass


class MenuButton(ParentBootstrapStyle):
    """
    This is a pure static class (meaning just class methods) with predefined ttkbootstrap styles for menu buttons

    @see `ttkbootsrap documentation - Style guide <https://ttkbootstrap.readthedocs.io/en/latest/styleguide/menubutton/>`__
    """
    @classmethod
    def outline(cls, bootstrap_style: BootstrapStyle = BootstrapStyle.DEFAULT) -> str:
        return f'{bootstrap_style.value}-outline' if bootstrap_style is not BootstrapStyle.DEFAULT else 'outline'


class Meter(ParentBootstrapStyle):
    """
    This is a pure static class (meaning just class methods) with predefined ttkbootstrap styles for meters

    @see `ttkbootsrap documentation - Style guide <https://ttkbootstrap.readthedocs.io/en/latest/styleguide/meter/>`__
    """
    pass


class Notebook(ParentBootstrapStyle):
    """
    This is a pure static class (meaning just class methods) with predefined ttkbootstrap styles for notebooks

    @see `ttkbootsrap documentation - Style guide <https://ttkbootstrap.readthedocs.io/en/latest/styleguide/notebook/>`__
    """
    pass


class PanedWindow(ParentBootstrapStyle):
    """
    This is a pure static class (meaning just class methods) with predefined ttkbootstrap styles for paned windows

    @see `ttkbootsrap documentation - Style guide <https://ttkbootstrap.readthedocs.io/en/latest/styleguide/panedwindow/>`__
    """
    pass


class Progressbar(ParentBootstrapStyle):
    """
    This is a pure static class (meaning just class methods) with predefined ttkbootstrap styles for progress bars

    @see `ttkbootsrap documentation - Style guide <https://ttkbootstrap.readthedocs.io/en/latest/styleguide/progressbar/>`__
    """
    @classmethod
    def striped(cls, bootstrap_style: BootstrapStyle = BootstrapStyle.DEFAULT) -> str:
        return f'{bootstrap_style.value}-striped' if bootstrap_style is not BootstrapStyle.DEFAULT else 'striped'


class Radiobutton(ParentBootstrapStyle):
    """
    This is a pure static class (meaning just class methods) with predefined ttkbootstrap styles for radio buttons

    @see `ttkbootsrap documentation - Style guide <https://ttkbootstrap.readthedocs.io/en/latest/styleguide/radiobutton/>`__
    """
    @classmethod
    def solid_tool_button(cls, bootstrap_style: BootstrapStyle = BootstrapStyle.DEFAULT) -> str:
        return f'{bootstrap_style.value}-toolbutton' if bootstrap_style is not BootstrapStyle.DEFAULT else 'toolbutton'

    @classmethod
    def outline_tool_button(cls, bootstrap_style: BootstrapStyle = BootstrapStyle.DEFAULT) -> str:
        return f'{bootstrap_style.value}-outline-toolbutton' if bootstrap_style is not BootstrapStyle.DEFAULT else 'outline-toolbutton'


class Scale(ParentBootstrapStyle):
    """
    This is a pure static class (meaning just class methods) with predefined ttkbootstrap styles for scales

    @see `ttkbootsrap documentation - Style guide <https://ttkbootstrap.readthedocs.io/en/latest/styleguide/scale/>`__
    """
    pass


class Scrollbar(ParentBootstrapStyle):
    """
    This is a pure static class (meaning just class methods) with predefined ttkbootstrap styles for scrollbars

    @see `ttkbootsrap documentation - Style guide <https://ttkbootstrap.readthedocs.io/en/latest/styleguide/scrollbar/>`__
    """
    @classmethod
    def round(cls, bootstrap_style: BootstrapStyle = BootstrapStyle.DEFAULT) -> str:
        return f'{bootstrap_style.value}-round' if bootstrap_style is not BootstrapStyle.DEFAULT else 'round'


class Separator(ParentBootstrapStyle):
    """
    This is a pure static class (meaning just class methods) with predefined ttkbootstrap styles for separators

    @see `ttkbootsrap documentation - Style guide <https://ttkbootstrap.readthedocs.io/en/latest/styleguide/separator/>`__
    """
    pass


class SizeGrip(ParentBootstrapStyle):
    """
    This is a pure static class (meaning just class methods) with predefined ttkbootstrap styles for size grips

    @see `ttkbootsrap documentation - Style guide <https://ttkbootstrap.readthedocs.io/en/latest/styleguide/sizegrip/>`__
    """
    pass


class SpinBox(ParentBootstrapStyle):
    """
    This is a pure static class (meaning just class methods) with predefined ttkbootstrap styles for spin boxes

    @see `ttkbootsrap documentation - Style guide <https://ttkbootstrap.readthedocs.io/en/latest/styleguide/spinbox/>`__
    """
    pass


class TreeView(ParentBootstrapStyle):
    """
    This is a pure static class (meaning just class methods) with predefined ttkbootstrap styles for tree views

    @see `ttkbootsrap documentation - Style guide <https://ttkbootstrap.readthedocs.io/en/latest/styleguide/treeview/>`__
    """
    pass
