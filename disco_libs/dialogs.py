# -*- coding: UTF-8 -*-
"""
  Author:  Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
  Created: 19.12.2023

  Purpose:
"""


import tkinter as tk
from inspect import currentframe
from datetime import datetime
from queue import Queue
from tkinter import ttk
from types import FrameType
from typing import Dict, List, Optional, Union
from jsktoolbox.raisetool import Raise
from jsktoolbox.attribtool import NoDynamicAttributes


import disco_libs.db_models as db
from disco_libs.data import DiscoData
from disco_libs.dialogs_tools import CreateToolTip
from disco_libs.base_logs import BLogClient
from disco_libs.pics import Pics
from disco_libs.system import LogClient
from disco_libs.dialogs_helper import DialogKeys


class ImageHelper(NoDynamicAttributes):
    """ImageHelper class.

    It analyzes the data and returns the appropriate image and description.
    """

    def get_geo_image(self, body: db.TBody) -> str:
        """Return base64 encoded image string."""
        signals: db.TBodySignals = body.signals
        gcount: int = signals.count_geo_signals
        codexes: db.TBodyCodexes = body.codexes
        test = []
        for item in codexes.codexes:
            codex: db.TCodex = item
            if "Geology" in codex.subcategory_localised:
                test.append(True)
        if gcount <= len(test):
            return Pics.geologic_16
        return Pics.scan_geologic_16

    def get_bio_image(self, body: db.TBody) -> str:
        """Return base64 encoded image string."""
        signals: db.TBodySignals = body.signals
        bcount: int = signals.count_bio_signals
        genuses: db.TBodyGenuses = body.genuses
        test = []
        for item in genuses.genuses:
            genus: db.TGenus = item
            for iscan in genus.scan:
                scan: db.TGenusScan = iscan
                if scan:
                    test.append(scan.done)
        if bcount <= len(test) and all(test):
            return Pics.genomic_16
        return Pics.scan_genomic_16

    def get_bio_descript(self, body: db.TBody) -> List[str]:
        """Return description about biological discoveries."""
        tmp = []
        genuses: db.TBodyGenuses = body.genuses
        codexes: db.TBodyCodexes = body.codexes
        features: db.TBodyFeatures = body.features

        if features.atmosfere:
            tmp.append(f"Atmosfere: {features.atmosfere}")

        for item in genuses.genuses:
            genus: db.TGenus = item
            name: str = genus.genus_localised
            for iscan in genus.scan:
                scan: db.TGenusScan = iscan
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

    def get_geo_descript(self, body: db.TBody) -> List[str]:
        """Return description about geological discoveries."""
        tmp = []
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

    def get_humans_image(self) -> str:
        """Return base64 encoded image string."""
        return Pics.humans_16

    def get_scoopable_image(self) -> str:
        """Return base64 encoded image string."""
        return Pics.scoopable_16

    def get_landable_image(self) -> str:
        """Return base64 encoded image string."""
        return Pics.landable_16

    def get_distance_image(self) -> str:
        """Return base64 encoded image string."""
        return Pics.distance_16

    def get_thermometer_image(self) -> str:
        """Return base64 encoded image string."""
        return Pics.temp_16

    def get_first_image(self) -> str:
        """Return base64 encoded image string."""
        return Pics.first_16

    def get_map_image(self) -> str:
        """Return base64 encoded image string."""
        return Pics.map_16

    def get_body_image(self, body: db.TBody) -> Optional[str]:
        """Return base64 encoded image string."""
        features: db.TBodyFeatures = body.features
        if features is None:
            return None
        # star
        if features.star_type is not None:
            # neutron star
            if features.star_type == "N":
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
                return Pics.planet_earthlike_16
            if features.atmosfere:
                return Pics.planet_atm_16
            return Pics.planet_16
        # ring or cluster
        if (
            features.body_type
            and features.body_type in ("Ring", "Cluster")
            or body.name.endswith(" Ring")
        ):
            return Pics.belt_16

        return None


class DiscoMainDialog(BLogClient, DiscoData, NoDynamicAttributes):
    """Create dialog for main EDMC window."""

    def __init__(
        self,
        parent: tk.Frame,
        log_queue: Queue,
        ddata: DiscoData,
    ):
        """Initialize datasets."""
        DiscoData.__init__(self)
        if isinstance(ddata, DiscoData):
            self._data = ddata._data
        else:
            raise Raise.error(
                f"Expected DiscoData type, received:'{type(ddata)}'.",
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

        if isinstance(parent, tk.Frame):
            self._data[DialogKeys.PARENT] = parent
        else:
            raise Raise.error(
                f"Expected tk.Frame type, received: '{type(parent)}'",
                TypeError,
                self._c_name,
                currentframe(),
            )

        # created dialogs
        self._data[DialogKeys.WINDOWS] = []

    def button(self) -> ttk.Button:
        """Create the button for main application frame."""
        if DialogKeys.BUTTON not in self._data or self._data[DialogKeys.BUTTON] is None:
            self._data[DialogKeys.BUTTON] = ttk.Button(
                self._data[DialogKeys.PARENT],
                text="Search System",
                command=self.__bt_callback,
                default=tk.ACTIVE,
            )
            self._data[DialogKeys.BUTTON].grid(sticky=tk.NSEW)
        return self._data[DialogKeys.BUTTON]

    def update(self, system: db.TSystem) -> None:
        """Update dialog."""
        self.system = system
        button: ttk.Button = self._data[DialogKeys.BUTTON]
        button[DialogKeys.TEXT] = f"{self.system.name} [{self.system.progress}]"
        self.logger.debug = f"UPDATE: {self._data}"

        # propagate update
        for window in self._data[DialogKeys.WINDOWS]:
            window.update(system)

    def __bt_callback(self) -> None:
        """Run main button callback."""
        self.debug(currentframe(), "click!")
        # purge closed window from list
        for window in self._data[DialogKeys.WINDOWS]:
            if window.is_closed:
                self._data[DialogKeys.WINDOWS].remove(window)
        # create new window
        window = DiscoSystemDialog(self.logger.queue, self._data)
        self._data[DialogKeys.WINDOWS].append(window)
        self.debug(
            currentframe(),
            f"numbers of windows: {len(self._data[DialogKeys.WINDOWS])}",
        )

    def debug(self, currentframe: FrameType, message: str = "") -> None:
        """Build debug message."""
        pname = f"{self.pluginname}"
        cname = f"{self._c_name}"
        mname = f"{currentframe.f_code.co_name}"
        if message != "":
            message = f": {message}"
        self.logger.debug = f"{pname}->{cname}.{mname}{message}"


class DiscoSystemDialog(tk.Toplevel, DiscoData, BLogClient):
    """Create new window for showing system features."""

    _w = None
    widgetName = None
    master = None
    tk = None
    _name = None
    children = None

    def __init__(self, log_queue: Queue, data: Dict, master=None) -> None:
        """Initialize datasets."""
        super().__init__(master=master)

        DiscoData.__init__(self)
        if isinstance(data, Dict):
            self._data = data
        else:
            raise Raise.error(
                f"Expected Dict type, received: '{type(data)}'.",
                TypeError,
                self._c_name,
                currentframe(),
            )
        self._data[DialogKeys.CLOSED] = False
        #  widgets container
        self._data[DialogKeys.WIDGETS] = {}
        #  widgets declaration (if any):
        self._data[DialogKeys.WIDGETS][DialogKeys.STATUS]: Optional[tk.StringVar] = None
        self._data[DialogKeys.WIDGETS][DialogKeys.SYSTEM]: Optional[tk.Entry] = None
        self._data[DialogKeys.WIDGETS][DialogKeys.SBUTTON]: Optional[tk.Button] = None
        self._data[DialogKeys.WIDGETS][DialogKeys.FDATA]: Optional[tk.LabelFrame] = None
        self._data[DialogKeys.WIDGETS][DialogKeys.SCROLLBAR]: Optional[
            tk.Scrollbar
        ] = None
        self._data[DialogKeys.WIDGETS][DialogKeys.SPANEL]: Optional[
            VerticalScrolledFrame
        ] = None

        # bodys data
        self._data[DialogKeys.BODIES] = []

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

    def __build_frame(self) -> None:
        """Create window."""
        self.debug(currentframe(), f"Data: {self._data}")
        self.title(self.pluginname)
        self.geometry("700x600")
        # grid configuration
        self.columnconfigure(0, weight=1)
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
        label.grid(row=r_label_idx)

        # create command panel
        command_frame = tk.LabelFrame(self, text=" Search System ")
        command_frame.grid(
            row=r_command_idx, padx=5, pady=5, ipadx=2, ipady=2, sticky=tk.EW
        )
        command_frame.columnconfigure(0, weight=1)
        command_frame.columnconfigure(1, weight=100)
        command_frame.columnconfigure(2, weight=1)
        command_frame.rowconfigure(0, weight=1)
        tk.Label(command_frame, text="Star System:").grid(row=0, column=0, sticky=tk.E)
        system_name = tk.Entry(command_frame, textvariable="")
        system_name.grid(row=0, column=1, sticky=tk.EW)
        system_name.bind("<Return>", self.__search_cb)
        if self.system is not None:
            system_name.delete(0, tk.END)
            system_name.insert(0, self.system.name)
        system_name.focus_set()
        self._data[DialogKeys.WIDGETS][DialogKeys.SYSTEM] = system_name

        bsearch = tk.Button(command_frame, text="Search", command=self.__search_cb)
        bsearch.grid(row=0, column=2, sticky=tk.E)
        CreateToolTip(bsearch, "Find system.")
        self._data[DialogKeys.WIDGETS][DialogKeys.SBUTTON] = bsearch

        # create data panel
        data_frame = tk.LabelFrame(self, text=" System ")
        data_frame.grid(row=r_data_idx, padx=5, pady=5, sticky=tk.NSEW)
        self._data[DialogKeys.WIDGETS][DialogKeys.FDATA] = data_frame

        # create scrolled panel
        spanel = VerticalScrolledFrame(data_frame)
        spanel.pack(ipadx=1, ipady=1, fill=tk.BOTH, expand=tk.TRUE)
        self._data[DialogKeys.WIDGETS][DialogKeys.SPANEL] = spanel

        # create status panel
        status_frame = tk.LabelFrame(self, text="")
        status_frame.grid(row=r_status_idx, padx=5, pady=5, sticky=tk.EW)
        status_string = tk.StringVar()
        status = tk.Label(status_frame, textvariable=status_string)
        status.pack(side=tk.LEFT)
        self._data[DialogKeys.WIDGETS][DialogKeys.STATUS] = status_string

        # closing event
        self.protocol("WM_DELETE_WINDOW", self.__on_closing)

    def __on_closing(self) -> None:
        """Run on closing event."""
        self.debug(currentframe(), "Window is closing now.")
        self._data[DialogKeys.CLOSED] = True
        self.destroy()

    def __search_cb(self, event=None) -> None:
        """Search system button callback."""
        self.status = ""
        system = self._data[DialogKeys.WIDGETS][DialogKeys.SYSTEM].get()

        if not system:
            self.status = "System name must be set for processing request."
            return

        # search database
        tsystem = self.db_processor.get_system_by_name(system)
        if tsystem is None:
            self.status = f"System '{system}' not found in local database."
            return
        self.logger.debug = f"System found: {tsystem}"
        self.logger.debug = f"SystemName: {tsystem.name}"
        self.logger.debug = f"Bodies count: {tsystem.bodycount}"

        # show system
        self.__system_show(tsystem)
        # self.logger.debug = f"After Show: {self._data}"

    def __system_show(self, system: db.TSystem) -> None:
        """Show system in frame."""
        # destroy prewious data
        self.system = system
        self.__clear_rows()
        self.__system_summary(system)
        count = 0
        for body in sorted(system.bodies, key=lambda x: x.bodyid):
            self.logger.debug = f"[{count}]: name '{body.name}', bodyid={body.bodyid}, parentid={body.parentid}"
            count += 1
        count = 0
        for body in self.__sort_bodies(system):
            if body:
                self.logger.debug = f"[{count}]: name '{body.name}', bodyid={body.bodyid}, parentid={body.parentid}"
                if not body.name:
                    self.logger.debug = body
            else:
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
            tmp.append(f"Sollar masses: {features.stellarmass:.3f}")
            if features.radius:
                tmp.append(f"Sollar radius: {int(features.radius)}")
            if features.surfacetemperature:
                tmp.append(
                    f"Surface temperature: {int(features.surfacetemperature or 0)} K"
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
        dt_object = datetime.fromtimestamp(system.timestamp)

        # frame
        frame = tk.Frame(
            self._data[DialogKeys.WIDGETS][DialogKeys.SPANEL].interior,
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
        cell = {
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
        self._data[DialogKeys.BODIES].append(list_object)

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
        """Destroy prewious data."""
        for item in self._data[DialogKeys.BODIES]:
            item[2].pack_forget()
            item[2].destroy()
        self._data[DialogKeys.BODIES] = []

    def __build_row_frame(self, count: int, body: db.TBody) -> None:
        """Build Frame row for search dialog."""
        list_object = []
        ih = ImageHelper()

        # [0] count
        list_object.append(count)

        # [1] body
        list_object.append(body)

        # [2] frame
        frame = tk.Frame(
            self._data[DialogKeys.WIDGETS][DialogKeys.SPANEL].interior,
            # background="#ffffff",
            # relief='solid',
            # borderwidth=1,
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
                if not features.star_type:
                    name = name.replace(self.system.name, "").strip()
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
                    scoop.image = img
                    scoop.pack(side=tk.RIGHT)
                    CreateToolTip(scoop, "Scoopable")
                # get distance to arrival
                if features.distance:
                    img = tk.PhotoImage(data=ih.get_distance_image())
                    distance = tk.Label(
                        frame,
                        text=f"{int(features.distance)} ls",
                        compound=tk.LEFT,
                        image=img,
                    )
                    distance.image = img
                    distance.pack(side=tk.RIGHT)
                    CreateToolTip(distance, "Distance to arrival")
                # get landable flag
                if features.landable:
                    # get temperature
                    img2 = tk.PhotoImage(data=ih.get_thermometer_image())
                    temp = tk.Label(
                        frame,
                        text=f"{int(features.surfacetemperature)}K",
                        compound=tk.LEFT,
                        image=img2,
                    )
                    temp.image = img2
                    temp.pack(side=tk.RIGHT)
                    CreateToolTip(temp, "Surface temperature")
                    img = tk.PhotoImage(data=ih.get_landable_image())
                    landable = tk.Label(frame, image=img)
                    landable.image = img
                    landable.pack(side=tk.RIGHT)
                    CreateToolTip(landable, "Planetary Landing")
                # get humans city on the planet
                if signals.count_humans_signals > 0:
                    img = tk.PhotoImage(data=ih.get_humans_image())
                    humans = tk.Label(
                        frame,
                        text=f"{signals.count_humans_signals}",
                        compound=tk.LEFT,
                        image=img,
                    )
                    humans.image = img
                    humans.pack(side=tk.RIGHT)
                    CreateToolTip(humans, "Planetary Base")
                # get biological signals count
                if signals.count_bio_signals > 0:
                    img = tk.PhotoImage(data=ih.get_bio_image(body))
                    cbio = tk.Label(
                        frame,
                        text=f"{signals.count_bio_signals }",
                        compound=tk.LEFT,
                        image=img,
                    )
                    cbio.image = img
                    cbio.pack(side=tk.RIGHT)
                    CreateToolTip(cbio, ih.get_bio_descript(body))
                # get geological signals count
                if signals.count_geo_signals > 0:
                    img = tk.PhotoImage(data=ih.get_geo_image(body))
                    cgeo = tk.Label(
                        frame,
                        text=f"{signals.count_geo_signals}",
                        compound=tk.LEFT,
                        image=img,
                    )
                    cgeo.image = img
                    cgeo.pack(side=tk.RIGHT)
                    CreateToolTip(cgeo, ih.get_geo_descript(body))
                # first mapped
                if features.mapped_first:
                    img = tk.PhotoImage(data=ih.get_map_image())
                    mape = tk.Label(frame, image=img)
                    mape.image = img
                    mape.pack(side=tk.RIGHT)
                    CreateToolTip(mape, "First mapped")
                # first discovered
                if features.discovered_first:
                    img = tk.PhotoImage(data=ih.get_first_image())
                    first = tk.Label(frame, image=img)
                    first.image = img
                    first.pack(side=tk.RIGHT)
                    CreateToolTip(first, "First discovered")
            elif not body.name:
                features: db.TBodyFeatures = body.features
                if features.body_type and features.body_type == "Ring":
                    name = "Ring"
            imgstr = ih.get_body_image(body)
            if imgstr:
                img = tk.PhotoImage(data=imgstr)
                lname = tk.Label(frame, text=f"{name}", compound=tk.LEFT, image=img)
                lname.image = img
            else:
                lname = tk.Label(frame, text=f"{name}")
            # generate body summaries tooltip
            desc = self.__body_summary(body)
            if desc:
                CreateToolTip(lname, desc)
        else:
            lname = tk.Label(frame, text="???")
        lname.pack(side=tk.LEFT)

        # finish
        self._data[DialogKeys.BODIES].append(list_object)

    def update(self, system: db.TSystem) -> None:
        """Update dialog."""
        if self.system is None or system is None:
            return
        if self.system.id == system.id:
            self.__system_show(system)

    @property
    def is_closed(self) -> bool:
        """Check, if window is closed."""
        return self._data[DialogKeys.CLOSED]

    def debug(self, currentframe: FrameType, message: str = "") -> None:
        """Build debug message."""
        pname = f"{self.pluginname}"
        cname = f"{self._c_name}"
        mname = f"{currentframe.f_code.co_name}"
        if message != "":
            message = f": {message}"
        self.logger.debug = f"{pname}->{cname}.{mname}{message}"

    @property
    def status(self) -> object:
        """Return status object."""
        if DialogKeys.STATUS not in self._data[DialogKeys.WIDGETS]:
            return None
        return self._data[DialogKeys.WIDGETS][DialogKeys.STATUS]

    @status.setter
    def status(self, message: Optional[Union[str, int, float]]) -> None:
        """Set status message."""
        if self._data[DialogKeys.WIDGETS][DialogKeys.STATUS] is not None:
            if message:
                self._data[DialogKeys.WIDGETS][DialogKeys.STATUS].set(f"{message}")
            else:
                self._data[DialogKeys.WIDGETS][DialogKeys.STATUS].set("")


class VerticalScrolledFrame(tk.Frame):
    """A pure Tkinter scrollable frame that actually works!
    * Use the 'interior' attribute to place widgets inside the scrollable frame.
    * Construct and pack/place/grid normally.
    * This frame only allows vertical scrolling.
    """

    def __init__(self, parent, *args, **kw) -> None:
        tk.Frame.__init__(self, parent, *args, **kw)

        # Create a canvas object and a vertical scrollbar for scrolling it.
        # vscrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL)
        vscrollbar = tk.Scrollbar(self, orient=tk.VERTICAL)
        vscrollbar.pack(fill=tk.Y, side=tk.RIGHT, expand=tk.FALSE)
        canvas = tk.Canvas(
            self, bd=0, highlightthickness=0, yscrollcommand=vscrollbar.set
        )
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.TRUE)
        vscrollbar.config(command=canvas.yview)

        # Reset the view
        canvas.xview_moveto(0)
        canvas.yview_moveto(0)

        # Create a frame inside the canvas which will be scrolled with it.
        # self.interior = interior = ttk.Frame(canvas)
        self.interior = interior = tk.Frame(canvas)
        interior_id = canvas.create_window(0, 0, window=interior, anchor=tk.NW)

        # Track changes to the canvas and frame width and sync them,
        # also updating the scrollbar.
        def _configure_interior(event):
            # Update the scrollbars to match the size of the inner frame.
            canvas.config(
                scrollregion=f"0 0 {interior.winfo_reqwidth()} {interior.winfo_reqheight()}"
            )
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # Update the canvas's width to fit the inner frame.
                canvas.config(width=interior.winfo_reqwidth())

        interior.bind("<Configure>", _configure_interior)

        def _configure_canvas(event):
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # Update the inner frame's width to fill the canvas.
                canvas.itemconfigure(interior_id, width=canvas.winfo_width())

        canvas.bind("<Configure>", _configure_canvas)


# #[EOF]#######################################################################
