
#!/usr/bin/python3

from random import randint
from random import shuffle
from datetime import datetime
import pprint
import sys

friends_dict = {}

def gen_friend_count(friends,ranges):
    max_friends_list = []
    for i in range(int(friends/len(ranges))):
        for j in range(len(ranges)):
            max_friends_list.append(randint(ranges[j][0]+1,ranges[j][1]+1))

    shuffle(max_friends_list)

    for i in range(friends):
        friends_dict[i] = {"allowed":max_friends_list[i],"friends":[],"max":max_friends_list[i]}


def print_data(f1,f2):
    print("f1:",friends_dict[f1]['friends'])
    print("f2:",friends_dict[f2]['friends'])
    l1 = len(friends_dict[f1]['friends'])
    l2 = len(friends_dict[f2]['friends'])
    m1 = friends_dict[f1]['max']
    m2 = friends_dict[f2]['max']
    print(f"len 1:{l1} < max1:{m1}  ,len 1:{l2} < max1:{m2}")

def add_friendship(f1,f2):
    #print_data(f1,f2)
    t1 = f2 not in friends_dict[f1]['friends'] 
    t2 = f1 not in friends_dict[f2]['friends']
    t3 = len(friends_dict[f1]['friends']) <  friends_dict[f1]['max']
    t4 = len(friends_dict[f2]['friends']) <  friends_dict[f2]['max']
    return (t1 and t2 and t3 and t4)

def connect_friends():
    max_friends = len(friends_dict)

    for f1 in friends_dict:

        # generate a random friend
        f2 = randint(0,(max_friends-1))
        
        while not add_friendship(f1,f2):
            f2 = randint(0,(max_friends-1))
        
        print("adding")
        # add the friendship to the list
        friends_dict[f1]['friends'].append(f2)
        friends_dict[f2]['friends'].append(f1)
        friends_dict[f1]['allowed'] -= 1
        friends_dict[f2]['allowed'] -= 1

def connections_left(friends_dict):
    sum = 0
    for f in friends_dict:
        sum += friends_dict[f]['max']
    
    return sum

    

if __name__=='__main__':
    now = datetime.now()
    start = datetime.timestamp(now)
    
    # Ranges of Number of friends 
    ranges = [[3,10],[11,25],[26,100],[101,250]]

    # Generate a friends dictionary with max friends and empty
    # friends list to fill
    gen_friend_count(1000,ranges)
    
    more = connections_left(friends_dict)
    loops = 0

    # while more:
    #     # start connecting friends
    #     connect_friends()
    #     loops += 1
    #     more = connections_left(friends_dict)
    #     if loops > 150:
    #         break
    #     print(loops,more)
    #     break

  
    # now = datetime.now()
    # end = datetime.timestamp(now)
    # print(end-start)

    pprint.pprint(friends_dict)
    