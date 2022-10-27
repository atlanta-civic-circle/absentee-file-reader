import pandas as pd
import csv

###
# Download an absentee voter file from the  Georgia Secretary of State's website: 
# https://elections.sos.ga.gov/Elections/voterabsenteefile.do

# No example is uploaded to this repo because the file is too big. 

# The file will be a zipped file with a number, probably like 32629.zip
# 
# STATEWIDE.csv is the hero file within that directory -- it's got all the absentee ballots listed.
# The other files in that zipped directory are just the same data, but split up into file for each county.

# So, the SoS generates a new absentee zip file every day. To get a different day's data, you have to
# download the data on that day.
###

# out_path is where I'm going to save a summary of accpted ballots grouped by county.
# I want to bake the date into the filename, Oct 26 2022, so I don't mix up different day's files.
# out_headers is going to be the column name in my outfile that shows county and number of accepted votes 

in_path = 'input/36269/STATEWIDE.csv'
out_path = 'output/20221026_accepted_summary.csv'
out_headers = ['20221026_accepted']

# Use pandas to read the csv. "Ignore" encoding errors -- that's things like accents in names that the computer can't always
# read correctly offhand. I'm not displaying names — I'm only counting them — so it doesn't matter if I have garbled characters in them. 

df = pd.read_csv(in_path, dtype=str, encoding_errors="ignore")

######
# some summary info 
######

print(df.info())

###
# See the number of rows in the data.
# There's a row for each voter who has voted or applied for a mail ballot.
###
print('Total number of rows in the file: accepted ballots, requested ballots, contested ballots, everything:')
print(len(df.index))

#######
# See a summary of ballot styles for the whole universe of this file.
# Styles are: In Person, Mailed, Electronic
# Electronic is the smallest category and it's for Georgians who are overseas, mainly military voters.
#######

print('Breakdown of ballot type: electronic, in-person and mail')
print(df['Ballot Style'].value_counts().sort_index())


#####
# See ballot status for the whole universe of this file.
# Statuses are:
# A: Accepted
# C: Cancelled 
# R: Rejected
# S: Spoiled
######

print('Breakdown of status: accepted, rejected, contested etc')
print(df['Ballot Status'].value_counts().sort_index())


####
# But I want to see accepted ballots x county
# All I care about is *accepted* ballots
# I don't care whether the ballot is in-person, mailed or electronic.
# So let me filter down to where Ballot Status = A
#####

accepted_df = df[df['Ballot Status'] == 'A']

####
#
# Print the number of rows in the data
# There were about 1.2 million as of Oct. 26.
#
####

print('Total number of accepted ballots so far of all kinds:')
print(len(accepted_df.index))

###
#
#  But let me group the accepted ballots by county and count how many accepted ballots there are from each county.
#  Or in pandas lingo, get the "size" of each county. 
#  Then write that data to a .csv that I can use to make a map.
#
#####

out_series = accepted_df.groupby(['County']).size()

# view a sample of the data
print("here's a random 10-county sample of the file you're writing: county x accepted ballots:")
print(out_series.sample(10))

# then save county x accepted ballots to a csv that's small enough to open with excel so you can peruse it or use it to make a turnout map.

out_series.to_csv(out_path, header=out_headers)



