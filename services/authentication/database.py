import os
import sqlite3
import internal.database
from typing import Generator
from dotenv import load_dotenv
from internal.database import fetch_rows, extract_row, set_db_path

load_dotenv()

rw_paths = [
    "run/authentication/primary/fuse/auth.db",
]

ro_paths = [
    "run/authentication/secondary1/fuse/auth.db",
    "run/authentication/secondary2/fuse/auth.db",
]


ro_path = 0
rw_path = 0


def get_db(read_only=False) -> Generator[sqlite3.Connection, None, None]:
    global ro_path
    global rw_path

    if read_only:
        # TODO: fix ro_path so that it retries the next path if the current one
        # is down
        ro_path = (ro_path + 1) % len(ro_paths)
        db_path = ro_paths[ro_path]
    else:
        rw_path = (rw_path + 1) % len(rw_paths)
        db_path = rw_paths[rw_path]

    return internal.database.get_db(db_path, read_only=read_only)


def get_read_db() -> Generator[sqlite3.Connection, None, None]:
    return get_db(read_only=True)