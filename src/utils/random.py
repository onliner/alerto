import random
from typing import List

_DROPPED_QUIPS: List[str] = [
    "This drop count? Rigged. Everyone knows it!",
    "No one respects rate limits more than me. Nobody!",
    "What a limit! Everyone’s talking about it. Not good!",
    "So many messages. The best messages. They’ll be back!",
    "We were sending perfectly. Then—boom—rate limits. Sad!",
    "These rate limits — total hoax, folks. Everyone agrees!",
    "Many events. Tremendous events. Some were dropped. Very unfair!",
    "It was going great. Absolutely great. Then the limits showed up.",
    "People are saying these rate limits are the worst. Total disaster!",
    "We had the best uptime. Then they hit us with limits. Unbelievable!",
]


def get_dropped_quip() -> str:
    return random.choice(_DROPPED_QUIPS)
