#!/usr/bin/env python

##
#
# Generate the initial prompts for judges in the bilateral scenario, without any input from the avocates.
# ... facts and legal issue only.
#
##


import csv
import os
import sys
from pprint import pprint

path = "."

sys.path.append(os.path.join(path, "utils"))
import persuasion_utils as util

scenarios_path = os.path.join(path, "data", "scenarios.csv")


def generate_judge_prompt(case_id):

    scenarios = util.load_scenarios(scenarios_path)

    courts = ["a US court", "an English court", "an Irish court"]
    court_string = courts[(int(case_id) - 1) // 5]

    facts = scenarios[case_id]["facts"]
    legal_issue = scenarios[case_id]["legal_issue"]
    party_1 = scenarios[case_id]["party_1"]
    party_2 = scenarios[case_id]["party_2"]

    return util.generate_initial_bilateral_judge_prompt(
        court_string, facts, legal_issue, party_1, party_2
    )


if __name__ == "__main__":
    with open(os.path.join(path, "data", "bilateral_scenarios.csv"), "r") as f:
        lines = f.readlines()

        writer = csv.writer(sys.stdout)

        counter = 1
        for line in lines:
            argstring = line.strip()
            (case_id, arg1, arg2) = argstring.split(",")
            case_id = int(case_id)
            writer.writerow([counter, case_id, generate_judge_prompt(case_id)])
            counter += 1
