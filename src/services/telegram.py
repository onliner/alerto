from aiogram import Bot
from aiogram.enums import ParseMode


class TelegramClient:
    def __init__(self, token: str, chat_id: str):
        self._bot = Bot(token=token)
        self._chat_id = chat_id

    async def start(self) -> None:
        pass

    async def close(self) -> None:
        await self._bot.session.close()

    async def send(self, text: str) -> bool:
        await self._bot.send_message(
            self._chat_id,
            text,
            disable_web_page_preview=True,
            parse_mode=ParseMode.HTML,
        )
        return True
