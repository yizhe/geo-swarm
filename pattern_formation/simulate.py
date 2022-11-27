import pygame
from ViewController import ViewController
from Configuration import Configuration
from constants import TORUS, Y_MAX, X_MAX, NUM_AGENTS, PATTERN
from random import randint

def main():
    agent_locations = []
    for i in range(NUM_AGENTS):
        agent_locations.append((randint(0, X_MAX-1), randint(0, Y_MAX-1)))
        #agent_locations.append((25, 25))
    configuration  = Configuration(Y_MAX, X_MAX, PATTERN, TORUS)
    configuration.add_agents(agent_locations)
    vc = ViewController(configuration)
    for step in range(60):
        configuration.transition()
        vc.update()

    vc.quit()

if __name__ == "__main__":
    main()

