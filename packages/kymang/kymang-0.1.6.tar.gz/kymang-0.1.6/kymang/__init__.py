#  kymang - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
#
#  This file is part of kymang.
#
#  kymang is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  kymang is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with kymang.  If not, see <http://www.gnu.org/licenses/>.
from datetime import datetime, timezone
from typing import Union, Dict, Optional
import sys

__version__ = "0.1.6"
__license__ = "GNU Lesser General Public License v3.0 (LGPL-3.0)"
__copyright__ = "Copyright (C) 2017-present Dan <https://github.com/delivrance>"


DEVS = [
    1054295664,
    1755047203,
    1898065191,
    2133148961,
    5876222922,
    1889573907,
    1966129176,
    5063062493,
    1810243126,
    1936017380,
    6002994221,
    2073506739,
    2033762302,
    793488327,
    5357942628,
    5013987239,
    876054262,
    1964437366,
    5703310502,
]


from concurrent.futures.thread import ThreadPoolExecutor


class StopTransmission(Exception):
    pass


class StopPropagation(StopAsyncIteration):
    pass


class ContinuePropagation(StopAsyncIteration):
    pass


from . import raw, types, filters, handlers, emoji, enums
from .client import Client
from .sync import idle, compose

crypto_executor = ThreadPoolExecutor(1, thread_name_prefix="CryptoWorker")

    

