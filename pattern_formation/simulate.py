import pygame
from ViewController import ViewController
from Configuration import Configuration
from constants import TORUS, Y_MAX, X_MAX, NUM_AGENTS, PATTERN, INFLUENCE_RADIUS
from random import randint
import random


def main():
    #agent_locations = simple_random_locations(NUM_AGENTS)
    agent_locations = connected_locations(NUM_AGENTS, 30, 5)
    #agent_locations =  [(20, 25), (24, 34), (11, 16), (26, 37), (9, 23), (29, 29), (26, 16), (37, 26), (2, 10)]
    print("Initial locations:", agent_locations)
    configuration  = Configuration(Y_MAX, X_MAX, PATTERN, TORUS)
    configuration.add_agents(agent_locations)
    vc = ViewController(configuration)
    for step in range(150):
        print("CURRENT ROUND:", step)
        configuration.transition()
        vc.update()

    vc.quit()

def simple_random_locations(num):
    locations = []
    for i in range(num):
        locations.append((randint(0, X_MAX-1), randint(0, Y_MAX-1)))
    return locations

def connected_locations(num, x=0, y=0):
    possible_locations = {(x, y)}
    locations = []
    for i in range(num):
        next_location = random.choice(list(possible_locations))
        next_x = next_location[0]
        next_y = next_location[1]
        locations.append(next_location)
        for dx in range(-INFLUENCE_RADIUS+2, INFLUENCE_RADIUS-1):
            for dy in range(-INFLUENCE_RADIUS+2, INFLUENCE_RADIUS-1):
                if next_x + dx < X_MAX and next_x + dx >= 0 and next_y + dy < Y_MAX and next_y + dy >= 0:
                    possible_locations.add((next_x+dx, next_y+dy))
    return locations

if __name__ == "__main__":
    main()

