###########################
# 6.0002 Problem Set 1a: Space Cows 
# Name:Daniel Castro
# Collaborators:
# Time:

from ps1_partition import get_partitions
import time
#================================
# Part A: Transporting Space Cows
#================================


class Cows(object):
    def __init__(self, c, w):
        self.name = c
        self.weight = w
    def getName(self):
        return self.name
    def getWeight(self):
        return self.weight
    def __str__(self):
        return self.name + ': <' + str(self.name)\
                 + ', ' + str(self.weight) + '>'




# Problem 1
def load_cows(filename):
    """
    Read the contents of the given file.  Assumes the file contents contain
    data in the form of comma-separated cow name, weight pairs, and return a
    dictionary containing cow names as keys and corresponding weights as values.

    Parameters:
    filename - the name of the data file as a string

    Returns:
    a dictionary of cow name (string), weight (int) pairs
    """
    cowsdict={}
    menu=[]
    f = open(filename, 'r')
    for line in f:
        l=line.rstrip().split(',')
        cowsdict[l[0]]=int(l[1])
        menu.append(Cows(l[0],int(l[1])))
    return menu


def load_cows1(filename):
    """
    Read the contents of the given file.  Assumes the file contents contain
    data in the form of comma-separated cow name, weight pairs, and return a
    dictionary containing cow names as keys and corresponding weights as values.
    Parameters:
    filename - the name of the data file as a string
    Returns:
    a dictionary of cow name (string), weight (int) pairs
    """
    with open(filename) as file:
        read_data = file.read().split("\n")
        mapping_cow_weight = {}
        for data in read_data:
            cow, weight = data.split(",")
            weight = int(weight)
            mapping_cow_weight[cow] = weight
    file.close()
    return mapping_cow_weight



cowsdict=load_cows1('ps1_cow_data.txt')
cowsdict={k: v for k, v in sorted(cowsdict.items(), key=lambda a: a[1], reverse = True)}
# print("cowsdict",cowsdict)



# Problem 2
def greedy_cow_transport(cows,limit=10):
    """
    Uses a greedy heuristic to determine an allocation of cows that attempts to
    minimize the number of spaceship trips needed to transport all the cows. The
    returned allocation of cows may or may not be optimal.
    The greedy heuristic should follow the following method:
    1. As long as the current trip can fit another cow, add the largest cow that will fit
        to the trip
    2. Once the trip is full, begin a new trip to transport the remaining cows
    Does not mutate the given dictionary of cows.
    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    trips = []
    duplicate_cows = dict(cows)
    for j in range(len(cows)):
        if len(duplicate_cows) != 0:
            x = []
            fit = []
            temp_limit = limit
            max1 = max(duplicate_cows.values())
            temp_limit -= max1
            name = list(duplicate_cows.keys())[list(duplicate_cows.values()).index(max1)]
            del duplicate_cows[name]
            x.append(name)
            for k in duplicate_cows:
                if temp_limit >= duplicate_cows[k]:
                    fit.append(duplicate_cows[k])
            if len(fit) == 0:
                trips.append(x)
                continue
            else:
                for c in fit:
                    max2 = max(fit)
                    if temp_limit - max2 >= 0:
                        temp_limit -= max2
                        name2 = list(duplicate_cows.keys())[list(duplicate_cows.values()).index(max2)]
                        x.append(name2)
                        del duplicate_cows[name2]
                    else:
                        continue
            trips.append(x)
    return trips

def onetrip(cowsdict, spaceleft):
    trip=[]
    for name, weight in cowsdict.items():
        
        if spaceleft>=weight:
            trip.append(name)
            spaceleft-=weight
        # print(name,weight, trip)
    return trip

def alltrips(cowsdict,limit=10):
    dict_original=cowsdict
    dict_mutable=dict(cowsdict) #cowsdict is already a dict. Like this cowsdict does not mutate
    trips=[]
    while len(dict_mutable)>0:
        trip= onetrip(dict_mutable, limit)
        [dict_mutable.pop(key) for key in trip]
        # print(trip,len(dict_mutable))
        trips.append(trip)
    return trips









# Problem 3
def checktripweigth(trips,limit):
    for trip in trips:
        tripweight=0
        for cowname in trip:
            cow_weight=cowsdict[cowname]
            tripweight+=cow_weight
            # print(trip,cowname,tripweight)
        if tripweight>limit:
            return False
    return True

        
trip1=[['Miss Bella'], ['Miss Moo-dy'], ['Betsy'], ['Lotus'], ['Rose'], ['Dottie'], ['Milkshake'], ['Horns']]
trip2=[['Miss Bella', 'Lotus'], ['Milkshake', 'Miss Moo-dy', 'Rose'], ['Betsy'], ['Horns', 'Dottie']]
# print(checktripweigth(trip2,10))







def brute_force_cow_transport(cowsdict,limit=10):
    """
    Finds the allocation of cows that minimizes the number of spaceship trips
    via brute force.  The brute force algorithm should follow the following method:

    1. Enumerate all possible ways that the cows can be divided into separate trips 
        Use the given get_partitions function in ps1_partition.py to help you!
    2. Select the allocation that minimizes the number of trips without making any trip
        that does not obey the weight limitation
            
    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    min_trips=limit
    correct_trips=[]
    cowsnamelist=list(cowsdict.keys())
    for partition in get_partitions(cowsnamelist):
        # print(partition)
        if checktripweigth(partition,limit):
        # print(checktripweigth(partition,limit))
            correct_trips.append(partition)
            if len(partition)<min_trips:
                min_trips=len(partition)
                choosentrip=partition
    return choosentrip
    # print(correct_trips)
    # print(min_trips)





# print("greedy_cow_transport",greedy_cow_transport(cowsdict,10))
# print("alltrips",alltrips(cowsdict,10))
# print("brute_force_cow_transport",brute_force_cow_transport(cowsdict,limit=10))





# Problem 4
def compare_cow_transport_algorithms():
    """
    Using the data from ps1_cow_data.txt and the specified weight limit, run your
    greedy_cow_transport and brute_force_cow_transport functions here. Use the
    default weight limits of 10 for both greedy_cow_transport and
    brute_force_cow_transport.
    
    Print out the number of trips returned by each method, and how long each
    method takes to run in seconds.

    Returns:
    Does not return anything.
    """


    start1 = time.time()
    trips1=greedy_cow_transport(cowsdict,10)
    end1 = time.time()
    print("greedy_cow_transport:", len(trips1), "time",end1-start1)

    start2 = time.time()
    trips2=alltrips(cowsdict,10)
    end2 = time.time()
    print("alltrips:", len(trips2), "time",end2-start2)

    start3 = time.time()
    trips3=brute_force_cow_transport(cowsdict,limit=10)
    end3 = time.time()
    print("brute_force_cow_transport:",len(trips3), "time:", end3-start3)

# compare_cow_transport_algorithms()


"""
Questions Part A

1. What were your results from compare_cow_transport_algorithms? Which
algorithm runs faster? Why?
The greedy algoritm runs faster because does not need to compute all possible combinations of trips like it is done by the brute force algorithm. 
The time to complete the brute force algorithm is much higher.

2.Does the greedy algorithm return the optimal solution? Why/why not?
No, it does not return optimal solution because it is dependent of how the initial dictionary is sorted.

3. Does the brute force algorithm return the optimal solution? Why/why not?
Yes, it does necessarily return the optimal solution because it tests every possible combination of trips. Although, in some cases might take too long...
"""
