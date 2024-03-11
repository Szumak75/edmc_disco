# -*- coding: UTF-8 -*-
"""
  Author:  Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
  Created: 18.12.2023

  Purpose: edmc plugin entry point
"""

import tkinter as tk
from tkinter import ttk
from typing import Dict, Optional, Tuple

from jsktoolbox.tktool.widgets import CreateToolTip

from config import config

from disco_libs.system import LogLevels
from disco_libs.dialogs import DiscoMainDialog
from disco_libs.disco import Disco

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
    elif entry["event"] == "FSSDiscoveryScan":
        disco_object.data.system = disco_object.data.db_processor.update_system(entry)  # type: ignore
        test = True
        disco_object.logger.debug = f"FSSDiscoveryScan: {disco_object.data.system}"
    elif entry["event"] == "FSSBodySignals":
        disco_object.data.system = disco_object.data.db_processor.add_signal(entry)  # type: ignore
        test = True
        disco_object.logger.debug = f"FSSBodySignals: {disco_object.data.system}"
    elif entry["event"] == "SAASignalsFound":
        disco_object.data.db_processor.add_signal(entry)
        disco_object.data.system = disco_object.data.db_processor.add_genus(entry)  # type: ignore
        test = True
        disco_object.logger.debug = f"SAASignalsFound: {disco_object.data.system}"
    elif entry["event"] == "CodexEntry":
        disco_object.data.system = disco_object.data.db_processor.add_codex(entry)  # type: ignore
        test = True
        disco_object.logger.debug = f"CodexEntry: {disco_object.data.system}"
    elif entry["event"] == "ScanOrganic":
        disco_object.data.system = disco_object.data.db_processor.add_genus(entry)  # type: ignore
        test = True
        disco_object.logger.debug = f"ScanOrganic: {disco_object.data.system}"
    elif entry["event"] == "SAAScanComplete":
        disco_object.data.system = disco_object.data.db_processor.mapped_body(entry)  # type: ignore
        test = True
    elif entry["event"] == "Location" and "StarSystem" in entry:
        disco_object.data.system = disco_object.data.db_processor.get_system_by_name(
            entry["StarSystem"]
        )  # type: ignore
        test = True
    if test:
        dialog = disco_object.data.dialog
        dialog.update(disco_object.data.system)  # type: ignore


# #[EOF]#######################################################################
