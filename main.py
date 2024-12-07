from dotenv import load_dotenv
from os import getenv
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime

import discord
import lostark_api

load_dotenv()

class AdalineClient(discord.Client):
    async def setup_hook(self):
        await self.tree.sync()

    async def on_ready(self):
        print(f"Logged in as {self.user} (ID: {self.user.id})")
        print("------")

        # Every Wed 10:00 AM, notify lostark patch note.
        schedurel = AsyncIOScheduler()
        schedurel.add_job(self.on_lostark_patch_completed, CronTrigger(day_of_week="wed", hour=10))
        schedurel.start()

    # Notify lostark patch note.
    async def on_lostark_patch_completed(self):
        message = "안녕하세요, 영주님! 즐거운 로요일이 돌아왔습니다.\n"

        # Get new notices
        notice_list=[]
        notice_result = await lostark_api.get_news_notice(search_text="업데이트", type="공지")
        if "error" in notice_result:
            print(f"'GET /news/notice' request failed. error code {notice_result['error']}")
        else:
            for notice in notice_result:
                notice_date = datetime.strptime(notice["Date"], "%Y-%m-%dT%H:%M:%S.%f").date()
                if notice_date < datetime.today().date(): # Break loop if notice date is older than today.
                    break

                notice_list.append(f"[{notice['Title']}]({notice['Link']})")

        if notice_list:
            message += "오늘 올라온 공지사항들을 확인해 주시겠어요?\n"
            for index, notice in enumerate(notice_list):
                message += f"{index}. {notice}\n"
        else:
            message += "오늘 올라온 공지사항이 없습니다.\n"

        message += "@everyone"

        for guild in self.guilds:
            if guild.system_channel:
                await guild.system_channel.send(message)

intents = discord.Intents.default()
intents.guilds = True
intents.guild_message = True

client = AdalineClient(intents=intents)
client.run(getenv("DISCORD_APP_TOKEN"))
