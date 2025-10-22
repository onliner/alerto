from os import environ as env
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(slots=True)
class Settings:
    # Port on which the server
    port: int = int(env.get("PORT", 8080))

    # Telegram chat ID to send messages to
    chat_id: str = env.get("CHAT_ID")

    # Telegram bot API token
    telegram_token: str = env.get("TELEGRAM_TOKEN")

    # Max delay (in ms) to wait before giving up on sending a message
    max_delay: int = 10_000

    # Max number of messages allowed per minute
    messages_per_minute: int = int(env.get("MAX_MESSAGES_PER_MINUTE", 30))

    # Max length of a single message (in characters);
    # longer text will be truncated before sending
    message_max_len: int = 512

    # Optional Bearer token for webhook authentication
    auth_token: str = env.get('AUTH_TOKEN')

    # Web URL of the Graylog dashboard (admin panel)
    graylog_url: str = "https://logs.onliner.by"

    def validate(self) -> None:
        if not self.chat_id or not self.telegram_token:
            raise SystemExit("Set CHAT_ID, TELEGRAM_TOKEN")


settings = Settings()
settings.validate()
