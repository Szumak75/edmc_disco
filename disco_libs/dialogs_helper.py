#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
  Author:  Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
  Created: 19.12.2023

  Purpose: dialogs helper classes.
"""

from jsktoolbox.attribtool import ReadOnlyClass


class DialogKeys(object, metaclass=ReadOnlyClass):
    """Keys container class for dialogs."""

    WAITTIME = "_waittime_"
    WRAPLENGTH = "_wraplength_"
    WIDGET = "_widget_"
    WIDGETS = "_widgets_"
    ID = "_id_"
    TW = "_tw_"
    TT_TEXT = "_tool_tip_text_"
    TEXT = "text"

    BUTTON = "_button_"
    PARENT = "_parent_"
    WINDOWS = "_windows_"

    CLOSED = "_closed_"
    STATUS = "_status_"
    SYSTEM = "_system_"
    SBUTTON = "_sbutton_"
    FDATA = "_fdata_"
    SCROLLBAR = "_scrollbar_"
    SPANEL = "_spanel_"
    BODIES = "_bodies_"


# #[EOF]#######################################################################
