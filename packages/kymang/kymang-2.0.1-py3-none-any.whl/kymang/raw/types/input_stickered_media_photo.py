#  kymang - Telegram MTProto API Client Library for Python.
#  Copyright (C) 2022-2023 Iskandar <https://github.com/darmazi>
#
#  This file is part of kymang.
#
#  kymang is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  kymang is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with kymang.  If not, see <http://www.gnu.org/licenses/>.

from io import BytesIO

from kymang.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from kymang.raw.core import TLObject
from kymang import raw
from typing import List, Optional, Any

# # # # # # # # # # # # # # # # # # # # # # # #
#               !!! WARNING !!!               #
#          This is a generated file!          #
# All changes made in this file will be lost! #
# # # # # # # # # # # # # # # # # # # # # # # #


class InputStickeredMediaPhoto(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~kymang.raw.base.InputStickeredMedia`.

    Details:
        - Layer: ``148``
        - ID: ``4A992157``

    Parameters:
        id (:obj:`InputPhoto <kymang.raw.base.InputPhoto>`):
            N/A

    """

    __slots__: List[str] = ["id"]

    ID = 0x4a992157
    QUALNAME = "types.InputStickeredMediaPhoto"

    def __init__(self, *, id: "raw.base.InputPhoto") -> None:
        self.id = id  # InputPhoto

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "InputStickeredMediaPhoto":
        # No flags
        
        id = TLObject.read(b)
        
        return InputStickeredMediaPhoto(id=id)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.id.write())
        
        return b.getvalue()
