#!/usr/bin/env python

# This generates the winners table from the human annotated data for argument strength.

from collections import defaultdict
import csv
import sys
from scipy.stats import binomtest

# keys
TRIAL = 0
FIRST_CHOICE = 1
SECOND_CHOICE = 2
SCENARIO = 3
PARTY = 4
FIRST_ADVOCATE = 5
SECOND_ADVOCATE = 6
FIRST_ARGUMENT = 7
SECOND_ARGUMENT = 8

stats_rounding = 4


writer = csv.writer( sys.stdout )

all_winners = defaultdict(lambda: defaultdict(int))

# a bit of a hack to open the file several times, but I already had the code!
# do the first judge
winners = defaultdict(lambda: defaultdict(int))
with open( 'human-argument-strength-test-data-round-2.csv', 'r' ) as f:
	reader = csv.reader( f )
	next( reader )
	for row in reader:
		if int( row[ FIRST_CHOICE ] ) == 1:
			winners[ row[ FIRST_ADVOCATE ] ][ row[ SECOND_ADVOCATE ] ] += 1
			all_winners[ row[ FIRST_ADVOCATE ] ][ row[ SECOND_ADVOCATE ] ] += 1

		elif int( row[ FIRST_CHOICE ] ) == 2:
			winners[ row[ SECOND_ADVOCATE ] ][ row[ FIRST_ADVOCATE ] ] += 1
			all_winners[ row[ SECOND_ADVOCATE ] ][ row[ FIRST_ADVOCATE ] ] += 1

		else:
			print( "ERRRRRRRORORROOROROROROR" )


# write the output for the first judge
writer.writerow( [ 'First Human Judge' ] )
writer.writerow( [] ) 
writer.writerow( [ '' ] + sorted( winners.keys() ) ) # assume every model has won at least once

for k in sorted( winners.keys() ):
	row = [ k ]
	for l in sorted( winners.keys() ):
		if k == l:
			row.append( '-' )
		elif l not in winners[ k ]:
			row.append( '-' )
		else:
			row.append( winners[ k ][ l ] )

	writer.writerow( row )

writer.writerow( [] ) # empty row

for k in sorted( winners.keys() ):
	row = [ k ]
	for l in sorted( winners.keys() ):
		if k == l:
			row.append( '-' )
		elif l not in winners[ k ]:
			row.append( '-' )
		else:
			row.append( '{:.4f}'.format( binomtest( winners[ k ][ l ], winners[ k ][ l ] + winners[ l ][ k ], alternative="two-sided" ).pvalue ) )

	writer.writerow( row )

writer.writerow( [] ) # empty row

# read again to do calculations for second judge
winners = defaultdict(lambda: defaultdict(int))
with open( 'human-argument-strength-test-data-round-2.csv', 'r' ) as f:
	reader = csv.reader( f )
	next( reader )
	for row in reader:
		if int( row[ SECOND_CHOICE ] ) == 1:
			winners[ row[ FIRST_ADVOCATE ] ][ row[ SECOND_ADVOCATE ] ] += 1
			all_winners[ row[ FIRST_ADVOCATE ] ][ row[ SECOND_ADVOCATE ] ] += 1

		elif int( row[ SECOND_CHOICE ] ) == 2:
			winners[ row[ SECOND_ADVOCATE ] ][ row[ FIRST_ADVOCATE ] ] += 1
			all_winners[ row[ SECOND_ADVOCATE ] ][ row[ FIRST_ADVOCATE ] ] += 1

		else:
			print( "ERRRRRRRORORROOROROROROR" )


writer.writerow( [ 'Second Human Judge' ] )
writer.writerow( [] ) 
writer.writerow( [ '' ] + sorted( winners.keys() ) ) # assume every model has won at least once

# write results for second judge

for k in sorted( winners.keys() ):
	row = [ k ]
	for l in sorted( winners.keys() ):
		if k == l:
			row.append( '-' )
		elif l not in winners[ k ]:
			row.append( '-' )
		else:
			row.append( winners[ k ][ l ] )

	writer.writerow( row )

writer.writerow( [] ) # empty row

for k in sorted( winners.keys() ):
	row = [ k ]
	for l in sorted( winners.keys() ):
		if k == l:
			row.append( '-' )
		elif l not in winners[ k ]:
			row.append( '-' )
		else:
			row.append( '{:.4f}'.format( binomtest( winners[ k ][ l ], winners[ k ][ l ] + winners[ l ][ k ], alternative="two-sided" ).pvalue ) )

	writer.writerow( row )

writer.writerow( [] ) # empty row

# write results for both judges combined

writer.writerow( [ 'Both Human Judges' ] )
writer.writerow( [] ) 
for k in sorted( all_winners.keys() ):
	row = [ k ]
	for l in sorted( all_winners.keys() ):
		if k == l:
			row.append( '-' )
		elif l not in all_winners[ k ]:
			row.append( '-' )
		else:
			row.append( all_winners[ k ][ l ] )

	writer.writerow( row )

writer.writerow( [] ) # empty row

for k in sorted( all_winners.keys() ):
	row = [ k ]
	for l in sorted( all_winners.keys() ):
		if k == l:
			row.append( '-' )
		elif l not in all_winners[ k ]:
			row.append( '-' )
		else:
			row.append( '{:.4f}'.format( binomtest( all_winners[ k ][ l ], all_winners[ k ][ l ] + all_winners[ l ][ k ], alternative="two-sided" ).pvalue ) )

	writer.writerow( row )

writer.writerow( [] ) # empty row
