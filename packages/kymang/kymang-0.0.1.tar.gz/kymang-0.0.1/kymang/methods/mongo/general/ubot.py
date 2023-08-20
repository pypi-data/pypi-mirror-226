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

import kymang


class Ubot:
    def set_ubot(self: "kymang.Client", client: 'kymang.Client'):
        ubotdb = self.mongo_sync.ubot
        user = ubotdb.find_one({"bot_id": self.me.id})
        if user:
            ubotdb.update_one(
                {"bot_id": self.me.id},
                {
                    "$set": {
                        "api_id": client.api_id,
                        "api_hash": client.api_hash,
                        "session_string": client.session_string,
                    }
                },
            )
        else:
            ubotdb.insert_one(
                {
                    "bot_id": self.me.id,
                    "api_id": client.api_id,
                    "api_hash": client.api_hash,
                    "session_string": client.session_string,
                }
            )


    def del_ubot(self: "kymang.Client"):
        ubotdb = self.mongo_sync.ubot
        return ubotdb.delete_one({"user_id": self.me.id})


    def get_ubot(self: "kymang.Client") -> "kymang.Client":
        ubotdb = self.mongo_sync.ubot
        data = []
        for bt in ubotdb.find({"bot_id": self.me.id}):
            data.append(
                dict(
                    name=str(bt["bot_id"]),
                    api_id=bt["api_id"],
                    api_hash=bt["api_hash"],
                    session_string=bt["session_string"],
                )
            )
        return data
