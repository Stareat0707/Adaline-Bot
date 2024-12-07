from os import getenv
from typing import Literal

from dotenv import load_dotenv
from aiohttp import ClientSession

load_dotenv()
LOSTARK_API_KEY = getenv("LOSTARK_API_KEY")
BASE_URL = "https://developer-lostark.game.onstove.com"

# Get notice
async def get_news_notice(search_text: str = None, type: Literal["공지", "점검", "상점", "이벤트"] = None):
    async with ClientSession() as session:
        url = BASE_URL + "/news/notices"
        headers = {
            "accept": "application/json",
            "authorization": f"bearer {LOSTARK_API_KEY}",
            "searchText": "f{search_text}",
            "type": "f{type}"
        }

        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                return await response.json()
            else:
                return {"error": response.status}
