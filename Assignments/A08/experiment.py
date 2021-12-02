import json
import random

# Number of records to insert initially
N = [50000,100000,500000,10000000]

heavy_range =  [.50,.70]
medium_range = [.30,.49]
light_range =  [.10,.39]

def randomFloat(min,max,precision=2):
    """Generates a random float between two values

    Args:
        (float) min                 : minimum range value
        (float) max                 : maximum range value
        (int, optional) precision   : decimal places to round to. Defaults to 2.

    Returns:
        (float): Random floating point
    """
    return round(random.uniform(min, max), precision)

def experimentWeights(keys=["search","update","delete"]):
    """
    This method returns random percentages summing to 1 for any number of 
    keys provided in a dictionary.

    @params:
        (dict) items    : dictionary of keys in which to populate with percentages adding to 1

    @returns:
        dict            : dictionary with keys and values 

    @example:
        Given:
            vals = ["search","update","delete"]
        Returns:
            vals = {"search":.19,"update":.61,"delete":.20}
    """

    random.shuffle(keys)

    results = {}
    

    while(1):
        weights = []
        one = 1.0
        weights.append(randomFloat(heavy_range[0],heavy_range[1]))
        one -= weights[0]
        r =  random.random()
        weights.append(round(one*r,2))
        weights.append(round((1-r)*one,2))

        toosmall = False
        for i in weights:
            if i < .05:
                toosmall = True
        if not toosmall:
            break

    for k in keys:
        results[k] = weights.pop()
    
    return results

"""
Adjust your experiments by mixing and matching the above lists
    for example our first run will be heavy searching, medium updates, and light deletes
    and the last run will be light searches, heavy updates, and medium deletes

You can add as well as mix and match to adjust what you want to do.

Keep these lists the same length, or the driver below will break!
"""
# experiments = [
#     {"search" : heavy, "updates" : medium, "deletes" : light},
#     {"search" : heavy, "updates" : medium, "deletes" : light},
#     {"search" : heavy, "updates" : medium, "deletes" : light},
# ]
# runs_list_length = 3 # This value is how long the lists above are. 

# Instead of inerting all the records right off the bat, you could create another list 
# called inserts and also perform inserts like you do the above searches updates and deletes


if __name__ == '__main__':

    print(experimentWeights(["search","update","delete"]))

    # keys = list(experiments.keys())
    # for n in N:
    #     print(n)
    #     for k in keys:
    #         print(k)
    #         for i in experiments:
    #             print(i)
            

        