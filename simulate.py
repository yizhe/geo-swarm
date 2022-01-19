import pygame
from ViewController import ViewController
from Configuration import Configuration
from random import randint

N = 50
M = 50
num_agents = 50

def main():
    agent_locations = []
    for i in range(num_agents):
        agent_locations.append((randint(0, M-1), randint(0, N-1)))
        #agent_locations.append((25, 25))
    configuration  = Configuration(agent_locations, N, M, True)
    vc = ViewController(configuration)
    for step in range(60):
        configuration.transition()
        vc.update()

    vc.quit()

if __name__ == "__main__":
    main()

