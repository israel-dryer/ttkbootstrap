"""Publisher-Subscriber pattern implementation for ttkbootstrap.

This module implements a simple publisher-subscriber (pub-sub) pattern used
for theme change notifications and widget updates throughout ttkbootstrap.

The Publisher class manages subscribers on different channels and broadcasts
messages to all subscribers when events occur (like theme changes).

Classes:
    Channel: Enum defining subscriber channels (STD for tk, TTK for ttk)
    Subscriber: Data class storing subscriber information
    Publisher: Manages subscriptions and publishes messages to subscribers

Example:
    ```python
    from ttkbootstrap.publisher import Publisher, Channel

    # Subscribe a function to theme changes
    def on_theme_change():
        print("Theme changed!")

    Publisher.subscribe(
        func=on_theme_change,
        channel=Channel.TTK
    )

    # Publish a message to all TTK subscribers
    Publisher.publish(Channel.TTK)
    ```

"""
from enum import Enum
from typing import List


class Channel(Enum):
    """A grouping for Publisher subscribers.

    Indicates whether the
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
    """A subscriber data class for Publisher subscriptions."""

    def __init__(self, name, func, channel):
        """Create a subscriber.

        Args:
            name: The name of the subscriber

            func: The function to call when messaging.

            channel: The subscription channel.

        """
        self.name = name
        self.func = func
        self.channel = channel


class Publisher:
    """Publish events to subscribed widgets for theme changes or configuration updates."""

    __subscribers = {}

    @staticmethod
    def subscriber_count():
        """Return the number of active subscribers."""
        return len(Publisher.__subscribers)

    @staticmethod
    def subscribe(name, func, channel):
        """Subscribe to an event.

        Args:
            name: The widget's tkinter/tcl name.

            func: A function to call when passing a message.

            channel: Indicates the channel grouping the subscribers.

        """
        subs = Publisher.__subscribers
        subs[name] = Subscriber(name, func, channel)

    @staticmethod
    def unsubscribe(name):
        """Remove a subscriber.

        Args:
            name: The widget's tkinter/tcl name.

        """
        subs = Publisher.__subscribers
        try:
            del subs[str(name)]
        except:
            pass

    def get_subscribers(channel):
        """Return a list of subscribers.

        Returns:
            List:
                List of key-value tuples

        """
        subs = Publisher.__subscribers.values()
        channel_subs = [s for s in subs if s.channel == channel]
        return channel_subs

    def publish_message(channel, *args):
        """Publish a message to all subscribers.

        Args:
            channel: The name of the channel to publish to.
            *args: Optional arguments forwarded to each subscriber.

        """
        subs: list[Subscriber] = Publisher.get_subscribers(channel)
        for sub in subs:
            sub.func(*args)

    @staticmethod
    def clear_subscribers():
        """Reset all subscriptions."""
        Publisher.__subscribers.clear()
