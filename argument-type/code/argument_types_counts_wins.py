#!/usr/bin/env python

# extract stats etc. about argument types with respect to the advocates

from collections import defaultdict
from scipy.stats import binomtest
import csv
import sys

# fields
SCENARIO            = 1
PARTY1_ADVOCATE     = 2
PARTY1_ARGUMENT_ID  = 3
PARTY2_ADVOCATE     = 4
PARTY2_ARGUMENT_ID  = 5
JUDGE               = 8
WINNING_ADVOCATE    = 9


counts = {}

# load data for argument counts per advocate
with open( 'argument-types/argument_counts_table.csv', 'r', encoding='utf-8-sig') as f:
	reader = csv.reader( f )
	for row in reader:
		counts[ row[0] ] = row[1]
		
judge_argument_counts = defaultdict( lambda: [0,0,0] )

writer = csv.writer( sys.stdout )
with open( 'data/all_outcomes.csv', 'r' ) as f:
	reader = csv.reader( f )
	arg = 'arguments'
	for row in reader:
		if row[JUDGE].endswith( "_noarguments" ):
			row[JUDGE] = row[JUDGE][:-12]
			arg = 'noarguments'

		key1 = '='.join( [ row[SCENARIO], arg, row[PARTY1_ADVOCATE], "1", row[PARTY1_ARGUMENT_ID] ] )
		key2 = '='.join( [ row[SCENARIO], arg, row[PARTY2_ADVOCATE], "2", row[PARTY2_ARGUMENT_ID] ] )

		writer.writerow( [ row[JUDGE], counts[key1], "1" if row[WINNING_ADVOCATE] == row[PARTY1_ADVOCATE] else "0" ] )
		writer.writerow( [ row[JUDGE], counts[key2], "1" if row[WINNING_ADVOCATE] == row[PARTY2_ADVOCATE] else "0" ] )

		# separately 
		winner = row[WINNING_ADVOCATE]
		winner_count = counts[key1 if winner == row[PARTY1_ADVOCATE] else key2]
		loser_count = counts[key2 if winner == row[PARTY1_ADVOCATE] else key1]

		# [winners higher, losers higher, equal]
		if winner_count > loser_count:
			judge_argument_counts[row[JUDGE]][0] += 1
		elif loser_count > winner_count:
			judge_argument_counts[row[JUDGE]][1] += 1
		else:
			judge_argument_counts[row[JUDGE]][2] += 1
		

with open( 'argument_counts_by_judge.csv', 'w' ) as f:
	writer2 = csv.writer( f )
	writer2.writerow( ['judge', 'more_wins', 'more_win_percentage', 'total_not_tied', 'total_ties', 'pvalue' ] )
	for judge in judge_argument_counts.keys():
		total = judge_argument_counts[judge][0] + judge_argument_counts[judge][1] + judge_argument_counts[judge][2]
		total_not_drawn = judge_argument_counts[judge][0] + judge_argument_counts[judge][1]
		more_win_percentage = judge_argument_counts[judge][0] / total_not_drawn
		
		result_p = binomtest( judge_argument_counts[judge][0], total_not_drawn, 0.5).pvalue

		writer2.writerow( [ judge, judge_argument_counts[judge][0], f'{more_win_percentage:.4f}', total_not_drawn, judge_argument_counts[judge][2], result_p ] )




