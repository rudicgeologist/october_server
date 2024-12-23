import asyncio

import Config as cfg
from ws import WSRV as wss
from utils import DB_Adapter as dba

async def startNserver():

    db = dba.DB_Adapter(  
        user=cfg.DB_USER,
        password=cfg.DB_PASSWORD,
        database=cfg.DB_NAME,
        host=cfg.DB_HOST
    )

    # Connect to the database
    await db.connect()

    ws_server = wss.WSRV(cfg.SERVER_HOST, cfg.SERVER_PORT, db)
    await ws_server.StartServer()


def Run():
    asyncio.run(startNserver())
