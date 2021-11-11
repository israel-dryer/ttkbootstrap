from enum import Enum
from collections import namedtuple
from typing import List

Subscriber = namedtuple('Subscriber', ['name', 'func', 'channel'])


class Channel(Enum):
    """A grouping for Publisher subscribers. Indicates whether the
    widget is a legacy `STD` tk widget or a styled `TTK` widget.
    """
    STD = 1
    TTK = 2
    

class Publisher:

    __subscribers = {}
    
    @staticmethod
    def subscribe(name, func, channel):
        """Subscribe to an event.
        
        Parameters
        ----------
        name : str
            The widget's tkinter/tcl name.

        func : Callable
            A function to call when passing a message.

        channel : Channel
            Indicates the channel grouping the subscribers.
        """
        subs = Publisher.__subscribers
        subs[name] = Subscriber(name, func, channel)

    @staticmethod
    def unsubscribe(name):
        """Subscribe to an event.
        
        Parameters
        ----------
        name : str
            The widget's tkinter/tcl name.

        func : Callable
            A function to call when passing a message.
        """
        subs = Publisher.__subscribers
        try:
            del(subs[name])
        except:
            pass
    
    def get_subscribers(channel):
        """Return a list of subscribers
        
        Returns
        -------
        dict_items
            List of key-value tuples        
        """
        subs = Publisher.__subscribers.values()
        channel_subs = [s for s in subs if s.channel == channel]
        return  channel_subs
    
    def publish_message(channel, *args):
        """Publish a message to all subscribers"""
        subs: List[Subscriber] = Publisher.get_subscribers(channel)
        for sub in subs:
            sub.func(*args)

    @staticmethod
    def clear_subscribers():
        Publisher.__subscribers.clear()
