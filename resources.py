from zipfile import ZipFile
from pathlib import Path
import json, random

def get_texture(name) -> Path:
    try:
        with open(f"resources/textures/block/{name}.json", "r") as f:
            data = json.load(f)
            chosen_texture = random.choice(data["textures"])
            if not Path(f"resources/textures/block/{chosen_texture}").exists():
                raise FileNotFoundError(f"Texture '{chosen_texture}' not found")
            return Path(f"resources/textures/block/{chosen_texture}")
    except:
        return Path("resources/textures/missing.png")
