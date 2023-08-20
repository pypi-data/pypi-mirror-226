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


class Admins:
    async def add_admin(self: "kymang.Client", user, nama, is_bot: bool = False):
        adminsdb = self.mongo_async.admins
        cek = await adminsdb.find_one({"user_id": self.me.id, "user": user})
        if cek:
            await adminsdb.update_one(
                {"user_id": self.me.id},
                {
                    "$set": {
                        "user": user,
                        "nama": nama,
                        "is_bot": is_bot,
                    }
                },
            )
        else:
            await adminsdb.insert_one({"user_id": self.me.id, "user": user, "nama": nama})


    async def del_sudo(self: "kymang.Client", user):
        adminsdb = self.mongo_async.admins
        await adminsdb.delete_one({"user_id": self.me.id, "user": user})


    async def get_all_admin(self: "kymang.Client"):
        adminsdb = self.mongo_async.admins
        r = [jo async for jo in adminsdb.find({"user_id": self.me.id})]
        if r:
            return r
        else:
            return False
