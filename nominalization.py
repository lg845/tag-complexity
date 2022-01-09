#this script was used to count nominalizations, focusing on the most productive suffixes in the corpus

import os
import re
import argparse

#TO RUN THIS SCRIPT
#python nominalization.py --folder=PATH TO FOLDER HERE

file_out = open("nominalization_count.csv", "w+")
file_out.write("file, nominalization, \n")

#starts nominalization count
nom_count = 0

# Define the way we retrieve arguments sent to the script.
parser = argparse.ArgumentParser(description='dissertation nominalization script')
parser.add_argument('--overwrite', action='store_true')
parser.add_argument('--folder', action="store", dest='dir', default='')
args = parser.parse_args()

#gets the texts from the original folder
for dirpath, dirnames, files in os.walk(args.dir):
    for name in files:
        textfile = open(os.path.join(dirpath, name), "r")

        # cleans the file name and creates a new folder to store the edited texts
        cleaned_filename = re.sub(r'\.\.[\\\/]', r'', name)
        output_directory = 'nominalization_L2'
        output_filename = os.path.join(output_directory, cleaned_filename)
        directory = os.path.dirname(output_filename)
        if not os.path.exists(directory):
            os.makedirs(directory)

        # opens the new file
        output_file = open(output_filename, 'w')

        #makes the text lower case
        #splits the text into words by "\n" or "\r"
        text = textfile.read()
        text = text.lower()
        lines = text.split("\n")

        for i, w in enumerate(lines):
            ##NOMINALIZATION
            #searches for all the words that end in the most productive suffixes that form nominalizations
            if re.search("\^nn+", lines[i]) and re.search("tion |tions |ity |ities |ness "
                                                          "|isms |ism |ment |ments |ant |ants |ship "
                                                          "|ships |ery ", lines[i]):
                #after checking all the words that came out from the previous search
                #deletes all the words that are not nominalization from this list
                if not re.match('precondition|soultion|segments|implants|artery|'
                                'condition|positions|solution|section|notions|quations|'
                                'increments|gelation|lottery|entities|proppants|artillery|'
                                'surfactants|constants|commodity|commodities|entity|deity|'
                                'nation|mention|mystery|elephants|prisms|motion|'
                                'intuition|question|quality|dysfunction|fiction|nations|'
                                'environments|cution|undulations|quantity|jurisdiction|friction|'
                                'cutions|proportion|portions|surgery|conditions|cities|pity|'
                                'sanitation|hajbaghery|traction|ants|subsumtion|quantities|plants|'
                                'vitrification|unity|tradition|qualities|nements|traditions|'
                                'moments|questions|disparity|duration|cavity|business|notation|'
                                'ubiquitinylation|vicinities|masculinity|utility|sections|function|'
                                'microorganisms|infants|functions|prism|mentions|elements|preconditions|'
                                'notion|city|reception|ration|incantation|tuberosity|schism|humility|'
                                'auction|ductility|chelation|colliery|merchants|pigment|diction|'
                                'clarity|cements|currants|ablation|abutments|aeration|advection|'
                                'amenities|apportions|avection|bastion|celerity|'
                                'deities|consonants|elation|equity|equities|'
                                'fraction|fractions|fruity|garments|lig|lymbery|misery|'
                                'nsities|overy|polity|potions|sitation|station|suction|theism|'
                                'timents|tuition|wants', lines[i]):
                    nom_count +=1
                    nominalization = re.sub("\+=","+tion+=", lines[i])
                    output_file.write(nominalization + "\n")
                else:
                    output_file.write(w + "\n")
            else:
                output_file.write(w + "\n")

        file_out.write(name + "," + str(nom_count) + "\n")
        nom_count = 0

