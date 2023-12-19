# -*- coding: UTF-8 -*-
"""
  Author:  Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
  Created: 19.12.2023

  Purpose: ToolTip
"""

import tkinter as tk
from typing import List, Tuple, Union, Optional

from jsktoolbox.libs.base_data import BData
from jsktoolbox.attribtool import ReadOnlyClass


class _Keys(object, metaclass=ReadOnlyClass):
    """Keys container class."""

    WAITTIME = "_waittime_"
    WRAPLENGTH = "_wraplength_"
    WIDGET = "_widget_"
    ID = "_id_"
    TW = "_tw_"
    TEXT = "_text_"


class CreateToolTip(BData):
    """Create a tooltip for a given widget."""

    def __init__(
        self,
        widget,
        text: Union[str, List, Tuple] = "widget info",
        wait_time: int = 500,
        wrap_length: int = 300,
    ) -> None:
        """Create class object."""
        self._data[_Keys.WAITTIME] = wait_time  # miliseconds
        self._data[_Keys.WRAPLENGTH] = wrap_length  # pixels
        self._data[_Keys.WIDGET] = widget  # parent widget
        self._data[_Keys.ID] = None
        self._data[_Keys.TW] = None
        self._data[_Keys.TEXT] = ""

        # set message
        self.text = text
        self._data[_Keys.WIDGET].bind("<Enter>", self.enter)
        self._data[_Keys.WIDGET].bind("<Leave>", self.leave)
        self._data[_Keys.WIDGET].bind("<ButtonPress>", self.leave)

    def enter(self, event: Optional[tk.Event] = None) -> None:
        """Call on <Enter> event."""
        self.schedule()

    def leave(self, event: Optional[tk.Event] = None) -> None:
        """Call on <Leave> event."""
        self.unschedule()
        self.hidetip()

    def schedule(self) -> None:
        """Schedule method."""
        self.unschedule()
        self._data[_Keys.ID] = self._data[_Keys.WIDGET].after(
            self._data[_Keys.WAITTIME], self.showtip
        )

    def unschedule(self) -> None:
        """Unschedule method."""
        __id = self._data[_Keys.ID]
        self._data[_Keys.ID] = None
        if __id:
            self._data[_Keys.WIDGET].after_cancel(__id)

    def showtip(self, event: Optional[tk.Event] = None) -> None:
        """Show tooltip."""
        __x = __y = 0
        __x, __y, __cx, __cy = self._data[_Keys.WIDGET].bbox("insert")
        __x += self._data[_Keys.WIDGET].winfo_rootx() + 25
        __y += self._data[_Keys.WIDGET].winfo_rooty() + 20
        # creates a toplevel window
        self._data[_Keys.TW] = tk.Toplevel(self._data[_Keys.WIDGET])
        # Leaves only the label and removes the app window
        self._data[_Keys.TW].wm_overrideredirect(True)
        self._data[_Keys.TW].wm_geometry(f"+{__x}+{__y}")
        label = tk.Label(
            self._data[_Keys.TW],
            text=self.text,
            justify="left",
            background="#ffffff",
            relief="solid",
            borderwidth=1,
            wraplength=self._data[_Keys.WRAPLENGTH],
        )
        label.pack(ipadx=1)

    def hidetip(self) -> None:
        """Hide tooltip."""
        __tw = self._data[_Keys.TW]
        self._data[_Keys.TW] = None
        if __tw:
            __tw.destroy()

    @property
    def text(self) -> str:
        """Return text message."""
        if _Keys.TEXT not in self.__data:
            self._data[_Keys.TEXT] = ""
        if isinstance(self._data[_Keys.TEXT], (List, Tuple)):
            tmp = ""
            for msg in self._data[_Keys.TEXT]:
                tmp += msg if not tmp else f"\n{msg}"
            return tmp
        return self._data[_Keys.TEXT]

    @text.setter
    def text(self, value: Union[str, List, Tuple]) -> None:
        """Set text message object."""
        self._data[_Keys.TEXT] = value


# #[EOF]#######################################################################
