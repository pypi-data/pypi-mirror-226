"""
Dictionary and counter in Python to find winner of election
Given an array of names of candidates in an election. A candidate name in array represents a vote
casted to the candidate. Print the name of candidates received Max vote.
If there is tie, print lexicographically smaller name.

Examples:

Input :  votes[] = {"john", "johnny", "jackie",
                    "johnny", "john", "jackie",
                    "jamie", "jamie", "john",
                    "johnny", "jamie", "johnny",
                    "john"};
Output : John
We have four Candidates with name as 'John',
'Johnny', 'jamie', 'jackie'. The candidates
John and Johny get maximum votes. Since John
is alphabetically smaller, we print it.

"""


def find_winner(vote_list):
    vote_dict = {}
    for vote in vote_list:
        if vote in vote_dict:
            vote_dict.update({vote: vote_dict.get(vote) + 1})
        else:
            vote_dict.update({vote: 1})

    # find max vote count
    max_vote_count = max(vote_dict.values())

    # Find candidate with max vote
    max_vote_dict = {}
    for k, v in vote_dict.items():
        if v == max_vote_count:
            max_vote_dict.update({k: v})

    if len(max_vote_dict) > 1:
        max_vote_dict_keys = max_vote_dict.keys()
        max_vote_dict_keys.sort()
        return max_vote_dict_keys[0]
    else:
        max_vote_dict.keys()[0]


if __name__ == "__main__":
    input =['john','johnny','jackie','johnny','john','jackie','jamie','jamie',
'john','johnny','jamie','johnny','john']
    print find_winner(input) # John