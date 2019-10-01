#!usr/bin/env python3

""""Program name: Gale-Shapley test run
Created by: Jake Pham
Date: 09/24/2019
PURPOSE: Learn the implementation of the Gale-Shapley algorithm
Input:
Output:
Examples:
"""

import time
import random

#Create a dictionary for the preference orders of the suitors
suitor_rank_list = {
    'Jake': ['Flo', 'Kat', 'Nel', 'Cait', 'Jinx', 'Anna', 'Liz', 'Ruby', 'Rose', 'Mary'],
    'Will': ['Flo', 'Jinx', 'Kat', 'Cait', 'Ruby', 'Mary', 'Anna', 'Nel', 'Rose', 'Liz'],
    'Zack': ['Rose', 'Flo', 'Nel', 'Ruby', 'Anna', 'Mary', 'Cait', 'Kat', 'Liz', 'Jinx'],
    'Alex': ['Cait', 'Anna', 'Ruby', 'Nel', 'Jinx', 'Mary', 'Liz', 'Flo', 'Rose', 'Kat'],
    'Kyle': ['Liz', 'Ruby', 'Kat', 'Jinx', 'Mary', 'Flo', 'Anna', 'Rose', 'Nel', 'Cait'],
    'Sam': ['Nel', 'Ruby', 'Liz', 'Anna', 'Kat', 'Mary', 'Flo', 'Jinx', 'Cait', 'Rose'],
    'Joe': ['Ruby', 'Flo', 'Kat', 'Jinx', 'Anna', 'Rose', 'Liz', 'Nel', 'Cait', 'Mary'],
    'Josh': ['Nel', 'Liz', 'Kat', 'Mary', 'Jinx', 'Anna', 'Ruby', 'Rose', 'Cait', 'Flo'],
    'Mike': ['Kat', 'Anna', 'Flo', 'Mary', 'Jinx', 'Ruby', 'Cait', 'Nel', 'Liz', 'Rose'],
    'Ryan': ['Mary', 'Jinx', 'Nel', 'Flo', 'Kat', 'Rose', 'Cait', 'Liz', 'Ruby', 'Anna']
}

#Create a dictionary for the preference orders of the girls
girl_rank_list = {
    'Flo': ['Jake', 'Will', 'Zack', 'Alex', 'Kyle', 'Sam', 'Joe', 'Josh', 'Mike', 'Ryan'],
    'Kat': ['Will', 'Mike', 'Sam', 'Kyle', 'Zack', 'Jake', 'Alex', 'Joe', 'Ryan', 'Josh'],
    'Nel': ['Kyle', 'Will', 'Ryan', 'Mike', 'Josh', 'Zack', 'Joe', 'Alex', 'Sam', 'Jake'],
    'Cait': ['Zack', 'Joe', 'Jake', 'Will', 'Alex', 'Ryan', 'Mike', 'Josh', 'Kyle', 'Sam'],
    'Jinx': ['Alex', 'Zack', 'Sam', 'Josh', 'Joe', 'Will', 'Kyle', 'Mike', 'Ryan', 'Jake'],
    'Anna': ['Jake', 'Sam', 'Ryan', 'Will', 'Alex', 'Mike', 'Joe', 'Josh', 'Kyle', 'Zack'],
    'Liz': ['Mike', 'Kyle', 'Zack', 'Jake', 'Alex', 'Will', 'Joe', 'Josh', 'Sam', 'Ryan'],
    'Ruby': ['Ryan', 'Kyle', 'Alex', 'Will', 'Mike', 'Sam', 'Jake', 'Josh', 'Zack', 'Joe'],
    'Rose': ['Will', 'Jake', 'Mike', 'Kyle', 'Joe', 'Zack', 'Alex', 'Ryan', 'Josh', 'Sam'],
    'Mary': ['Joe', 'Zack', 'Jake', 'Alex', 'Ryan', 'Mike', 'Will', 'Josh', 'Kyle', 'Sam']
}

#Create an empty list that contains the engaged couples as tuples
engaged = []

#Create an empty list that will later contain the suitors that are not engaged
suitor_available = []

#Initialize the list of available suitors
def singleSuitor():
    for suitor in suitor_rank_list.keys():
        suitor_available.append(suitor)

#Calls the function to match suitors with girls
def matcher():
    print('- Matching will now begin:')
    while(len(suitor_available) > 0):
        for suitor in suitor_available:
            proposal(suitor)
            time.sleep(1)

    #Empty out the list in case of another trial
    engaged[:] = []
    suitor_available[:] = []

#Where the magic happens
def proposal(suitor):
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
def participants():
    print('- Participants:')
    for suitor in suitor_rank_list:
        print(suitor, end = ' ')
    print('')
    for girl in girl_rank_list:
        print(girl, end = ' ')
    print('\n')

#Print the preferences of all suitors and girls
def preferences():
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
def pairing():
    print('')
    print('- Pairing:')
    for pair in engaged:
        print('{:<5s} {:^2} {:>2s}'.format(pair[0], '-', pair[1]))

#Shuffle
def shuffler():
    for suitor in suitor_rank_list:
        random.shuffle(suitor_rank_list[suitor])
    for girl in girl_rank_list:
        random.shuffle(girl_rank_list[girl])

#All methods go here just for easy access
def doEverything():
    shuffler()
    participants()
    preferences()
    singleSuitor()
    matcher()
    pairing()
    print('Elapsed wall clock time: {:.2f}'.format(time.perf_counter()))
    print('Elapsed CPU time: {:.4f}'.format(time.process_time()))
    print('Stable matchup.')

#The main function
def main():
    doEverything()
    prompt = input('Another trial? (Y)es / (N)o \n')
    if prompt.lower() == 'y' or prompt.lower() == 'yes':
        doEverything()
    elif prompt.lower() == 'n' or prompt.lower() == 'no':
        pass
    else:
        input('Another trial? (Y)es / (N)o \n')

if __name__ == "__main__":
    main()

        
        



