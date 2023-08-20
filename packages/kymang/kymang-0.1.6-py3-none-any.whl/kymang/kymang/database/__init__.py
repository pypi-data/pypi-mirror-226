
import logging
import motor.motor_asyncio
import codecs
import pickle

from string import ascii_lowercase
from typing import Dict, List, Union

from ubot.config import MONGO_URL

mongo = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL)
db = mongo

from kymang.kymang.database.expired import *
from kymang.kymang.database.notes import *
from kymang.kymang.database.premium import *
from kymang.kymang.database.reseller import *
from kymang.kymang.database.saved import *
from kymang.kymang.database.userbot import *
from kymang.kymang.database.bcast import *
from kymang.kymang.database.gbans import *
from kymang.kymang.database.pref import *
from kymang.kymang.database.otp import *