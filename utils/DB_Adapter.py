import asyncpg
import asyncio


class DB_Adapter:
    def __init__(self, user, password, database, host, port=5432):
        self.user = user
        self.password = password
        self.database = database
        self.host = host
        self.port = port
        self.pool = None

    async def connect(self):
        """Creates a connection pool."""
        self.pool = await asyncpg.create_pool(
            user=self.user,
            password=self.password,
            database=self.database,
            host=self.host,
            port=self.port,
            min_size=1,
            max_size=10
        )
        print("Connected to the database.")

    async def disconnect(self):
        """Closes the connection pool."""
        if self.pool:
            await self.pool.close()
            print("Disconnected from the database.")

    async def execute_scalar_procedure(self, procedure_name, *args):
        """Executes a stored procedure."""
        async with self.pool.acquire() as connection:
            print(f'SELECT * FROM {procedure_name}({", ".join(["$" + str(i + 1) for i in range(len(args))])});', *args)
            result = await connection.fetch(
                f'SELECT * FROM {procedure_name}({", ".join(["$" + str(i + 1) for i in range(len(args))])});', *args
            )
            return result

    async def registerUser(self, login, pass_hash, pass_salt): 
        async with self.pool.acquire() as connection:
            sql_str = f"select oct.register_user('{login}', '{pass_hash}', '{pass_salt}', null)"
            print(sql_str)
            result = await connection.fetch(sql_str)
            print(result)
            user_uuid = result[0][0]
            print(user_uuid)
            return user_uuid

    async def loginUser(self, _login, _passH=None, _uuid=None):
        print(_login, _passH, _uuid)
        async with self.pool.acquire() as connection:
            # sql_str = f"select oct.loginuser('{_login}', '{_passH}', '{_uuid}')"
            sql_str = f"select oct.login_user('{_login}', null)"      #, '{_passH}')"
            print(sql_str)
            result = await connection.fetch(sql_str)
            pswd = result[0][0]
            print(pswd)
            return pswd
            # if user_uuid != None:
            #     return True
            # else:
            #     return False

    async def createChat(self, uuid_cr, _name, phones_js):
        print(uuid_cr, _name, phones_js)
        async with self.pool.acquire() as connection:
            sql_str = f"select oct.create_chat('{uuid_cr}', '{_name}', null, '{phones_js}')"
            print(sql_str)
            result = await connection.fetch(sql_str)
            bit_result = int(result[0][0][0])
            if bit_result == 1:
                return True
            else:
                return False

    async def disconnectUser(self, _uuid):
        print(_uuid)
        async with self.pool.acquire() as connection:
            sql_str = f"select oct.disconnect_user('{_uuid}')"
            print(sql_str)
            result = await connection.fetch(sql_str)
            bit_result = int(result[0][0][0])
            if bit_result == 1:
                return True
            else:
                return False
