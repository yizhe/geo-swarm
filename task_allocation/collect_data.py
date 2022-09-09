import pygame
from ViewController import ViewController
from Configuration import Configuration
from constants import TORUS, N, M, NUM_AGENTS, Q_MIN, Q_MAX
from random import randint
from VertexState import VertexState
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd


graphics_on = True
num_trials = 1

def main():
    configuration  = Configuration(N, M, TORUS)

    # siteA = VertexState("A", 0.7, ((7, 11), (7,11)))
    # siteB = VertexState("B", 0.9, ((36, 40), (36, 40)))
    # home = VertexState("Home", 0, ((22, 26), (22, 26)))

    # 9x as far 
    # siteA = VertexState("A", 0.3, ((37, 39), (6,11)))
    # siteB = VertexState("B", 0.3, ((292, 294), (6,11)))
    # home = VertexState("Home", 0, ((7, 9), (6,11)))

    # 2x as far
    # siteA = VertexState("A", 0.3, ((39, 41), (5,10)))
    # siteB = VertexState("B", 0.3, ((69, 71), (5,10)))
    # home = VertexState("Home", 0, ((9, 11), (5,10)))

    # 3x as far
    # siteA = VertexState("A", 0.3, ((74, 76), (6,11)))
    # siteB = VertexState("B", 0.3, ((134, 136), (6,11)))
    # home = VertexState("Home", 0, ((44, 46), (6,11)))

    # 4x as far
    #siteA = VertexState("A", 0.3, ((59, 61), (6,11)))
    #siteB = VertexState("B", 0.3, ((149, 151), (6,11)))
    # home = VertexState("Home", 0, ((29, 31), (6,11)))

    # Test all distances
    # Not in the way
    # siteA = VertexState("A", 0.3, ((9, 11), (6,11)))
    # siteB = VertexState("B", 0.9, ((69, 71), (6,11)))
    # home = VertexState("Home", 0,  ((39, 41), (6,11)))
    # In the way
    siteA = VertexState("A", 0.3, ((39, 41), (6,11)))
    siteB = VertexState("B", 0.9, ((69, 71), (6,11)))
    home = VertexState("Home", 0,  ((9, 11), (6,11)))

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

    message_rate = 1/15
    for distance_mult in range(8, 10):
        print(distance_mult)

        #reset old site B
        for x in range(siteB.site_location[0][0], siteB.site_location[0][1]+1):
            for y in range(siteB.site_location[1][0], siteB.site_location[1][1]+1):
                configuration.vertices[(x,y)].state = VertexState()

        siteB.site_location = ((30*distance_mult+10-1, 30*distance_mult+10+1), (6, 11))

        for x in range(siteB.site_location[0][0], siteB.site_location[0][1]+1):
            for y in range(siteB.site_location[1][0], siteB.site_location[1][1]+1):
                configuration.vertices[(x,y)].state = siteB

        L = 1/((distance_mult+1)*30)
        print(L/9)

        print("quorum", Q_MIN, Q_MAX)
        print("siteA", siteA.site_value, "siteB", siteB.site_value)
        total_num_rounds = []
        total_accuracy = []
        total_splits = []
        total_a = []
        total_b = []
        total_trial_num = []

        for trial in range(0, num_trials):
            # Reset simulation info
            for agent_id in configuration.agents:
                configuration.agents[agent_id].reset(agent_id, configuration.agents[agent_id].location, home, L)

            for agent_id in configuration.agents:
                configuration.agents[agent_id].MESSAGE_RATE = message_rate

            print(trial)
            if graphics_on:
                vc = ViewController(configuration)

            # Data collection
            num_rounds = 1
            accuracy = 0
            split = False

            visited_A = 0
            visited_B = 0 


            while not configuration.all_agents_terminated():
                num_rounds += 1
                configuration.transition()

                if graphics_on:
                    vc.update()

            if graphics_on:
                vc.quit()

            # Gather data after simulation over
            for agent_id in configuration.agents:
                if configuration.agents[agent_id].quorum_site == siteB:
                    accuracy += 1

            for agent_id in configuration.agents:
                if configuration.agents[agent_id].favored_site == siteB:
                    visited_B += 1
                elif configuration.agents[agent_id].favored_site == siteA:
                    visited_A += 1

            if accuracy != NUM_AGENTS and accuracy != 0:
                split = True

            # Update data for this specific trial
            print(num_rounds)
            total_num_rounds.append(num_rounds)
            total_accuracy.append(accuracy/NUM_AGENTS)
            total_splits.append(split)
            total_a.append(visited_A)
            total_b.append(visited_B)
          
            print(accuracy)

            agent_locations = []
            for i in range(NUM_AGENTS):
                agent_locations.append((randint(home.site_location[0][0], home.site_location[0][1]), randint(home.site_location[1][0], home.site_location[1][1])))
                configuration.reset_agent_locations(agent_locations, home)

            

        print(message_rate, np.mean(total_num_rounds), np.mean(total_accuracy), np.sum(total_splits))
        print("rounds:", total_num_rounds)
        print("accuracy:", total_accuracy)
        print("splits:", total_splits)

        data = {
            "type" : ["fixed quorum"]*num_trials,
            "dist": [str(distance_mult)+"x"]*num_trials, 
            "accuracy": total_accuracy,
            "time": total_num_rounds,
            "splits": total_splits
            
        }
        df = pd.DataFrame(data=data)

        df.to_csv("fixed_all_dists_"+str(distance_mult)+".csv", sep='\t')


if __name__ == "__main__":
    main()

