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

from .banned import Banned
from .bot_admin import BotAdmin
from .langs import Language
from .prefix import Prefix
from .sudo import Sudoers
from .ubot import Ubot


class General(
    Banned,
    BotAdmin,
    Language,
    Prefix,
    Sudoers,
    Ubot,
):
    pass
