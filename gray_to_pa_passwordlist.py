# Written by Paul Ampletzer @ paul.ampletzer@gmail.com

from hashlib import new
import re
import glob

# print the name of the passwords.txt file that is found
print(''.join(glob.glob('*_passwords.txt')))

# open the passwords file
textfile = open(''.join(glob.glob('*_passwords.txt')), 'r')
# create the regex pattern for the row with the password
pattern = re.compile(".*Item value:.*")
matches = []

# go through the passwords.txt and write all lines with the regex matches in the list
for line in textfile:
    matches += pattern.findall(line)

# go through the list and delete the text befor the password itself
matches = ''.join(matches).replace("Item value:", "").split()
print(matches)
textfile.close

# list to string with new line for every password
listofpasswords = '\n'.join(matches)
print(listofpasswords)

#write string of passwords in new txt file for PA
newpasswordfile = open('newpasswordlist.txt', 'w')
newpasswordfile.write(listofpasswords)
newpasswordfile.close

#//.replace("Item value:", "")
