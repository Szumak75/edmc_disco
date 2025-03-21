# -*- coding: UTF-8 -*-
"""
Author:  Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
Created: 19.12.2023

Purpose:
"""


import stat
import tkinter as tk
from inspect import currentframe
from datetime import datetime
from queue import Queue, SimpleQueue
from tkinter import ttk
from types import FrameType
from typing import Dict, List, Optional, Union, Any

from disco.jsktoolbox.basetool.data import BData
from disco.jsktoolbox.raisetool import Raise
from disco.jsktoolbox.attribtool import NoDynamicAttributes
from disco.jsktoolbox.tktool.widgets import (
    CreateToolTip,
    VerticalScrolledTkFrame,
    StatusBarTkFrame,
)
from disco.jsktoolbox.tktool.base import TkBase
from disco.jsktoolbox.edmctool.base import BLogClient
from disco.jsktoolbox.edmctool.logs import LogClient
from disco.jsktoolbox.edmctool.ed_keys import EDKeys
from disco.jsktoolbox.edmctool.data import RscanData
from disco.jsktoolbox.edmctool.stars import StarsSystem

import disco.db_models as db
from disco.pics import Pics
from disco.dialogs_helper import DialogKeys
from disco.data import DiscoData


class _BDiscoDialog(BData):
    """Base class for Disco Dialogs."""

    @property
    def _button(self) -> ttk.Button:
        """Return the button widget."""
        return self._get_data(key=DialogKeys.BUTTON, default_value=None)  # type: ignore

    @_button.setter
    def _button(self, value: ttk.Button) -> None:
        """Set the button widget."""
        self._set_data(key=DialogKeys.BUTTON, value=value, set_default_type=ttk.Button)

    @property
    def _parent(self) -> tk.Frame:
        """Return the parent widget."""
        return self._get_data(key=DialogKeys.PARENT, default_value=None)  # type: ignore

    @_parent.setter
    def _parent(self, value: tk.Frame) -> None:
        """Set the parent widget."""
        self._set_data(key=DialogKeys.PARENT, value=value, set_default_type=tk.Frame)

    @property
    def _r_data(self) -> RscanData:
        """Return the RscanData object."""
        return self._get_data(key=DialogKeys.DATA)  # type: ignore

    @_r_data.setter
    def _r_data(self, value: RscanData) -> None:
        """Set the RscanData object."""
        self._set_data(key=DialogKeys.DATA, value=value, set_default_type=RscanData)

    @property
    def _fonts(self) -> BData:
        """Return the fonts object."""
        if self._get_data(key=DialogKeys.FONT_KEY, default_value=None) is None:  # type: ignore
            self._set_data(
                key=DialogKeys.FONT_KEY, value=BData(), set_default_type=BData
            )
        return self._get_data(key=DialogKeys.FONT_KEY)  # type: ignore

    @property
    def _tools(self) -> BData:
        """Return the tools object."""
        if self._get_data(key=DialogKeys.TOOLS_KEY, default_value=None) is None:  # type: ignore
            self._set_data(
                key=DialogKeys.TOOLS_KEY, value=BData(), set_default_type=BData
            )
        return self._get_data(key=DialogKeys.TOOLS_KEY)  # type: ignore

    @property
    def _widgets(self) -> BData:
        """Return the widgets object."""
        if self._get_data(key=DialogKeys.WIDGETS_KEY, default_value=None) is None:  # type: ignore
            self._set_data(
                key=DialogKeys.WIDGETS_KEY, value=BData(), set_default_type=BData
            )
        return self._get_data(key=DialogKeys.WIDGETS_KEY)  # type: ignore

    @property
    def _windows(self) -> List["DiscoSystemDialog"]:
        """Return the list of windows."""
        return self._get_data(key=DialogKeys.WINDOWS, default_value=None)  # type: ignore

    @_windows.setter
    def _windows(self, value: List) -> None:
        """Set the list of windows."""
        self._set_data(key=DialogKeys.WINDOWS, value=value, set_default_type=List)

    @property
    def _stars(self) -> List:
        """Return the list of stars."""
        return self._get_data(key=DialogKeys.STARS, default_value=None)  # type: ignore

    @_stars.setter
    def _stars(self, value: List) -> None:
        """Set the list of stars."""
        self._set_data(key=DialogKeys.STARS, value=value, set_default_type=List)

    @property
    def _start(self) -> StarsSystem:
        """Return the start object."""
        return self._get_data(key=DialogKeys.START, default_value=None)  # type: ignore

    @_start.setter
    def _start(self, value: StarsSystem) -> None:
        """Set the start object."""
        self._set_data(key=DialogKeys.START, value=value, set_default_type=StarsSystem)


class ImageHelper(NoDynamicAttributes):
    """ImageHelper class.

    It analyzes the data and returns the appropriate image and description.
    """

    def get_geo_image(self, body: db.TBody) -> bytes:
        """Return base64 encoded image string."""
        signals: db.TBodySignals = body.signals
        g_count: int = signals.count_geo_signals
        codexes: db.TBodyCodexes = body.codexes
        test: List[bool] = []
        for item in codexes.codexes:
            codex: db.TCodex = item
            if "Geology" in codex.subcategory_localised:
                test.append(True)
        if g_count <= len(test):
            return Pics.geologic_16
        return Pics.scan_geologic_16

    def get_bio_image(self, body: db.TBody) -> bytes:
        """Return base64 encoded image string."""
        signals: db.TBodySignals = body.signals
        b_count: int = signals.count_bio_signals
        genuses: db.TBodyGenuses = body.genuses
        test: List[bool] = []
        for item in genuses.genuses:
            genus: db.TGenus = item
            for item_scan in genus.scan:
                scan: db.TGenusScan = item_scan
                if scan:
                    test.append(scan.done)
        if b_count <= len(test) and all(test):
            return Pics.genomic_16
        return Pics.scan_genomic_16

    def get_bio_description(self, body: db.TBody) -> List[str]:
        """Return description about biological discoveries."""
        tmp: List[str] = []
        genuses: db.TBodyGenuses = body.genuses
        codexes: db.TBodyCodexes = body.codexes
        features: db.TBodyFeatures = body.features

        if features.atmosfere:
            tmp.append(f"Atmosfere: {features.atmosfere}")

        for item in genuses.genuses:
            genus: db.TGenus = item
            name: str = genus.genus_localised
            for item_scan in genus.scan:
                scan: db.TGenusScan = item_scan
                if scan:
                    name = (
                        scan.species_localised
                        if scan.variant_localised == ""
                        else scan.variant_localised
                    )
                if scan.variant_localised == "" and scan.done:
                    for item in codexes.codexes:
                        codex: db.TCodex = item
                        if scan.species_localised in codex.name_localised:
                            name = codex.name_localised
                if scan.done:
                    tmp.append(name)
                else:
                    tmp.append(f"[{scan.count}]: {name}")
            if not genus.scan:
                tmp.append(f"[0]: {name}")
        if not genuses.genuses:
            tmp.append("Detailed surface scanning needed.")
        return tmp

    def get_geo_description(self, body: db.TBody) -> List[str]:
        """Return description about geological discoveries."""
        tmp: List[str] = []
        codexes: db.TBodyCodexes = body.codexes
        features: db.TBodyFeatures = body.features

        if features.volcanism:
            tmp.append(f"Features: {features.volcanism}")

        for item in codexes.codexes:
            codex: db.TCodex = item
            if "Geology" in codex.subcategory_localised:
                tmp.append(f"{codex.name_localised}")
        if not codexes.codexes:
            tmp.append("Detailed surface scanning needed.")
        return tmp

    def get_human_image(self) -> bytes:
        """Return base64 encoded image string."""
        return Pics.human_16

    def get_scoopable_image(self) -> bytes:
        """Return base64 encoded image string."""
        return Pics.scoopable_16

    def get_landable_image(self) -> bytes:
        """Return base64 encoded image string."""
        return Pics.landable_16

    def get_distance_image(self) -> bytes:
        """Return base64 encoded image string."""
        return Pics.distance_16

    def get_thermometer_image(self) -> bytes:
        """Return base64 encoded image string."""
        return Pics.temp_16

    def get_terraform_image(self) -> bytes:
        """Returns base64 encoding image."""
        return Pics.terraform_16

    def get_first_image(self) -> bytes:
        """Return base64 encoded image string."""
        return Pics.first_16

    def get_map_image(self) -> bytes:
        """Return base64 encoded image string."""
        return Pics.map_16

    def get_body_image(self, body: db.TBody) -> Optional[bytes]:
        """Return base64 encoded image string."""
        features: db.TBodyFeatures = body.features
        if features is None:
            return None
        # star
        if features.star_type is not None:
            # neutron star
            if features.star_type in (
                "N",
                "DA",
                "DAB",
                "DAV",
                "DAZ",
                "DB",
                "DBV",
                "DBZ",
                "DOV",
                "DC",
                "DCV",
            ):
                return Pics.neutron_16
            # blackhole
            if features.star_type == "H" and features.luminosity == "VII":
                return Pics.blackhole_16
            # other
            return Pics.star_16
        # planet
        if features.body_type and features.body_type == "Planet":
            if features.planet_class and "Rocky" in features.planet_class:
                if features.atmosfere:
                    return Pics.rocky_atm_16
                return Pics.rocky_16
            if features.planet_class and "gas giant" in features.planet_class:
                return Pics.gassy_16
            if features.atmosferetype == "EarthLike":
                return Pics.planet_earth_like_16
            if features.atmosfere:
                return Pics.planet_atm_16
            return Pics.planet_16
        # ring or cluster
        if (
            features.body_type
            and features.body_type in ("Cluster", EDKeys.RING)
            or body.name.endswith(" Ring")
        ):
            return Pics.belt_16

        return None


class DiscoMainDialog(BLogClient, DiscoData, NoDynamicAttributes):
    """Create dialog for main EDMC window."""

    def __init__(
        self,
        parent: tk.Frame,
        log_queue: Union[Queue, SimpleQueue],
        disco_data: DiscoData,
    ) -> None:
        """Initialize datasets."""
        DiscoData.__init__(self)
        if isinstance(disco_data, DiscoData):
            for keys in disco_data._data.keys():
                self._data[keys] = disco_data._data[keys]
        else:
            raise Raise.error(
                f"Expected DiscoData type, received:'{type(disco_data)}'.",
                TypeError,
                self._c_name,
                currentframe(),
            )

        # init log subsystem
        self.logger = LogClient(log_queue)

        self._set_data(key=DialogKeys.PARENT, value=parent, set_default_type=tk.Frame)

        # created dialogs
        self._set_data(key=DialogKeys.WINDOWS, value=[], set_default_type=List)

    @property
    def button(self) -> ttk.Button:
        """Create the button for main application frame."""
        if self._get_data(key=DialogKeys.BUTTON, default_value=None) is None:
            self._set_data(
                key=DialogKeys.BUTTON,
                value=ttk.Button(
                    self._get_data(key=DialogKeys.PARENT),
                    text="Search System",
                    command=self.__bt_callback,
                    default=tk.ACTIVE,
                ),
                set_default_type=ttk.Button,
            )
            self._get_data(DialogKeys.BUTTON).grid(sticky=tk.NSEW)  # type: ignore
        return self._get_data(DialogKeys.BUTTON)  # type: ignore

    def dialog_update(self, system: db.TSystem) -> None:
        """Update dialog."""
        self.system = system
        if self.system is not None and self.system.name != "":
            self.button[DialogKeys.TEXT] = (
                f"{self.system.name} [{self.system.progress}]"
            )
        if self.logger:
            self.logger.debug = f"UPDATE: {self._data}"

        # propagate update
        for window in self._get_data(key=DialogKeys.WINDOWS):  # type:ignore
            if not window.is_closed:
                window.dialog_update(system)

    def __bt_callback(self) -> None:
        """Run main button callback."""
        self.debug(currentframe(), "click!")
        # purge closed window from list
        for window in self._get_data(key=DialogKeys.WINDOWS):  # type:ignore
            if window.is_closed:
                self._get_data(key=DialogKeys.WINDOWS).remove(window)  # type: ignore
        # create new window
        if self.logger:
            window = DiscoSystemDialog(self.logger.queue, self._data)
            self._get_data(key=DialogKeys.WINDOWS).append(window)  # type: ignore
            self.debug(
                currentframe(),
                f"numbers of windows: {len(self._get_data(key=DialogKeys.WINDOWS))}",  # type: ignore
            )

    def debug(self, currentframe: Optional[FrameType], message: str = "") -> None:
        """Build debug message."""
        p_name: str = f"{self.plugin_name}"
        c_name: str = f"{self._c_name}"
        m_name: str = f"{currentframe.f_code.co_name}" if currentframe else ""
        if message != "":
            message = f": {message}"
        if self.logger:
            self.logger.debug = f"{p_name}->{c_name}.{m_name}{message}"


class DiscoSystemDialog(tk.Toplevel, TkBase, DiscoData, BLogClient):
    """Create new window for showing system features."""

    def __init__(
        self, log_queue: Union[Queue, SimpleQueue], data: Dict, master=None
    ) -> None:
        """Initialize datasets."""
        super().__init__(master=master)

        DiscoData.__init__(self)
        if isinstance(data, Dict):
            for keys in data.keys():
                self._data[keys] = data[keys]
        else:
            raise Raise.error(
                f"Expected Dict type, received: '{type(data)}'.",
                TypeError,
                self._c_name,
                currentframe(),
            )
        self._set_data(key=DialogKeys.CLOSED, value=False, set_default_type=bool)
        #  widgets container
        self._set_data(key=DialogKeys.WIDGETS, value={}, set_default_type=Dict)
        #  widgets declaration (if any):
        self.widgets[DialogKeys.STATUS] = None  #: Optional[tk.StringVar]
        self.widgets[DialogKeys.SYSTEM] = None  #: Optional[tk.Entry]
        self.widgets[DialogKeys.S_BUTTON] = None  #: Optional[tk.Button]
        self.widgets[DialogKeys.F_DATA] = None  #: Optional[tk.LabelFrame]
        self.widgets[DialogKeys.SCROLLBAR] = None  #: Optional[tk.Scrollbar]
        self.widgets[DialogKeys.S_PANEL] = None  #: Optional[VerticalScrolledFrame]
        self.widgets[DialogKeys.S_MENU] = None  #: Optional[tk.Menu]

        # bodies data
        self.bodies = []

        # init log subsystem
        if isinstance(log_queue, Queue):
            self.logger = LogClient(log_queue)
        else:
            raise Raise.error(
                f"Expected Queue type, received: '{type(log_queue)}'.",
                TypeError,
                self._c_name,
                currentframe(),
            )
        self.debug(currentframe(), "Initialize dataset")
        #  some other init

        # create frame
        self.__build_frame()

        # search system if was in data
        if self.system:
            self.__search_cb()

        # end work
        self.debug(currentframe(), "Constructor work done")

    @property
    def widgets(self) -> Dict:
        """Return widgets dictionary."""
        return self._get_data(
            DialogKeys.WIDGETS,
        )  # type: ignore

    @property
    def bodies(self) -> List:
        """Return bodies list."""
        return self._get_data(key=DialogKeys.BODIES)  # type: ignore

    @bodies.setter
    def bodies(self, value: List) -> None:
        if self._get_data(key=DialogKeys.BODIES):
            # freeing last object list
            self._clear_data(key=DialogKeys.BODIES)
        self._set_data(
            key=DialogKeys.BODIES,
            value=value,
            set_default_type=List,
        )

    def __build_frame(self) -> None:
        """Create window."""
        self.debug(currentframe(), f"Data: {self._data}")
        self.title(self.plugin_name)
        self.geometry("700x600")
        self.minsize(height=500, width=400)
        # menu TODO
        # menubar = tk.Menu(self)
        # self.config(menu=menubar)
        # search_bio_menu = tk.Menu(
        #     menubar,
        #     tearoff=0,
        # )
        # search_bio_menu.add_cascade(label="Nearest", command=self.__search_bio_cb)
        # search_bio_menu.add_cascade(
        #     label="Nearest unexplored", command=self.__search_unx_bio_cb
        # )
        # menubar.add_cascade(label="Search Bio", menu=search_bio_menu)
        # self.widgets[DialogKeys.S_MENU] = menubar
        # grid configuration
        self.columnconfigure(0, weight=100)
        self.columnconfigure(1, weight=1)
        # label row
        r_label_idx = 0
        self.rowconfigure(r_label_idx, weight=1)
        # command row
        r_command_idx = r_label_idx + 1
        self.rowconfigure(r_command_idx, weight=1)
        # data row
        r_data_idx = r_command_idx + 1
        self.rowconfigure(r_data_idx, weight=100)
        # status row
        r_status_idx = r_data_idx + 1
        self.rowconfigure(r_status_idx, weight=1)

        # create label
        label = tk.Label(self, text="Discoveries Explorer")
        label.grid(row=r_label_idx, column=0, columnspan=2)

        # create command panel
        command_frame = tk.LabelFrame(self, text=" Search System ")
        command_frame.grid(
            row=r_command_idx,
            column=0,
            columnspan=2,
            padx=5,
            pady=5,
            ipadx=5,
            ipady=5,
            sticky=tk.EW,
        )
        command_frame.columnconfigure(0, weight=1)
        command_frame.columnconfigure(1, weight=100)
        command_frame.columnconfigure(2, weight=1)
        command_frame.rowconfigure(0, weight=1)
        tk.Label(command_frame, text="Star System:").grid(row=0, column=0, sticky=tk.E)
        system_name = tk.Entry(command_frame, textvariable=tk.StringVar(value=""))
        system_name.grid(row=0, column=1, sticky=tk.EW)
        system_name.bind("<Return>", self.__search_cb)
        if self.system is not None:
            system_name.delete(0, tk.END)
            system_name.insert(0, self.system.name)
        system_name.focus_set()
        self.widgets[DialogKeys.SYSTEM] = system_name

        button_search_img = tk.PhotoImage(data=Pics.SEARCH_16)
        button_search = tk.Button(
            command_frame, image=button_search_img, command=self.__search_cb
        )
        button_search.image = button_search_img  # type: ignore
        button_search.grid(row=0, column=2, sticky=tk.E, padx=5)
        CreateToolTip(button_search, "Find system.")
        self.widgets[DialogKeys.S_BUTTON] = button_search

        # create data panel
        data_frame = tk.LabelFrame(self, text=" System ")
        data_frame.grid(
            row=r_data_idx, column=0, columnspan=2, padx=5, pady=5, sticky=tk.NSEW
        )
        self.widgets[DialogKeys.F_DATA] = data_frame

        # create scrolled panel
        s_panel = VerticalScrolledTkFrame(data_frame)
        s_panel.pack(ipadx=1, ipady=1, fill=tk.BOTH, expand=tk.TRUE)
        self.widgets[DialogKeys.S_PANEL] = s_panel

        # create status panel
        status_frame = StatusBarTkFrame(self)
        status_frame.grid(row=r_status_idx, column=0, columnspan=2, sticky=tk.EW)

        self.widgets[DialogKeys.STATUS] = status_frame
        status_frame.clear()

        # closing event
        self.protocol("WM_DELETE_WINDOW", self.__on_closing)

    def __on_closing(self) -> None:
        """Run on closing event."""
        self.debug(currentframe(), "Window is closing now.")
        self._set_data(key=DialogKeys.CLOSED, value=True)
        self.destroy()

    def __search_cb(self, event=None) -> None:
        """Search system button callback."""
        self.status = ""
        system = self.widgets[DialogKeys.SYSTEM].get()

        if not system:
            self.status = "System name must be set for processing request."
            return

        # search database
        t_system: Optional[db.TSystem] = self.db_processor.get_system_by_name(system)
        if t_system is None:
            self.status = f"System '{system}' not found in local database."
            return
        if self.logger:
            self.logger.debug = f"System found: {t_system}"
            self.logger.debug = f"SystemName: {t_system.name}"
            self.logger.debug = f"Bodies count: {t_system.bodycount}"

        # show system
        self.__system_show(t_system)
        # self.logger.debug = f"After Show: {self._data}"

    def __search_bio_cb(self, event=None) -> None:
        """Search system button callback."""

    def __search_unx_bio_cb(self, event=None) -> None:
        """Search system button callback."""

    def __system_show(self, system: db.TSystem) -> None:
        """Show system in frame."""
        # destroy previous data
        self.system = system
        self.__clear_rows()
        self.__system_summary(system)
        count = 0
        for body in sorted(system.bodies, key=lambda x: x.bodyid):
            if self.logger:
                self.logger.debug = f"[{count}]: name '{body.name}', bodyid={body.bodyid}, parentid={body.parentid}"
            count += 1
        count = 0
        for body in self.__sort_bodies(system):
            if body:
                if self.logger:
                    self.logger.debug = f"[{count}]: name '{body.name}', bodyid={body.bodyid}, parentid={body.parentid}"
                if not body.name:
                    if self.logger:
                        self.logger.debug = f"Error in TBody: {body}"
            else:
                if self.logger:
                    self.logger.debug = f"[{count}]: None"
            # add to form
            self.__build_row_frame(count, body)
            count += 1

    def __body_summary(self, body: db.TBody) -> List[str]:
        """Create body info string for tooltip."""
        tmp = []
        features: db.TBodyFeatures = body.features
        # star
        if features.star_type:
            tmp.append(
                f"Spectral class: {features.star_type or ''}{features.subclass or ''} {features.luminosity or ''}"
            )
            tmp.append(f"Solar masses: {features.stellarmass:.3f}")
            if features.radius:
                tmp.append(f"Solar radius: {int(features.radius)}")
            if features.surfacetemperature:
                tmp.append(
                    f"Surface temperature: {int(features.surfacetemperature or '??')} K"
                )
        # planet
        if features.body_type and features.body_type == "Planet":
            tmp.append(f"Planet class: {features.planet_class}")
            if features.surfacegravity:
                tmp.append(f"Gravity: {features.surfacegravity:.3f}")
            if features.massem:
                tmp.append(f"Earth mass: {features.massem:.3f}")
            if features.radius:
                tmp.append(f"Radius: {int(features.radius)}")
            if features.surfacetemperature:
                tmp.append(
                    f"Surface temp.: {int(features.surfacetemperature) or '??'} K"
                )
            if features.surfacepressure:
                tmp.append(f"Surface press.: {int(features.surfacepressure / 100)} hPa")
            if features.volcanism:
                tmp.append(f"Volcanism: {features.volcanism}")
            tmp.append(f"Atmosfere: {features.atmosfere or features.atmosferetype}")
            if features.terraformstate:
                tmp.append(f"Terraforming: {features.terraformstate}")

        return tmp

    def __system_summary(self, system: db.TSystem) -> None:
        """Create system info."""
        list_object = [-1, None]
        dt_object: datetime = datetime.fromtimestamp(system.timestamp)

        # frame
        frame = tk.Frame(
            self.widgets[DialogKeys.S_PANEL].interior,
            borderwidth=1,
            relief=tk.GROOVE,
        )
        frame.pack(fill=tk.X)
        list_object.append(frame)
        features: db.TSystemFeatures = system.features

        # grid configure
        for i in range(3):
            frame.columnconfigure(i)
            for j in range(2):
                frame.rowconfigure(j)

        # create info
        cell: Dict[str, Any] = {
            "ipadx": 10,
            "sticky": tk.W,
        }
        tk.Label(frame, text=f"Security: {features.security}").grid(
            column=0, row=0, **cell
        )
        tk.Label(
            frame,
            text=f"Allegiance: {features.allegiance or 'None'}",
        ).grid(column=1, row=0, **cell)
        tk.Label(frame, text=f"Population: {features.population}").grid(
            column=2, row=0, **cell
        )
        tk.Label(frame, text=f"Body count: {system.bodycount}").grid(
            column=0, row=1, **cell
        )
        tk.Label(
            frame,
            text=f"Discovered: {system.scanned_body_count}",
        ).grid(column=1, row=1, **cell)
        tk.Label(frame, text=f"Last update: {dt_object}").grid(column=2, row=1, **cell)

        # finish
        self.bodies.append(list_object)

    def __sort_bodies(self, system: db.TSystem) -> List[db.TBody]:
        """Return sorted db.Bodies List."""
        bodies = []
        # find max bodyid
        bid = 0
        for body in system.bodies:
            if bid < body.bodyid:
                bid = body.bodyid
        # generate null table
        i = 0
        while i in range(bid + 1):
            bodies.append(None)
            i += 1
        # fill in the table
        for body in system.bodies:
            bodies[body.bodyid] = body
            if bodies[body.parentid] is None:
                bodies[body.parentid] = ""
        # copy output table
        out = []
        for body in bodies:
            if body is not None:
                if not isinstance(body, str):
                    features: db.TBodyFeatures = body.features
                    if features.body_type and features.body_type == "Null":
                        continue
                out.append(body)
        return out
        # return sorted(out, key=lambda x: x.features.distance)

    def __clear_rows(self) -> None:
        """Destroy previous data."""
        for item in self.bodies:
            item[2].pack_forget()
            item[2].destroy()
        self.bodies = []

    def __build_row_frame(self, count: int, body: db.TBody) -> None:
        """Build Frame row for search dialog."""
        list_object = []
        ih = ImageHelper()

        # color = 0xD9D9D9
        # color1: str = hex(color - 20).replace("0x", "#")
        # color2: str = hex(color + 20).replace("0x", "#")

        # [0] count
        list_object.append(count)

        # [1] body
        list_object.append(body)

        # [2] frame
        frame = tk.Frame(
            self.widgets[DialogKeys.S_PANEL].interior,
            # background=color1 if count % 2 else color2,
            relief=tk.GROOVE,
            borderwidth=1,
        )

        frame.pack(fill=tk.X)
        list_object.append(frame)

        # create labels
        lname = None
        if body:
            name = f"??? id: {body.bodyid}"
            if body.name:
                name = body.name
                signals: db.TBodySignals = body.signals
                features: db.TBodyFeatures = body.features
                if not features.star_type and self.system:
                    name: str = name.replace(self.system.name, "").strip()
                # get scoopable
                if features.star_type and features.star_type in (
                    "O",
                    "B",
                    "A",
                    "F",
                    "G",
                    "K",
                    "M",
                ):
                    img = tk.PhotoImage(data=ih.get_scoopable_image())
                    scoop = tk.Label(frame, image=img)
                    scoop.image = img  # type: ignore
                    scoop.pack(side=tk.RIGHT)
                    CreateToolTip(scoop, "Scoopable")
                # get distance to arrival
                if features.distance:
                    img = tk.PhotoImage(data=ih.get_distance_image())
                    distance = tk.Label(
                        frame,
                        text=f"{int(features.distance)} ls",  # type: ignore
                        compound=tk.LEFT,
                        image=img,
                    )
                    distance.image = img  # type: ignore
                    distance.pack(side=tk.RIGHT)
                    CreateToolTip(distance, "Distance to arrival")
                # get landable flag
                if features.landable:
                    # get temperature
                    img2 = tk.PhotoImage(data=ih.get_thermometer_image())
                    temp = tk.Label(
                        frame,
                        text=f"{int(features.surfacetemperature)}K",  # type: ignore
                        compound=tk.LEFT,
                        image=img2,
                    )
                    temp.image = img2  # type: ignore
                    temp.pack(side=tk.RIGHT)
                    CreateToolTip(temp, "Surface temperature")
                    img = tk.PhotoImage(data=ih.get_landable_image())
                    landable = tk.Label(frame, image=img)
                    landable.image = img  # type: ignore
                    landable.pack(side=tk.RIGHT)
                    CreateToolTip(landable, "Planetary Landing")
                # get terraformstate state
                if features.terraformstate:
                    img = tk.PhotoImage(data=ih.get_terraform_image())
                    terraform = tk.Label(frame, image=img)
                    terraform.image = img  # type: ignore
                    terraform.pack(side=tk.RIGHT)
                    CreateToolTip(
                        terraform, f"Terraform state: {features.terraformstate}"
                    )
                # get human signals
                if signals.count_humans_signals > 0:
                    img = tk.PhotoImage(data=ih.get_human_image())
                    humans = tk.Label(
                        frame,
                        text=f"{signals.count_humans_signals}",
                        compound=tk.LEFT,
                        image=img,
                    )
                    humans.image = img  # type: ignore
                    humans.pack(side=tk.RIGHT)
                    CreateToolTip(humans, "Human signals")
                # get biological signals count
                if signals.count_bio_signals > 0:
                    img = tk.PhotoImage(data=ih.get_bio_image(body))
                    count_bio = tk.Label(
                        frame,
                        text=f"{signals.count_bio_signals }",
                        compound=tk.LEFT,
                        image=img,
                    )
                    count_bio.image = img  # type: ignore
                    count_bio.pack(side=tk.RIGHT)
                    CreateToolTip(count_bio, ih.get_bio_description(body))
                # get geological signals count
                if signals.count_geo_signals > 0:
                    img = tk.PhotoImage(data=ih.get_geo_image(body))
                    count_geo = tk.Label(
                        frame,
                        text=f"{signals.count_geo_signals}",
                        compound=tk.LEFT,
                        image=img,
                    )
                    count_geo.image = img  # type: ignore
                    count_geo.pack(side=tk.RIGHT)
                    CreateToolTip(count_geo, ih.get_geo_description(body))
                # first mapped
                if features.mapped_first:
                    img = tk.PhotoImage(data=ih.get_map_image())
                    mape = tk.Label(frame, image=img)
                    mape.image = img  # type: ignore
                    mape.pack(side=tk.RIGHT)
                    CreateToolTip(mape, "First mapped")
                # first discovered
                if features.discovered_first:
                    img = tk.PhotoImage(data=ih.get_first_image())
                    first = tk.Label(frame, image=img)
                    first.image = img  # type: ignore
                    first.pack(side=tk.RIGHT)
                    CreateToolTip(first, "First discovered")
            elif not body.name:
                features: db.TBodyFeatures = body.features
                if features.body_type and features.body_type == EDKeys.RING:
                    name = EDKeys.RING
            img_byte: Optional[bytes] = ih.get_body_image(body)
            if img_byte:
                img = tk.PhotoImage(data=img_byte)
                lname = tk.Label(frame, text=f"{name}", compound=tk.LEFT, image=img)
                lname.image = img  # type: ignore
            else:
                lname = tk.Label(frame, text=f"{name}")
            # generate body summaries tooltip
            desc: List[str] = self.__body_summary(body)
            if desc:
                CreateToolTip(lname, desc)
        else:
            lname = tk.Label(frame, text="???")
        lname.pack(side=tk.LEFT)

        # finish
        self.bodies.append(list_object)

    def dialog_update(self, system: Optional[db.TSystem]) -> None:
        """Update dialog."""
        if self.system is None or system is None:
            return
        if self.system.id == system.id:
            self.__system_show(system)

    @property
    def is_closed(self) -> bool:
        """Check, if window is closed."""
        return self._get_data(key=DialogKeys.CLOSED)  # type: ignore

    def debug(self, currentframe: Optional[FrameType], message: str = "") -> None:
        """Build debug message."""
        p_name: str = f"{self.plugin_name}"
        c_name: str = f"{self._c_name}"
        m_name: str = f"{currentframe.f_code.co_name}" if currentframe else ""
        if message != "":
            message = f": {message}"
        if self.logger:
            self.logger.debug = f"{p_name}->{c_name}.{m_name}{message}"

    @property
    def status(self) -> StatusBarTkFrame:
        """Return status object."""
        return self.widgets[DialogKeys.STATUS]

    @status.setter
    def status(self, message: Optional[Union[str, int, float]]) -> None:
        """Set status message."""
        if self.status is not None:
            if message:
                self.status.set(f"{message}")
            else:
                self.status.clear()


class DiscoSearchSystem(tk.Toplevel, TkBase, _BDiscoDialog, DiscoData, BLogClient):
    """Dialog for search system."""

    def __init__(
        self, log_queue: Union[Queue, SimpleQueue], data: Dict, master=None
    ) -> None:
        """Initialize dialog."""
        super().__init__(master=master)

        DiscoData.__init__(self)
        if isinstance(data, Dict):
            for keys in data.keys():
                self._data[keys] = data[keys]
        else:
            raise Raise.error(
                f"Expected Dict type, received: '{type(data)}'.",
                TypeError,
                self._c_name,
                currentframe(),
            )

        # init log subsystem
        if isinstance(log_queue, Queue):
            self.logger = LogClient(log_queue)
        else:
            raise Raise.error(
                f"Expected Queue type, received: '{type(log_queue)}'.",
                TypeError,
                self._c_name,
                currentframe(),
            )

        self._set_data(key=DialogKeys.CLOSED, value=False, set_default_type=bool)

        #  widgets container
        self._widgets._set_data(
            key=DialogKeys.STATUS,
            value=None,
            set_default_type=Optional[StatusBarTkFrame],
        )

        self.debug(currentframe(), "Initialize dataset")
        #  some other init

        # create frame
        self.__build_frame()

        # end work
        self.debug(currentframe(), "Constructor work done")

    def __build_frame(self) -> None:
        """Create window."""
        self.debug(currentframe(), f"Data: {self._data}")
        self.title(self.plugin_name)
        self.geometry("700x600")
        self.minsize(height=500, width=400)

        # closing event
        self.protocol("WM_DELETE_WINDOW", self.__on_closing)

    def __on_closing(self) -> None:
        """Run on closing event."""
        self.debug(currentframe(), "Window is closing now.")
        self._set_data(key=DialogKeys.CLOSED, value=True)
        self.destroy()

    def debug(self, currentframe: Optional[FrameType], message: str = "") -> None:
        """Build debug message."""
        p_name: str = f"{self.plugin_name}"
        c_name: str = f"{self._c_name}"
        m_name: str = f"{currentframe.f_code.co_name}" if currentframe else ""
        if message != "":
            message = f": {message}"
        if self.logger:
            self.logger.debug = f"{p_name}->{c_name}.{m_name}{message}"


# #[EOF]#######################################################################
