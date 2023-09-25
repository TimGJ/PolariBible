""" Creates an PPK (Pickled Polari) file with marked-up Polari as
 part of the 2012 version of the Polari Bible
 (C) 2004-2012 Tim Greening-Jackson """

Id = ""

from PolariBibleGlobals import *
import re
import time
import pickle
import sys

def ProcessDictionaryEntries(b):
    """ Takes a list of dictionary entries from a file and
     processes it line by line, discarding comments and
     then covnerting each source:destination pair in to
     a DictionaryEntry object. """
    t = []
    for l in b:
        try:
            r, s = l.strip().split('#')[0].split(':')
        except ValueError:
            pass
        else:
            t.append(Translation(r, s))
    return t        
        
def CompileTranslationDictionary(files):
    """ Given a list of filenames, reads the contents of each in to a buffer,
     passes that buffer to ProcessDictionaryEntries (which produces a
     translation table). The completed table is returned to the caller. """
    
    table = []
    if type(files) == str:
        files = [files]
    elif type(files) != list:
        print("To compile the dictionary I require a list of files. Instead I got {foo}".format(foo=files))
    else:
        for f in files:
            if type(f) != str:
                print("'{s}' is not a valid filename".format(s=f))
                continue
            try:
                buff = open(f, 'r').readlines()
            except IOError:
                print("Having problems opening '{f}' for reading".format(f=f))
            else:
                print("Reading dictionary file {}".format(f))
                table += ProcessDictionaryEntries(buff)
    return table
    
def MakeHash(table):
    """ Returns a dictionary keyed on the token nubmer from
        the translation table """
    return {t.index: t for t in table}

def Polarify(verse, table, hash):
    """ Returns the text v as mangled by translation table t """
    n = verse
    # First of all tokenise the input...

    for t in table:
        token="<token>{}</token>".format(t.index)
        r = re.compile(r'\b{}\b'.format(t.english), re.IGNORECASE)
        n = r.sub(token, n)

    # Now de-tokenise it (in a single line of code). To explain...
    # We have a line containing zero or more tokens - i.e. <token>nnn</token>
    #
    # The re.sub() function can take either a replacement string
    # or a function which will be called with a single argument, that
    # argument being the re.match() object. We need to look up
    # the lexical value of token nnn and return that, hence the
    # "hash" table on which the various tokens are keyed by their
    # index number.
    #
    # Now if we explicitly called an external function then the
    # hash structure wouldn't be in scope so we would have to do
    # something horrible like make it a global; so instead we
    # use a lambda which achieves the same thing as a function but
    # with the hash structure accessible.

    m = re.sub("<token>(\d+)</token>", lambda x: \
               "<polari><from>"+hash[int(x.group(1))].english+\
               "</from><to>"+hash[int(x.group(1))].polari+"</to></polari>", n)
    # Finally, if the replaced token was at the beginning of a sentence
    # we need to make sure that the first letter is capitalised.
    rb = re.compile("^<polari><from>(.*?)</from><to>(.*?)</to></polari>")
    rw = re.compile("^(<polari><from>.*?</from><to>.*?</to></polari>)?")
    sentences = m.split('.')
    for i in range(len(sentences)):
        sentences[i] = sentences[i].strip()
        matched = rb.match(sentences[i])
        if matched:
            f = "{}".format(matched.groups()[0].capitalize())
            t = "{}".format(matched.groups()[1].capitalize())
            r = "<polari><from>{}</from><to>{}</to></polari>".format(f, t)
            sentences[i] = rw.sub(r, sentences[i])
    n = ". ".join(sentences)

    return n

def ProcessVerse(v, t, h):
    """ Process a verse. Called by ProcessChapter() """
    v.text = Polarify(v.text, t, h)

def ProcessChapter(c, t, h):
    """ Process a chapter. Called by ProcessBook() """
    for v in c.verses:
        ProcessVerse(v, t, h)

def ProcessBook(book, table, hash):
    for c in book.chapters:
        ProcessChapter(c, table, hash)

def ProcessBible(bible, table, hash):
    for book in bible:
        print("Polarifying {:<20} ({:3d} Chapters)".format(book.title, len(book.chapters)))
        ProcessBook(book, table, hash)

def WriteLexicon(t):
    # Writes the lexicon of Polari words and phrases used in the translation

    f = open('lexicon.rhtml', 'w')
    f.write('<h1>Lexicon of Polari words and phrases</h1>\n')
    s = {k.polari:[] for k in t}
    for k in t:
        s[k.polari].append(k.english)

    for m in sorted(s):
        f.write('<p><em>{}</em>: {}\n'.format(m, ", ".join(s[m])))

    f.close()

def ProcessRawText():
    """ Slurp the text in and go through it line by line. The start
     of a new book (e.g. Genesis) is caught using the regexp
     and a new "Book" instance started. Chapter and verse indicators
     are at the beginning of each new verse. Note that a particular
     verse can be split on to multiple lines. """
    buff = open('kjv12.txt', 'r').readlines()
    print("Processing raw bible text ({} lines)".format(len(buff)))
    bookre  = re.compile('^Book (?P<index>\d+)\s+(?P<title>\w.*)$')
    blankre = re.compile('^\s*$')
    versere = re.compile('^(?P<ref>\d+:\d+)\s*(?P<text>.*)$')
    index = 0
    Bible = []
    for line in buff:
        line = line.strip()
        # Ignore blank lines
        if re.match(blankre, line): continue
        m = re.match(bookre, line)
        if m:
            index = int(m.groupdict()['index'])
            Bible.append(Book(index, m.groupdict()['title']))
            oldchapnum = 0
            continue
        if index == 0: continue
        # All verses begin nnn:mmm, so we can use this as a delimiter,
        # and also if nnn changes it indicates a new chapter.
        m = re.match(versere, line)
        if m:
            (chapnum, versenum) = map(int, m.groupdict()['ref'].split(':'))
            if oldchapnum != chapnum:
                oldchapnum = chapnum
                Bible[-1].chapters.append(Chapter(chapnum))
            Bible[-1].chapters[-1].verses.append(Verse(versenum,m.groupdict()['text']))
        else:
            Bible[-1].chapters[-1].verses[-1].text += " " + line
        
    return Bible        


if __name__ == '__main__':

    dictfiles = ['phrases.dict', 'words.dict']
    table = CompileTranslationDictionary(dictfiles)
    hash  = MakeHash(table)
    bible = ProcessRawText()
    ProcessBible(bible, table, hash)
    pickled="bible.pkl"
    with open(pickled, "wb") as picklefile:
        print("Dumping bible to {}".format(pickled))
        pickle.dump(bible, picklefile)
    pickled="dictionaries.pkl"
    with open(pickled, "wb") as picklefile:
        print("Dumping dictionaries to {}".format(pickled))
        pickle.dump(table, picklefile)
