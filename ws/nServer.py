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



    # # Example stored procedure execution with parameters
    # procedure_name = 'your_stored_procedure'
    # parameters = ('param1', 123)  # Adjust these parameters as per your stored procedure
    #
    # try:
    #     result = await db.execute_stored_procedure(procedure_name, *parameters)
    #     print("Stored procedure result:", result)
    # finally:
    #     # Disconnect from the database
    #     await db.disconnect()

    # server = await asyncio.start_server(handle_client, cfg.HOST, cfg.PORT)
    # addr = server.sockets[0].getsockname()
    # print(f"Server started on {addr}")

    # async with server:
    #     await server.serve_forever()


def Run():
    asyncio.run(startNserver())

    # wsServer.Run()