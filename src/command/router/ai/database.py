import aiosqlite

class Database:
    def __init__(self):
        self.connection: aiosqlite.Connection = None

    async def open_connection(self, database: str):
        self.connection = await aiosqlite.connect(database)
        await self.connection.execute("PRAGMA foreign_keys = 1")  # включаем поддержку FK, если надо

    async def close_connection(self):
        if self.connection:
            await self.connection.close()

    async def execute_query(self, query: str, params: tuple = None) -> None:
        async with self.connection.execute(query, params or ()):
            await self.connection.commit()

    async def execute_get_query(self, query: str, params: tuple = None):
        async with self.connection.execute(query, params or ()) as cursor:
            rows = await cursor.fetchall()
            return rows

class ProjectDatabase(Database):
    def __init__(self):
        super().__init__()

    async def get_or_create_user(self, tg_id: int, create_if_not_found: bool = True):
        res = await self.execute_get_query("SELECT * FROM users WHERE id = ?", (tg_id,))
        if not res and create_if_not_found:
            await self.execute_query("INSERT INTO users(id) VALUES (?)", (tg_id,))
            res = await self.execute_get_query("SELECT * FROM users WHERE id = ?", (tg_id,))
            return res[0] if res else None
        return res[0] if res else None

    async def get_subscriptions(self):
        return await self.execute_get_query("SELECT * FROM subscriptions")

    async def get_subscription(self, subscription_id: int):
        res = await self.execute_get_query("SELECT * FROM subscriptions WHERE id = ?", (subscription_id,))
        return res[0] if res else None

    async def get_subscription_models(self, subscription_id: int):
        return await self.execute_get_query("SELECT model_id FROM s_models WHERE sub_id = ?", (subscription_id,))

    async def get_model(self, model_id: int):
        res = await self.execute_get_query("SELECT * FROM models WHERE id = ?", (model_id,))
        return res[0] if res else None

    async def set_user_subscription(self, user_id: int, sub_id: int, time: str):
        await self.execute_query("UPDATE users SET sub_type = ?, sub_time = ? WHERE id = ?", (sub_id, time, user_id))

    async def get_user_context(self, user_id: int):
        return await self.execute_get_query("SELECT * FROM u_context WHERE user_id = ?", (user_id,))

    async def add_context_message(self, user_id: int, message: str, role: str, image_data: str = None):
        await self.execute_query("INSERT INTO u_context(user_id, role, image_data, content) VALUES (?, ?, ?, ?)", (user_id, role, image_data, message))

    async def info_api_key(self, client_id: str):
        return await self.execute_get_query("SELECT * FROM api_key WHERE client_id = ?", (client_id,))

    async def add_api_key(self, client_id: str, key: str):
        await self.execute_query("INSERT INTO api_key(client_id, key) VALUES (?, ?)", (client_id, key))

    async def delete_api_key(self, client_id: str):
        await self.execute_query("DELETE FROM api_key WHERE client_id = ?", (client_id,))

    async def clear_context(self, user_id: int):
        await self.execute_query("DELETE FROM u_context WHERE user_id = ?", (user_id,))

    async def set_ban(self, num: int, user_id: int):
        await self.execute_query("UPDATE users SET ban = ? WHERE id = ?", (num, user_id))

    async def set_user_balance(self, sum: int, user_id: int):
        await self.execute_query("UPDATE users SET balance = ? WHERE id = ?", (sum, user_id))

    async def set_role(self, num: int, user_id: int):
        await self.execute_query("UPDATE users SET role = ? WHERE id = ?", (num, user_id))

    async def set_credits_info(self, user_id: int, amount: int, time: float):
        await self.execute_query("UPDATE users SET credits = ?, next_credits_time = ? WHERE id = ?", (amount, time, user_id))

    async def set_user_setting(self, user_id: int, name: str, value):
        await self.execute_query(f"UPDATE users SET {name} = ? WHERE id = ?", (value, user_id))

    async def limit_user_context_length(self, user_id: int, limit: int):
        await self.execute_query(
            "DELETE FROM u_context WHERE user_id = ? AND timestamp NOT IN ("
            "SELECT timestamp FROM u_context WHERE user_id = ? ORDER BY timestamp DESC LIMIT ?"
            ")",
            (user_id, user_id, limit)
        )

    async def api_key_print(self):
        return await self.execute_get_query("SELECT * FROM api_key")

DATABASE = ProjectDatabase()