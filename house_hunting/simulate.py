graphics_on = False
if graphics_on:
    import pygame
    from ViewController import ViewController
from Configuration import Configuration
from constants import TORUS, N, M, NUM_AGENTS
from random import randint
from VertexState import VertexState
import multiprocessing as mp

graphics_on = False

def main():
    pool = mp.Pool(mp.cpu_count())
    configuration  = Configuration(N, M, TORUS, pool)

    # siteA = VertexState("A", 0.7, ((7, 11), (7,11)))
    # siteB = VertexState("B", 0.9, ((36, 40), (36, 40)))
    # home = VertexState("Home", 0, ((22, 26), (22, 26)))

    siteA = VertexState("A", 0.3, ((59, 61), (6,11)))
    siteB = VertexState("B", 0.9, ((149, 151), (6,11)))
    home = VertexState("Home", 0, ((29, 31), (6,11)))

    # Initialize sites 
    for x in range(home.site_location[0][0], home.site_location[0][1]+1):
        for y in range(home.site_location[1][0], home.site_location[1][1]+1):
            configuration.vertices[(x,y)].state = home

    for x in range(siteA.site_location[0][0], siteA.site_location[0][1]+1):
        for y in range(siteA.site_location[1][0], siteA.site_location[1][1]+1):
            configuration.vertices[(x,y)].state = siteA

    for x in range(siteB.site_location[0][0], siteB.site_location[0][1]+1):
        for y in range(siteB.site_location[1][0], siteB.site_location[1][1]+1):
            configuration.vertices[(x,y)].state = siteB


    # Initialize agents
    agent_locations = []
    for i in range(NUM_AGENTS):
        agent_locations.append((randint(home.site_location[0][0], home.site_location[0][1]), randint(home.site_location[1][0], home.site_location[1][1])))
        #agent_locations.append((25, 25))
    configuration.add_agents(agent_locations, home)
    if graphics_on:
        vc = ViewController(configuration)
    ct = 0
    while not configuration.all_agents_terminated():
        print(ct)
        ct+=1
        configuration.transition()
        if graphics_on:
            vc.update()
    if graphics_on:
        vc.quit()

    pool.join()
    pool.close()

if __name__ == "__main__":
    main()

