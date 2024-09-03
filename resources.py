from pathlib import Path
import json, random

# def make_texture_pack

def get_texture(name, side) -> Path:
    try:
        with open(f"resources/textures/block/{name}.json", "r") as f:
            data = json.load(f)
            chosen_texture = random.choice(data["textures"]["all"])
            if not Path(f"resources/textures/block/{chosen_texture}").exists():
                raise FileNotFoundError(f"Texture '{chosen_texture}' not found")
            return Path(f"resources/textures/block/{chosen_texture}")
    except:
        return Path("resources/textures/missing.png")

def get_block_data(name) -> dict:
    try:
        with open(f"resources/textures/block/{name}.json", "r") as f:
            return json.load(f)
    except:
        return {"textures": {"all": ["missing.png"]}}

def is_block_transparent(name) -> bool:
    if name == "air":
        return True
    try:
        with open(f"resources/textures/block/{name}.json", "r") as f:
            data = json.load(f)
            try:
                if data["textures"]["transparent"]:
                    return True
                else:
                    return False
            except KeyError:
                return False
    except:
        return False

def is_block_billboard(name) -> bool:
    if name == "air":
        return False
    try:
        with open(f"resources/textures/block/{name}.json", "r") as f:
            data = json.load(f)
            try:
                if data["textures"]["billboard"]:
                    return True
                else:
                    return False
            except KeyError:
                return False
    except:
        return False
