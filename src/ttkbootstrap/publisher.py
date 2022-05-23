from enum import Enum
from typing import List


class Channel(Enum):
    """A grouping for Publisher subscribers. Indicates whether the
    widget is a legacy `STD` tk widget or a styled `TTK` widget.

    Attributes:

        STD (1):
            Legacy tkinter widgets.

        TTK (2):
            Themed tkinter widgets.
    """

    STD = 1
    TTK = 2


class Subscriber:
    """A subcriber data class used to store information about a specific
    subcriber to the `Publisher`."""

    def __init__(self, name, func, channel):
        """Create a subscriber.

        Parameters:

            name (str):
                The name of the subscriber

            func (Callable):
                The function to call when messaging.

            channel (Channel):
                The subscription channel.
        """
        self.name = name
        self.func = func
        self.channel = channel


class Publisher:
    """A class used to publish events for widget updates for theme changes
    or configurations"""

    __subscribers = {}

    @staticmethod
    def subscriber_count():
        return len(Publisher.__subscribers)

    @staticmethod
    def subscribe(name, func, channel):
        """Subscribe to an event.

        Parameters:

            name (str):
                The widget's tkinter/tcl name.

            func (Callable):
                A function to call when passing a message.

            channel (Channel):
                Indicates the channel grouping the subscribers.
        """
        subs = Publisher.__subscribers
        subs[name] = Subscriber(name, func, channel)

    @staticmethod
    def unsubscribe(name):
        """Remove a subscriber

        Parameters:

            name (str):
                The widget's tkinter/tcl name.
        """
        subs = Publisher.__subscribers
        try:
            del subs[str(name)]
        except:
            pass

    def get_subscribers(channel):
        """Return a list of subscribers

        Returns:

            List:
                List of key-value tuples
        """
        subs = Publisher.__subscribers.values()
        channel_subs = [s for s in subs if s.channel == channel]
        return channel_subs

    def publish_message(channel, *args):
        """Publish a message to all subscribers

        Parameters:

            channel (Channel):
                The name of the channel to subscribe.

            **args:
                optional arguments to pass to the subscribers.
        """
        subs: List[Subscriber] = Publisher.get_subscribers(channel)
        for sub in subs:
            sub.func(*args)

    @staticmethod
    def clear_subscribers():
        """Reset all subscriptions."""
        Publisher.__subscribers.clear()
