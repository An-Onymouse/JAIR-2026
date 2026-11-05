#!/usr/bin/env python
# merge all the bilateral argument files

# for each judge and each situation, get the initially preferred party
# get new preferred party after counter-argument only (2)
# get new preferred party after chat scenario (3)

import os
import sys
from pathlib import Path
from collections import defaultdict
import csv
PROJECT_ROOT = Path(__file__).parent.parent.parent

sys.path.append(os.path.join(PROJECT_ROOT, "utils"))
import persuasion_utils as util

OUTCOMES_FOLDER_INITIAL = os.path.join( PROJECT_ROOT, 'data', 'outcomes-bilateral-initial' )
OUTCOMES_FOLDER_2 = os.path.join( PROJECT_ROOT, 'data', 'outcomes-bilateral-2' )
OUTCOMES_FOLDER_3 = os.path.join( PROJECT_ROOT, 'data', 'outcomes-bilateral-3' )

results = defaultdict(list)

with open( 'stability.csv', 'w' ) as sta:
	sta_writer = csv.writer(sta)

	# capture initial choice, but also measure the stability of the initial choices
	for filepath in Path( OUTCOMES_FOLDER_INITIAL ).glob( '*.csv' ):
		stability_num = [0] * 15
		stability_den = [0] * 15
		stability_initial = [None] * 15
		overall_num = 0
		overall_den = 0
		model = None
		with open( filepath, 'r' ) as f:
			reader = csv.reader( f )
			next(reader)
			for row in reader:
				model = row[4]
				results[row[4]].append( {"case_id": row[1], "initial" : row[5] } )
				case_index = int( row[1] ) - 1
				stability_den[ case_index ] += 1
				overall_den += 1
				if stability_initial[ case_index ] is None: # record which one they went with the first time
					stability_initial[ case_index ] = row[5]
				if stability_initial[ case_index ] == row[5]: # keep counting each time they chose the same party
					stability_num[ case_index ] += 1

			stability = []
			#now check which party they preferred more often and flip the proportion if the initial one was the less frequently chosen one
			for i in range(len(stability_num)):
				stability.append( stability_num[i] / stability_den[i] )
				if stability[-1] < 0.5:
					overall_num += stability_den[i] - stability_num[i]
					stability[-1] = 1 - stability[-1]
				else:
					overall_num += stability_num[i]
			stability.append( overall_num / overall_den )
			
			sta_writer.writerow( [model] + [ f'{v:.3f}' for v in stability ] )



for filepath in Path( OUTCOMES_FOLDER_2 ).glob( '*.csv' ):
	with open( filepath, 'r' ) as f:
		reader = csv.reader( f )
		next(reader)
		counter = 0
		for row in reader:
			results[row[4]][counter]["counter"] = row[5]
			counter += 1
		if counter != 100:
			print( "Counter ERROR: " + os.path.basename( filepath ) )

for filepath in Path( OUTCOMES_FOLDER_3 ).glob( '*.csv' ):
	with open( filepath, 'r' ) as f:
		reader = csv.reader( f )
		next(reader)
		counter = 0
		for row in reader:
			results[row[4]][counter]["chat"] = row[5]
			counter += 1
		if counter != 100:
			print( "Chat ERROR: " + os.path.basename( filepath ) )

model_categories = {
	"Large Closed" : [ 'claude-sonnet-4-5-20250929_8k-thinking', 'claude-sonnet-4-5-20250929_1k-thinking', 'gemini-3.1-pro-preview_8k-thinking', 'gemini-3.1-pro-preview_1k-thinking', 'gpt-5.1_medium-reasoning', 'gpt-5.1_low-reasoning' ],
	"Large Open" : [ 'deepseek-reasoner_defaults', 'deepseek-chat_defaults', 'Qwen/Qwen3-32B_thinking', 'Qwen/Qwen3-32B_nothinking' ],
	"Small Closed" : [ 'claude-haiku-4-5-20251001_8k-thinking', 'claude-haiku-4-5-20251001_nothinking', 'gemini-2.5-flash-lite_reasoning', 'gemini-2.5-flash-lite_nonreasoning', 'gpt-5-nano_medium-reasoning', 'gpt-5-nano_minimal-reasoning' ],
	"Small Open" : [ 'mistralai/Magistral-Small-2506_defaults', 'mistralai/Mistral-Small-3.2-24B-Instruct-2506_defaults', 'QWen/Qwen3-8B_thinking', 'QWen/Qwen3-8B_nothinking' ]
}

with open( 'bilateral_results.csv', 'w' ) as f:
	writer = csv.writer( f )
	writer.writerow( [ 'Model', 'Counter Flipped', 'Chat Flipped', 'Both Flipped' ] )
	for cat in model_categories:
		writer.writerow( [cat] )
		for model in model_categories[cat]:
			changed_2 = 0
			changed_3 = 0
			changed_both = 0
			for row in results[model]:
				
				if row['initial'] != row['counter']:
					changed_2 += 1
				if row['initial'] != row['chat']:
					changed_3 += 1
				if row['initial'] != row['counter'] and row['initial'] != row['chat']:
					changed_both += 1
			
			writer.writerow( [ model, '{:.2f}'.format( changed_2 / len( results[model] ) ), '{:.2f}'.format( changed_3 / len( results[model] ) ), '{:.2f}'.format( changed_both / len( results[model] ) ) ] )
