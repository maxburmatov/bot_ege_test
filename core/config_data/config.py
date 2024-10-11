from environs import Env
from dataclasses import dataclass


@dataclass
class Bots:
    bot_token: str
    admin_id: list[int]


@dataclass
class Config:
    bots: Bots


def get_config(path: str):
    env = Env()
    env.read_env(path)
    admin_id = list(map(int, env.list('ADMIN_ID')))
    return Config(
        bots=Bots(
            bot_token=env.str("TOKEN"),
            admin_id=admin_id
        )
    )


config = get_config('input')

