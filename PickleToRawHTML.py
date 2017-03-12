""" Converts PPK files to raw HTML (i.e. has markup tags
like <h2>...</h2> but no CSS or other header information 
Part of Polari Bible 5th edition software Copyright (c) 
2004 - 2012 Tim Greening-Jackson"""

import pickle
import re
import sys
import PolariBibleGlobals

def WriteHTMLHeader(o, n):
    """
    Writes HTML header information to file o
    """
    o.write(
"""
<!DOCTYPE html>
<html lang="en-UK">
<head>
<link rel="stylesheet" href="w3.css">
<title>"{}"</title>
</head>
<body>""".format(n))

def BookHTMLFileName(b):
    """
    Simply returns the html name of a file
    """
    return b.stem+".html"


def WriteHTMLIndexEntry(index, b):
    """
    Writes an entry in the index.html file for book b
    """
    index.write("<a href=\"{}\"><h2>{}</h2></a>\n".
                format(BookHTMLFileName(b), b.title))

def WriteHTMLFooter(o):
    """
    Writes HTML footer information
    """
    o.write("</body>\n</html>\n")

def ProcessBook(book):
    pre = re.compile('<polari><from>.*?</from><to>(.*?)</to></polari>')
    
    with open(BookHTMLFileName(book), "w") as o:
        print("Writing {}".format(BookHTMLFileName(book)))
        WriteHTMLHeader(o, book.title)
# Following line commented out as we are trying to
# automate import in to WordPress...
#        o.write("<h2>{}</h2>\n".format(book.title))
        chaptitle = "Psalm" if book.psalms else "Chapter"
        for c in book.chapters:
            o.write("<h3>{} {}</h3>\n<ol>\n".format(chaptitle, c.index))
            for v in c.verses:
                v.text = pre.sub("<em>\g<1></em>", v.text)
                o.write("<li>{}\n".format(v.text))
            o.write("</ol>\n")
        WriteHTMLFooter(o)

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("Syntax {} pickle file [pickle file [...]]".format(sys.argv[0]))
    else:
        with open("index.html", "w") as index:
            WriteHTMLHeader(index, "The Polari Bible 7th Edition")
            for s in sys.argv[1:]:
                with open(s, "rb") as o:
                    book = pickle.load(o)
                    for b in book:
                        if b.title == 'Genesis':
                            index.write("<h1>Old Testament</h1>")
                        elif b.title == 'Matthew':
                            index.write("<h1>New Testament</h1>")
                        WriteHTMLIndexEntry(index, b)
                        ProcessBook(b)
            WriteHTMLFooter(index)
                    
            
