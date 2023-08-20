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

from pytgcalls.types.input_stream import AudioPiped, AudioVideoPiped
from pytgcalls.types.input_stream.quality import (
    HighQualityAudio,
    HighQualityVideo,
    LowQualityVideo,
    MediumQualityVideo,
)


class Queues:
    queue = {}
    def add_to_queue(self: 'kymang.Client', chat_id, songname, link, ref, type, quality):
        if chat_id in self.queue:
            chat_queue = self.queue[chat_id]
            chat_queue.append([songname, link, ref, type, quality])
            return int(len(chat_queue) - 1)
        self.queue[chat_id] = [[songname, link, ref, type, quality]]

    def get_queue(self: 'kymang.Client', chat_id):
        if chat_id in self.queue:
            return self.queue[chat_id]
        return 0

    def pop_an_item(self: 'kymang.Client', chat_id):
        if chat_id in self.queue:
            chat_queue = self.queue[chat_id]
            chat_queue.pop(0)
            return 1
        return 0

    def clear_queue(self: 'kymang.Client', chat_id: int):
        if chat_id in self.queue:
            self.queue.pop(chat_id)
            return 1
        return 0

    async def skip_current_song(self: 'kymang.Client', calls, chat_id: int):
        if chat_id not in self.queue:
            return 0
        chat_queue = self.get_queue(chat_id)
        if len(chat_queue) == 1:
            await calls.leave_group_call(chat_id)
            self.clear_queue(chat_id)
            return 1
        songname = chat_queue[1][0]
        url = chat_queue[1][1]
        link = chat_queue[1][2]
        type = chat_queue[1][3]
        RESOLUSI = chat_queue[1][4]
        if type == "Audio":
            await calls.change_stream(
                chat_id,
                AudioPiped(
                    url,
                    HighQualityAudio(),
                ),
            )
        elif type == "Video":
            if RESOLUSI == 720:
                hm = HighQualityVideo()
            elif RESOLUSI == 480:
                hm = MediumQualityVideo()
            elif RESOLUSI == 360:
                hm = LowQualityVideo()
            await calls.change_stream(
                chat_id, AudioVideoPiped(url, HighQualityAudio(), hm)
            )
        self.pop_an_item(chat_id)
        return [songname, link, type]

    async def skip_item(self: 'kymang.Client', chat_id, h):
        if chat_id in self.queue:
            chat_queue = self.get_queue(chat_id)
            try:
                x = int(h)
                songname = chat_queue[x][0]
                chat_queue.pop(x)
                return songname
            except Exception as e:
                print(e)
                return 0
        else:
            return 0
