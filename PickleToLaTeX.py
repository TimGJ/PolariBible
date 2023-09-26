""" Converts PPK files to LaTeX source text for onwards 
output of PDF. This is the easiest way to get multi-column
nicely typset text. 

Part of Polari Bible 7th edition software Copyright (c) 
2004 - 2014 Tim Greening-Jackson
"""

Id = ""

import pickle
import re
import sys
import PolariBible

LaTeXHeader = r"""
\documentclass[a4paper,10pt]{book}
\usepackage{multicol}
\usepackage{fontspec}
\usepackage{graphicx}
\setmainfont{Times New Roman}
\setcounter{secnumdepth}{-2}
\setcounter{tocdepth}{1}
\usepackage[margin=2.5cm]{geometry}
\usepackage{tocloft}
\setlength\cftparskip{-2pt}
\setlength\cftbeforesecskip{1pt}
\setlength\cftaftertoctitleskip{2pt}
\setlength{\parskip}{1cm plus4mm minus3mm}
\begin{document}
\title{The Polari Bible\\\large{\emph{Seventh Edition}}}
\author{Translatrix: Sister Debbie Ann Linux of the Virtual Habit}
\maketitle
\begin{center}
\makebox[\textwidth]{\includegraphics[width=\textwidth]{FlyLeaf}}
\end{center}
\tableofcontents
\begin{center}
\makebox[\textwidth]{\includegraphics[width=\textwidth]{GoodSamaritan}}
\end{center}
\include{introduction}
\begin{center}
\makebox[\textwidth]{\includegraphics[width=\textwidth]{ATypicalFridayNightOnCanalStreet}}
\end{center}
\include{buildinfo}
"""

def InsertIllustration(handle, name):
    """
    Inserts an illustration in to the document
    """
    print("\\newpage", file = handle)
    print("\\begin{center}", file = handle)
    print("\\makebox[\\textwidth]{{\\includegraphics[width=\\textwidth]{{{}}}}}".format(name), file = handle)
    print("\\end{center}", file = handle)
    print("\\newpage", file = handle)

def MakeLexicon(handle):
    """
    Produces and inserts the lexicon. Note that the dictionary definitions are pickled as part of the 
    initial translation and so should be current.
    """

    with open("dictionaries.pkl", "rb") as p:
        print("\\chapter{Lexicon of Polari Words and Phrases}", file=handle)
        print("\\begin{multicols}{3}", file=handle)
        t = pickle.load(p)
        s = {k.polari.capitalize():[] for k in t}
        for k in t:
            s[k.polari.capitalize()].append(k.english)

        current = ""
        for m in sorted(s):
            initial = m[0].upper()
            if initial != current:
                current = initial
                print("\\section{{{}}}".format(initial), file=handle)

            print('\\emph{{{}}}: {}\\\\'.format(m, ", ".join(s[m])), file=handle)
        print("\\end{multicols}", file=handle)

def ProcessBook(book):
    pre = re.compile('<polari><from>.*?</from><to>(.*?)</to></polari>')
    outfile = book.stem+".tex"
    print("Writing {}".format(outfile))

    with open(outfile, "w") as o:
        print("\\begin{multicols}{2}", file=o)
        print("Writing {}".format(outfile))
        print("\\section{{{}}}".format(book.title), file=o)
        chaptitle = "Psalm" if book.psalms else "Chapter"
        for c in book.chapters:
            print("\\subsection{{{} {}}}".format(chaptitle, c.index), file=o)
            for v in c.verses:
                if "<polari>" in v.text:
                    v.text = pre.sub("[emph] {\g<1>}", v.text)
                    v.text = v.text.replace("[emph]", "\\emph")
                print("\\emph{{{}}} {}\\\\".format(v.index, v.text), file=o)
        print("\\end{multicols}", file=o)


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("Syntax {} pickle file [pickle file [...]]".format(sys.argv[0]))
    else:
        with open("bible.tex", "w") as master:
            print(LaTeXHeader, file=master)
            for s in sys.argv[1:]:
                with open(s, "rb") as p:
                    volume = pickle.load(p)
                    for book in volume:
                        if book.stem == "genesis":
                            print("\\chapter{Old Testament}", file=master)
                            InsertIllustration(master, "MosesWithTablets")
                        elif book.stem == "matthew":
                            print("\\chapter{New Testament}", file=master)
                            InsertIllustration(master, "SermonOnTheMount")
                        ProcessBook(book)
                        print("\\include{{{}}}".format(book.stem), file = master)
            InsertIllustration(master, "LookItsTheLawScarper")
            MakeLexicon(master)
            InsertIllustration(master, "GethsemeneWasANotoriousCruisingGround")
            print("\\end{document}", file=master)
