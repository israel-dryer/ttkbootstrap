from __future__ import annotations

from typing import Sequence


class BindtagsMixin:
    """Bindtags helpers (bindtags).

    Bindtags control **the order in which Tk processes bindings** for an event.

    Every widget has a list of bindtags. When an event occurs on a widget, Tk
    processes bindings in tag order. Each tag may have bindings associated with it.

    Typical default bindtags for a widget look like:

        (widget_pathname, widget_class, toplevel_pathname, "all")

    Practical uses:
        - Insert a custom tag (e.g. "MyApp") to apply shared behaviors across widgets.
        - Reorder tags to change precedence (e.g. run class bindings before widget bindings).
        - Remove a tag to disable a layer of default behavior (use with care).

    Notes:
        - Bindtags affect event dispatch only; they do not change focus or grab behavior.
        - Misordering tags can break default widget behaviors (Tab traversal, selection,
          text editing, etc.), so keep changes minimal and well-scoped.
    """

    def bindtags(self, tags: Sequence[str] | None = None) -> tuple[str, ...]:
        """Get or set the bindtags for this widget.

        Args:
            tags: The bindtags to set. If None, returns the current bindtags.
                Tags are processed in order when dispatching events.

        Returns:
            The current bindtags as a tuple.
        """
        # Tkinter's `bindtags()` returns a tuple and accepts a sequence for setting.
        if tags is None:
            return super().bindtags()  # type: ignore[misc]
        return super().bindtags(tags)  # type: ignore[misc]

    # -------------------------------------------------------------------------
    # Convenience helpers (optional)
    # -------------------------------------------------------------------------

    def bindtags_prepend(self, tag: str) -> tuple[str, ...]:
        """Prepend a tag to the bindtags list.

        This increases the tag's priority (it will be processed earlier).

        Args:
            tag: Tag name to prepend.

        Returns:
            The updated bindtags tuple.
        """
        current = list(self.bindtags())
        if tag not in current:
            current.insert(0, tag)
            self.bindtags(current)
        return tuple(current)

    def bindtags_append(self, tag: str) -> tuple[str, ...]:
        """Append a tag to the bindtags list.

        This decreases the tag's priority (it will be processed later).

        Args:
            tag: Tag name to append.

        Returns:
            The updated bindtags tuple.
        """
        current = list(self.bindtags())
        if tag not in current:
            current.append(tag)
            self.bindtags(current)
        return tuple(current)

    def bindtags_remove(self, tag: str) -> tuple[str, ...]:
        """Remove a tag from the bindtags list.

        Args:
            tag: Tag name to remove.

        Returns:
            The updated bindtags tuple.
        """
        current = [t for t in self.bindtags() if t != tag]
        self.bindtags(current)
        return tuple(current)

    def bindtags_replace(self, old: str, new: str) -> tuple[str, ...]:
        """Replace a bindtag with another tag.

        Args:
            old: Existing tag name.
            new: Replacement tag name.

        Returns:
            The updated bindtags tuple.
        """
        current = list(self.bindtags())
        try:
            idx = current.index(old)
        except ValueError:
            return tuple(current)
        current[idx] = new
        self.bindtags(current)
        return tuple(current)
