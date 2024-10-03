#!usr/bin/env python3
import json
import sys
import os

INPUT_FILE = 'testdata.json' # Constant variables are usually in ALL CAPS

class User:
    def __init__(self, name, gender, preferences, grad_year, responses):
        self.name = name
        self.gender = gender
        self.preferences = preferences
        self.grad_year = grad_year
        self.responses = responses


# Takes in two user objects and outputs a float denoting compatibility
def compute_score(user1, user2):
    # check for gender preference match
    pref_1 = False
    for gender in user1.preferences:
        if user2.gender == gender:
            pref_1 = True # user 1 -> 2
    pref_2 = False
    for gender in user2.preferences:
        if user1.gender == gender:
            pref_2 = True # user 2 -> 1
    if pref_1 == False or pref_2 == False:
        return 0

    # if the grades don't touch neither do you
    gap = abs(user1.grad_year - user2.grad_year)
    if gap > 1:
        return 0

    # response-based scoring
    match = 0
    for i in range(len(user1.responses)):
        if user1.responses[i] == user2.responses[i]:
            match += 1

    score = match / len(user1.responses)

    return score


if __name__ == '__main__':
    # Make sure input file is valid
    if not os.path.exists(INPUT_FILE):
        print('Input file not found')
        sys.exit(0)

    users = []
    with open(INPUT_FILE) as json_file:
        data = json.load(json_file)
        for user_obj in data['users']:
            new_user = User(user_obj['name'], user_obj['gender'],
                            user_obj['preferences'], user_obj['gradYear'],
                            user_obj['responses'])
            users.append(new_user)

    for i in range(len(users)-1):
        for j in range(i+1, len(users)):
            user1 = users[i]
            user2 = users[j]
            score = compute_score(user1, user2)
            print('Compatibility between {} and {}: {}'.format(user1.name, user2.name, score))
