# Ayiin - Ubot
# Copyright (C) 2022-2023 @AyiinXd
#
# This file is a part of < https://github.com/AyiinXd/AyiinUbot >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/AyiinXd/AyiinUbot/blob/main/LICENSE/>.
#
# FROM AyiinUbot <https://github.com/AyiinXd/AyiinUbot>
# t.me/AyiinChats & t.me/AyiinChannel


# ========================×========================
#            Jangan Hapus Credit Ngentod
# ========================×========================

import codecs
import pickle
import json
import kymang
from typing import BinaryIO

from pytgcalls import PyTgCalls
from pytgcalls.exceptions import NoMtProtoClientSet, PyTgCallsAlreadyRunning


def obj_to_str(obj):
    if not obj:
        return False
    string = (codecs.encode(pickle.dumps(obj), "base64").decode())
    return string


def str_to_obj(string: str):
    obj = (pickle.loads(codecs.decode(string.encode(), "base64")))
    return obj


class Assistant:
    def set_assistant(self: "kymang.Client", call_py: PyTgCalls):
        asstdb = self.mongo_sync.assistant
        asstdb.update_one(
            {"bot_id": self.me.id},
            {"$set": {"calls": obj_to_str(call_py._app)}},
            upsert=True,
        )

    def del_assistant(self: "kymang.Client"):
        asstdb = self.mongo_sync.assistant
        return asstdb.delete_one({"bot_id": self.me.id})


    def get_assistant(self: "kymang.Client"):
        for xd in self.get_ubot():
            asst = kymang.Client(
                **xd
            )
            return asst

    async def get_call_py(self: "kymang.Client") -> PyTgCalls:
        for x in self.get_ubot():
            asst = kymang.Client(**x)
            call = PyTgCalls(asst, cache_duration=100)
            return call
