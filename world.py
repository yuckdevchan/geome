import numpy, random

from config import config

def generate_chunk(x: int, y: int) -> numpy.ndarray:
    chunk = numpy.zeros((config["World"]["chunk_width"], config["World"]["chunk_width"], config["World"]["max_world_height"]), dtype=object)
    for i in range(config["World"]["chunk_width"]):
        for j in range(config["World"]["chunk_width"]):
            for k in range(config["World"]["max_world_height"]):
                block = random.choice(["dirt", "stone", "cobblestone"])
                print(k)
                chunk[i][j][k] = block
    return chunk

def initialize_world(width: int, height: int) -> list:
    world = [[None for _ in range(width)] for _ in range(height)]
    for x in range(width):
        for y in range(height):
            world[x][y] = generate_chunk(x, y)
    return world

world = initialize_world(1, 1)
