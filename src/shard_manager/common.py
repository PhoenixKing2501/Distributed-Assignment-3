from __future__ import annotations

import asyncio
import random
import sys
from typing import Any, Dict, List, Optional, Set, Tuple

import aiohttp
import asyncpg
from aiodocker import Docker
from colorama import Fore, Style
from icecream import ic

from consts import *

# Postgres connection pool
pool: asyncpg.Pool[asyncpg.Record]


# List of all servers
replicas: list[str] = []
