"""
The Polari Bible is "bookended" by two files: an introduction 
the source for which is written in a sort of vaguely-HTML
mark-up language and a lexicon of the various words and 
phrases used. 

This script builds both LaTeX files for inclusion.


Tim Greening-Jackson 

"""

import re
import sys

def CreateIntroduction(ifile = "introduction.txt", ofile = "introduction.tex"):
# Reads the text input, performs various re substitutions
# and writes the output. Nothing to see here. Move along.

    subs = {"<h1>": "\\section{", "</h1>":"}",
            "<h2>": "\\subsection{", "</h2>":"}",
            "<em>": "\\emph{", "</em>": "}",
            "<i>": "\\emph{", "</i>": "}",
            "<tt>": "\\emph{", "</tt>": "}",
            "<p>" : "", "</p>": "\n",
            "<br>": "\\\\", "LaTeX": "\\LaTeX"}

    with open(ifile, "r") as i, open(ofile, "w") as o:
        inbuf= i.readlines()
        for line in inbuf:
            outbuf = line
            for sub in subs:
                outbuf=outbuf.replace(sub, subs[sub])
            print(outbuf, file = o)

        
if __name__ == '__main__':

# Normally this would be passed the names of the dictionary files 
# from the command line.

    CreateIntroduction()
