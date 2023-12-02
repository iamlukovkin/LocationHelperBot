import sys
import logging
import asyncio

from app.bot_app import launch_bot
from app.database.models import conn_to_db
from app.handlers import *


if __name__ == "__main__":
    try:
        logging.basicConfig(level=logging.INFO, stream=sys.stdout)
        asyncio.run(conn_to_db())
        asyncio.run(launch_bot())
    except KeyboardInterrupt:
        print("Exit")
