# -*- coding: UTF-8 -*-
"""
Created on 30 jan 2023.

@author: szumak@virthost.pl
"""


from abc import ABCMeta, abstractmethod


class IBase(metaclass=ABCMeta):
    """Interface class for database data models."""

    @abstractmethod
    def event_parser(self, value: dict) -> None:
        """Event parser.

        Analyze dict from journal and import data into the object.
        """


# #[EOF]#######################################################################
