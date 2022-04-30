import pygame
from ViewController import ViewController
from Configuration import Configuration
from constants import TORUS, N, M, NUM_AGENTS
from random import randint

def main():
    agent_locations = []
    for i in range(NUM_AGENTS):
        agent_locations.append((randint(0, M-1), randint(0, N-1)))
        #agent_locations.append((25, 25))
    configuration  = Configuration(N, M, TORUS)
    configuration.add_agents(agent_locations)
    vc = ViewController(configuration)
    for step in range(60):
        configuration.transition()
        vc.update()

    vc.quit()

if __name__ == "__main__":
    main()

