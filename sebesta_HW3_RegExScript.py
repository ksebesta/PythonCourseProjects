
'''
Title: sebesta_HW3_RegExScript.py
Author: Kalea Sebesta
Date: 11/24/2017
Due Date: 11/28/2015
Part 2,
Use the attached RegExInput.txt file as input.
Write a single Python script named yourlastname_HW3_RegExScript.py that when
run against the RegExInput.txt file will provide only the following output
(in order, e.g., all email addresses before domains before dates, etc.).
Provide a label for each of the six output items. All searches must be conducted
using regular expressions (i.e. not through alternative string methods).

1). All email addresses in the input document via one RegEx search expression.
2). All email address domains (everything after the @ symbol).
3). All dates in the input document, regardless of input format.
4). Possibly valid Visa and Mastercard numbers (apply the rule that Visa cards
5). begin with ‘4’ and Mastercards begin with ‘5’ – all other credit card
6). generation rules need not be checked for).
7). Any sentences that contain the string ‘dog’ or ‘cat’ via one RegEx command.
8). Any sentence beginning with the word ‘Mocha.’

'''
# --------------------------------------------------------------------------
# import modules
import re
import os
# --------------------------------------------------------------------------

# get input file
os.chdir("/Volumes/UTSA QRT2/IS 6713 Data Foundations/Assignments/HW3")
RegEx=open("HW3-RegExInput.txt").read()
# --------------------------------------------------------------------------

# 1). All email addresses in the input document via one RegEx search expression.
# the w Matches any alphanumeric character
emails = re.findall(r'[\w\.-]+@[\w\.-]+', RegEx)
emailStr = ",".join(str(x) for x in emails)
# --------------------------------------------------------------------------

# 2). All email address domains (everything after the @ symbol).
email = re.findall(r'@[\w\.-]+', emailStr)
domainStr = ",".join(str(x) for x in email)
domains = re.sub('@*','',domainStr)
# --------------------------------------------------------------------------

# 3). All dates in the input document, regardless of input format.
# make patterns
# can I create a empty list and then append it with the the different date patterns?
pattern_DMY = re.compile('(\d{2}-*[A-Z a-z]{3}-*\d{2})')
pattern_WDMY_time = re.compile('\w+,+\s+\d+\s+\w+\s+\d+\s+\d+:+\d+:+\d+')
pattern_allD = re.compile('(\d+/+\d+/+\d+)')
# --------------------------------------------------------------------------

# 4). Possibly valid Visa and Mastercard numbers (apply the rule that Visa
# cards begin with ‘4’
pattern_visa = re.compile('4\d{3}.+\d{4}.\d{4}.\d{4}')
# --------------------------------------------------------------------------

# 5). Possibly Mastercards begin with ‘5’
pattern_MC = re.compile('5\d{3}.+\d{4}.\d{4}.+')
# --------------------------------------------------------------------------
# 6). All other credit cards generation rules need not be checked for).
# MY ^ is not working
pattern_CC=re.compile('\d{4}.+\d{4}.\d{4}.\d{4}')

# THIS ISN'T WORKING
#pattern_CC=re.compile('^[^4|5]\d{3}.+\d{4}.\d{4}.\d{4}')
#print(pattern_CC.findall(RegEx))

# -------------------------------------------------------------------------
# 7). Any sentences that contain the string ‘dog’ or ‘cat’ via one RegEx command.
pattern_dog_cat=re.compile('([^.]*?(cat|dog)[^.]*\.)')
# --------------------------------------------------------------------------

# 8). Any sentence beginning with the word ‘Mocha.’
# try using re.search or re.match (look back at in class examples)

#^ Mocha[^.]* is not working for me, figure out why
#pattern_mocha=re.compile('^\sMocha[^.]*')
i=0
pattern_mocha=re.compile('[^.]*?Mocha[^.]*\.')
sentences = pattern_mocha.findall(RegEx)
for i in range(len(sentences)):
    sentences[i]=sentences[i].lstrip()
for i in sentences:
    mocha = re.match('^Mocha[^.]*\.', i)
#----------------------------------------------------------------------------

# write to output file
# sebesta_HW3_RegExOutput.txt
fout = open('sebesta_HW3_RegExOutput.txt', 'w')
fout.write('Kalea Sebesta HW3 RegExOutput.txt \n')
fout.write('\nEmail Addresses Found: \n')
i=0
for i in range(len(emails)):
    fout.write(emails[i])
    fout.write('\n')

i=0
fout.write('\nDomains Found: \n')
for i in range(len(domains.split(','))):
    fout.write(domains.split(',')[i])
    fout.write('\n')

i=0
fout.write('\nAll Dates in the Input Document: \n')
for i in range(len(pattern_DMY.findall(RegEx))):
    fout.write(pattern_DMY.findall(RegEx)[i])
    fout.write('\n')

i=0
for i in range(len(pattern_WDMY_time.findall(RegEx))):
    fout.write(pattern_WDMY_time.findall(RegEx)[i])
    fout.write('\n')

i=0
for i in range(len(pattern_allD.findall(RegEx))):
    fout.write(pattern_allD.findall(RegEx)[i])
    fout.write('\n')

i=0
fout.write('\nVisa Cards: \n')
for i in range(len(pattern_visa.findall(RegEx))):
    fout.write(pattern_visa.findall(RegEx)[i])
    fout.write('\n')

i=0
fout.write('\nMastercards Cards: \n')
for i in range(len(pattern_MC.findall(RegEx))):
    if len(pattern_MC.findall(RegEx)[i]) == 19:
        fout.write(pattern_MC.findall(RegEx)[i])
        fout.write('\n')

i=0
fout.write('\nOther Credit Cards: \n')
for i in range(len(cc)):
    cc[i]=cc[i].lstrip('\n')
    if pattern_CC.findall(RegEx)[i][0]!='4' and pattern_CC.findall(RegEx)[i][0]!='5':
        fout.write(pattern_CC.findall(RegEx)[i])
        fout.write('\n')

i=0
fout.write('\nSentences Containing "dog" or "cat": \n')
for i in range(len(pattern_dog_cat.findall(RegEx))):
    fout.write(pattern_dog_cat.findall(RegEx)[i][0])
    fout.write('\n')

fout.write('\nSentences beginning with Mocha: \n')
fout.write(mocha.group())
fout.close()
# ------------------------------------------------------------------------------