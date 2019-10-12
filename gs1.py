#!usr/bin/env python3

""""Program name: Gale-Shapley Algorithm Python
Created by: Jake Pham
Date: 09/30/2019
PURPOSE: Demonstrate the implementation of the Gale-Shapley algorithm
Input: gs1input.txt
Output: gs2output.txt
"""

import time
import random
import argparse
import sys, os

"""A few words before we start:
This version of gs1 creates a completely random dictionary whose number
of elements are determined by the user input, using sample random within a
certain range to avoid duplicates within groups.
"""


#Create an empty list that contains the engaged couples as tuples
engaged = []
    
#Create an empty list that will later contain the suitors that are not engaged
suitor_available = []

#Initialize a dictionary for the preference orders of the suitors
def initializeM(n):    
    suitor_rank_list = {
        suitor: random.sample(range(n,2*n), n) for suitor in range(0, n)
    }
    return suitor_rank_list

#Initialize a dictionary for the preference orders of the girls
def initializeF(n):
    girl_rank_list = {
        girl: random.sample(range(0,n), n) for girl in range(n, 2*n)
    }
    return girl_rank_list
    
#Initialize the list of available suitors
def singleSuitor(suitor_rank_list):
    for suitor in suitor_rank_list.keys():
        suitor_available.append(suitor)
    return suitor_available

#Calls the function to match suitors with girls
def matcher(suitor_available, suitor_rank_list, girl_rank_list):
    print('- Matching will now begin:')
    while(len(suitor_available) > 0):
        for suitor in suitor_available:
            proposal(suitor, suitor_available, suitor_rank_list, girl_rank_list)
            
#Where the magic happens
def proposal(suitor, suitor_available, suitor_rank_list, girl_rank_list):
    """We will loop through the list of suitors, along with their
    preferences one-by-one. This way, it is possible to ensure everyone
    has their match in the end, since the number of suitors and girls
    are even.
    """
    #The big loop
    for girl in suitor_rank_list[suitor]:
        #Check whether each girl is engaged to a suitor
        engagement = [couple for couple in engaged if girl in couple]

        #If the length of the list is 0, it means the girl is free
        if(len(engagement) == 0):
            print('%s proposes to %s' %(suitor, girl))
            #Add a couple to the initialized list as a tuple
            engaged.append([suitor, girl])
            #This suitor is no longer single/available
            suitor_available.remove(suitor)
            print('%s is engaged to %s' %(suitor, girl))
            break
        #It's also ok to specify len > 0 with elif
        else:
            """The idea here is to assign the suitor that the girl is
            currently engaged to to an index value from the girl's preference
            list, then compare it with that of the newcomer that is
            proposing to the girl. If the newcomer is higher in the
            list, then the girl would dump the current suitor for him.
            """

            #Assign index values
            fiance = girl_rank_list[girl].index(engagement[0][0])
            new_suitor = girl_rank_list[girl].index(suitor)

            #Compare the 2 values
            if(new_suitor < fiance):
                print('%s proposes to %s' %(suitor, girl))
                
                print('%s dumps %s' %(girl, engagement[0][0]))
                #The fiance is dumped and now available to propose again
                suitor_available.append(engagement[0][0])

                #Remove the old couple and replace with the newly formed
                engaged.remove([engagement[0][0], girl])
                engaged.append([suitor, girl])
                
                print('%s is engaged to %s' %(suitor, girl))
                #The newcomer (suitor) is now an engaged man
                suitor_available.remove(suitor)

                break
            else:
                continue
            
    #Empty out the list in case of another trial
    engagement[:] = []

#Print the list of participating suitors and girls
def participants(suitor_rank_list, girl_rank_list):
    print('- Participants:')
    for suitor in suitor_rank_list:
        print(suitor, end = ' ')
    print('')
    for girl in girl_rank_list:
        print(girl, end = ' ')
    print('\n')

#Print the preferences of all suitors and girls
def preferences(suitor_rank_list, girl_rank_list):
    print('- Preferences:')
    print('Suitors:')
    for suitor in suitor_rank_list:
        print('%s : ' % (suitor), end = ' ')
        for girl_order in suitor_rank_list[suitor]:
            print('%s' % (girl_order), end = ' ')
        print('')
    print('\nGirls:')
    for girl in girl_rank_list:
        print('%s : ' % (girl), end = ' ')
        for suitor_order in girl_rank_list[girl]:
            print('%s' % (suitor_order), end = ' ')
        print('')
    print('')

#Print all matched pairs
def pairing(engaged):
    print('')
    print('- Pairing:')
    for pair in engaged:
        print('{:<3} {:^2} {:>2}'.format(pair[0], '-', pair[1]))

#Shuffle
def shuffler():
    for suitor in suitor_rank_list:
        random.shuffle(suitor_rank_list[suitor])
    for girl in girl_rank_list:
        random.shuffle(girl_rank_list[girl])

#Just for cleaning
def empty():
    engaged[:] = []
    suitor_available[:] = []

#Disable printing
def noPrint():
    sys.stdout = open(os.devnull, 'w')

#Allow printing
def yesPrint():
    sys.stdout = sys.__stdout__

#The main function
def main():
    
    #Set up the argument
    parser = argparse.ArgumentParser(description="What to do with the file")
    parser.add_argument('number_of_suitors',type=int)
    
    #Set up the flags for shortened or full output
    parser.add_argument('-l', '--long', action="store_true",
                        help="display all content when the program is run")
    parser.add_argument('-s', '--short', action="store_true",
                        help="display only time when the program is run")
    args = parser.parse_args()

    #Initialize the chosen value and dictionaries
    n = args.number_of_suitors
    
    suitor_rank_list = initializeM(n)
    girl_rank_list = initializeF(n)

    #Proceed as normal and print everything along the way
    if args.long:
        participants(suitor_rank_list, girl_rank_list)
        preferences(suitor_rank_list, girl_rank_list)
        singleSuitor(suitor_rank_list)

        start = time.time()
        matcher(suitor_available, suitor_rank_list, girl_rank_list)
        end = time.time()
        pairing(engaged)

        print('')
        print('Stable match.')
        print('Chosen number: %s' %(n))
        print('Elapsed wall clock time: {:.2f}'.format(end-start))
        print('Elapsed CPU time: {:.4f}'.format(time.process_time()))  

    #Suppress printing until the end if the short flag is chosen
    elif args.short:
        noPrint()
    
        participants(suitor_rank_list, girl_rank_list)
        preferences(suitor_rank_list, girl_rank_list)
        singleSuitor(suitor_rank_list)

        start = time.time()
        matcher(suitor_available, suitor_rank_list, girl_rank_list)
        end = time.time()
        pairing(engaged)

        yesPrint()
        
        print(n, end = '    ')
        print('{:.4f}'.format(end-start))

    #Clean the lists for a potential re-run.
    empty()

if __name__ == "__main__":
    main()
