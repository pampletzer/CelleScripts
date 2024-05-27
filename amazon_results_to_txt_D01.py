# Written by Paul Ampletzer @ paul.ampletzer@gmail.com


import pandas as pd
import os
import re



#declare files and paths
d01xlsx = os.path.join(os.path.dirname(__file__), 'Exported results.xlsx')
onlyd01 = os.path.join(os.path.dirname(__file__), "onlyd01.txt")

# output the found File
print(d01xlsx)

# create the reggex
p = re.compile("D01-"+'\d{7}'+"-"+'\d{7}'+"")

# open the xlsx File
df = pd.read_excel(d01xlsx)

# create Matches as List 
matches = []

# Only the Body is important for the D01
# Running through every line and save the matched regex in matches
for line in df['Body']:
    matches += p.findall(line)

# we only need every D01 once
unique_list_1 = list(dict.fromkeys(matches))


# list to string with new line for every D01
listofd01 = '\n'.join(unique_list_1)
print(listofd01)

#write string of D01 in new txt file 
newpasswordfile = open(onlyd01, 'w')
newpasswordfile.write(listofd01)
newpasswordfile.close
