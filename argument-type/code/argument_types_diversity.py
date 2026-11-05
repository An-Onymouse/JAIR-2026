#!/usr/bin/env python

# extract stats etc. about argument types with respect to the advocates
#
# output to argument_types_3_diversity.csv

from collections import defaultdict
import csv
import sys
import numpy as np
from scipy.stats import chi2_contingency

# fields
SCENARIO            = 1
PARTY1_ADVOCATE     = 2
PARTY1_ARGUMENT_ID  = 3
PARTY2_ADVOCATE     = 4
PARTY2_ARGUMENT_ID  = 5
JUDGE               = 8
WINNING_ADVOCATE    = 9

# keys where the three argument types were the same
sames = set()

# load data for argument counts per advocate
with open( 'argument-types/same_argument_types.csv', 'r' ) as f:
	reader = csv.reader( f )
	for row in reader:
		sames.add( row[0] )

writer = csv.writer( sys.stdout )

contingencies = defaultdict( lambda: np.array([[0,0],[0,0]]))

with open( 'data/all_outcomes.csv', 'r' ) as f:
	reader = csv.reader( f )
	for row in reader:
		arg = 'arguments'
		if row[JUDGE].endswith( "_noarguments" ):
			row[JUDGE] = row[JUDGE][:-12]
			arg = 'noarguments'

		key1 = '='.join( [ row[SCENARIO], arg, row[PARTY1_ADVOCATE], "1", row[PARTY1_ARGUMENT_ID] ] )
		key2 = '='.join( [ row[SCENARIO], arg, row[PARTY2_ADVOCATE], "2", row[PARTY2_ARGUMENT_ID] ] )

		winner = key1 if row[WINNING_ADVOCATE] == row[PARTY1_ADVOCATE] else key2
		loser = key1 if row[WINNING_ADVOCATE] == row[PARTY2_ADVOCATE] else key2

		# build contingency tables for chi-squared
		# -           wins losses
		# same
		# not same

		if winner in sames: # winner had same arguments everywhere
			contingencies['all'][0][0] += 1
			contingencies[row[JUDGE]][0][0] += 1
		else:
			contingencies['all'][1][0] += 1
			contingencies[row[JUDGE]][1][0] += 1
		if loser in sames: # loser had same arguments everywhere
			contingencies['all'][0][1] += 1
			contingencies[row[JUDGE]][0][1] += 1
		else:
			contingencies['all'][1][1] += 1
			contingencies[row[JUDGE]][1][1] += 1



writer = csv.writer( sys.stdout )

writer.writerow( ['All Judges'] )

chi2, p, dof, expected = chi2_contingency(contingencies['all'])

writer.writerow(["chi2:", chi2])
writer.writerow( [ "p-value:", p ] )
writer.writerow( [ "significant:", p < 0.05] )
writer.writerow( ["Actual counts:"] )
writer.writerow( ["", "Wins", "Losses"])
writer.writerow(["Same Types", str( contingencies['all'][0][0] ), str( contingencies['all'][0][1] ) ] )
writer.writerow(["Different Types", str( contingencies['all'][1][0] ), str( contingencies['all'][1][1] ) ] )
writer.writerow([])
writer.writerow(["Expected counts:"])
writer.writerow( ["", "Wins", "Losses"])
writer.writerow(["Same Types", str( expected[0][0] ), str( expected[0][1] ) ] )
writer.writerow(["Different Types", str( expected[1][0] ), str( expected[1][1] ) ] )
writer.writerow([])

for judge in contingencies.keys():
	if judge == 'all':
		continue

	writer.writerow( [judge] )

	chi2, p, dof, expected = chi2_contingency(contingencies[judge])

	writer.writerow(["chi2:", chi2])
	writer.writerow( [ "p-value:", p ] )
	writer.writerow( [ "significant:", p < 0.05] )
	writer.writerow( ["Actual counts:"] )
	writer.writerow( ["", "Wins", "Losses"])
	writer.writerow(["Same Types", str( contingencies[judge][0][0] ), str( contingencies[judge][0][1] ) ] )
	writer.writerow(["Different Types", str( contingencies[judge][1][0] ), str( contingencies[judge][1][1] ) ] )
	writer.writerow([])
	writer.writerow(["Expected counts:"])
	writer.writerow( ["", "Wins", "Losses"])
	writer.writerow(["Same Types", str( expected[0][0] ), str( expected[0][1] ) ] )
	writer.writerow(["Different Types", str( expected[1][0] ), str( expected[1][1] ) ] )

	writer.writerow([])
