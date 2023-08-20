#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
#
#  This file is part of Pyrogram.
#
#  Pyrogram is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Pyrogram is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Pyrogram.  If not, see <http://www.gnu.org/licenses/>.

from uuid import uuid4

import kymang
from kymang import types
from ..object import Object


class InlineQueryResult(Object):
    """One result of an inline query.

    - :obj:`~kymang.types.InlineQueryResultCachedAudio`
    - :obj:`~kymang.types.InlineQueryResultCachedDocument`
    - :obj:`~kymang.types.InlineQueryResultCachedAnimation`
    - :obj:`~kymang.types.InlineQueryResultCachedPhoto`
    - :obj:`~kymang.types.InlineQueryResultCachedSticker`
    - :obj:`~kymang.types.InlineQueryResultCachedVideo`
    - :obj:`~kymang.types.InlineQueryResultCachedVoice`
    - :obj:`~kymang.types.InlineQueryResultArticle`
    - :obj:`~kymang.types.InlineQueryResultAudio`
    - :obj:`~kymang.types.InlineQueryResultContact`
    - :obj:`~kymang.types.InlineQueryResultDocument`
    - :obj:`~kymang.types.InlineQueryResultAnimation`
    - :obj:`~kymang.types.InlineQueryResultLocation`
    - :obj:`~kymang.types.InlineQueryResultPhoto`
    - :obj:`~kymang.types.InlineQueryResultVenue`
    - :obj:`~kymang.types.InlineQueryResultVideo`
    - :obj:`~kymang.types.InlineQueryResultVoice`
    """

    def __init__(
        self,
        type: str,
        id: str,
        input_message_content: "types.InputMessageContent",
        reply_markup: "types.InlineKeyboardMarkup"
    ):
        super().__init__()

        self.type = type
        self.id = str(uuid4()) if id is None else str(id)
        self.input_message_content = input_message_content
        self.reply_markup = reply_markup

    async def write(self, client: "kymang.Client"):
        pass
