#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
  Author:  Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
  Created: 19.12.2023

  Purpose: dialogs helper classes.
"""

from disco.jsktoolbox.attribtool import ReadOnlyClass


class DialogKeys(object, metaclass=ReadOnlyClass):
    """Keys container class for dialogs."""

    BODIES: str = "_bodies_"
    BUTTON: str = "_button_"
    CLOSED: str = "_closed_"
    F_DATA: str = "_f_data_"
    ID: str = "_id_"
    PARENT: str = "_parent_"
    SCROLLBAR: str = "_scrollbar_"
    STATUS: str = "_status_"
    SYSTEM: str = "_system_"
    S_BUTTON: str = "_s_button_"
    S_MENU: str = "_s_menu_"
    S_PANEL: str = "_s_panel_"
    TEXT: str = "text"
    TT_TEXT: str = "_tool_tip_text_"
    TW: str = "_tw_"
    WAIT_TIME: str = "_wait_time_"
    WIDGET: str = "_widget_"
    WIDGETS: str = "_widgets_"
    WINDOWS: str = "_windows_"
    WRAPLENGTH: str = "_wraplength_"


# #[EOF]#######################################################################
