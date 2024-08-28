from datetime import datetime as dt
from config import core

def log(msg: str):
    print(f"{core["game_name"]} [{dt.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}")
