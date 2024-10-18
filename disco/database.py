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
        print(system)
        # count bodies
        self._data[_Keys.BODY_COUNT] = system.bodycount

        # count scanned bodies
        count = 0
        # for item in system.bodies:
        # pass
        self._data[_Keys.BODY_SCAN] = count


class Database(BData):
    """Database class engine for store devices variable."""

    def __init__(self, debug: bool) -> None:
        """Database initialization instance."""
        self._data[_Keys.DB] = "disco.db"
        self._data[_Keys.DEBUG] = debug

        # create engine
        self._data[_Keys.ENGINE] = self.__create_engine()

        if self._data[_Keys.ENGINE] is not None:
            # metadata
            db.DiscoBase.metadata.create_all(self._data[_Keys.ENGINE])
        else:
            raise Raise.error(
                "Database creation error.",
                OSError,
                self._c_name,
                currentframe(),
            )

    def __create_engine(self) -> Engine:
        engine = create_engine(
            f"sqlite+pysqlite:///{self.db_path}",
            echo=self._data[_Keys.DEBUG],
        )
        if engine is None:
            raise Raise.error(
                "Database engine creation error.",
                OSError,
                self._c_name,
                currentframe(),
            )
        return engine  # type: ignore

    @property
    def session(self) -> Session:
        """Get session handler."""
        return Session(self.engine)

    @property
    def engine(self) -> Engine:
        """Return database engine."""
        return self._data[_Keys.ENGINE]

    @property
    def db_path(self) -> str:
        """Return database path."""
        print(f"{EnvLocal().plugin_dir}/data/{self._data[_Keys.DB]}")
        return f"{EnvLocal().plugin_dir}/data/{self._data[_Keys.DB]}"


class DBProcessor(BData):
    """Database processor class."""

    def __init__(self, session: Session) -> None:
        """Create instance of class."""
        if session is None or not isinstance(session, Session):
            raise Raise.error(
                "Expected Session type.",
                TypeError,
                self._c_name,
                currentframe(),
            )
        self._data[_Keys.SESSION] = session

    def close(self) -> None:
        """Close database session."""
        if self._data[_Keys.SESSION] is not None:
            self._data[_Keys.SESSION].close()
        self._data[_Keys.SESSION] = None

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
        if "SystemAddress" not in entry:
            return None
        session: Session = self._data[_Keys.SESSION]
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
            session.add(system)
            session.commit()
        else:
            # update
            if system.timestamp <= self.str_time(entry[EDKeys.TIMESTAMP]):
                system.timestamp = entry["timestamp"]
                # update features
                system.features.event_parser(entry)
                session.commit()
        return system

    def update_system(self, entry: Dict) -> Optional[db.TSystem]:
        """Update TSystem information about discovered BodyCount."""
        if EDKeys.SYSTEM_ADDRESS not in entry:
            return None
        session: Session = self._data[_Keys.SESSION]
        system: Optional[TSystem] = self.__get__system(entry[EDKeys.SYSTEM_ADDRESS])
        if not system:
            return None
        else:
            #  update
            if EDKeys.BODY_COUNT in entry:
                system.bodycount = entry[EDKeys.BODY_COUNT]
            if EDKeys.NON_BODY_COUNT in entry:
                system.nonbodycount = entry[EDKeys.NON_BODY_COUNT]
            session.commit()
        return system

    def add_body(self, entry: Dict) -> Optional[db.TSystem]:
        """Check and add body after scan."""
        if EDKeys.SYSTEM_ADDRESS not in entry:
            return None
        if EDKeys.BODY_ID not in entry:
            return None
        session: Session = self._data[_Keys.SESSION]
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
            session.commit()
        return system

    def mapped_body(self, entry: Dict) -> Optional[db.TSystem]:
        """Check and update mapped body."""
        if EDKeys.SYSTEM_ADDRESS not in entry:
            return None
        if EDKeys.BODY_ID not in entry:
            return None
        session: Session = self._data[_Keys.SESSION]
        system: Optional[TSystem] = self.__get__system(entry[EDKeys.SYSTEM_ADDRESS])
        if entry[EDKeys.EVENT] != EDKeys.SAA_SCAN_COMPLETE:
            return system
        if system and system.timestamp <= self.str_time(entry[EDKeys.TIMESTAMP]):
            body: Optional[db.TBody] = system.get_body(entry[EDKeys.BODY_ID])
            if body:
                body.features.mapped_first = True
                session.commit()
        return system

    def add_signal(self, entry: Dict) -> Optional[db.TSystem]:
        """Check and add discovered signal."""
        if EDKeys.SYSTEM_ADDRESS not in entry:
            return None
        if EDKeys.BODY_ID not in entry:
            return None
        session: Session = self._data[_Keys.SESSION]
        system: Optional[TSystem] = self.__get__system(entry[EDKeys.SYSTEM_ADDRESS])
        if system and system.timestamp <= self.str_time(entry[EDKeys.TIMESTAMP]):
            body: Optional[db.TBody] = system.get_body(entry[EDKeys.BODY_ID])
            if not body:
                body = db.TBody()
                system.bodies.append(body)
                body.event_parser(entry)
                session.commit()
            if body.signals.event_parser(entry):
                system.timestamp = entry[EDKeys.TIMESTAMP]
                session.commit()
        return system

    def add_genus(self, entry: Dict) -> Optional[db.TSystem]:
        """Check and add discovered genuses."""
        if EDKeys.SYSTEM_ADDRESS not in entry:
            return None
        if EDKeys.BODY_ID not in entry and EDKeys.BODY not in entry:
            return None
        session: Session = self._data[_Keys.SESSION]
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
                session.commit()
        return system

    def add_codex(self, entry: Dict) -> Optional[db.TSystem]:
        """Check and add discovered codex."""
        if EDKeys.SYSTEM_ADDRESS not in entry:
            return None
        if EDKeys.BODY_ID not in entry:
            return None
        session: Session = self._data[_Keys.SESSION]
        system: Optional[TSystem] = self.__get__system(entry[EDKeys.SYSTEM_ADDRESS])
        if system and system.timestamp <= self.str_time(entry[EDKeys.TIMESTAMP]):
            body: Optional[db.TBody] = system.get_body(entry[EDKeys.BODY_ID])
            if not body:
                return None
            if body.codexes.event_parser(entry):
                system.timestamp = entry[EDKeys.TIMESTAMP]
                session.commit()
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
        session: Session = self._data[_Keys.SESSION]
        return (
            session.query(db.TSystem)
            .filter(db.TSystem.systemaddress == system_address)
            .first()
        )

    def get_system_by_name(self, system_name: str) -> Optional[db.TSystem]:
        """Get TSystem by name."""
        session: Session = self._data[_Keys.SESSION]
        return (
            session.query(db.TSystem)
            .filter(func.lower(db.TSystem.name) == func.lower(system_name))
            .first()
        )


# #[EOF]#######################################################################
