#The purpose of this script is to tag-fix tags that are consistently wrong in my corpus
#This script was written after tag checking 15 texts written by L1 and 15 texts written by L2 students, making a total of 30 texts
#So, the fixes here represent errors that are common in my dissertation corpus and not all corpora

import re
import argparse
import os

#TO RUN THIS SCRIPT
#python tag_fixing_dissertation.py --folder=PATH TO FOLDER HERE

# Define the way we retrieve arguments sent to the script.
parser = argparse.ArgumentParser(description='tag_fixing')
parser.add_argument('--overwrite', action='store_true')
parser.add_argument('--folder', action="store", dest='dir', default='')
args = parser.parse_args()

#gets the texts from the original folder
for dirpath, dirnames, files in os.walk(args.dir):
    for name in files:
        textfile = open(os.path.join(dirpath, name), "r")

        # cleans the file name and creates a new folder to store the edited texts
        cleaned_filename = re.sub(r'\.\.[\\\/]', r'', name)
        output_directory = 'tag_fixed' #this determines the name of the folder where the texts will go to
        output_filename = os.path.join(output_directory, cleaned_filename)
        directory = os.path.dirname(output_filename)
        if not os.path.exists(directory):
            os.makedirs(directory)

        # opens the new file
        output_file = open(output_filename, 'w')

        # splits the text into words by "\n" or "\r"
        text = textfile.read()
        lines = text.split("\n")


        for i, w in enumerate(lines):

            #Fix "that" verb complement clause miss-tagged as subordinator
            #searches for subordinator preceded by verb and changes the subordinator tag for a verb complement clause tag
            if re.search("that \^cs\+sub", lines[i]) and re.search("\^vb", lines[i - 1]):
                linecs = re.sub("cs\+sub", "tht+vcmp", lines[i])
                output_file.write(linecs + "\n")

            #Fix "that" preceded by the verb "point out" which is consistantly misstageed as subordinator
            #search for that preceded by out and by point and changes the tag from cs+sub to tht+vcmp
            elif re.search("that \^cs\+sub", lines[i]) and re.search("out", lines[i-1]) and re.search("point", lines[i-2]):
                line3 = re.sub("cs\+sub", "tht+vcmp", lines[i])
                output_file.write(line3 + "\n")


            #Fix "that" verb complement clauses miss-tagged as determinders
            # searches for determiners preceded by a verb and changes the determiner tag to vcmp
            elif re.search("that \^dt", lines[i]) and re.search("\^vb", lines[i-1]):
                linedt = re.sub("dt\+dem", "tht+vcmp", lines[i])
                output_file.write(linedt + "\n")


            # Fix "that" noun complement clauses that were tagged as determiners "dt+dem"
            # searches for that determiners preceded by one of the most common words with that-NCC (LGSWE 648 and 649)
            # if there is an intervening ^zzz, then it fixes the tag from dt+dem to tht+ncmp
            # I found this error while checking all occurrences of the most common nouns in NCCs
            elif re.search("that \^dt", lines[i]) \
                    and re.match("(assertion|comment|contention|conviction|discovery|expectation|feeling|implication|"
                                 "impression|indication|opinion|perception|presumption|principle|probability|"
                                 "proposition|realisation|realization|reason|remark|requirement|result|"
                                 "rumor|rumour|statement|suspicion|thesis|fact|idea|hope|possibility|doubt|"
                                 "suggestion|belief|sign|conclusion|claim|ground|view|fear|knowledge|news|"
                                 "sense|report|notion|assumption|thought|hypothesis|observation) \^n+", lines[i - 2]) \
                    and re.search(" \^zz\+\+\+\+=", lines[i - 1]):
                linenouncomp = re.sub("\^dt\+dem\+", "^tht+ncmp+", lines[i])
                output_file.write(linenouncomp + "\n")


            # Fix third person verbs tagged as nouns
            #Searches for means, states, claims and demonstrates and changes the tag from noun to verb
            #This causes claims as a noun to be miss-tagged but since these are way less frequent in the corpus...
            #it is the best solution to improve precision/recall for both nouns and verbs
            elif re.match("means|states|claims|demonstrates", lines[i]) and re.search("that", lines[i+1]):
                linevb = re.sub("nns|np", "vbz", lines[i])
                output_file.write(linevb + "\n")


            #Fix noun complement clauses that were tagged as relative clauses
            # searches for "that" preceded by means, states, claims and demonstrates
            #This also might cause some ncmp to be miss-tagged as vcmp (because of claims)
            #But this is not common in the corpus
            elif re.search("tht\+rel", lines[i]) and re.match("means|states|claims|demonstrates", lines[i-1]):
                linerel = re.sub("tht\+rel", "tht+vcmp", lines[i])
                output_file.write(linerel + "\n")


            #Fix infinitive verbs that are misstagged as nominalizations after jcmp (adjective complement clause)
            #First, I printed all jcmps then I found all the words that were misstaged, and listed them.
            #Then, I used this list to search for these words preceded by jcmp
            #Finally, tags are changed from nominalization to vbi
            #issue: it doesn't include words tagged as nns (plural nouns) such as address and process, since it only happens twice in the corpus I didn't fix it
            elif re.match("(accelerate|accommodate|accumulate|activate|address|advance|anticipate|"
                           "assimilate|associate|calculate|complement|consider|correlate|differentiate"
                           "|discriminate|encourage|estimate|evaluate|explicate|express|formulate|"
                           "generate|illustrate|implement|incorporate|indicate|integrate|interrogate|"
                           "isolate|manipulate|mention|negotiat|ooperate|participate|postulate|process|"
                           "propagate|question|reiterate|remember|repudiate|retaliate|simulate|tolerate|"
                           "translate|validate) \^", lines[i]) and re.search("\^to\+jcmp", lines[i-1]):
                linencmp = re.sub("\^nn\+nom\+", "^vbi++", lines[i])
                output_file.write(linencmp + "\n")


            #any other line that doesn't match the previous criteria is simply printed in the new file
            else:
                output_file.write(w + "\n")