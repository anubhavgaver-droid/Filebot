#========================================================================
# Don't Remove Credit Tg - @TDBotDev
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@TDBotDev
# Ask Doubt on telegram https://t.me/TDBotDev
#========================================================================

from aiohttp import web
from TDBotDev import web_server
import asyncio
import pyromod.listen
from pyrogram import Client
from pyrogram.types import BotCommand
from pyrogram.enums import ParseMode
import sys
import pytz
from datetime import datetime
from config import *
from database.db_premium import *
from database.database import *
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import logging

# Suppress APScheduler logs below WARNING level
logging.getLogger("apscheduler").setLevel(logging.WARNING)

scheduler = AsyncIOScheduler(timezone="Asia/Kolkata")
scheduler.add_job(remove_expired_users, "interval", seconds=10)

# Reset verify count for all users daily at 00:00 IST
async def daily_reset_task():
    try:
        await db.reset_all_verify_counts()
    except Exception:
        pass  

scheduler.add_job(daily_reset_task, "cron", hour=0, minute=0)
#scheduler.start()


def get_indian_time():
    """Returns the current time in IST."""
    ist = pytz.timezone("Asia/Kolkata")
    return datetime.now(ist)


name = """
 BY TDBotDev
"""

class Bot(Client):
    def __init__(self):
        super().__init__(
            name="Bot",
            api_hash=API_HASH,
            api_id=APP_ID,
            plugins={
                "root": "TDBotDev"
            },
            workers=TG_BOT_WORKERS,
            bot_token=TG_BOT_TOKEN
        )
        self.LOGGER = LOGGER

    async def start(self):
        await super().start()
        await self.set_bot_commands()
        scheduler.start()
        usr_bot_me = await self.get_me()
        self.uptime = get_indian_time()

        try:
            db_channel = await self.get_chat(CHANNEL_ID)
            self.db_channel = db_channel
            test = await self.send_message(chat_id = db_channel.id, text = "Test Message")
            await test.delete()
        except Exception as e:
            self.LOGGER(__name__).warning(e)
            self.LOGGER(__name__).warning(f"Make Sure bot is Admin in DB Channel, and Double check the CHANNEL_ID Value, Current Value {CHANNEL_ID}")
            self.LOGGER(__name__).info("\nBot Stopped. Join https://t.me/TDBotDev for support")
            sys.exit()

        self.set_parse_mode(ParseMode.HTML)
        self.LOGGER(__name__).info(f"Bot Running..!\n\nCreated by \nhttps://t.me/TDBotDev")
        self.LOGGER(__name__).info(r"""


  ___ ___  ___  ___ ___ _    _____  _____  ___ _____ ___ 
 / __/ _ \|   \| __| __| |  |_ _\ \/ / _ )/ _ \_   _/ __|
| (_| (_) | |) | _|| _|| |__ | | >  <| _ \ (_) || | \__ \
 \___\___/|___/|___|_| |____|___/_/\_\___/\___/ |_| |___/
                                                         
 
                                          """)

        self.username = usr_bot_me.username
        self.LOGGER(__name__).info(f"Bot Running..! Made by @TDBotDev")

        # Start Web Server
        app = web.AppRunner(await web_server())
        await app.setup()
        await web.TCPSite(app, "0.0.0.0", PORT).start()


        try:
            await self.send_message(OWNER_ID, text=f"<b><blockquote>Bot Started Successfully... by @TDBotDev</blockquote></b>")
            admins = await db.get_all_admins()
            for admin_id in admins:
                if admin_id != OWNER_ID:
                    try:
                        await self.send_message(admin_id, text=f"<b><blockquote>Bot Started Successfully... by @TDBotDev</blockquote></b>")
                    except Exception:
                        pass
        except Exception as e:
            self.LOGGER(__name__).error(f"Error sending startup message: {e}")

    async def set_bot_commands(self):
        commands = [
            BotCommand("start", "Start the bot"),
            BotCommand("batch", "Create batch links"),
            BotCommand("genlink", "Generate single link"),
            BotCommand("custom_batch", "Create custom batch"),
            BotCommand("stats", "Check bot stats"),
            BotCommand("users", "Check user count"),
            BotCommand("broadcast", "Broadcast message"),
            BotCommand("dbroadcast", "Broadcast with auto-delete"),
            BotCommand("pbroadcast", "Broadcast photo with pin"),
            BotCommand("dlt_time", "Set auto-delete time"),
            BotCommand("check_dlt_time", "Check auto-delete time"),
            BotCommand("ban", "Ban a user"),
            BotCommand("unban", "Unban a user"),
            BotCommand("banlist", "View banned users"),
            BotCommand("addchnl", "Add force sub channel"),
            BotCommand("delchnl", "Remove force sub channel"),
            BotCommand("listchnl", "List force sub channels"),
            BotCommand("fsub_mode", "Toggle force sub mode"),
            BotCommand("add_admin", "Add an admin"),
            BotCommand("deladmin", "Remove an admin"),
            BotCommand("admins", "List all admins"),
            BotCommand("addpremium", "Add premium user"),
            BotCommand("remove_premium", "Remove premium user"),
            BotCommand("premium_users", "List premium users"),
            BotCommand("myplan", "Check your premium plan"),
            BotCommand("count", "Check verification count"),
            BotCommand("delreq", "Remove leftover request users"),
            BotCommand("commands", "Show all commands")
        ]
        try:
            await self.set_bot_commands_list(commands)
            self.LOGGER(__name__).info("Bot commands set successfully.")
        except Exception as e:
            self.LOGGER(__name__).error(f"Failed to set bot commands: {e}")

    async def set_bot_commands_list(self, commands):
        # We use the built-in method from pyrogram Client
        await super().set_bot_commands(commands)

    async def stop(self, *args):
        await super().stop()
        self.LOGGER(__name__).info("Bot stopped.")

    def run(self):
        """Run the bot."""
        loop = asyncio.get_event_loop()
        try:
            loop.run_until_complete(self.start())
            self.LOGGER(__name__).info("Bot is now running. Thanks to @TDBotDev")
            loop.run_forever()
        except KeyboardInterrupt:
            self.LOGGER(__name__).info("Shutting down...")
        except Exception as e:
            self.LOGGER(__name__).error(f"Fatal error during bot run: {e}", exc_info=True)
        finally:
            try:
                loop.run_until_complete(self.stop())
            except Exception:
                pass

#========================================================================
# Don't Remove Credit Tg - @TDBotDev
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@TDBotDev
# Ask Doubt on telegram https://t.me/TDBotDev
#========================================================================
