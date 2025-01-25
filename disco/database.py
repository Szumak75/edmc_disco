# -*- coding: UTF-8 -*-
"""
  Author:  Jacek 'Szumak' Kotlarski --<szumak@virthost.pl>
  Created: 19.12.2023

  Purpose: database backend.
"""

import datetime
import time
from inspect import currentframe
from typing import Optional, Dict

from sqlalchemy import create_engine, func
from sqlalchemy.orm import Session
from sqlalchemy.engine.base import Engine

from disco.jsktoolbox.basetool.data import BData
from disco.jsktoolbox.raisetool import Raise
from disco.jsktoolbox.attribtool import ReadOnlyClass
from disco.jsktoolbox.edmctool.ed_keys import EDKeys

import disco.db_models as db
from disco.db_models.system import TSystem

from disco.jsktoolbox.edmctool.system import EnvLocal


class _Keys(object, metaclass=ReadOnlyClass):
    """Keys container class."""

    BODY_COUNT: str = "body_count"
    BODY_SCAN: str = "body_scan"
    DB: str = "__db__"
    DEBUG: str = "__debug__"
    ENGINE: str = "__engine__"
    SESSION: str = "__session__"


class DataAnalyzer(BData):
    """TSystem dataset analyzer."""

    def __init__(self, system: db.TSystem) -> None:
        """Initialize dataset."""
        self.__system_analyze(system)

    def __system_analyze(self, system: db.TSystem) -> None:
        """Analyze TSystem dataset and set raport to data."""
        if not isinstance(system, db.TSystem):
            raise Raise.error(
                f"Expected TSystem type, received: '{type(system)}'",
                TypeError,
                self._c_name,
                currentframe(),
            )
        # print(system)
        # count bodies
        self._set_data(
            key=_Keys.BODY_COUNT, value=system.bodycount, set_default_type=int
        )

        # count scanned bodies
        count = 0
        # for item in system.bodies:
        # pass
        self._set_data(key=_Keys.BODY_SCAN, value=count, set_default_type=int)


class Database(BData):
    """Database class engine for store devices variable."""

    def __init__(self, debug: bool) -> None:
        """Database initialization instance."""
        self._set_data(key=_Keys.DB, value="disco.db", set_default_type=str)
        self._set_data(key=_Keys.DEBUG, value=debug, set_default_type=bool)

        # create engine
        self._set_data(
            key=_Keys.ENGINE, value=self.__create_engine(), set_default_type=Engine
        )

        if self.engine is not None:
            # metadata
            db.DiscoBase.metadata.create_all(self.engine)
        else:
            raise Raise.error(
                "Database creation error.",
                OSError,
                self._c_name,
                currentframe(),
            )

    def __create_engine(self) -> Engine:
        engine: Engine = create_engine(
            f"sqlite+pysqlite:///{self.db_path}",
            echo=self._get_data(key=_Keys.DEBUG),
        )
        if engine is None:
            raise Raise.error(
                "Database engine creation error.",
                OSError,
                self._c_name,
                currentframe(),
            )
        return engine

    @property
    def session(self) -> Session:
        """Get session handler."""
        return Session(self.engine)

    @property
    def engine(self) -> Engine:
        """Return database engine."""
        return self._get_data(key=_Keys.ENGINE)  # type: ignore

    @property
    def db_path(self) -> str:
        """Return database path."""
        return f"{EnvLocal().plugin_dir}/data/{self._data[_Keys.DB]}"


class DBProcessor(BData):
    """Database processor class."""

    def __init__(self, session: Session) -> None:
        """Create instance of class."""
        # self._set_data(key=_Keys.SESSION, value=session, set_default_type=Optional[Session])
        self.session = session

    @property
    def session(self) -> Optional[Session]:
        """Get session handler."""
        return self._get_data(key=_Keys.SESSION)

    @session.setter
    def session(self, value: Optional[Session]) -> None:
        self._set_data(
            key=_Keys.SESSION, value=value, set_default_type=Optional[Session]
        )

    def close(self) -> None:
        """Close database session."""
        if self.session is not None:
            self.session.close()
        self.session = None

    def str_time(self, arg: str) -> int:
        """Timestamp from logs in local time convert to game time string.

        input: 2023-01-01T03:01:43Z
        output: 1672538503
        """
        # create struct_time
        str_time: time.struct_time = time.strptime(arg, "%Y-%m-%dT%H:%M:%SZ")

        # create datetime object
        dt_obj = datetime.datetime(*str_time[:6])

        return int(dt_obj.timestamp())

    def add_system(self, entry: Dict) -> Optional[db.TSystem]:
        """Check and add system after FSDJump."""
        if "SystemAddress" not in entry or self.session is None:
            return None

        system: Optional[TSystem] = self.__get__system(entry[EDKeys.SYSTEM_ADDRESS])
        if not system:
            system = db.TSystem()
            system.event_parser(entry)
            # add feature
            system.features.event_parser(entry)
            # add primary star
            if EDKeys.BODY in entry:
                p_star = db.TBody()
                p_star.event_parser(entry)
                system.bodies.append(p_star)
            self.session.add(system)
            self.session.commit()
        else:
            # update
            if system.timestamp <= self.str_time(entry[EDKeys.TIMESTAMP]):
                system.timestamp = entry[EDKeys.TIMESTAMP]
                # update features
                system.features.event_parser(entry)
                self.session.commit()
        return system

    def update_system(self, entry: Dict) -> Optional[db.TSystem]:
        """Update TSystem information about discovered BodyCount."""
        if EDKeys.SYSTEM_ADDRESS not in entry or self.session is None:
            return None

        system: Optional[TSystem] = self.__get__system(entry[EDKeys.SYSTEM_ADDRESS])
        if not system:
            return None
        else:
            #  update
            if EDKeys.BODY_COUNT in entry:
                system.bodycount = entry[EDKeys.BODY_COUNT]
            if EDKeys.NON_BODY_COUNT in entry:
                system.nonbodycount = entry[EDKeys.NON_BODY_COUNT]
            self.session.commit()
        return system

    def add_body(self, entry: Dict) -> Optional[db.TSystem]:
        """Check and add body after scan."""
        if EDKeys.SYSTEM_ADDRESS not in entry or self.session is None:
            return None
        if EDKeys.BODY_ID not in entry:
            return None
        system: Optional[TSystem] = self.__get__system(entry[EDKeys.SYSTEM_ADDRESS])
        if system and system.timestamp <= self.str_time(entry[EDKeys.TIMESTAMP]):
            body: Optional[db.TBody] = system.get_body(entry[EDKeys.BODY_ID])
            if not body:
                body = db.TBody()
                system.bodies.append(body)
            body.event_parser(entry)
            body.features.event_parser(entry)
            if entry[EDKeys.EVENT] == EDKeys.SCAN and entry[EDKeys.SCAN_TYPE] in (
                EDKeys.BASIC,
                EDKeys.AUTO_SCAN,
                EDKeys.DETAILED,
            ):
                body.features.discovered_first = True
            # add null parents if needed
            self.__add_null_parents(system, entry)
            self.session.commit()
        return system

    def mapped_body(self, entry: Dict) -> Optional[db.TSystem]:
        """Check and update mapped body."""
        if EDKeys.SYSTEM_ADDRESS not in entry or self.session is None:
            return None
        if EDKeys.BODY_ID not in entry:
            return None
        system: Optional[TSystem] = self.__get__system(entry[EDKeys.SYSTEM_ADDRESS])
        if entry[EDKeys.EVENT] != EDKeys.SAA_SCAN_COMPLETE:
            return system
        if system and system.timestamp <= self.str_time(entry[EDKeys.TIMESTAMP]):
            body: Optional[db.TBody] = system.get_body(entry[EDKeys.BODY_ID])
            if body:
                body.features.mapped_first = True
                self.session.commit()
        return system

    def add_signal(self, entry: Dict) -> Optional[db.TSystem]:
        """Check and add discovered signal."""
        if EDKeys.SYSTEM_ADDRESS not in entry or self.session is None:
            return None
        if EDKeys.BODY_ID not in entry:
            return None
        system: Optional[TSystem] = self.__get__system(entry[EDKeys.SYSTEM_ADDRESS])
        if system and system.timestamp <= self.str_time(entry[EDKeys.TIMESTAMP]):
            body: Optional[db.TBody] = system.get_body(entry[EDKeys.BODY_ID])
            if not body:
                body = db.TBody()
                system.bodies.append(body)
                body.event_parser(entry)
                self.session.commit()
            if body.signals.event_parser(entry):
                system.timestamp = entry[EDKeys.TIMESTAMP]
                self.session.commit()
        return system

    def add_genus(self, entry: Dict) -> Optional[db.TSystem]:
        """Check and add discovered genuses."""
        if EDKeys.SYSTEM_ADDRESS not in entry or self.session is None:
            return None
        if EDKeys.BODY_ID not in entry and EDKeys.BODY not in entry:
            return None
        system: Optional[TSystem] = self.__get__system(entry[EDKeys.SYSTEM_ADDRESS])
        # print(system)
        if system and system.timestamp <= self.str_time(entry[EDKeys.TIMESTAMP]):
            body_id = -1
            if EDKeys.BODY_ID in entry:
                body_id = entry[EDKeys.BODY_ID]
            elif EDKeys.BODY in entry:
                body_id = entry[EDKeys.BODY]
            body: Optional[db.TBody] = system.get_body(body_id)
            if not body:
                return None
            if body.genuses.event_parser(entry):
                system.timestamp = entry[EDKeys.TIMESTAMP]
                self.session.commit()
        return system

    def add_codex(self, entry: Dict) -> Optional[db.TSystem]:
        """Check and add discovered codex."""
        if EDKeys.SYSTEM_ADDRESS not in entry or self.session is None:
            return None
        if EDKeys.BODY_ID not in entry:
            return None
        system: Optional[TSystem] = self.__get__system(entry[EDKeys.SYSTEM_ADDRESS])
        if system and system.timestamp <= self.str_time(entry[EDKeys.TIMESTAMP]):
            body: Optional[db.TBody] = system.get_body(entry[EDKeys.BODY_ID])
            if not body:
                return None
            if body.codexes.event_parser(entry):
                system.timestamp = entry[EDKeys.TIMESTAMP]
                self.session.commit()
        return system

    def __add_null_parents(self, system: Optional[db.TSystem], entry: Dict) -> None:
        if system is None:
            return None
        if EDKeys.PARENTS in entry:
            for parent in entry[EDKeys.PARENTS]:
                for k_var, v_var in parent.items():
                    test = False
                    for body in system.bodies:
                        if body.bodyid == v_var:
                            test = True
                    if not test:
                        null = db.TBody()
                        null.bodyid = v_var
                        null.features = db.TBodyFeatures()
                        null.features.body_type = k_var
                        system.bodies.append(null)
        return None

    def __get__system(self, system_address: int) -> Optional[db.TSystem]:
        return (
            (
                self.session.query(db.TSystem)
                .filter(db.TSystem.systemaddress == system_address)
                .first()
            )
            if self.session
            else None
        )

    def get_system_by_name(self, system_name: str) -> Optional[db.TSystem]:
        """Get TSystem by name."""
        return (
            (
                self.session.query(db.TSystem)
                .filter(func.lower(db.TSystem.name) == func.lower(system_name))
                .first()
            )
            if self.session
            else None
        )


# #[EOF]#######################################################################
