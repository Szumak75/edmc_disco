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

    BODIES = "_bodies_"
    BUTTON = "_button_"
    CLOSED = "_closed_"
    FDATA = "_fdata_"
    ID = "_id_"
    PARENT = "_parent_"
    SBUTTON = "_sbutton_"
    SCROLLBAR = "_scrollbar_"
    SPANEL = "_spanel_"
    STATUS = "_status_"
    SYSTEM = "_system_"
    TEXT = "text"
    TT_TEXT = "_tool_tip_text_"
    TW = "_tw_"
    WAITTIME = "_waittime_"
    WIDGET = "_widget_"
    WIDGETS = "_widgets_"
    WINDOWS = "_windows_"
    WRAPLENGTH = "_wraplength_"


# #[EOF]#######################################################################
