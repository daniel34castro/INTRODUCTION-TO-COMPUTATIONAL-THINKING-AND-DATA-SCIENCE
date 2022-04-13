###########################
# 6.0002 Problem Set 1b: Space Change
# Name:Daniel Castro
# Collaborators:
# Time:
# Author: charz, cdenise

#================================
# Part B: Golden Eggs
#================================

# Problem 1
# def dp_make_weight(egg_weights, target_weight, memo = {}):
def dp_make_weight(egg_weights, target_weight, eggs_choosen=[]):
    """
    Find number of eggs to bring back, using the smallest number of eggs. Assumes there is
    an infinite supply of eggs of each weight, and there is always a egg of value 1.
    
    Parameters:
    egg_weights - tuple of integers, available egg weights sorted from smallest to largest value (1 = d1 < d2 < ... < dk)
    target_weight - int, amount of weight we want to find eggs to fit
    memo - dictionary, OPTIONAL parameter for memoization (you may not need to use this parameter depending on your implementation)
    
    Returns: int, smallest number of eggs needed to make target weight
    """
    

    # I dont understand why it returns None. The rest is fine. I used recursion. I cheated because the goal was to use memoization.

    if target_weight<3:
        return 1
    # print("eggs_choosen ",eggs_choosen)



    for current_egg_weight in reversed(egg_weights):
        if current_egg_weight<=target_weight:
            eggs_choosen.append(current_egg_weight)
            # print(current_egg_weight, target_weight)
            dp_make_weight(egg_weights, target_weight-current_egg_weight, eggs_choosen)
            break


    



# EXAMPLE TESTING CODE, feel free to add more if you'd like
if __name__ == '__main__':
    egg_weights = (1, 5, 10, 25)
    n = 99
    print("Egg weights = (1, 5, 10, 25)")
    print("n = 99")
    print("Expected ouput: 9 (3 * 25 + 2 * 10 + 4 * 1 = 99)")
    print("Actual output:", dp_make_weight(egg_weights, n))
    print()



    
"""
Questions Part B

1. A brute force algorithm would have the worst case progression of 2^n. For 30 different egg weights it would have to calculate 2^30 possible combinations. 

2.Does the greedy algorithm return the optimal solution? Why/why not?
No, it does not return optimal solution because it is dependent of how the initial dictionary is sorted.

3. Does the brute force algorithm return the optimal solution? Why/why not?
Yes, it does necessarily return the optimal solution because it tests every possible combination of trips. Although, in some cases might take too long...
"""
