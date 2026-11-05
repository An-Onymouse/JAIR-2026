#!/usr/bin/env python

##
#
# In the bilateral setting, present judge with arguments counter to its initial decision, without including its initial decision.
#
##


import csv
import os
import sys
from pathlib import Path
from pprint import pprint

PROJECT_ROOT = Path(__file__).parent.parent.parent

sys.path.append(os.path.join(PROJECT_ROOT, "utils"))
import persuasion_utils as util

scenarios_path = os.path.join(PROJECT_ROOT, "data", "scenarios.csv")


def generate_judge_prompt(case_id,arguing_party_id, argument):

    scenarios = util.load_scenarios(scenarios_path)

    courts = ["a US court", "an English court", "an Irish court"]
    court_string = courts[(int(case_id) - 1) // 5]

    facts = scenarios[case_id]["facts"]
    legal_issue = scenarios[case_id]["legal_issue"]
    party_1 = scenarios[case_id]["party_1"]
    party_2 = scenarios[case_id]["party_2"]
    arguing_party = party_1 if arguing_party_id == 1 else party_2

    return util.judgment_prompt_bilateral_2(
        court_string, facts, legal_issue, arguing_party, argument, party_1, party_2
    )

## return 1 for each judgment the judge preferred party 1 for
# or 2 where it preferred party 2
# or None if it didn't have a preference (i.e. problematic output)
def find_preferred_parties(outcomes_file):
    preferred = {}
    with open(outcomes_file, "r") as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            judgment_id = int(row[0])
            party1 = row[2]
            party2 = row[3]
            winner = row[5]

            if party1.lower() == winner.lower():
                preferred[judgment_id] = 1
            elif party2.lower() == winner.lower():
                preferred[judgment_id] = 2
            else:
                preferred[judgment_id] = None
    return preferred


if __name__ == "__main__":
	# Check if an argument was provided
	if len(sys.argv) < 2:
		print("Usage: {} /path/to/bilateral_initial_outcomes_folder".format(sys.argv[0]))
		sys.exit(1)

	for filename in os.listdir( sys.argv[1] ):
		if filename.endswith( ".csv" ):
			outfile = (
				os.path.join(PROJECT_ROOT, "prompts", "bilateral_prompts_2", os.path.basename(filename).replace("_bilateral_initial.csv", "")
	         	+ "_bilateral_prompt_2.csv" )
	    	)

			preferred = find_preferred_parties(os.path.join( sys.argv[1], filename) )

			# inelegant to open this again and again but this is just a once off so it'll do...
			with open( os.path.join( PROJECT_ROOT, 'data', 'bilateral_scenarios.csv' ), 'r' ) as f:
				reader = csv.reader( f )

				with open (outfile, 'w') as outf:
					writer = csv.writer( outf )

					judgment_id = 1

					for row in reader:
						case_id = int( row[0] )
						arg1 = row[1]
						arg2 = row[2]
						argument1 = row[3]
						argument2 = row[4]

						# the judge preferred party 1, so present it with arguments for party 2
						if preferred[judgment_id] == 1:
							arguing_party_id = 2
							argument = argument2
							# ... or vice versa
						else:
							arguing_party_id = 1
							argument = argument1

						writer.writerow( [ judgment_id, case_id, generate_judge_prompt( case_id, arguing_party_id, argument ) ] )
						judgment_id += 1
