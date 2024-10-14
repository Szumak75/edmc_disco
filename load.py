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

disco_object = Disco()


def plugin_start3(plugin_dir: str) -> str:
    """Load plugin into EDMC.

    plugin_dir:     plugin directory
    return:         local name of the plugin
    """
    if disco_object.logger:
        disco_object.logger.debug = (
            f"{disco_object.data.pluginname}->plugin_start3 start..."
        )
    # loglevel set from config
    if disco_object.log_processor:
        disco_object.log_processor.loglevel = LogLevels().get(
            config.get_str("loglevel")
        )  # type: ignore
    if disco_object.logger:
        disco_object.logger.debug = (
            f"{disco_object.data.pluginname}->plugin_start3 done."
        )
    return f"{disco_object.data.pluginname}"


def plugin_stop() -> None:
    """Stop plugin if EDMC is closing."""
    if disco_object.logger:
        disco_object.logger.debug = (
            f"{disco_object.data.pluginname}->plugin_stop: start..."
        )
    disco_object.data.shutting_down = True
    if disco_object.logger:
        disco_object.logger.debug = (
            f"{disco_object.data.pluginname}->plugin_stop: shut down flag is set"
        )
    # something to do

    disco_object.data.db_processor.close()

    # shut down logger at last
    if disco_object.logger:
        disco_object.logger.debug = (
            f"{disco_object.data.pluginname}->plugin_stop: terminating the logger"
        )
    disco_object.qlog.put(None)
    disco_object.th_log.join()
    disco_object.th_log = None  # type: ignore


def plugin_app(parent: tk.Frame) -> ttk.Button:
    """Create a pair of TK widgets for the EDMarketConnector main window.

    parent:     The root EDMarketConnector window
    """
    if disco_object.data.dialog is None:
        disco_object.data.dialog = DiscoMainDialog(
            parent, disco_object.qlog, disco_object.data
        )
    button = disco_object.data.dialog.button()  # type: ignore
    CreateToolTip(
        button,
        [
            f"{disco_object.data.pluginname} v{disco_object.data.version}",
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
    disco_object.logger.debug = (
        f"{disco_object.data.pluginname}->prefs_changed: start..."
    )
    # set loglevel after config update
    disco_object.log_processor.loglevel = LogLevels().get(config.get_str("loglevel"))  # type: ignore
    disco_object.logger.debug = f"{disco_object.data.pluginname}->prefs_changed: done."


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

    if entry["event"] == "FSDJump":
        disco_object.data.system = disco_object.data.db_processor.add_system(entry)  # type: ignore
        test = True
        disco_object.logger.debug = f"FSDJump: {disco_object.data.system}"
    elif entry["event"] == "Scan" and entry["ScanType"] in (
        "AutoScan",
        "Detailed",
        "Basic",
        "NavBeaconDetail",
    ):
        disco_object.data.system = disco_object.data.db_processor.add_body(entry)  # type: ignore
        test = True
        disco_object.logger.debug = f"Scan: {disco_object.data.system}"
    elif entry[EDKeys.EVENT] == EDKeys.FSS_DISCOVERY_SCAN:
        disco_object.data.system = disco_object.data.db_processor.update_system(entry)  # type: ignore
        test = True
        disco_object.logger.debug = (
            f"{EDKeys.FSS_DISCOVERY_SCAN}: {disco_object.data.system}"
        )
    elif entry[EDKeys.EVENT] == EDKeys.FSS_BODY_SIGNALS:
        disco_object.data.system = disco_object.data.db_processor.add_signal(entry)  # type: ignore
        test = True
        disco_object.logger.debug = (
            f"{EDKeys.FSS_BODY_SIGNALS}: {disco_object.data.system}"
        )
    elif entry[EDKeys.EVENT] == EDKeys.SAA_SIGNALS_FOUND:
        disco_object.data.db_processor.add_signal(entry)
        disco_object.data.system = disco_object.data.db_processor.add_genus(entry)  # type: ignore
        test = True
        disco_object.logger.debug = (
            f"{EDKeys.SAA_SIGNALS_FOUND}: {disco_object.data.system}"
        )
    elif entry[EDKeys.EVENT] == "CodexEntry":
        disco_object.data.system = disco_object.data.db_processor.add_codex(entry)  # type: ignore
        test = True
        disco_object.logger.debug = f"CodexEntry: {disco_object.data.system}"
    elif entry[EDKeys.EVENT] == EDKeys.SCAN_ORGANIC:
        disco_object.data.system = disco_object.data.db_processor.add_genus(entry)  # type: ignore
        test = True
        disco_object.logger.debug = f"{EDKeys.SCAN_ORGANIC}: {disco_object.data.system}"
    elif entry[EDKeys.EVENT] == "SAAScanComplete":
        disco_object.data.system = disco_object.data.db_processor.mapped_body(entry)  # type: ignore
        test = True
    elif entry[EDKeys.EVENT] == "Location" and EDKeys.STAR_SYSTEM in entry:
        disco_object.data.system = disco_object.data.db_processor.get_system_by_name(
            entry[EDKeys.STAR_SYSTEM]
        )  # type: ignore
        test = True
    if test:
        dialog = disco_object.data.dialog
        dialog.update(disco_object.data.system)  # type: ignore


# #[EOF]#######################################################################
