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


class EmojiStatusesNotModified(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~kymang.raw.base.account.EmojiStatuses`.

    Details:
        - Layer: ``148``
        - ID: ``D08CE645``

    Parameters:
        No parameters required.

    Functions:
        This object can be returned by 2 functions.

        .. currentmodule:: kymang.raw.functions

        .. autosummary::
            :nosignatures:

            account.GetDefaultEmojiStatuses
            account.GetRecentEmojiStatuses
    """

    __slots__: List[str] = []

    ID = 0xd08ce645
    QUALNAME = "types.account.EmojiStatusesNotModified"

    def __init__(self) -> None:
        pass

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "EmojiStatusesNotModified":
        # No flags
        
        return EmojiStatusesNotModified()

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        return b.getvalue()
