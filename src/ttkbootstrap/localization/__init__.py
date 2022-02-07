"""
    A partial wrapper on the tcl/tk msgcat (Tcl message catalog)

    The MessageCatalog provides a set of functions that can be used to 
    manage multi-lingual user interfaces. Text strings are defined in a 
    “message catalog” which is independent from the application, and 
    which can be edited or localized without modifying the application 
    source code. New languages or locales may be provided by adding a 
    new file to the message catalog.

    https://www.tcl.tk/man/tcl/TclCmd/msgcat.html    
"""
from ttkbootstrap.localization import msgs
from ttkbootstrap.localization.msgcat import MessageCatalog
import importlib.resources

with importlib.resources.path(msgs, 'en.msg') as f:
    MSGS_PATH = f.parent.as_posix()

def initialize_localities():
    """Load all custom msg files."""
    MessageCatalog.load(MSGS_PATH)    


