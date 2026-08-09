import aiosqlite

DB_NAME = "profiles.db"


async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS profiles (
                telegram_id INTEGER PRIMARY KEY,
                name TEXT,
                age INTEGER,
                email TEXT
            )
        """)
        await db.commit()


async def save_profile(telegram_id, name, age, email):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            """INSERT OR REPLACE INTO profiles (telegram_id, name, age, email)
               VALUES (?, ?, ?, ?)""",
            (telegram_id, name, age, email),
        )
        await db.commit()


async def get_profile(telegram_id):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute(
            "SELECT name, age, email FROM profiles WHERE telegram_id = ?",
            (telegram_id,),
        )
        return await cursor.fetchone()
