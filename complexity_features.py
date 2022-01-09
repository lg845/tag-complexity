#this script was used to count nominalizations, focusing on the most productive suffixes in the corpus
import os
import re
import argparse

#TO RUN THIS SCRIPT
#python all_together.py --folder=PATH TO FOLDER HERE

file_out = open("complexity_count.csv", "w+")
file_out.write("file, genitive_of, genitive_s, atrb, premod,"
               " prep, subordinator, common_vcc, ncommon_vcc, wh_vcc, to_vcc, "
               "ing_vcc, advl, post_nom, NCC, NFNCC, jcmp_that, jcmp_to, it_extra, it_to,\n")

#starts the counts
genitive_of = 0
genitive_s = 0
atrb = 0
premod = 0
prep = 0
sub = 0
common_vcc = 0
noncommon_vcc = 0
wh_vcc = 0
to_vcc = 0
ing_vcc = 0
advl = 0
post_nom = 0
NCC = 0
NFNCC = 0
jcmp_that = 0
jcmp_to = 0
it_extra = 0
it_to = 0

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
        output_directory = 'complexity_L2'
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

            ##PREMODIFYING NOUNS
            # noun + noun
            if re.search("\^nn\+", lines[i]) and re.search("\^nn+", lines[i + 1]) and not re.search("\^jj?", lines[i - 1]):
                premod += 1
                nn_tag = re.sub("\^nn\+", "^nn+npren+", lines[i])
                output_file.write(nn_tag + "\n")

            elif re.search("\^nns\+", lines[i]) and re.search("\^nn+", lines[i + 1]) and not re.search("\^jj?", lines[i - 1]):
                premod += 1
                nn_tag2 = re.sub("\^nns\+", "^nns+npren+", lines[i])
                output_file.write(nn_tag2 + "\n")

            ##GENITIVE
            #noun + of + noun  or pronoun
            elif re.search("of \^in\+\+\+", lines[i]) and re.search("\^nn+|\^np+|\^nr+", lines[i-1]) and not\
                    re.match("(piece|part|light|lot|way|all|half|"
                             "some|both|few|many|much|lots|sort|bit|sum) \^", lines[i - 1]) \
                    and re.search("\^nn+|\^np+|\^nr+", lines[i+1]):
                genitive_of +=1
                genitive_tag = re.sub("\+\+=of", "++gen+=of", lines[i])
                output_file.write(genitive_tag + "\n")

            #noun + of + attributive adjective/determiner/article/pronoun + noun or pronoun
            elif re.search("of \^in\+\+\+", lines[i]) and re.search("\^nn+|\^np+|\^nr+", lines[i-1]) and not \
                    re.match("(piece|part|light|lot|way|all|half|some|section|sections|"
                             "number|plenty|both|few|many|much|lots|sort|bit|sum) \^", lines[i - 1]) and \
                    re.search("\^jj|\^dt+|\^at+|\^ap|\^pp+", lines[i+1]) and re.search("\^nn+|\^np+|\^nr+", lines[i+2]):
                genitive_of += 1
                genitive_tag = re.sub("\+\+=of", "++gen+=of", lines[i])
                output_file.write(genitive_tag + "\n")

            #noun + of + article + adjective + noun or pronoun
            elif re.search("of \^in\+\+\+", lines[i]) and re.search("\^nn+|\^np+", lines[i-1]) and \
                    re.match("(piece|part|light|lot|way|all|half|some|section|sections|"
                             "number|plenty|both|few|many|much|lots|bit|sum) \^", lines[i - 1]) and \
                    re.search("\^at+", lines[i+1]) and re.search("\^jj+", lines[i+2]) and re.search("\^nn+|\^np+", lines[i+3]):
                genitive_of += 1
                genitive_tag = re.sub("\+\+=of", "++gen+=of", lines[i])
                output_file.write(genitive_tag + "\n")

            ##COUNT 'S GENITIVE
            #noun + s + noun
            #for the 's I am searching for $ because this tag appears in my L1 corpus
            # I am also searching for 's ^zz because this tag appears in my L2 corpus
            elif re.search("\^\$|'s \^zz", lines[i]) and re.search("\^nn+|\^np+|\^nr+", lines[i - 1]) and \
                    re.search("\^nn+|\^np+|\^nr+", lines[i+1]):
                genitive_s +=1
                gens_tag = re.sub("\+\+=", "++sgen+=", lines[i])
                output_file.write(gens_tag + "\n")

            # noun + 's + adjective/determiner/number/adverb + noun
            # All possible intervening words were included (adj, det, num, etc).
            # The goal is to increase recall for the complexity feature even if the original biber tag was wrong.
            elif re.search("\^\$|'s \^zz", lines[i]) and re.search("\^nn+|\^np+|\^nr+", lines[i-1]) and \
                    re.search("\^ap|\^od|\^rb|\^cd|\^jj+", lines[i+1]) and re.search("\^nn+|\^np+|\^nr+", lines[i+2]):
                genitive_s += 1
                gens_tag = re.sub("\+\+=", "++sgen+=", lines[i])
                output_file.write(gens_tag + "\n")

            ##ATTRIBUTIVE ADJECTIVES
            #adjective + noun
            elif re.search("\^jj?", lines[i]) and re.search("\^nn+|\^np+|\^nr+", lines[i+1]):
                atrb +=1
                atrb_tag = re.sub("\+\+=", "++att+=", lines[i])
                output_file.write(atrb_tag + "\n")

            elif re.search("\^jj?", lines[i]) and re.search("\^jj+", lines[i + 1]) and re.search("\^nn+|\^np+|\^nr+", lines[i + 2]):
                atrb +=1
                atrb_tag = re.sub("\+\+=", "++att+=", lines[i])
                output_file.write(atrb_tag + "\n")

            elif re.search("\^jj?", lines[i]) and re.search("\^jj+", lines[i + 1]) and re.search("\^jj+", lines[i + 2]) and re.search("\^nn+|\^np+|\^nr+", lines[i + 3]):
                atrb +=1
                atrb_tag = re.sub("\+\+=", "++att+=", lines[i])
                output_file.write(atrb_tag + "\n")

            ##PREPOSITIONAL PHRASES
            #noun + most common prepositions in postmodifying position (LGSWE p.635) + noun that is not -ing
            elif re.match("(in|for|on|to|with) \^in", lines[i]) and re.search("\^nn+|\^np+|\^nr+", lines[i - 1]) and \
                 re.search("\^nn+|\^np+|\^nr+", lines[i + 1]) and not re.findall("ing", lines[i + 1]):
                prep +=1
                pp_tag = re.sub("\+\+=|\+\?\?\+=", "++prep+=", lines[i])
                output_file.write(pp_tag + "\n")

            #noun + most common prepositions in postmodifying position (LGSWE p.635) + adjective/article/determiner + noun
            elif re.match("(in|for|on|to|with) \^in", lines[i]) and re.search("\^nn+|\^np+|\^nr+", lines[i - 1]) and re.search("\^nn+|\^np+|\^nr+", lines[i + 2]) and not re.findall("ing|\^vb+|\^wh+", lines[i + 1]):
                prep +=1
                pp_tag = re.sub("\+\+=|\+\?\?\+=", "++prep+=", lines[i])
                output_file.write(pp_tag + "\n")

            #noun + most common prepositions in postmodifying position (LGSWE p.635) + adjective/article/determiner (2) + noun
            elif re.match("(in|for|on|to|with) \^in", lines[i]) and re.search("\^nn+|\^np+|\^nr+", lines[i - 1]) and re.search("\^nn+|\^np+|\^nr+", lines[i + 3]) and not re.findall("ing|\^vb+|\^wh+", lines[i + 1]):
                prep +=1
                pp_tag = re.sub("\+\+=|\+\?\?\+=", "++prep+=", lines[i])
                output_file.write(pp_tag + "\n")

            ##SUBORDINATOR
            #subordinator + noun or pronoun or modal + verb
            elif re.search("\^cs\+", lines[i]) and \
                    re.search("\^pp+|\^nn+|\^np+|\^nr+", lines[i+1]) and \
                    re.search("\^vb+", lines[i+2]):
                sub += 1
                sub_tag = re.sub("\+=", "+subo+=", lines[i])
                output_file.write(sub_tag + "\n")

            #subordinator + one intervening word + noun or pronoun or modal + verb
            elif re.search("\^cs\+", lines[i]) and \
                    re.search("\^pp+|\^nn+|\^np+|\^nr+|\^md+|\^dt+", lines[i+2]) and \
                    re.search("\^vb+", lines[i+3]):
                sub += 1
                sub_tag = re.sub("\+=", "+subo+=", lines[i])
                output_file.write(sub_tag + "\r")

            #subordinator + two intervening words + noun or pronoun or modal + verb
            elif re.search("\^cs\+", lines[i]) and \
                    re.search("\^pp+|\^nn+|\^np+|\^nr+|\^md+|\^dt+", lines[i+3])and \
                    re.search("\^vb+", lines[i+4]):
                sub += 1
                sub_tag = re.sub("\+=", "+subo+=", lines[i])
                output_file.write(sub_tag + "\n")

            ##FINITE VCC - COMMON VERBS
            #common verbs from LGSWE (p.663) + that tagged as verb complement clause
            elif re.search("\^tht\+vcmp", lines[i]) and re.match("(think|thinks|"
                                                                "thought|thinking|say|said|says|saying|"
                                                                "know|knows|knowing|knew|see|sees|seeing|saw|"
                                                                "find|found|finds|finding|believes|believe|"
                                                                "believed|believing|feel|suggest|show|felt|"
                                                                "suggested|showed|feels|suggests|shows|shown|"
                                                                "known|seen) \^vb+", lines[i-1]):
                common_vcc += 1
                commonv_tag = re.sub("\+=", "+comm-vcc+=", lines[i])
                output_file.write(commonv_tag  + "\n")

            ##FINITE VCC - Other verbs
            #all verbs except for the ones in the list of common verbs + that tagged as verb complement clauses
            elif re.search("\^tht\+vcmp", lines[i]) and not re.search("(think|thinks|"
                                                                "thought|thinking|say|said|says|saying|"
                                                                "know|knows|knowing|knew|see|sees|seeing|saw|"
                                                                "find|found|finds|finding|believes|believe|"
                                                                "believed|believing|feel|suggest|show|felt|"
                                                                "suggested|showed|feels|suggests|shows|shown|"
                                                                "known|seen) \^vb+", lines[i - 1]):
                noncommon_vcc+= 1
                noncommonv_tag = re.sub("\+=", "+ncm-vcc+=", lines[i])
                output_file.write(noncommonv_tag + "\n")

            ##FINITE VERB COMPLEMENT CLAUSE-WH
            #common verbs from LGSWE (p.686) + wh-word
            elif re.match("(know|knowing|knows|knew|see|sees|seeing|saw|tell|"
                           "told|tells|telling|wonder|wonders|"
                           "wondering|wondered|ask|asked|asks|"
                           "asking|understand|understands|understood|understanding) \^vb+", lines[i]) and\
                    re.match("what|where|which|who|how|when|whom|whose|why|whatever|"
                             "whoever|whichever", lines[i+1]):
                wh_vcc += 1
                wh_vcc_tag = re.sub("\+=", "+wh-vcc+=", lines[i])
                output_file.write(wh_vcc_tag + "\n")

            # common verbs from LGSWE (p.686) + pronoun or noun +  wh-word
            elif re.match("(know|knowing|knows|knew|see|sees|seeing|saw|tell|"
                           "told|tells|telling|wonder|wonders|"
                           "wondering|wondered|ask|asked|asks|"
                           "asking|understand|understands|understood|understanding) \^vb+", lines[i]) and \
                    re.search("\^pp+|\^nn+|\^np+|\^nr+", lines[i+1]) and \
                    re.match("(what|where|which|who|how|when|whom|whose|why|whatever|"
                             "whoever|whichever) \^w+", lines[i+2]):
                    wh_vcc += 1
                    wh_vcc_tag = re.sub("\+=", "+wh-vcc+=", lines[i])
                    output_file.write(wh_vcc_tag + "\n")

            # common verbs from LGSWE (p.686) + one intervening word + noun or pronoun + wh-word
            elif re.match("(tell|told|tells|telling) \^vb+", lines[i]) and \
                    re.search("\^pp+|\^nn+|\^np+|\^nr+", lines[i + 2]) and \
                    re.match("(what|where|which|who|how|when|whom|whose|why|whatever|"
                                 "whoever|whichever) \^w+", lines[i+3]):
                        wh_vcc += 1
                        wh_vcc_tag = re.sub("\+=", "+wh-vcc+=", lines[i])
                        output_file.write(wh_vcc_tag + "\n")

            ##NON-FINITE VERB COMPLEMENT CLAUSE
            #WITH TO-VCC
            #there is already a tag for to-vcc, so first the script search for this tag
            elif re.search("\^to\+vcmp", lines[i]):
                to_vcc += 1
                to_vcc_tag = re.sub("\+=", "+to-vcc+=", lines[i])
                output_file.write(to_vcc_tag + "\n")

            #some to-vccs are not tagged, so I am using the most common verbs to search for them
            #common verb LGSWE (p.699) + to + VB
            elif re.search("\^to", lines[i]) and re.search("\^vbi", lines[i+1]) and not re.search(" \^to\+vcmp", lines[i]) and \
                    re.match("(want|try|seem|like|begin|tend|attempt|"
                              "wanted|tried|seemed|liked|tended|attempted|"
                              "wants|tries|seems|likes|begins|tends|attempts|"
                              "wanting|trying|seeming|liking|tending|attempting) \^vb+", lines[i-1]):
                to_vcc += 1
                to_vcc_tag = re.sub("\+=", "+to-vcc+=", lines[i])
                output_file.write(to_vcc_tag + "\n")

            # Common verb LGSWE (p.699) + noun or pronoun + to + VB
            elif re.search("\^to", lines[i]) and re.search("\^vbi", lines[i+1]) and not re.search(" \^to\+vcmp", lines[i]) and\
                    re.search("\^pp+|\^nn+|\^np+|\^nr+", lines[i - 1]) and \
                    re.match("(want|try|seem|like|begin|tend|attempt|"
                              "wanted|tried|seemed|liked|tended|attempted|begun|"
                              "wants|tries|seems|likes|begins|tends|attempts|"
                              "wanting|trying|seeming|liking|tending|attempting) \^vb+", lines[i-2]):
                to_vcc += 1
                to_vcc_tag = re.sub("\+=", "+to-vcc+=", lines[i])
                output_file.write(to_vcc_tag + "\n")

            #WITH -ING
            #Common verbs LGSWE (p. 741) + xvbg tag
            #I chose to use the "xvbg" because checking the results I realized there were a lot of mistags
            #This way recall we improve the recall
            elif re.match("(keep|start|see|go|stop|begin|"
                              "kept|started|saw|went|stopped|begun|began|seen|gone|"
                              "keeps|starts|sees|goes|stops|begins|"
                              "keeping|starting|seeing|going|beginning) \^vb+", lines[i]) and \
                    re.search("xvbg", lines[i+1]):
                ing_vcc += 1
                ing_vcc_tag = re.sub("\+=", "+ing-vcc+=", lines[i])
                output_file.write(ing_vcc_tag + "\n")

            #Common verb + noun or pronoun + xvbg, vwbg, or vbg
            elif re.match("(see|saw|seen|sees|seeing|) \^vb+", lines[i]) and re.search("\^xvbg|\^vwbg|\^vbg", lines[i+2]) and \
                    re.search("\^pp+|\^nn+|\^np+|\^nr+", lines[i+1]):
                ing_vcc += 1
                ing_vcc_tag = re.sub("\+=", "+ing-vcc+=", lines[i])
                output_file.write(ing_vcc_tag + "\n")

            #Common verb + NP (2 intervening words) + v-ing
            elif re.match("(see|saw|seen|sees|seeing|) \^vb+", lines[i]) and\
                    re.search("\^xvbg|\^vwbg|\^vbg", lines[i + 4]) and \
                    re.search("\^pp+|\^nn+|\^np+|\^nr+", lines[i + 3]):
                ing_vcc += 1
                ing_vcc_tag = re.sub("\+=", "+ing-vcc+=", lines[i])
                output_file.write(ing_vcc_tag + "\n")

            ##ADVERB AS ADVERBIAL
            #Most common adverbs of circumstance LGSWE (p. 796) tagged as an adverb
            #Most common adverbs of stance LGSWE (p. 869) tagged as an adverb (deleted in fact, of course, sort of, kind of, according to and "like")
            #Most common linking adverbs LGSWE (p. 887) (deleted all prepositional phrases and so)
            #not followed by adverb, adjective, numeral or preposition of
            #not preceded by article (to increase precision)
            elif re.search("\^rb|\^wrb", lines[i]) and re.match("(just|only|also|even|too|now|never|"
                                                         "again|always|still|today|yesterday|"
                                                         "already|ever|sometimes|often|usually|"
                                                         "there|here|probably|maybe|perhaps|"
                                                         "certainly|definitely|really|actually|generally|"
                                                         "then|though|anyway|however|thus|therefore|"
                                                         "first|finally|furthermore|hence|nevertheless|rather|yet) \^", lines[i]) \
                    and not re.search("\^rb+|\^cd+|of \^", lines[i+1])\
                    and not re.search("\^at+|\^rb+", lines[i-1]):
                advl += 1
                advl_tag = re.sub("\+=", "+advl+=", lines[i])
                output_file.write(advl_tag + "\n")

            ##-ing AND -ed CLAUSES AS POSTNOMINAL CLAUSES
            #there are two tags for this vwbg (ing) and vwbn (ed)
            #checks to see if word preceding the tag is really a noun and deletes good (to increase precision)
            elif re.search("\^vwbg|\^vwbn", lines[i]) and not \
                    re.search("good", lines[i-1]) and re.search("\^nn+|\^np+|\^nr+", lines[i-1]):
                post_nom += 1
                post_nom_tag = re.sub("\+=", "+post-nom+=", lines[i])
                output_file.write(post_nom_tag + "\n")

            ##FINITE NCC
            #NCCs are tagged as ncmp. The search patterns is that + ncmp
            elif re.search("ncmp", lines[i]) and re.search("that", lines[i]) and not re.search("vb+", lines[i-1]):
                NCC += 1
                NCC_tag = re.sub("\+=", "+ncc+=", lines[i])
                output_file.write(NCC_tag + "\n")

            ##NON-FINITE NCC - to
            # NCCs are tagged as ncmp. The search patterns is to + ncmp
            elif re.search("ncmp", lines[i]) and re.search("to", lines[i]):
                NFNCC += 1
                NFNCC_tag = re.sub("\+=", "+nf-ncc+=", lines[i])
                output_file.write(NFNCC_tag + "\n")

            ##IT EXTRAPOSED WITH THAT-CLAUSES
            # Searches for it + word + adjective + adjective complement clause with that
            elif re.search("jcmp", lines[i]) and re.search("that \^", lines[i]) and re.search("\^jj+", lines[i - 1]) and re.search("it \^pp3", lines[i - 3]):
                it_extra += 1
                it_extra_tag = re.sub("\+=", "+it-extra+=", lines[i])
                output_file.write(it_extra_tag + "\n")

            #searches for it + word + word + adjective + adjective complement clause with that
            elif re.search("jcmp", lines[i]) and re.search("that \^", lines[i]) and re.search("\^jj+", lines[i - 1]) and re.search("it \^pp3", lines[i - 4]):
                it_extra += 1
                it_extra_tag = re.sub("\+=", "+it-extra+=", lines[i])
                output_file.write(it_extra_tag + "\n")

            #searches for it + word + word +word + adjective + adjective complement clause with that
            elif re.search("jcmp", lines[i]) and re.search("that \^", lines[i]) and re.search("\^jj+", lines[i - 1]) and re.search("it \^pp3", lines[i - 5]):
                it_extra += 1
                it_extra_tag = re.sub("\+=", "+it-extra+=", lines[i])
                output_file.write(it_extra_tag + "\n")

            ##IT EXTRAPOSED WITH T0-CLAUSES
            #searches for it + word + adjective + adjective complement clause with to
            elif re.search("jcmp", lines[i]) and re.search("to \^", lines[i]) and re.search("\^jj+",lines[i-1]) and re.search("it \^pp3", lines[i-3]):
                it_to += 1
                it_to_tag = re.sub("\+=", "+it-to+=", lines[i])
                output_file.write(it_to_tag + "\n")

            #searches for it + word + word + adjective + adjective complement clause with to
            elif re.search("jcmp", lines[i]) and re.search("to \^", lines[i]) and re.search("\^jj+",lines[i-1]) and re.search("it \^pp3", lines[i-4]):
                it_to += 1
                it_to_tag = re.sub("\+=", "+it-to+=", lines[i])
                output_file.write(it_to_tag + "\n")

            #searches for it + word + word + adjective + adjective complement clause with to
            elif re.search("jcmp", lines[i]) and re.search("to \^", lines[i]) and re.search("\^jj+",lines[i-1]) and re.search("it \^pp3", lines[i-5]):
                it_to += 1
                it_to_tag = re.sub("\+=", "+it-to+=", lines[i])
                output_file.write(it_to_tag + "\n")

            ##ALL OTHER FINITE JCC
            #Any that-JCMP that is not preceded by it
            elif re.search("jcmp", lines[i]) and re.search("that \^", lines[i]) and not re.search("it \^pp3", lines[i-3]) \
                    and not re.search ("it \^pp3", lines[i-4]) and not re.search ("it \^pp3", lines[i-5]):
                jcmp_that += 1
                jcmp_that_tag = re.sub("\+=", "+jcmp-that+=", lines[i])
                output_file.write(jcmp_that_tag + "\n")


            #ALL OTHER NON-FINITE JCC
            # Any to-JCMP that is not preceded by it
            elif re.search("jcmp", lines[i]) and re.search("to \^", lines[i]) and not re.search("it \^pp3", lines[i-3]) \
                    and not re.search ("it \^pp3", lines[i-4]) and not re.search ("it \^pp3", lines[i-5]):
                jcmp_to += 1
                jcmp_to_tag = re.sub("\+=", "+jcmp-to+=", lines[i])
                output_file.write(jcmp_to_tag + "\n")

            else:
                output_file.write(w + "\n")


        file_out.write(name + "," + str(genitive_of) + "," + str(genitive_s) +
                       "," + str(atrb) + "," + str(premod) + "," + str(prep) + "," + str(sub) +
                       "," + str(common_vcc) + "," + str(noncommon_vcc) + "," + str(wh_vcc) +
                       "," + str(to_vcc) + "," + str(ing_vcc) + "," + str(advl) + "," + str(post_nom) +
                       "," + str(NCC) + "," + str(NFNCC) + "," + str(jcmp_that) +
                       "," + str(jcmp_to) + "," + str(it_extra) + "," + str(it_to) + "\n")

        genitive_of = 0
        genitive_s = 0
        atrb = 0
        premod = 0
        prep = 0
        sub = 0
        common_vcc = 0
        noncommon_vcc = 0
        wh_vcc = 0
        to_vcc = 0
        ing_vcc = 0
        advl = 0
        post_nom = 0
        NCC = 0
        NFNCC = 0
        jcmp_that = 0
        jcmp_to = 0
        it_extra = 0
        it_to = 0