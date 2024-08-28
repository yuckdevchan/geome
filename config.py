import toml, json

with open("config.toml") as f:
    config = toml.load(f)

with open("core.json", "r") as f:
    core = json.load(f)
