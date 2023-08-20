
import logging
import motor.motor_asyncio
import codecs
import pickle

from string import ascii_lowercase
from typing import Dict, List, Union

from ubot.config import MONGO_URL

mongo = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL)
db = mongo

from .expired import *
from .notes import *
from .premium import *
from .reseller import *
from .saved import *
from .userbot import *
from .bcast import *
from .gbans import *
from .pref import *
from .otp import *