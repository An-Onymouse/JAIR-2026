#!/usr/bin/env python

import csv
import os
import re
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent

sys.path.append(os.path.join(PROJECT_ROOT, "utils"))
import persuasion_utils as util

debug = True

csv.field_size_limit(100000000)


def main():
	# Check if an argument was provided
	if len(sys.argv) < 3:
		print("Usage: {} /path/to/output/folder /path/to/judgment_file.csv".format(sys.argv[0]))
		sys.exit(1)



	# Read the first command-line argument
	judgment_file = sys.argv[2]
	output_folder = sys.argv[1]

	scenarios = util.load_scenarios(os.path.join(PROJECT_ROOT, "data", "scenarios.csv"))

	judgments = util.load_judgments_bilateral_initial(judgment_file)

	with open( os.path.join( output_folder, os.path.basename( judgment_file ) ), 'w') as f:
		writer = csv.writer(f)
		writer.writerow(
			[
				"judgment_id",
				"case_id",
				"party_1",
				"party_2",
				"judge_model_string",
				"winner",
				"manual_check_required",
			]
		)

		for j in judgments:
			chosen = j["chosen_party"]
			(party1, party2) = (
				scenarios[j["case_id"]]["party_1"].strip(),
				scenarios[j["case_id"]]["party_2"].strip(),
			)

			# mistral sometimes underlines the answer with ``` on the line below
			chosen = re.sub("```$", "", chosen.strip())

			# print( party1 + " " + party2 )
			chosen = chosen.replace("**", "").strip()  # Claude wraps last line in **
			chosen = chosen.replace("- ", "")

			chosen = re.sub(
				"^(?:The )?(?:Final|End) (?:answer )?line(?: \\((?:as requested|required|separate|per instructions)\\))?: ",
				"",
				chosen,
				flags=re.IGNORECASE,
			).strip()  # many lines from GPT start this way
			if ":" in chosen:
				chosen = chosen.rsplit(":", 1)[
					-1
				].strip()  # sometimes there's a preceding label
			if "?" in chosen:
				chosen = chosen.rsplit("?", 1)[
					-1
				].strip()  # sometimes there's a preceding label
			chosen = re.sub('^"', "", chosen)
			chosen = re.sub('"$', "", chosen)

			chosen = re.sub(" should prevail\\.?$", "", chosen)

			chosen = re.sub(
				"(?<!Corp)\\.$", "", chosen
			)  # remove trailing dot except in "Corp." (which is in an actual party name)

			manual = ""
			if chosen.lower() != party1.lower() and chosen.lower() != party2.lower():
				if debug:
					print(
						f"MANUAL CHECK REQUIRED: judgment_id {j['judgment_id']} chosen party '{chosen}' does not match either party '{party1}' or '{party2}'",
						file=sys.stderr,
					)
				manual = "MANUAL_CHECK REQUIRED"


			writer.writerow(
				[
					j["judgment_id"],
					j["case_id"],
					party1,
					party2,
					j["judge_model_string"],
					chosen,
					manual,
				]
			)


if __name__ == "__main__":
	main()
