# -*- coding: UTF-8 -*-
"""
  Author:  Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
  Created: 18.12.2023

  Purpose: edmc plugin entry point
"""

import tkinter as tk
from tkinter import ttk
from typing import Dict, Optional

from config import config
from disco.jsktoolbox.tktool.widgets import CreateToolTip
from disco.jsktoolbox.edmctool.logs import LogLevels
from disco.jsktoolbox.edmctool.ed_keys import EDKeys

from disco.dialogs import DiscoMainDialog
from disco.disco import Disco

disco = Disco()


def plugin_start3(plugin_dir: str) -> str:
    """Load plugin into EDMC.

    plugin_dir:     plugin directory
    return:         local name of the plugin
    """
    if disco.logger:
        disco.logger.debug = f"{disco.data.plugin_name}->plugin_start3 start..."
    # loglevel set from config
    if disco.log_processor:
        disco.log_processor.loglevel = LogLevels().get(
            config.get_str("loglevel")
        )  # type: ignore
    if disco.logger:
        disco.logger.debug = f"{disco.data.plugin_name}->plugin_start3 done."
    return f"{disco.data.plugin_name}"


def plugin_stop() -> None:
    """Stop plugin if EDMC is closing."""
    if disco.logger:
        disco.logger.debug = f"{disco.data.plugin_name}->plugin_stop: start..."
    disco.data.shutting_down = True
    if disco.logger:
        disco.logger.debug = (
            f"{disco.data.plugin_name}->plugin_stop: shut down flag is set"
        )
    # something to do

    disco.data.db_processor.close()

    # shut down logger at last
    if disco.logger:
        disco.logger.debug = (
            f"{disco.data.plugin_name}->plugin_stop: terminating the logger"
        )
    disco.qlog.put(None)
    disco.th_log.join()


def plugin_app(parent: tk.Frame) -> ttk.Button:
    """Create a pair of TK widgets for the EDMarketConnector main window.

    parent:     The root EDMarketConnector window
    """
    if disco.data.dialog is None:
        disco.data.dialog = DiscoMainDialog(parent, disco.qlog, disco.data)
    button = disco.data.dialog.button()  # type: ignore
    CreateToolTip(
        button,
        [
            f"{disco.data.plugin_name} v{disco.data.version}",
            "",
            "Show or search for discovered system data.",
        ],
    )
    return button


def prefs_changed(cmdr: str, is_beta: bool) -> None:
    """Save settings.

    cmdr:       The current commander
    is_beta:    If the game is currently a beta version
    """
    disco.logger.debug = f"{disco.data.plugin_name}->prefs_changed: start..."
    # set loglevel after config update
    disco.log_processor.loglevel = LogLevels().get(config.get_str("loglevel"))  # type: ignore
    disco.logger.debug = f"{disco.data.plugin_name}->prefs_changed: done."


def journal_entry(
    cmdr: str,
    is_beta: bool,
    system: str,
    station: str,
    entry: Dict,
    state: Dict,
) -> Optional[str]:
    """Get new entry in the game's journal.

    cmdr:       Current commander name
    is_beta:    Is the game currently in beta
    system:     Current system, if known
    station:    Current station, if any
    entry:      The journal event
    state:      More info about the commander, their ship, and their cargo
    """
    test = False

    if entry[EDKeys.EVENT] == EDKeys.FSD_JUMP:
        disco.data.system = disco.data.db_processor.add_system(entry)  # type: ignore
        test = True
        disco.logger.debug = f"{EDKeys.FSD_JUMP}: {disco.data.system}"
    elif entry[EDKeys.EVENT] == EDKeys.SCAN and entry[EDKeys.SCAN_TYPE] in (
        EDKeys.AUTO_SCAN,
        EDKeys.DETAILED,
        EDKeys.BASIC,
        EDKeys.NAV_BEACON_DETAIL,
    ):
        disco.data.system = disco.data.db_processor.add_body(entry)  # type: ignore
        test = True
        disco.logger.debug = f"{EDKeys.SCAN}: {disco.data.system}"
    elif entry[EDKeys.EVENT] == EDKeys.FSS_DISCOVERY_SCAN:
        disco.data.system = disco.data.db_processor.update_system(entry)  # type: ignore
        test = True
        disco.logger.debug = f"{EDKeys.FSS_DISCOVERY_SCAN}: {disco.data.system}"
    elif entry[EDKeys.EVENT] == EDKeys.FSS_BODY_SIGNALS:
        disco.data.system = disco.data.db_processor.add_signal(entry)  # type: ignore
        test = True
        disco.logger.debug = f"{EDKeys.FSS_BODY_SIGNALS}: {disco.data.system}"
    elif entry[EDKeys.EVENT] == EDKeys.SAA_SIGNALS_FOUND:
        disco.data.db_processor.add_signal(entry)
        disco.data.system = disco.data.db_processor.add_genus(entry)  # type: ignore
        test = True
        disco.logger.debug = f"{EDKeys.SAA_SIGNALS_FOUND}: {disco.data.system}"
    elif entry[EDKeys.EVENT] == EDKeys.CODEX_ENTRY:
        disco.data.system = disco.data.db_processor.add_codex(entry)  # type: ignore
        test = True
        disco.logger.debug = f"{EDKeys.CODEX_ENTRY}: {disco.data.system}"
    elif entry[EDKeys.EVENT] == EDKeys.SCAN_ORGANIC:
        disco.data.system = disco.data.db_processor.add_genus(entry)  # type: ignore
        test = True
        disco.logger.debug = f"{EDKeys.SCAN_ORGANIC}: {disco.data.system}"
    elif entry[EDKeys.EVENT] == EDKeys.SAA_SCAN_COMPLETE:
        disco.data.system = disco.data.db_processor.mapped_body(entry)  # type: ignore
        test = True
    elif entry[EDKeys.EVENT] == EDKeys.LOCATION and EDKeys.STAR_SYSTEM in entry:
        disco.data.system = disco.data.db_processor.get_system_by_name(
            entry[EDKeys.STAR_SYSTEM]
        )  # type: ignore
        test = True
    if test:
        dialog = disco.data.dialog
        dialog.update(disco.data.system)  # type: ignore


# #[EOF]#######################################################################
