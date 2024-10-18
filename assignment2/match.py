import numpy as np
from typing import List, Tuple
import random

def run_matching(scores: List[List], gender_id: List, gender_pref: List) -> List[Tuple]:
    """
    TODO: Implement Gale-Shapley stable matching!
    :param scores: raw N x N matrix of compatibility scores. Use this to derive a preference rankings.
    :param gender_id: list of N gender identities (Male, Female, Non-binary) corresponding to each user
    :param gender_pref: list of N gender preferences (Men, Women, Bisexual) corresponding to each user
    :return: `matches`, a List of (Proposer, Acceptor) Tuples representing monogamous matches

    Some Guiding Questions/Hints:
        - This is not the standard Men proposing & Women receiving scheme Gale-Shapley is introduced as
        - Instead, to account for various gender identity/preference combinations, it would be better to choose a random half of users to act as "Men" (proposers) and the other half as "Women" (receivers)
            - From there, you can construct your two preferences lists (as seen in the canonical Gale-Shapley algorithm; one for each half of users
        - Before doing so, it is worth addressing incompatible gender identity/preference combinations (e.g. gay men should not be matched with straight men).
            - One easy way of doing this is setting the scores of such combinations to be 0
            - Think carefully of all the various (Proposer-Preference:Receiver-Gender) combinations and whether they make sense as a match
        - How will you keep track of the Proposers who get "freed" up from matches?
        - We know that Receivers never become unmatched in the algorithm.
            - What data structure can you use to take advantage of this fact when forming your matches?
        - This is by no means an exhaustive list, feel free to reach out to us for more help!
    """

    # process the scores by gender preferences
    for i in range(len(gender_pref)):
        for j in range(len(gender_id)):
            if i == j:
                continue
            elif (gender_pref[i] == "Men" and
                  gender_id[j] in ("Female", "Nonbinary")):
                scores[i][j], scores[j][i] = 0, 0
            elif (gender_pref[i] == "Women" and
                  gender_id[j] in ("Male", "Nonbinary")):
                scores[i][j], scores[j][i] = 0, 0
            # no implementation needed for i with pref "Bisexual"

    """
    Require: Initialize each person to be free (unmatched)
        while Some man is free and hasn’t proposed to every woman do
            Choose such a man m
            w ← 1st woman on m’s list to whom m has not yet proposed
            if w is free then
                Match m and w
            else if w prefers m to her current match m′ then
                Match m and w, and free up m′
            else
                w rejects m
            end if
        end while
    """

    # generate random list of 5 indices to be proposers
    proposers = random.sample(range(len(gender_pref)), len(gender_pref) // 2)
    receivers = list(set(range(len(gender_pref))) - set(proposers))

    """
    init lists of single proposers, number of proposals completed by each,
    and a list of all the matches
    """
    free_proposers = list(proposers)
    proposals = {p: 0 for p in proposers}
    matches = {r: None for r in receivers}

    """
    this loop is verbose to show how this successfully implements
    the necessary variation of gale-shapely
    """
    while free_proposers:
        # take loner from beginning of the list
        loner = free_proposers.pop(0)

        # check if loner has proposed to all receivers
        if proposals[loner] >= len(receivers):
            print(f"{loner} has exhausted all proposals :\(")
            continue

        # the next receiver is the index of how many proposals the loner has done
        receiver = receivers[proposals[loner]]
        proposals[loner] += 1 # increase loner's proposal count

        # if the score is 0, the gender preferences are incompatible
        if scores[loner][receiver] == 0:
            free_proposers.append(loner)
            print(f"{loner} and {receiver} are incompatible.")
            continue

        # if the receiver is single, automatic match
        elif matches[receiver] is None:
            print(f"{receiver} is single so {loner} is matched")
            matches[receiver] = loner

        # if the receiver is taken, compare the scores
        else:
            old_match = matches[receiver]
            print(f"{receiver} likes {old_match} {scores[receiver][old_match]}")
            print(f"{receiver} likes {loner} {scores[receiver][loner]}")
            # compare the receiver's preference toward each
            if scores[receiver][loner] > scores[receiver][old_match]:
                matches[receiver] = loner
                free_proposers.append(old_match)
                print(f"{loner} wins {receiver}, {old_match} is single")
            else:
                free_proposers.append(loner)
                print(f"{old_match} wins {receiver}, {loner} is rejected")


    # unfortunately some will be unpaired due to gender preferences :(
    matches = [(proposer, receiver) for receiver, proposer in matches.items()]
    return matches

if __name__ == "__main__":
    raw_scores = np.loadtxt('raw_scores.txt').tolist()
    genders = []
    with open('genders.txt', 'r') as file:
        for line in file:
            curr = line[:-1]
            genders.append(curr)

    gender_preferences = []
    with open('gender_preferences.txt', 'r') as file:
        for line in file:
            curr = line[:-1]
            gender_preferences.append(curr)

    gs_matches = run_matching(raw_scores, genders, gender_preferences)
