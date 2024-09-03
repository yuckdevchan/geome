import numpy, random, time

from log import log
from config import config

def generate_chunk(x: int, y: int) -> numpy.ndarray:
    chunk = numpy.zeros((config["World"]["chunk_width"], config["World"]["chunk_width"], config["World"]["max_world_height"]), dtype=object)
    for i in range(config["World"]["chunk_width"]):
        for j in range(config["World"]["chunk_width"]):
            for k in range(config["World"]["max_world_height"]):
                if k == 0:
                    block = random.choice(["bedrock"])
                elif k < 5:
                    block = random.choice(["cobblestone", "deepslate", "bedrock"])
                elif k < 8:
                    block = random.choice(["deepslate", "stone", "cobblestone", "stone_bricks"])
                elif k < 10:
                    block = random.choice(["stone", "cobblestone", "stone_bricks"])
                elif k < 11:
                    block = random.choice(["cobblestone", "air", "cobweb"])
                else:
                    block = "air"
                chunk[i][j][k] = block
    return chunk

def get_chunk(x: int, y: int) -> numpy.ndarray:
    while len(world) <= x:
        world.append([])
    while len(world[x]) <= y:
        world[x].append(None)
    if world[x][y] is None:
        world[x][y] = generate_chunk(x, y)
    return world[x][y]
    

def initialize_world(width: int, height: int) -> list:
    world_timer = time.time()
    world = [[None for _ in range(width)] for _ in range(height)]
    for x in range(width):
        for y in range(height):
            world[x][y] = generate_chunk(x, y)
    log(f"World initialized in {round(time.time() - world_timer, 2)} seconds.")
    return world

world = initialize_world(2, 2)
