#!/usr/bin/env python
import math
import random

def percentile(data, percentiles):
    # input: a list of percentiles, e.g. quartiles would be [25, 50, 75]
    # output: a list of the results corresponding to those input percentiles for the given input data
    output = [None] * len(percentiles)
    size = len(data)
    for i in range(len(percentiles)):
        perc = percentiles[i]
        output[i] = sorted(data)[int(math.ceil((size * perc) / 100)) - 1]
    return output


DROP_PROBABILITY = 0.25
SIMULATIONS = 2048
MAX_RAIDS = 20 # lines up with a bit less than 5 months, maybe that's the length of phase?


def simulate_single_raid():
    number_dropped = 0
    for i in range(MAX_RAIDS):
        loot_dropped = random.random() < DROP_PROBABILITY
        if loot_dropped:
            number_dropped += 1
        if number_dropped == 2:
            return i
    return MAX_RAIDS # else no loot dropped, treat it as having waited 16 weeks for your drop


# if allowed, then if TWO drops have happened in the other raid, but NO drops have happened in yours,
# then second mage is allowed to go to the other raid
# imagine the POV is from a raid 1 raider
def simulate_two_raids():
    numdrops_1 = 0
    numdrops_2 = 0
    for i in range(MAX_RAIDS):
        dropped_in_1 = random.random() < DROP_PROBABILITY
        if dropped_in_1:
            numdrops_1 += 1
        dropped_in_2 = random.random() < DROP_PROBABILITY
        if dropped_in_2:
            numdrops_2 += 1
        if numdrops_1 == 2:
            # if it's dropped in raid 1 twice, then you'd have received it
            return i
        elif numdrops_2 == 3:
            # else, if it's dropped in raid 2 three times, you'd have received it by having been rostered to
            # raid 2 to receive the third SCB while your other raid 1 mage gets the first SCB that drops in
            # raid 1
            return i
    return MAX_RAIDS


# assumptions: we assume raider has set this loot in the first row, and we assume each raid has 2 such raiders
# who use the first row for this loot item (imagine they're mages and it's SCB)
def main():
    print("--- Simulating assuming raiders are NOT allowed to move to other raid ---")
    # if not allowed to move to other raid, then you can imagine our raider is in a guild with a single raid
    sim_results = [None] * SIMULATIONS # all the number of raids taken for every simulations
    for i in range(SIMULATIONS):
        sim_results[i] = simulate_single_raid()
    percentiles = percentile(sim_results, [2, 5, 10, 20, 50, 80, 90, 95, 98])
    print("Simulation results: 2nd, 5th, 10th, 20th, 50th (Median), 80th, 90th, 95th, 98th percentiles are:")
    print(percentiles)

    print("--- Simulating assuming raiders are allowed to move to other raid ---")
    sim_results_2 = [None] * SIMULATIONS
    for i in range(SIMULATIONS):
        sim_results_2[i] = simulate_two_raids()
    percentiles_2 = percentile(sim_results_2, [2, 5, 10, 20, 50, 80, 90, 95, 98])
    print("Simulation results: 2nd, 5th, 10th, 20th, 50th (Median), 80th, 90th, 95th, 98th percentiles are:")
    print(percentiles_2)

if __name__ == "__main__":
    main()
